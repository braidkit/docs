# Vendored web fonts

Self-hosted so the site makes no third-party request to render text, and so a
Google Fonts outage or policy change cannot affect the docs.

| File | Family | Faces | Bytes |
| --- | --- | --- | --- |
| `hanken-grotesk-variable.woff2` | Hanken Grotesk | variable, weight 400–700 upright | 34,664 |
| `hanken-grotesk-italic.woff2` | Hanken Grotesk | static, weight 400 italic | 13,884 |
| `jetbrains-mono.woff2` | JetBrains Mono | static, weight 400 | 21,212 |

All three are the **latin subset** as served by Google Fonts — the same bytes,
fetched once and committed rather than requested per visitor.

Two sizing decisions worth keeping:

* **Upright is the variable file, italic is a static instance.** Google serves a
  variable file when you request a weight *range* and a smaller static instance
  when you request a single weight. We use 400, 600 and 700 upright, so the
  34,664-byte variable file beats three statics at 41,092 bytes — and it is one
  request instead of three. We use italic at 400 only, where the static is
  13,884 bytes against 35,684 for the variable. Do not "simplify" these to
  match each other; the arithmetic points opposite ways.
* **Only the weights the CSS uses are here.** Upright 400/600/700 and italic
  400. Nothing renders bold code, so there is no mono 700. Adding a weight to
  the stylesheet means adding the face here — see the note in `tokens.css`.

Both families are licensed under the SIL Open Font License 1.1; see `OFL.txt`.
Hanken Grotesk by Alfredo Marco Pradil. JetBrains Mono by JetBrains.

To refresh, request the same families from the Google Fonts css2 API with a
woff2-capable user agent and take the `latin` subset URLs.
