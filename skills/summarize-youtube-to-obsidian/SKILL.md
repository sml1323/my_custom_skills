---
name: summarize-youtube-to-obsidian
description: Convert a YouTube video URL, transcript, or timestamp notes into an Obsidian markdown note with YAML frontmatter, a clean summary structure, and GitHub-compatible callouts. Use when asked to summarize a YouTube video into an Obsidian note, turn a transcript into study/reference notes, or save a video as frontmatter-first markdown for Obsidian and GitHub.
---

# Summarize Youtube To Obsidian

Create a reviewable Obsidian note from a YouTube source. Prefer transcript-backed summaries, keep claims traceable to the source, and use only callouts that render on GitHub.

## Workflow

### 1. Gather source material

- Require at least one of: YouTube URL, transcript, timestamp notes, or detailed user notes.
- Extract or confirm title, source URL, video ID, channel, language, and published date when available.
- Prefer transcript-backed summaries. If a transcript is unavailable, say so explicitly and summarize only from the available metadata or user notes.
- Never invent timestamps, quotes, speaker claims, or publication metadata.

### 2. Decide the note scope

- Default to a reusable reference note rather than a play-by-play recap.
- If the user asks for study notes, emphasize concepts, arguments, and takeaways.
- If the user asks for archival notes, preserve more timestamps and source phrasing.

### 3. Write frontmatter first

- Start every note with YAML frontmatter.
- Use the template in [references/output-template.md](references/output-template.md).
- Keep the schema stable unless the user requests a different vault convention.
- Use the current local time for `created`.
- Use lowercase kebab-case tags unless the vault already follows a different style.
- Omit unknown fields instead of guessing.

### 4. Write the body

- Use `# <video title>` as the note title.
- Use the default section order from [references/output-template.md](references/output-template.md) unless the user asks for another structure.
- Compress repetitive material. Prefer thematic synthesis over transcript paraphrase.
- Use short paragraphs for synthesis and bullets for timelines or checklists.
- Include direct quotes only when they are verifiable from the transcript.
- Match the user's language. If the request is in Korean, write natural Korean unless the user requests English.

### 5. Restrict callouts to GitHub-compatible types

- Follow [references/github-callouts.md](references/github-callouts.md).
- Allowed callouts are `NOTE`, `TIP`, `IMPORTANT`, `WARNING`, and `CAUTION`.
- Do not use Obsidian-only callouts such as `info`, `summary`, `check`, `done`, `question`, `example`, or `quote`.
- Do not nest callouts or stack several callouts back-to-back.

### 6. Review before saving

- Show the draft first unless the user explicitly asks for immediate save or gives an exact destination path.
- If saving is requested without a path, infer the best location from the user's PARA structure and confirm the choice when the path is ambiguous.
- Default filename to the video title with `.md`, sanitized only as much as the filesystem requires.
- If transcript coverage is partial, mention that limitation in the note or in the delivery message.

## Quality Bar

- Preserve factual fidelity to the source.
- Prefer fewer clear sections over exhaustive prose.
- Mark uncertainty explicitly.
- When the note is meant to sync to GitHub, favor standard Markdown over Obsidian-specific syntax except YAML frontmatter and the five supported callouts.

## References

- Use [references/output-template.md](references/output-template.md) for the canonical frontmatter and section skeleton.
- Use [references/github-callouts.md](references/github-callouts.md) for the only allowed callout types and formatting rules.
