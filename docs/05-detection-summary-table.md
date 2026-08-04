# 05 — Detection Summary Table

| Attack Technique | ATT&CK ID | Detection Rule | Result |
|---|---|---|---|
| Brute Force: Password Guessing (SSH) | T1110.001 | [`rules/T1110-brute-force.xml`](../rules/T1110-brute-force.xml) | ✅ Fast burst caught in ~22s / ❌ slow-drip (1 attempt/30s) missed |
| PowerShell: encoded/obfuscated execution | T1059.001 | [`rules/T1059.001-powershell.xml`](../rules/T1059.001-powershell.xml) | ✅ Command-line layer caught it / ⚠️ decoded-content layer needs a more realistic malicious atomic to fully validate |
| Scheduled Task creation | T1053.005 | [`rules/T1053.005-scheduled-task.xml`](../rules/T1053.005-scheduled-task.xml) | ✅ Caught, but only after manually enabling the 4698 audit subcategory (off by default) |
| OS Credential Dumping: LSASS Memory | T1003.001 | [`rules/T1003.001-lsass-dump.xml`](../rules/T1003.001-lsass-dump.xml) | ✅ Caught cleanly; AV/WMI noise-suppression rule added proactively |
| Remote Services: RDP | T1021.001 | [`rules/T1021.001-rdp.xml`](../rules/T1021.001-rdp.xml) | ✅ Successful/failed RDP logons both caught; off-hours escalation syntax-tested only |
