#!/usr/bin/env bash
# install-wazuh-manager.sh
# Automated Wazuh all-in-one install for the manager VM (Ubuntu 22.04).
# Run as root/sudo. Idempotent-ish: safe to re-run, skips if already installed.
set -euo pipefail

if systemctl is-active --quiet wazuh-manager 2>/dev/null; then
  echo "[*] wazuh-manager already running, skipping install."
  exit 0
fi

echo "[*] Downloading Wazuh all-in-one installer..."
curl -sO https://packages.wazuh.com/4.9/wazuh-install.sh

echo "[*] Running installer (manager + indexer + dashboard)..."
bash ./wazuh-install.sh -a | tee wazuh-install.log

echo "[*] Done. Admin credentials are in wazuh-install.log (search for 'admin')."
echo "[*] Dashboard: https://$(hostname -I | awk '{print $1}'):443"

echo "[*] Deploying this repo's custom local rules..."
LOCAL_RULES="/var/ossec/etc/rules/local_rules.xml"
REPO_RULES="$(dirname "$0")/../rules/local_rules.xml"
if [ -f "$REPO_RULES" ]; then
  cp "$REPO_RULES" "$LOCAL_RULES"
  systemctl restart wazuh-manager
  echo "[*] Custom rules deployed and manager restarted."
else
  echo "[!] $REPO_RULES not found — build it first (see rules/local_rules.xml)."
fi
