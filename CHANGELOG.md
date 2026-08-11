# Changelog

## v0.2 (T1110 rule-logic simulation)
- Added `scripts/simulate_rule_match.py`: computes T1110 rule firing (rules
  100010/100011) from real parsed sshd log timestamps, replacing hand-traced
  reasoning for that technique.
- Added `results/sample-logs/T1110-auth-log-run2-slow-drip.txt` — the
  slow-drip scenario referenced in results/T1110-results.md previously had
  no corresponding log artifact.
- Corrected `results/T1110-results.md`: Run 1's "fires ~22s after burst"
  claim was a hand-tracing error; the actual computed value is 14s.
- Added `scripts/test_simulate_rule_match.py` (5 unit tests) and wired both
  into CI (`.github/workflows/validate-rules.yml`).
- Still open: the other 4 techniques remain hand-traced (harder to simulate
  faithfully — Sysmon/Windows field decoding), and no technique has been
  run against a live Wazuh agent yet. See ROADMAP.md.

## v0.1 (initial build)
- Environment setup docs (Wazuh, Splunk alt, victim VMs, Sysmon, ART)
- 5 techniques selected and mapped to MITRE ATT&CK
- Detection rules + test results for all 5 techniques
- Cross-technique correlation rule (first pass)
- Limitations, lessons learned, troubleshooting, FAQ, glossary docs
