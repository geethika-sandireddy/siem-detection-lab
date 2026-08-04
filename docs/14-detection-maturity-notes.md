# 14 — Where This Sits on a Detection Maturity Curve

Roughly mapping this lab against common SOC maturity models (e.g. the
Pyramid of Pain / David Bianco):

| Detection basis used here | Pyramid of Pain level | Durability |
|---|---|---|
| Specific command-line flags (`-enc`, etc.) | Tools | Low — trivially changed by attacker |
| GrantedAccess bitmask on LSASS | Tools / TTPs boundary | Medium |
| LogonType + off-hours timing | Host artifacts / TTPs | Medium-high |
| Cross-technique correlation (chained-attack.xml) | TTPs | Highest — behavior-based, harder to route around |

The takeaway reflected in this repo's rule set: single indicator-of-tool
rules (Layer 1 of T1059.001) are cheap to write and useful as a first
filter, but the correlation rule and the behavior-based LSASS access rule
sit higher up the pyramid and would survive an attacker changing tools.
