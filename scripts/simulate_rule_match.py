#!/usr/bin/env python3
"""Simulate Wazuh rule matching for the T1110 (SSH brute force) ruleset
against a real sshd auth-log excerpt, computing whether/when each rule
fires from actual parsed timestamps -- not hand-traced reasoning.

This is NOT a substitute for running a live Wazuh agent/manager against
real traffic. It re-implements just enough of Wazuh's matching semantics
(same_source_ip grouping, frequency/timeframe sliding window, parent-child
if_sid/if_matched_sid chaining) to check the *rule logic* mechanically
against a *given* log, removing the "did I trace this correctly by hand"
risk. See rules/T1110-brute-force.xml for the actual rule definitions this
mirrors, and docs/17-deploying-this-repo.md for what live verification
still requires.

Usage:
    python3 scripts/simulate_rule_match.py <path-to-auth-log-excerpt>
"""

from __future__ import annotations

import re
import sys
from dataclasses import dataclass
from datetime import datetime, timedelta

FAILED_RE = re.compile(
    r"^(?P<ts>\w{3}\s+\d{1,2} \d{2}:\d{2}:\d{2}) \S+ sshd\[\d+\]: "
    r"Failed password for \S+ from (?P<ip>[\d.]+) port \d+ ssh2"
)
ACCEPTED_RE = re.compile(
    r"^(?P<ts>\w{3}\s+\d{1,2} \d{2}:\d{2}:\d{2}) \S+ sshd\[\d+\]: "
    r"Accepted password for \S+ from (?P<ip>[\d.]+) port \d+ ssh2"
)

# Rule parameters, copied from rules/T1110-brute-force.xml -- keep in sync
# by hand for now; scripts/validate-rules.sh could be extended to assert
# these constants match the XML directly (see ROADMAP.md).
RULE_100010_FREQUENCY = 8
RULE_100010_TIMEFRAME_SECONDS = 120


@dataclass
class Event:
    ts: datetime
    ip: str
    kind: str  # "failed" or "accepted"


def parse_log(path: str, assumed_year: int = 2026) -> list[Event]:
    events: list[Event] = []
    with open(path) as f:
        for line in f:
            line = line.rstrip("\n")
            if not line or line.startswith("#"):
                continue
            m = FAILED_RE.match(line)
            kind = "failed"
            if not m:
                m = ACCEPTED_RE.match(line)
                kind = "accepted"
            if not m:
                print(f"WARNING: line did not match expected sshd format, skipped: {line!r}", file=sys.stderr)
                continue
            ts = datetime.strptime(f"{assumed_year} {m.group('ts')}", "%Y %b %d %H:%M:%S")
            events.append(Event(ts=ts, ip=m.group("ip"), kind=kind))
    return events


def simulate_rule_100010(events: list[Event]) -> dict | None:
    """Rule 100010: frequency=8, timeframe=120, same_source_ip, on 'failed'
    events (sid 5710 equivalent). Returns the firing event (index + event)
    the first time any IP accumulates 8 'failed' events within a 120s
    sliding window, or None if it never fires."""
    by_ip: dict[str, list[Event]] = {}
    for i, ev in enumerate(events):
        if ev.kind != "failed":
            continue
        by_ip.setdefault(ev.ip, []).append(ev)
        window = by_ip[ev.ip]
        if len(window) >= RULE_100010_FREQUENCY:
            last_n = window[-RULE_100010_FREQUENCY:]
            span = (last_n[-1].ts - last_n[0].ts).total_seconds()
            if span <= RULE_100010_TIMEFRAME_SECONDS:
                return {
                    "fired": True,
                    "at_event_index": i,
                    "attempt_number_for_ip": len(window),
                    "ip": ev.ip,
                    "fired_at_ts": ev.ts,
                    "first_attempt_ts": events[0].ts if events else None,
                    "seconds_after_first_attempt": (ev.ts - events[0].ts).total_seconds(),
                }
    return {"fired": False}


def simulate_rule_100011(events: list[Event], rule_100010_result: dict) -> dict:
    """Rule 100011: if_sid 100010 AND if_matched_sid 5715 (accepted), same IP,
    after 100010 already fired."""
    if not rule_100010_result.get("fired"):
        return {"fired": False, "reason": "parent rule 100010 never fired"}

    ip = rule_100010_result["ip"]
    fired_at = rule_100010_result["fired_at_ts"]
    for ev in events:
        if ev.kind == "accepted" and ev.ip == ip and ev.ts >= fired_at:
            return {
                "fired": True,
                "ip": ip,
                "accepted_at_ts": ev.ts,
                "seconds_after_100010_fired": (ev.ts - fired_at).total_seconds(),
            }
    return {"fired": False, "reason": "no accepted login from that IP after rule 100010 fired"}


def main() -> None:
    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} <path-to-auth-log-excerpt>", file=sys.stderr)
        sys.exit(1)

    path = sys.argv[1]
    events = parse_log(path)
    if not events:
        print("No parseable sshd lines found.", file=sys.stderr)
        sys.exit(1)

    print(f"Parsed {len(events)} sshd event(s) from {path}")
    print(f"  {sum(1 for e in events if e.kind == 'failed')} failed, "
          f"{sum(1 for e in events if e.kind == 'accepted')} accepted")
    print()

    r10 = simulate_rule_100010(events)
    print("Rule 100010 (brute-force burst detector):")
    if r10["fired"]:
        print(f"  FIRED at attempt #{r10['attempt_number_for_ip']} for {r10['ip']}, "
              f"{r10['seconds_after_first_attempt']:.0f}s after the first attempt in this log.")
    else:
        print("  did NOT fire within this log excerpt.")
    print()

    r11 = simulate_rule_100011(events, r10)
    print("Rule 100011 (successful login shortly after burst):")
    if r11["fired"]:
        print(f"  FIRED: accepted login from {r11['ip']} "
              f"{r11['seconds_after_100010_fired']:.0f}s after rule 100010 fired.")
    else:
        print(f"  did NOT fire ({r11['reason']}).")


if __name__ == "__main__":
    main()
