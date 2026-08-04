# 10 — Cost & Hardware Notes

Everything in this build is free, but worth being precise about hardware:

| Component | Tool | Cost | RAM footprint |
|---|---|---|---|
| SIEM | Wazuh (all-in-one) | Free, open source | ~4 GB |
| Alt. SIEM | Splunk Free | Free (500MB/day ingest cap) | ~2 GB |
| Windows victim | Windows 10/11 dev VM (Microsoft's free 90-day eval image) | Free, time-limited | ~4 GB |
| Linux victim | Ubuntu Server 22.04 | Free | ~1 GB |
| Attack simulation | Atomic Red Team | Free, open source | negligible |
| Hypervisor | VirtualBox | Free | — |

Total recommended host RAM: **16 GB** to run manager + both victims
comfortably at once; 8GB is workable if VMs are run one at a time.

Microsoft's free Windows evaluation VM images expire after 90 days — fine
for a lab, not for a "leave it running" setup.
