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

## Option B — Splunk Free (alternative)

Splunk Free allows up to 500MB/day ingest, which is plenty for a lab.

```bash
wget -O splunk.deb "<download link from splunk.com>"
sudo dpkg -i splunk.deb
sudo /opt/splunk/bin/splunk start --accept-license
```

Enable a listening port for forwarders:

```bash
sudo /opt/splunk/bin/splunk enable listen 9997
```

This project uses **Wazuh** for the worked examples (rules/, results/) since
its rule syntax is free to use without the daily-ingest ceiling, but the same
detections translate directly to Splunk SPL — see the "Splunk equivalent"
note at the bottom of each rule file.
