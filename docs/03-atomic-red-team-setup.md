# 03 — Installing Atomic Red Team

Atomic Red Team (by Red Canary) is a library of small, well-documented tests,
each mapped to a specific MITRE ATT&CK technique ID. Each "atomic" does the
minimum needed to trigger a detection opportunity — it is **not** a full
exploit chain, which is exactly what makes it safe for a lab.

## Install (Windows victim, PowerShell as Administrator)

```powershell
Install-Module -Name invoke-atomicredteam,powershell-yaml -Scope CurrentUser -Force
Import-Module invoke-atomicredteam -Force
Install-AtomicRedTeam -getAtomics
```

This clones the atomics library to `C:\AtomicRedTeam\atomics`.

## Sanity check

```powershell
Invoke-AtomicTest T1082 -ShowDetailsBrief
```

Should list the "System Information Discovery" tests without executing
anything (`-ShowDetailsBrief` is read-only).

## Safety notes

- Run only against the isolated lab VM, never a shared or production host.
- Some atomics modify the registry or create local users — snapshot the VM
  before starting so it's easy to roll back.
- Always run the matching `-Cleanup` command after a test where one exists.
