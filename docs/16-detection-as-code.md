# 16 — Treating Detections as Code

A few practices carried over from software engineering, applied to the
rules in this repo:

- Every rule lives in version control alongside the test that validates it
  (`rules/<ID>.xml` next to `results/<ID>-results.md`), the same way you'd
  keep a unit test next to the function it covers.
- Rule IDs are kept in the `100000+` range, reserved for local/custom
  rules, so they never collide with Wazuh's shipped ruleset — the
  equivalent of not stomping on a library's namespace.
- Each rule's MITRE ATT&CK ID is embedded directly in the rule (`<mitre><id>`),
  so the mapping in `docs/04-mitre-attack-mapping.md` can never drift out
  of sync with what the rule actually claims to detect.
