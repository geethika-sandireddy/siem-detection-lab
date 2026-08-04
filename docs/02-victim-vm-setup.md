# 02 — Victim VM Setup

## Choice of victim OS

Windows 10/11 is used for the primary walkthrough because most of the
high-signal MITRE techniques (PowerShell abuse, scheduled tasks, LSASS
access) are Windows-native and Atomic Red Team's Windows library is the most
mature. A Linux victim (Ubuntu) is used for the brute-force (SSH) technique.

## Networking

Both VMs sit on a **VirtualBox Host-Only network** (e.g. `192.168.56.0/24`).
This keeps the whole exercise isolated from the internet and the host LAN —
important since we're deliberately running attack tooling.

- Manager: `192.168.56.10`
- Windows victim: `192.168.56.20`
- Linux victim: `192.168.56.21`
