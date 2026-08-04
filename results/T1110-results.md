# T1110.001 — Brute Force: Password Guessing

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
once a login succeeds).

## What showed up in Wazuh

`/var/log/auth.log` on the victim, forwarded by the agent, produced a
`sshd` decoder match with `srcip` and `dstuser` extracted per failed
attempt. Wazuh's out-of-the-box ruleset already has generic SSH brute-force
rules (`5710`–`5712`), but they're tuned for noisy internet-facing servers
(threshold ~8 failures in a wide window) — I wrote a tighter custom rule for
a low-traffic lab host to see the mechanism, not just rely on the default.
