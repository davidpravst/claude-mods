# Claude Mods

Moji modi za Claude Code.

## Status line — zasedenost konteksta (`statusline/`)

Progress bar iz kvadratkov, ki kaže, koliko konteksta pogovora (od 1M tokenov) je porabljenega:

```
■■■■■■■□□□□□□□□□□□□□ 37.1%  │  Session ■■■■■■□□□□ 59% do 22:10  │  Teden ■■■□□□□□□□ 33% do 14. 10. 13:00
```

- **Kontekst:** 🟢 < 35 % · 🟠 35–50 % · 🔴 > 50 %. En kvadratek = 5 %.
- **Session (5 h) in Teden (7 dni):** poraba limita iz Claude Code (`rate_limits`), s časom ponastavitve. 🟢 < 50 % · 🟠 50–80 % · 🔴 > 80 %. En kvadratek = 10 %.

**Namestitev:**

```bash
gh repo clone davidpravst/claude-mods ~/Claude/claude-mods
~/Claude/claude-mods/statusline/install.sh
```

Nato ponovno zaženi Claude Code (ali pošlji naslednje sporočilo).
