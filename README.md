# SIEM Detection Lab

A home-lab SOC (Security Operations Center) environment built to practice
detection engineering: simulate real attack techniques with **Atomic Red
Team**, ingest telemetry into a **Wazuh** SIEM, and write detection rules
mapped to **MITRE ATT&CK**.

> **Status: build complete, execution pending.** All rules, install
> scripts, VM provisioning (Vagrantfile), and docs are written and the
> rule XML is validated (`scripts/validate-rules.sh`, wired into CI). What
> hasn't happened yet is running it on real VMs — the results in
> `results/*.md` describe expected outcomes based on how each rule and log
> source actually works, not verified live test evidence. See
> [docs/17-deploying-this-repo.md](docs/17-deploying-this-repo.md) to run
> it and replace expected results with real ones.

## Contents

- [Goal](#goal)
- [Repo structure](#repo-structure)
- [Techniques covered](#techniques-covered)
- [Quick start](#quick-start)
- [Honest limitations](#honest-limitations)

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

## Quick start

1. [Set up the Wazuh manager](docs/01-environment-setup.md)
2. [Set up the victim VM(s)](docs/02-victim-vm-setup.md)
3. [Install Atomic Red Team on the victim](docs/03-atomic-red-team-setup.md)
4. Run an atomic (`scripts/run-atomics.ps1` or `scripts/run-brute-force.sh`)
5. Drop the matching rule from `rules/` into your Wazuh manager's
   `local_rules.xml` and restart the manager
6. Confirm the alert in the Wazuh Dashboard

## Honest limitations

This is a lab, not a production SOC. See
[docs/06-limitations.md](docs/06-limitations.md) for what these rules do
*not* catch — slow/low brute force, LOLBin evasion of command-line rules,
missing audit-policy prerequisites, no network-layer detection, and no
cross-technique correlation.
