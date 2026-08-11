# T1110.001 — Brute Force: Password Guessing

> ⚠️ **Rule logic verified by simulation, not yet observed on a live Wazuh agent.** The numbers below are computed by `scripts/simulate_rule_match.py` against the actual sample logs in this repo — a real Python re-implementation of the rule's matching semantics (same_source_ip grouping, frequency/timeframe sliding window, parent-child chaining), run against real parsed timestamps. This replaces an earlier version of this table that was hand-traced from reading the XML and got the timing wrong (see note below). It is still **not** the same as watching `100010`/`100011` fire on a running Wazuh manager against live agent traffic — that step is still open, see docs/17-deploying-this-repo.md.

**Victim:** Linux (Ubuntu), SSH exposed on host-only network only.

## Atomic test used

Atomic Red Team T1110 doesn't ship a Linux SSH atomic by default, so this
one was simulated directly with `hydra` from a second lab VM (this is a
common, accepted substitution — the ATT&CK technique is about the *pattern*
of many failed auths, not the specific tool):

```bash
hydra -l labadmin -P /usr/share/wordlists/rockyou-sample.txt ssh://192.168.56.21 -t 4
```

15 failed attempts, then 1 success (the real password was seeded near the
end of the wordlist on purpose, to also verify the rule doesn't stop firing
once a login succeeds). The `hydra` run itself has not been executed on a
live VM pair yet; the log excerpts below are constructed to match this
described scenario and are what the simulator is run against.

## What showed up in Wazuh

`/var/log/auth.log` on the victim, forwarded by the agent, produced a
`sshd` decoder match with `srcip` and `dstuser` extracted per failed
attempt. Wazuh's out-of-the-box ruleset already has generic SSH brute-force
rules (`5710`–`5712`), but they're tuned for noisy internet-facing servers
(threshold ~8 failures in a wide window) — I wrote a tighter custom rule for
a low-traffic lab host to see the mechanism, not just rely on the default.

## Rule test result

Computed by `python3 scripts/simulate_rule_match.py <logfile>` against the
two log excerpts in `results/sample-logs/`:

| Run | Log file | Failures sent | Rule fired? | Time to fire |
|-----|----------|---------------|-------------|---------------|
| 1 (fast burst) | `T1110-auth-log-excerpt.txt` | 8 in 14s, then 1 accepted | ✅ rule `100010` at attempt #8, rule `100011` 2s later | 14s after the first attempt |
| 2 (slow drip: 1 attempt/30s) | `T1110-auth-log-run2-slow-drip.txt` | 15 over 7.5 min | ❌ did not fire | — outside the 120s timeframe window |

**Correction:** an earlier version of this table said Run 1 fired "~22s
after burst started," reasoned by hand from the rule's frequency/timeframe
values. The actual log timestamps (`02:14:01` → `02:14:15` for the 8th
failure) put it at 14s, not 22s — the hand-traced estimate was simply
wrong by 8 seconds. This is exactly the kind of small, easy-to-make error
that motivated writing `simulate_rule_match.py` instead of continuing to
eyeball it: the script derives it directly from the log content, and its
own behavior is covered in `scripts/test_simulate_rule_match.py` (fast
burst fires, slow drip doesn't, different source IPs don't combine, and
`100011` requires `100010` to have already fired).

**Verdict: partial catch.** The rule reliably catches a fast/naive brute
force but is blind to a slow, low-and-slow guesser that stays under the
frequency/timeframe threshold — a real attacker doing OPSEC-aware guessing
would tune around this. See [06-limitations](../docs/06-limitations.md).

