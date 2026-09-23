# secret-sauce

Trei prezentări în română, fiecare cu tema ei. Deschide `index.html`.

| # | Prezentare | Temă | Fonturi |
|---|---|---|---|
| 01 | [Arch, de jos în sus](linux/index.html) | Catppuccin Mocha + albastrul Arch, bara de sus e un waybar (workspace = capitol) | Martian Mono, JetBrains Mono |
| 02 | [Claude, pe bune](claude/index.html) | paleta Anthropic: ivory, slate, clay | Newsreader, Hanken Grotesk, JetBrains Mono |
| 03 | [Servere & agenți](agenti/index.html) | camera serverelor noaptea: șine de rack, gravurile Hermes, roșul OpenClaw | Bodoni Moda, IBM Plex Mono |

## Taste

`←` `→` / spațiu / click · `F` ecran complet · swipe pe telefon (ținut orizontal) · `Ctrl+P` → PDF, un slide pe pagină.
`#7` la finalul adresei deschide direct slide-ul 7.

## Decizia estetică

- **Public:** un prieten care pornește de la zero. Puține cuvinte pe slide; restul îl spui tu.
- **Linux:** arată ca un desktop tiling adevărat. Stiva de straturi, bootul, inelele kernelului, ferestrele care se așază singure: toate sunt SVG și CSS animate, nu imagini.
- **Claude:** documentar, editorial, în stilul Anthropic. Elementul care rămâne în minte: scânteia care se rotește și spinner-ul din Claude Code, cu glifele și verbele lui.
- **Agenți:** gravurile oficiale Hermes, alb-negru, pe cerneală. Fiecare slide e o unitate de rack (U01…U19).

## De unde vin materialele

- Capturi: KDE (kde.org), Hyprland (concursul de ricing de pe hypr.land), Claude Code (claude.com), WhatsApp cu OpenClaw (docs.openclaw.ai).
- Gravuri Hermes: hermes-agent.nousresearch.com. Logo OpenClaw: docs.openclaw.ai. Logo Arch: Simple Icons.
- Prețuri și modele Claude: septembrie 2026, per 1M tokeni (intrare / ieșire).
- Comenzile de instalare OpenClaw și Hermes: README-urile oficiale, septembrie 2026.
- Fonturile sunt găzduite local (`assets/fonts`, subseturi latin + latin-ext pentru diacritice). Fonturile Anthropic nu sunt libere, așa că Newsreader și Hanken Grotesk țin locul lor.
- La Bodoni, cifrele și cratima sunt linii foarte subțiri și dispar pe proiector, așa că `bodoni-core.css` le trimite pe Newsreader.

## Structură

```
index.html          pagina de start
deck/               motorul comun (scalare 1600×900, taste, animații de intrare)
linux/ claude/ agenti/
assets/             fonturi, capturi, gravuri, miniaturi
```

Merge și direct din fișier (dublu-click pe `index.html`), fără server.
