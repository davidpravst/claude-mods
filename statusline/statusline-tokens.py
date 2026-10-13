#!/usr/bin/env python3
"""Claude Code status line: session token usage as % of 1M context.

Green < 35%  |  Orange 35-50%  |  Red > 50%

Prefers the `context_window` block from the status-line stdin JSON (Claude Code
>= ~2.1). Falls back to parsing the transcript for older versions.
"""
import sys
import json
from datetime import datetime

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


USAGE_BAR_WIDTH = 10


def progress_bar(pct, color, width=BAR_WIDTH):
    """Progress bar iz kvadratkov: polni ■ v barvi stanja, prazni □ zatemnjeni."""
    pct = max(0.0, min(pct, 100.0))
    full = round(pct / 100 * width)
    return f"{color}{'■' * full}{RESET}{DIM}{'□' * (width - full)}{RESET}"


def usage_color(pct):
    """Poraba limita: zelena < 50 %, oranžna 50–80 %, rdeča > 80 %."""
    if pct > 80:
        return RED
    if pct >= 50:
        return ORANGE
    return GREEN


def format_reset(ts, with_date):
    """Reset time in local time: '22:10' or '14 Oct 13:00'."""
    try:
        t = datetime.fromtimestamp(float(ts))
    except (TypeError, ValueError, OSError):
        return ""
    return t.strftime(f"{t.day} %b %H:%M") if with_date else t.strftime("%H:%M")


def usage_segment(data):
    """Session (5 h) in tedenska (7 dni) poraba iz `rate_limits`, če so podatki na voljo."""
    rl = data.get("rate_limits")
    if not isinstance(rl, dict):
        return ""
    parts = []
    for key, label, with_date in (("five_hour", "Session (5 h)", False), ("seven_day", "Weekly", True)):
        lim = rl.get(key)
        if not isinstance(lim, dict) or lim.get("used_percentage") is None:
            continue
        pct = float(lim["used_percentage"])
        color = usage_color(pct)
        reset = format_reset(lim.get("resets_at"), with_date)
        reset = f" {DIM}resets {reset}{RESET}" if reset else ""
        parts.append(
            f"{DIM}{label}{RESET} {progress_bar(pct, color, USAGE_BAR_WIDTH)} "
            f"{color}{pct:.0f}%{RESET}{reset}"
        )
    return f"  {DIM}│{RESET}  ".join(parts)


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
    elif pct >= 35:
        color = ORANGE
    else:
        color = GREEN

    line = f"{DIM}Context{RESET} {progress_bar(pct, color)} {color}{pct:.1f}%{RESET}"
    usage = usage_segment(data)
    if usage:
        line += f"  {DIM}│{RESET}  {usage}"
    sys.stdout.write(line)


if __name__ == "__main__":
    main()
