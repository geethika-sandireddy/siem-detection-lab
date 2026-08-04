# 04 — Techniques Selected

Five techniques were chosen to cover a spread of ATT&CK tactics rather than
clustering in one area (e.g. all-PowerShell), since real intrusions chain
across tactics.

| # | Technique | ATT&CK ID | Tactic | Victim OS |
|---|-----------|-----------|--------|-----------|
| 1 | Brute Force: Password Guessing | T1110.001 | Credential Access | Linux (SSH) |
| 2 | Command and Scripting Interpreter: PowerShell | T1059.001 | Execution | Windows |
| 3 | Scheduled Task/Job: Scheduled Task | T1053.005 | Persistence / Execution | Windows |
| 4 | OS Credential Dumping: LSASS Memory | T1003.001 | Credential Access | Windows |
| 5 | Remote Services: Remote Desktop Protocol | T1021.001 | Lateral Movement | Windows |

Full write-up per technique lives in `results/`, and each rule lives in
`rules/`. The rollup table with pass/fail is in
[05-detection-summary-table.md](05-detection-summary-table.md).
