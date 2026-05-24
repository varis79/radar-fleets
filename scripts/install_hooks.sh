#!/bin/bash
# install_hooks.sh — instala git hooks para este repo.
#
# Uso (una vez por checkout):
#   bash scripts/install_hooks.sh

set -e
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
HOOKS_DIR="$ROOT/.git/hooks"

if [ ! -d "$HOOKS_DIR" ]; then
  echo "❌ No es un repo git (.git/hooks no existe)"
  exit 1
fi

cat > "$HOOKS_DIR/pre-commit" <<'HOOK'
#!/bin/bash
set -e
ROOT="$(git rev-parse --show-toplevel)"
cd "$ROOT"

STAGED=$(git diff --cached --name-only --diff-filter=ACM | grep -E '(temas|mercados|casos-uso|sectores|ciudades|evergreen)/.*index\.html$' || true)

if [ -z "$STAGED" ]; then
  exit 0
fi

echo "🔍 qa_pillars: $(echo "$STAGED" | wc -l | tr -d ' ') páginas editoriales staged…"

FAIL=0
for f in $STAGED; do
  if [ -f "$f" ]; then
    RESULT=$(python3 scripts/qa_pillars.py --file "$f" 2>&1 | tail -3)
    if echo "$RESULT" | grep -q "FAIL"; then
      echo ""
      echo "❌ $f tiene riesgo editorial bloqueante:"
      python3 scripts/qa_pillars.py --file "$f" --verbose 2>&1 | tail -15
      FAIL=$((FAIL+1))
    fi
  fi
done

if [ $FAIL -gt 0 ]; then
  echo ""
  echo "🚫 $FAIL página(s) bloqueadas por qa_pillars."
  echo "   Para forzar el commit (no recomendado): git commit --no-verify"
  exit 1
fi

echo "✅ qa_pillars: todas las páginas editorial OK"
exit 0
HOOK

chmod +x "$HOOKS_DIR/pre-commit"
echo "✅ Pre-commit hook instalado en $HOOKS_DIR/pre-commit"
echo "   Bloqueará commits con páginas editorial que tengan cifras inventadas."
