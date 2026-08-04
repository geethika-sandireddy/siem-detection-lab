# 01 — Environment Setup: Wazuh SIEM

## Requirements

- Host machine: 8+ GB RAM free for VMs (Wazuh all-in-one wants ~4GB alone)
- VirtualBox (free) or VMware Player
- Ubuntu Server 22.04 ISO for the Wazuh manager VM

## Option A — Wazuh all-in-one (recommended for a home lab)

Wazuh ships a single install script that sets up the manager, indexer
(OpenSearch-based), and dashboard together.

```bash
curl -sO https://packages.wazuh.com/4.9/wazuh-install.sh
sudo bash ./wazuh-install.sh -a
```

This prints an admin password at the end — save it, you'll need it for the
dashboard login.

## Verify

- Dashboard reachable at `https://<manager-ip>:443`
- `sudo systemctl status wazuh-manager` → active (running)
