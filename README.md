# Claude Mods

## Status line — kontekst in poraba limitov (`statusline/`)

Status line s progress bari iz kvadratkov: zasedenost konteksta pogovora (od 1M tokenov) ter poraba 5-urnega in tedenskega limita:

```
Context ■■■■■■■□□□□□□□□□□□□□ 37.1%  │  Session (5 h) ■■■■■■□□□□ 59% resets 22:10  │  Weekly ■■■□□□□□□□ 33% resets 14 Oct 13:00
────────────────────────────────────────────────────────────────────────────────────────────────────
```

- **Context:** 🟢 < 35 % · 🟠 35–50 % · 🔴 > 50 %. En kvadratek = 5 %.
- **Session (5 h) in Weekly (7 dni):** poraba limita iz Claude Code (`rate_limits`), s časom ponastavitve. 🟢 < 50 % · 🟠 50–80 % · 🔴 > 80 %. En kvadratek = 10 %.

**Namestitev:**

```bash
gh repo clone davidpravst/claude-mods ~/Claude/claude-mods
~/Claude/claude-mods/statusline/install.sh
```

Nato ponovno zaženi Claude Code (ali pošlji naslednje sporočilo).
