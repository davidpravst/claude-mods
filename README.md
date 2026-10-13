# Claude Mods

Moji modi za Claude Code.

## Status line — zasedenost konteksta (`statusline/`)

Srednje debel progress bar, ki kaže, koliko konteksta pogovora (od 1M tokenov) je porabljenega:

```
▄▄▄▄▄▄▖▄▄▄▄▄▄▄▄▄▄▄▄▄ 33.0% (330,000 / 1M tokens)
```

Barva: 🟢 < 33 % · 🟠 33–50 % · 🔴 > 50 %. Natančnost pol znaka (2,5 %).

**Namestitev:**

```bash
gh repo clone davidpravst/claude-mods ~/Claude/claude-mods
~/Claude/claude-mods/statusline/install.sh
```

Nato ponovno zaženi Claude Code (ali pošlji naslednje sporočilo).
