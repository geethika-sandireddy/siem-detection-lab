# SIEM Detection Lab

A home-lab SOC (Security Operations Center) environment built to practice
detection engineering: simulate real attack techniques with **Atomic Red
Team**, ingest telemetry into a **Wazuh** SIEM, and write detection rules
mapped to **MITRE ATT&CK**.

> Status: 🚧 in progress — see [docs/](docs/) for build log.

## Goal

Stand up a small, realistic SOC pipeline end-to-end:

1. Deploy a SIEM (Wazuh).
2. Deploy a victim VM and forward its logs/telemetry to the SIEM.
3. Use Atomic Red Team to safely execute real attacker techniques on the
   victim, mapped to MITRE ATT&CK.
4. Write and tune detection rules for each technique.
5. Document what was caught, what was missed, and why.

The point isn't the tools — it's the detection engineering loop:
**simulate → observe → write rule → test → tune → document.**

## Repo structure

```
siem-detection-lab/
├── docs/            build log, setup guides, MITRE mapping, limitations
├── rules/           Wazuh detection rules (XML), one per technique
├── results/         per-technique test write-ups: what fired, what didn't
├── scripts/         helper scripts to run the atomics / simulations
└── screenshots/      evidence captures (dashboard alerts, raw events)
```

## Techniques covered

| ATT&CK ID | Technique |
|---|---|
| T1110.001 | Brute Force: Password Guessing |
| T1059.001 | PowerShell |
| T1053.005 | Scheduled Task |
| T1003.001 | OS Credential Dumping: LSASS Memory |
| T1021.001 | Remote Desktop Protocol |

Full results table with pass/fail detail: [docs/05-detection-summary-table.md](docs/05-detection-summary-table.md)
