#!/usr/bin/env bash
# scripts/validate-structure.sh
# Study System Structure Validator
# Run from project root: bash scripts/validate-structure.sh
# Exit 0 = all checks pass, 1 = any check fails

set -euo pipefail
errors=0

RED='\033[0;31m'; GREEN='\033[0;32m'; YELLOW='\033[0;33m'; NC='\033[0m'
pass() { echo -e "${GREEN}[PASS]${NC} $1"; }
fail() { echo -e "${RED}[FAIL]${NC} $1"; errors=$((errors+1)); }
warn() { echo -e "${YELLOW}[WARN]${NC} $1"; }

PROJECT_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$PROJECT_ROOT"

echo "=== Study System Structure Validation ==="
echo ""

# ---- Check 1: CLAUDE.md line count ----
echo "--- Check 1: CLAUDE.md line count ---"
if [ -f CLAUDE.md ]; then
    lines=$(wc -l < CLAUDE.md)
    if [ "$lines" -le 120 ]; then
        pass "CLAUDE.md: ${lines} lines (<= 120)"
    else
        fail "CLAUDE.md: ${lines} lines (> 120, target <= 120)"
    fi
else
    fail "CLAUDE.md not found"
fi
echo ""

# ---- Check 2: docs/ references in CLAUDE.md resolve ----
echo "--- Check 2: docs/ references in CLAUDE.md ---"
if [ -f CLAUDE.md ]; then
    refs=$(grep -oP '\(docs/[^)]+\)' CLAUDE.md | sed 's/[()]//g' 2>/dev/null || true)
    if [ -z "$refs" ]; then
        fail "No docs/ references found in CLAUDE.md"
    else
        while IFS= read -r ref; do
            if [ -f "$ref" ]; then
                pass "Referenced file exists: $ref"
            else
                fail "Referenced file MISSING: $ref"
            fi
        done <<< "$refs"
    fi
else
    warn "CLAUDE.md not found, skipping doc reference check"
fi
echo ""

# ---- Check 3: Skill frontmatter ----
echo "--- Check 3: Skill frontmatter validation ---"
if [ -d .claude/skills ]; then
    skill_count=0
    for skill_dir in .claude/skills/*/; do
        [ -d "$skill_dir" ] || continue
        skill_count=$((skill_count + 1))
        skill_name=$(basename "$skill_dir")
        skill_file="${skill_dir}SKILL.md"
        if [ ! -f "$skill_file" ]; then
            fail "Skill '${skill_name}': SKILL.md not found"
            continue
        fi
        fm=$(sed -n '/^---$/,/^---$/p' "$skill_file" 2>/dev/null || true)
        # Check name field
        if echo "$fm" | grep -q '^name:'; then
            pass "Skill '${skill_name}': name field present"
        else
            fail "Skill '${skill_name}': name field MISSING in frontmatter"
        fi
        # Check description field (handles inline, pipe, and folded block scalars)
        if echo "$fm" | grep -qE '^description:'; then
            pass "Skill '${skill_name}': description field present"
        else
            fail "Skill '${skill_name}': description field MISSING in frontmatter"
        fi
    done
    echo "  ($skill_count skills checked)"
else
    fail ".claude/skills/ directory not found"
fi
echo ""

# ---- Check 4: Template frontmatter ----
echo "--- Check 4: Template frontmatter validation ---"
valid_types="concept|practice|compare|cheat-sheet|experience"
if [ -d templates ]; then
    tmpl_count=0
    for tmpl in templates/*.md; do
        [ -f "$tmpl" ] || continue
        tmpl_count=$((tmpl_count + 1))
        tmpl_name=$(basename "$tmpl")
        fm=$(sed -n '/^---$/,/^---$/p' "$tmpl" 2>/dev/null || true)
        if echo "$fm" | grep -q '^type:'; then
            type_val=$(echo "$fm" | grep '^type:' | sed 's/^type: *//')
            if echo "$type_val" | grep -qiE "^(${valid_types})$"; then
                pass "Template '${tmpl_name}': type='${type_val}' (valid)"
            else
                fail "Template '${tmpl_name}': type='${type_val}' (INVALID, must be: ${valid_types})"
            fi
        else
            fail "Template '${tmpl_name}': type field MISSING in frontmatter"
        fi
    done
    echo "  ($tmpl_count templates checked)"
else
    fail "templates/ directory not found"
fi
echo ""

# ---- Check 5: Config file required fields ----
echo "--- Check 5: Config file validation ---"
if [ -f .obsidian-config.md ]; then
    for field in VAULT_PATH SYSTEM_ROOT OUTPUT_PATH; do
        if grep -q "^${field}:" .obsidian-config.md; then
            pass ".obsidian-config.md: ${field} present"
        else
            fail ".obsidian-config.md: ${field} MISSING"
        fi
    done
else
    fail ".obsidian-config.md not found"
fi
echo ""

# ---- Summary ----
echo "=== Results: ${errors} error(s) ==="
if [ "$errors" -gt 0 ]; then
    echo -e "${RED}STRUCTURE VALIDATION FAILED${NC}"
    exit 1
else
    echo -e "${GREEN}STRUCTURE VALIDATION PASSED${NC}"
    exit 0
fi
