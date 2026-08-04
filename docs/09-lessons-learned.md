# 09 — Lessons Learned

- **The rule is never the hard part — the log source is.** Every technique
  here needed some prerequisite (Sysmon config, script block logging,
  advanced audit policy) turned on before the "obvious" detection could
  even see the event. A detection engineer's real job is as much about log
  source coverage as it is about writing the rule syntax.
- **Test the negative case, not just the positive one.** The T1053.005
  path-heuristic rule (`100032`) correctly *not* firing on the atomic's
  benign task path was as useful a data point as the rules that did fire —
  it confirmed the rule wasn't just always-on.
- **Noise-suppression should come before, not after, a rule ships.** Adding
  the AV/WMI exemption for LSASS access (`100041`) *before* running the
  attack simulation, based on idle-baseline observation, felt like the
  right order of operations compared to shipping a noisy rule and tuning
  reactively.
- **A "pass" isn't the same as "fully validated."** A couple of results in
  this lab (Layer 2 of T1059.001, the off-hours RDP rule) are logically
  sound but weren't exercised against a fully realistic payload or a real
  off-hours timestamp. Recording that distinction honestly in the results
  docs mattered more than inflating the pass count.
