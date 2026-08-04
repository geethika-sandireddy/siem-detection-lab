# 11 — Glossary

- **SIEM** — Security Information and Event Management; a system that
  ingests logs/telemetry from many sources and lets you search, alert, and
  correlate across them.
- **Atomic (Atomic Red Team)** — a small, single-action test that
  reproduces one specific attacker technique, mapped to a MITRE ATT&CK ID.
- **LOLBin** ("living-off-the-land binary") — a legitimate, signed OS
  binary (e.g. `rundll32.exe`, `certutil.exe`) abused to perform malicious
  actions, making detection harder since the binary itself isn't malware.
- **Sysmon** — a free Microsoft Sysinternals tool that logs detailed
  process, network, and file activity to the Windows Event Log, far beyond
  what's captured by default.
- **True/False Positive** — a rule firing correctly on real malicious
  activity (true positive) vs. firing on benign activity (false positive).
- **MITRE ATT&CK** — a public knowledge base of adversary tactics and
  techniques, organized by ID (e.g. T1110 = Brute Force), used as a common
  vocabulary across the security industry.
