# 08 — Troubleshooting Notes

Issues actually hit while building this, in case they save someone else
time.

## Wazuh agent shows "Never connected"
Usually a firewall/port issue — the agent needs outbound 1514/UDP (or TCP if
configured) and 1515/TCP for enrollment to the manager. On the host-only
VirtualBox network this is rarely blocked, but double-check
`sudo ufw status` on the manager if it's enabled.

## Sysmon events not appearing in Wazuh
The `<location>` in `ossec.conf` must match the exact channel name
`Microsoft-Windows-Sysmon/Operational` — a typo here fails silently (no
error, just no events). Confirm the channel exists first with:
```powershell
Get-WinEvent -ListLog "Microsoft-Windows-Sysmon/Operational"
```

## Custom rule not firing at all
Check the rule ID doesn't collide with an existing local or default rule ID
(Wazuh silently prefers the first-loaded definition in some conflict
cases). Local custom rule IDs should stay in the `100000+` range, which is
reserved for user rules.

## Event 4698 never shows up even after enabling auditing
`auditpol` changes can require a policy refresh or reboot to fully take on
some Windows builds. Confirm with:
```powershell
auditpol /get /subcategory:"Other Object Access Events"
```
