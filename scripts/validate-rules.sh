#!/usr/bin/env bash
# validate-rules.sh
# Lints every rule XML file for well-formedness before it's deployed.
#
# Note: individual rules/*.xml files each have a single <group> root and
# validate as standard XML directly. local_rules.xml intentionally
# contains multiple sibling <group> blocks — valid for Wazuh's own
# (non-strict) config parser, but not standard single-root XML — so it's
# checked by wrapping it in a temporary root element instead.
set -euo pipefail

fail=0

echo "== Individual rule files =="
for f in $(find rules -name '*.xml' ! -name 'local_rules.xml'); do
  if xmllint --noout "$f" 2>/tmp/err; then
    echo "OK   $f"
  else
    echo "FAIL $f"
    cat /tmp/err
    fail=1
  fi
done

echo ""
echo "== Merged local_rules.xml (wrapped for strict-XML check) =="
tmp=$(mktemp)
{ echo "<root>"; cat rules/local_rules.xml; echo "</root>"; } > "$tmp"
if xmllint --noout "$tmp" 2>/tmp/err; then
  echo "OK   rules/local_rules.xml (multi-group, wrapped)"
else
  echo "FAIL rules/local_rules.xml"
  cat /tmp/err
  fail=1
fi
rm -f "$tmp"

exit $fail
