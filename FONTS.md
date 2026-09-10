# Vendored web fonts

Self-hosted so the site makes no third-party request to render text, and so a
Google Fonts outage or policy change cannot affect the docs. It also means no
reader's browser tells a third party which of our pages they are reading.

| File | Family | Faces | Bytes |
| --- | --- | --- | --- |
| `archivo-variable.woff2` | Archivo | variable, weight 400–600 upright | 34,940 |
| `jetbrains-mono.woff2` | JetBrains Mono | static, weight 400 | 21,212 |

Both are the **latin subset** as served by Google Fonts — the same bytes,
fetched once and committed rather than requested per visitor.

Three sizing decisions worth keeping:

* **Upright is one variable file, and the range stops at 600.** Google serves a
  variable file when you request a weight *range* and a smaller static instance
  when you request a single weight. The design language holds the display voice
  at 400 and subheads at 500, so 400–600 covers everything the stylesheets use.
  Widening the range to 700 costs bytes for a weight nothing renders.
* **No italic face is loaded.** Nothing in the published documentation renders
  italic, so shipping one would cost every reader roughly 16 KB for nothing. If
  italic prose is introduced, vendor `archivo-italic.woff2` at the same time.
  Without a real face the browser slants the upright, which reads as an error
  even to people who cannot name what is wrong.
* **Only the weights the CSS uses are here.** Upright 400–600 and mono 400.
  Nothing renders bold code, so there is no mono 700. Adding a weight to the
  stylesheet means adding the face here — see the note in `tokens.css`.

Both families are licensed under the SIL Open Font License 1.1; see `OFL.txt`.
Archivo by Omnibus-Type. JetBrains Mono by JetBrains.

To refresh, request the same families from the Google Fonts css2 API with a
woff2-capable user agent and take the `latin` subset URLs.
