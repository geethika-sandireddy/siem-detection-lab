# 12 — Rule Testing Checklist

Used for each of the 5 rules before marking it "done" in the summary table.

- [ ] Rule loads without a Wazuh manager syntax error (`/var/ossec/bin/wazuh-logtest`)
- [ ] Required log source/audit policy confirmed enabled *before* testing
- [ ] Baseline idle period checked for false positives before the attack run
- [ ] Atomic executed, rule confirmed to fire in the dashboard
- [ ] Atomic cleanup step run afterward
- [ ] A plausible evasion noted, even if not built (see limitations doc)
- [ ] Result recorded in `results/<ID>-results.md`, including partial/negative results
