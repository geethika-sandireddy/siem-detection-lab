# 00 — Project Overview

## Why this project exists

Most "SOC in a box" tutorials stop at installing the SIEM. This project goes
one step further: every detection rule here was written *against a real,
observed attack run* — not copy-pasted from a blog post — using the loop:

1. Run an Atomic Red Team test (a single, documented attacker action).
2. Look at what actually showed up in Wazuh.
3. Write a rule that fires on that evidence.
4. Re-run the test to confirm the rule fires (true positive).
5. Note what a smarter attacker could do to dodge the rule (limitation).

## Architecture

```
 ┌─────────────────────┐        logs / events        ┌───────────────────────┐
 │   Victim VM          │ ───────────────────────────▶│   Wazuh Manager        │
 │  (Windows or Linux)  │   Wazuh agent (+ Sysmon on  │  + Indexer + Dashboard │
 │  Atomic Red Team     │   Windows) forwards events   │                       │
 └─────────────────────┘                               └───────────────────────┘
          ▲
          │ executes
 ┌─────────────────────┐
 │  Attacker actions    │
 │  (Atomic Red Team    │
 │   test library)      │
 └─────────────────────┘
```

Both VMs run locally (VirtualBox), on a host-only network so nothing is
exposed to the internet. See [01-environment-setup.md](01-environment-setup.md).
