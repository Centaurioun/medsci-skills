#!/usr/bin/env bash
# Regression test for scripts/validate_routing_assets.py — the gate that guards
# extracted references/ pointers (see docs/skill_references_load_model.md).
# Confirms a valid ${CLAUDE_SKILL_DIR}/references/... pointer passes and a
# dangling one fails under --strict. This is the coverage the validator lacked.
set -u

REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
V="$REPO_ROOT/scripts/validate_routing_assets.py"
TMP="$(mktemp -d)"
trap 'rm -rf "$TMP"' EXIT

pass=0
fail=0
ck() {
  local label="$1" expected="$2" actual="$3"
  if [ "$expected" = "$actual" ]; then
    printf '  PASS  %-46s exit=%s\n' "$label" "$actual"
    pass=$((pass + 1))
  else
    printf '  FAIL  %-46s expected=%s actual=%s\n' "$label" "$expected" "$actual"
    fail=$((fail + 1))
  fi
}

# 1) a valid ${CLAUDE_SKILL_DIR}/references/... pointer -> exit 0
mkdir -p "$TMP/good/references"
printf 'Body. See ${CLAUDE_SKILL_DIR}/references/exists.md before drafting.\n' > "$TMP/good/SKILL.md"
echo "ok" > "$TMP/good/references/exists.md"
python3 "$V" --strict --scan "$TMP/good/SKILL.md" > /dev/null 2>&1
ck "valid references/ pointer passes" 0 "$?"

# 2) a dangling pointer -> exit 1 under --strict
mkdir -p "$TMP/bad"
printf 'Body. See ${CLAUDE_SKILL_DIR}/references/missing.md before drafting.\n' > "$TMP/bad/SKILL.md"
python3 "$V" --strict --scan "$TMP/bad/SKILL.md" > /dev/null 2>&1
ck "dangling references/ pointer fails (--strict)" 1 "$?"

# 3) the same dangling pointer is reported but tolerated without --strict
python3 "$V" --scan "$TMP/bad/SKILL.md" > /dev/null 2>&1
ck "dangling pointer tolerated without --strict" 0 "$?"

# 4) the live repo's routing assets must be clean (the CI invariant)
python3 "$V" --strict > /dev/null 2>&1
ck "live repo routing assets clean" 0 "$?"

echo "----"
echo "test_routing_assets: $pass passed, $fail failed"
[ "$fail" -eq 0 ]
