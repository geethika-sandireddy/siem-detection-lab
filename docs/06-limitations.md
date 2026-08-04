# 06 — Limitations

Being upfront about what this lab does *not* catch is as much the point as
the rules that work.

## 1. Threshold/timeframe rules are evadable by slowing down
`T1110` (brute force) only fires within a 120-second, 8-attempt window. An
attacker doing low-and-slow password guessing (one attempt every few
minutes) defeats it entirely. A production fix would be a longer rolling
window with a lower per-window threshold, or better, an anomaly-based
baseline rather than a fixed count — out of scope for a rule-based lab SIEM
but worth naming.

## 2. Command-line detections are trivially evaded by an aware attacker
`T1059.001`'s Layer 1 rule keys off specific flags (`-enc`, `-nop`, etc).
Renaming `powershell.exe`, using `pwsh.exe`, invoking via COM, or building
the encoded string through string concatenation instead of a flag all
sidestep it. Layer 2 (script-block logging) is more robust since it
inspects decoded content, but wasn't exercised against a real
downloader-style payload in this lab — the atomic used produced benign
decoded content, so that rule's true-positive path is inferred from its
logic, not fully observed end-to-end.

## 3. Audit policy prerequisites are easy to silently miss
Both `T1053.005` (Event 4698) and general account-logon visibility depend
on non-default Windows advanced audit policy settings. A fleet that hasn't
explicitly enabled these will have "working" rules that never fire, with no
obvious error — this is arguably a bigger real-world risk than any single
missed technique.

## 4. No coverage for encrypted/tunneled C2
Nothing in this lab inspects TLS-wrapped or DNS-tunneled command and
control. All five techniques here are host-telemetry-based; there's no
network IDS (e.g. Suricata/Zeek) in this build, so any technique whose only
signal is on-the-wire traffic is fully out of scope.

## 5. Single-host, single-analyst scale
Rules were tuned against one victim VM generating almost no baseline noise.
Real environments running dozens of legitimate admin tools that also touch
LSASS, spawn PowerShell, or create scheduled tasks would need substantially
more allow-listing (see the `100041` suppression rule in
`T1003.001-lsass-dump.xml` for the one example built here) before these
rules could ship without an alert-fatigue problem.

## 6. Atomic Red Team tests are intentionally minimal
Each atomic does the smallest thing needed to trigger the technique. Real
intrusions chain multiple techniques together (e.g. phishing → PowerShell
→ scheduled task → LSASS dump → RDP lateral movement) and a mature SOC
would correlate *across* these five rules, not just alert on each in
isolation. This lab treats them as independent detections; a natural next
step (not built here) would be a correlation rule that raises severity when
two or more of these fire on the same host within a short window.
