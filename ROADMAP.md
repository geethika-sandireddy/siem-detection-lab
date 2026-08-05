# Roadmap / Future Work

Ideas for a v2, not built yet:

- [ ] Add a network layer (Suricata or Zeek) for the C2/tunneling blind spot noted in limitations
- [ ] Replace the fixed-threshold brute-force rule with a rolling baseline/anomaly approach
- [ ] Test the correlation rule against an actual chained atomic sequence, not just isolated techniques
- [ ] Validate T1059.001 Layer 2 against a realistic malicious payload (downloader/stager), not just the benign atomic default
- [ ] Add a second Linux victim technique (e.g. T1548 sudo abuse) for OS coverage balance
- [ ] Capture real dashboard screenshots into `screenshots/`
- [ ] Wire up `wazuh-logtest` in a small CI check so a future rule change is validated automatically before merge
