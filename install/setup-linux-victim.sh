#!/usr/bin/env bash
# setup-linux-victim.sh
# Installs the Wazuh agent on the Linux victim VM (Ubuntu 22.04) and points
# it at the manager. Run as root/sudo.
#
# Usage: ./setup-linux-victim.sh <manager-ip>
set -euo pipefail

MANAGER_IP="${1:?usage: setup-linux-victim.sh <manager-ip>}"

echo "[*] Installing Wazuh agent, manager=${MANAGER_IP}..."
curl -o wazuh-agent.deb https://packages.wazuh.com/4.x/apt/pool/main/w/wazuh-agent/wazuh-agent_4.9.0-1_amd64.deb
WAZUH_MANAGER="${MANAGER_IP}" dpkg -i ./wazuh-agent.deb

systemctl daemon-reload
systemctl enable wazuh-agent
systemctl start wazuh-agent

echo "[*] Installing hydra (for the T1110 brute-force simulation, run from the attacker box, not here)..."
echo "[*] Agent status:"
systemctl status wazuh-agent --no-pager || true

echo "[*] Done. Verify this host shows 'Active' in Wazuh Dashboard > Agents."
