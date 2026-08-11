# Roadmap / Future Work

Ideas for a v2, not built yet:

- [ ] Add a network layer (Suricata or Zeek) for the C2/tunneling blind spot noted in limitations
- [ ] Replace the fixed-threshold brute-force rule with a rolling baseline/anomaly approach
- [ ] Test the correlation rule against an actual chained atomic sequence, not just isolated techniques
- [ ] Validate T1059.001 Layer 2 against a realistic malicious payload (downloader/stager), not just the benign atomic default
- [ ] Add a second Linux victim technique (e.g. T1548 sudo abuse) for OS coverage balance
- [ ] Capture real dashboard screenshots into `screenshots/`
- [x] ~~Wire up `wazuh-logtest` in a small CI check~~ — partially addressed: `scripts/simulate_rule_match.py` re-implements the T1110 rule's matching logic in Python and runs in CI against the sample logs (see `results/T1110-results.md`). This is **not** the same as real `wazuh-logtest`, which runs against the actual Wazuh rule engine and would catch bugs a hand-rolled reimplementation can't (decoder mismatches, field-extraction issues, ruleset ordering effects). Still worth doing for real; this was the tractable subset achievable without a live Wazuh install.
- [ ] Run the actual `wazuh-logtest` CLI against all 5 rule files (requires a real Wazuh manager install, not just the rule XML)
- [ ] Extend rule-logic simulation to the four Windows/Sysmon-based rules (T1059.001, T1053.005, T1003.001, T1021.001) — harder than T1110 because it requires faithfully replicating Wazuh's Sysmon field decoders, not just a regex over syslog lines
- [ ] The actual live VM run (Vagrant up, real atomic execution, real Wazuh alerts) — this is still the biggest open item; everything above only strengthens confidence in the rule *logic*, not in the full pipeline
