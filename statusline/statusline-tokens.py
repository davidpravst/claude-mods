#!/usr/bin/env python3
"""Claude Code status line: session token usage as % of 1M context.

Green < 33%  |  Orange 33-50%  |  Red > 50%

Prefers the `context_window` block from the status-line stdin JSON (Claude Code
>= ~2.1). Falls back to parsing the transcript for older versions.
"""
import sys
import json

MAX_TOKENS = 1_000_000

GREEN = "\033[32m"
ORANGE = "\033[38;5;208m"
RED = "\033[31m"
DIM = "\033[2m"
RESET = "\033[0m"


def tokens_from_stdin(data):
    """Context tokens from the stdin `context_window` block, if present."""
    cw = data.get("context_window")
    if not isinstance(cw, dict):
        return None
    cu = cw.get("current_usage")
    if isinstance(cu, dict):
        total = (
            cu.get("input_tokens", 0)
            + cu.get("cache_creation_input_tokens", 0)
            + cu.get("cache_read_input_tokens", 0)
        )
        if total:
            return total
    # Fallback within the block.
    if cw.get("total_input_tokens"):
        return cw["total_input_tokens"]
    return None


def tokens_from_transcript(transcript_path):
    """Context tokens from the most recent main-chain assistant turn."""
    try:
        with open(transcript_path, "r") as f:
            lines = f.readlines()
    except (OSError, TypeError):
        return 0

    for line in reversed(lines):
        line = line.strip()
        if not line:
            continue
        try:
            obj = json.loads(line)
        except json.JSONDecodeError:
            continue
        if obj.get("isSidechain"):  # skip subagent turns
            continue
        msg = obj.get("message", {})
        if msg.get("role") != "assistant":
            continue
        u = msg.get("usage")
        if not u:
            continue
        total = (
            u.get("input_tokens", 0)
            + u.get("cache_creation_input_tokens", 0)
            + u.get("cache_read_input_tokens", 0)
        )
        if total:
            return total
    return 0


BAR_WIDTH = 20


def progress_bar(pct, color):
    """Srednje debel progress bar (spodnja polovica znaka) s 1/2 natančnostjo."""
    pct = max(0.0, min(pct, 100.0))
    halves = round(pct / 100 * BAR_WIDTH * 2)
    full, half = divmod(halves, 2)
    cells = []
    for i in range(BAR_WIDTH):
        if i < full:
            cells.append(f"{color}▄")
        elif i == full and half:
            cells.append(f"{color}▖")
        else:
            cells.append(f"{DIM}▄")
    return "".join(cells) + RESET


def main():
    try:
        data = json.load(sys.stdin)
    except (json.JSONDecodeError, ValueError):
        data = {}

    tokens = tokens_from_stdin(data)
    if tokens is None:
        tokens = tokens_from_transcript(data.get("transcript_path", ""))

    pct = tokens / MAX_TOKENS * 100

    if pct > 50:
        color = RED
    elif pct >= 33:
        color = ORANGE
    else:
        color = GREEN

    sys.stdout.write(
        f"{progress_bar(pct, color)} {color}{pct:.1f}%{RESET} "
        f"{DIM}({tokens:,} / 1M tokens){RESET}"
    )


if __name__ == "__main__":
    main()
