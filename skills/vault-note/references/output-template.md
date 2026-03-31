# Output Template

Use this as the default shape for generated notes. Omit sections that have no content.

```md
---
title: "<note title>"
created: "YYYY-MM-DD HH:mm:ss"
source: "<session|research>"
source_type: "<conversation|web-research>"
tags:
  - <topic-tag>
  - <topic-tag>
related:
  - "[[Related Note Title]]"
---

# <note title>

## Summary

> [!IMPORTANT]
> One short paragraph capturing the main topic, claim, or outcome.

## Key Insights

- <insight 1>
- <insight 2>
- <insight 3>

## Details

### <subtopic heading>

<detailed content organized by theme>

> [!TIP]
> <practical advice, shortcut, or reusable pattern if applicable>

### <subtopic heading>

<additional detailed content>

## Open Questions

- <unresolved question or area needing further research>

## Action Items

- [ ] <concrete next step>

## Sources

- <source title or description> — <URL if available>

## Related Notes

- [[<existing vault note>]]
```

## Section Logic

- **Summary**: High-signal synthesis in 2-4 sentences. Use an `[!IMPORTANT]` callout.
- **Key Insights**: The ideas worth remembering without rereading the full note. 3-7 bullet points.
- **Details**: Group content by themes, concepts, or arguments. Use `### subtopic` headings. Include `[!TIP]` callouts for actionable advice.
- **Open Questions**: Unresolved questions, areas needing further research, or uncertainties. Omit if none.
- **Action Items**: Concrete next steps as checkbox items. Omit if none.
- **Sources**: For session mode, reference the conversation context. For research mode, list all URLs and sources consulted.
- **Related Notes**: Wiki-links to existing vault notes that are topically related. Only include links that resolve to actual files in the vault.

## Adaptive Content

- Match the user's language. If input is Korean, write Korean. If English, write English.
- For short, focused content: Summary + Key Insights + Sources may be sufficient. Omit empty sections.
- For rich, multi-topic content: Use all sections with multiple subtopic headings under Details.
- Compress repetitive passages. Prefer thematic synthesis over source paraphrase.
- Include direct quotes only when they are present in the input and materially useful.
