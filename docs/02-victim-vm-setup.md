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

## Installing the Wazuh agent (Windows victim)

```powershell
Invoke-WebRequest -Uri https://packages.wazuh.com/4.x/windows/wazuh-agent-4.9.0-1.msi -OutFile wazuh-agent.msi
msiexec.exe /i wazuh-agent.msi /q WAZUH_MANAGER='192.168.56.10'
Start-Service -Name WazuhSvc
```

## Installing the Wazuh agent (Linux victim)

```bash
curl -o wazuh-agent.deb https://packages.wazuh.com/4.x/apt/pool/main/w/wazuh-agent/wazuh-agent_4.9.0-1_amd64.deb
sudo WAZUH_MANAGER='192.168.56.10' dpkg -i ./wazuh-agent.deb
sudo systemctl enable --now wazuh-agent
```

Confirm the agent shows **Active** in Wazuh Dashboard → Agents.
