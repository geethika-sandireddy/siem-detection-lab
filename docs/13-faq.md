# 13 — FAQ

**Q: Why Wazuh instead of Splunk?**
Both are used in the real market, but Wazuh's rule engine is free without
any ingest cap, which matters for a lab where you want to leave things
running and generating baseline noise for a while. Splunk Free's 500MB/day
cap is easy to hit once Sysmon is verbose-logging.

**Q: Why Atomic Red Team instead of a full red-team framework (Cobalt Strike, Metasploit)?**
Scope and safety. Atomic tests are single, documented, reversible actions
mapped 1:1 to a MITRE technique — ideal for isolating exactly one detection
opportunity at a time. A full C2 framework is a different (and much
heavier) project.

**Q: Are these rules production-ready?**
No — see [06-limitations.md](06-limitations.md). They're a solid starting
point and demonstrate the detection-engineering workflow, but would need
broader allow-listing, testing against a noisier real environment, and
review against current evasion techniques before shipping.

**Q: Why 100000+ for custom rule IDs?**
Wazuh reserves that range for local/user-defined rules so they never
collide with IDs in the shipped default ruleset — see
[16-detection-as-code.md](16-detection-as-code.md).
