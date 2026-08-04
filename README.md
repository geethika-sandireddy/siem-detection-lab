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
