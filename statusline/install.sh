#!/usr/bin/env bash
# Namesti status line (zasedenost konteksta + poraba limitov Session/Weekly):
#   - kopira statusline-tokens.py v ~/.claude/
#   - v ~/.claude/settings.json nastavi samo blok "statusLine" (ostale nastavitve ostanejo)
# Varno za večkratni zagon.
set -euo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"
PY="$(command -v python3)" || { echo "python3 ni najden" >&2; exit 1; }
mkdir -p "$HOME/.claude"
cp "$HERE/statusline-tokens.py" "$HOME/.claude/statusline-tokens.py"
chmod +x "$HOME/.claude/statusline-tokens.py"
SETTINGS="$HOME/.claude/settings.json" CMD="$PY $HOME/.claude/statusline-tokens.py" "$PY" - <<'PYEOF'
import json, os
p = os.environ["SETTINGS"]
d = {}
if os.path.exists(p):
    with open(p) as f:
        d = json.load(f)
d["statusLine"] = {"type": "command", "command": os.environ["CMD"], "padding": 0}
with open(p, "w") as f:
    json.dump(d, f, indent=2); f.write("\n")
PYEOF
echo "Status line nameščen. Preizkus:"
echo '{"context_window":{"current_usage":{"input_tokens":330000}},"rate_limits":{"five_hour":{"used_percentage":59},"seven_day":{"used_percentage":33}}}' | "$PY" "$HOME/.claude/statusline-tokens.py"; echo
