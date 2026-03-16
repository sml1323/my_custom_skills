# GitHub-Compatible Callouts

When the note needs callouts, use only GitHub-rendered alert syntax.

## Allowed Types

```md
> [!NOTE]
> Supporting context or quick reference information.

> [!TIP]
> A useful shortcut, pattern, or practical suggestion.

> [!IMPORTANT]
> The central claim, rule, or takeaway the reader should not miss.

> [!WARNING]
> A significant limitation, risk, or common mistake.

> [!CAUTION]
> A high-risk point with potential negative consequences.
```

## Rules

- Use uppercase alert names exactly as shown.
- Do not use Obsidian-only callout names such as `info`, `summary`, `question`, `example`, `check`, `done`, `bug`, or `quote`.
- Do not use folded callout variants such as `+` or `-`.
- Do not nest callouts inside lists, tables, or other callouts.
- Avoid consecutive callouts. Use one when emphasis materially helps the reader.
- Prefer normal headings and bullets for most content.

## Practical Mapping

- Use `IMPORTANT` for the video's main thesis or one-sentence summary.
- Use `TIP` for actionable advice.
- Use `WARNING` or `CAUTION` only for genuine downsides, failure modes, or risks.
- Use `NOTE` for brief context that improves comprehension but is not critical.
