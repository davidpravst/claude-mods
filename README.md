# Claude Mods

Moji modi za Claude Code.

## Status line — zasedenost konteksta (`statusline/`)

Progress bar iz kvadratkov, ki kaže, koliko konteksta pogovora (od 1M tokenov) je porabljenega:

```
■■■■■■■□□□□□□□□□□□□□ 35.6% (356,306 / 1M tokens)
```

Barva: 🟢 < 35 % · 🟠 35–50 % · 🔴 > 50 %. En kvadratek = 5 %, natančna vrednost je v številki.

**Namestitev:**

```bash
gh repo clone davidpravst/claude-mods ~/Claude/claude-mods
~/Claude/claude-mods/statusline/install.sh
```

Nato ponovno zaženi Claude Code (ali pošlji naslednje sporočilo).
