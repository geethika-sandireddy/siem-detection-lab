"""Unit tests for scripts/simulate_rule_match.py.

Run with: python3 -m pytest scripts/test_simulate_rule_match.py -v
(or python3 scripts/test_simulate_rule_match.py directly, no pytest needed --
see the __main__ block.)
"""

import os
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.dirname(__file__))
from simulate_rule_match import parse_log, simulate_rule_100010, simulate_rule_100011


def _write_log(lines: list[str]) -> str:
    fd, path = tempfile.mkstemp(suffix=".txt")
    with os.fdopen(fd, "w") as f:
        f.write("\n".join(lines) + "\n")
    return path


class TestRuleSimulation(unittest.TestCase):
    def test_fast_burst_fires_rule_100010(self):
        # 8 failed attempts, 2 seconds apart, well within the 120s window.
        lines = [
            f"Aug  4 02:14:{i:02d} victim sshd[190{i}]: Failed password for labadmin from 10.0.0.5 port 500{i} ssh2"
            for i in range(1, 17, 2)
        ][:8]
        path = _write_log(lines)
        events = parse_log(path)
        result = simulate_rule_100010(events)
        self.assertTrue(result["fired"])
        self.assertEqual(result["attempt_number_for_ip"], 8)
        os.unlink(path)

    def test_slow_drip_does_not_fire_rule_100010(self):
        # 8 attempts spread far enough apart that no 8-in-a-row window is <= 120s.
        lines = [
            f"Aug  4 02:{14 + 2 * i:02d}:00 victim sshd[19{i}]: Failed password for labadmin from 10.0.0.5 port 500{i} ssh2"
            for i in range(8)
        ]
        path = _write_log(lines)
        events = parse_log(path)
        result = simulate_rule_100010(events)
        self.assertFalse(result["fired"])
        os.unlink(path)

    def test_different_source_ips_do_not_combine(self):
        # 4 failures from one IP + 4 from another shouldn't sum to 8 for either.
        lines = []
        for i in range(4):
            lines.append(
                f"Aug  4 02:14:{i:02d} victim sshd[190{i}]: Failed password for labadmin from 10.0.0.5 port 500{i} ssh2"
            )
        for i in range(4):
            lines.append(
                f"Aug  4 02:14:{i + 10:02d} victim sshd[191{i}]: Failed password for labadmin from 10.0.0.6 port 501{i} ssh2"
            )
        path = _write_log(lines)
        events = parse_log(path)
        result = simulate_rule_100010(events)
        self.assertFalse(result["fired"])
        os.unlink(path)

    def test_rule_100011_requires_100010_to_have_fired_first(self):
        # An accepted login with no prior burst should not trigger 100011.
        lines = [
            "Aug  4 02:14:01 victim sshd[1900]: Failed password for labadmin from 10.0.0.5 port 5000 ssh2",
            "Aug  4 02:14:03 victim sshd[1901]: Accepted password for labadmin from 10.0.0.5 port 5001 ssh2",
        ]
        path = _write_log(lines)
        events = parse_log(path)
        r10 = simulate_rule_100010(events)
        r11 = simulate_rule_100011(events, r10)
        self.assertFalse(r10["fired"])
        self.assertFalse(r11["fired"])
        os.unlink(path)

    def test_rule_100011_fires_after_burst_then_accepted(self):
        lines = [
            f"Aug  4 02:14:{i:02d} victim sshd[190{i}]: Failed password for labadmin from 10.0.0.5 port 500{i} ssh2"
            for i in range(1, 9)
        ]
        lines.append("Aug  4 02:14:10 victim sshd[1999]: Accepted password for labadmin from 10.0.0.5 port 5999 ssh2")
        path = _write_log(lines)
        events = parse_log(path)
        r10 = simulate_rule_100010(events)
        r11 = simulate_rule_100011(events, r10)
        self.assertTrue(r10["fired"])
        self.assertTrue(r11["fired"])
        os.unlink(path)


if __name__ == "__main__":
    unittest.main()
