# Output Template

Use this as the default shape for the generated note. Omit fields you cannot verify.

```md
---
title: "<video title>"
source: "youtube"
source_url: "<full youtube url>"
video_id: "<youtube video id>"
channel: "<channel name>"
published: "YYYY-MM-DD"
created: "YYYY-MM-DD HH:mm:ss"
tags:
  - youtube
  - <topic-tag>
  - <topic-tag>
---

# <video title>

## Summary

> [!IMPORTANT]
> One short paragraph capturing the video's main claim, lesson, or outcome.

## Key Takeaways

- <takeaway 1>
- <takeaway 2>
- <takeaway 3>

## Timeline

- 00:00 <opening topic>
- 05:42 <major pivot or example>
- 11:03 <key explanation or conclusion>

## Notes

### <theme>

- <supporting idea>
- <supporting example>

## Links

- [YouTube](<full youtube url>)
- [Channel](<channel url or plain text name>)
```

## Field Rules

- `title`: Use the human-readable video title.
- `source`: Keep `"youtube"` unless the user wants a broader source taxonomy.
- `source_url`: Preserve the exact URL the user provided when it contains a meaningful timestamp.
- `video_id`: Extract from the URL when possible.
- `published`: Use `YYYY-MM-DD`. Omit if unknown.
- `created`: Use the current local datetime at note creation time.
- `tags`: Include `youtube` plus 2-5 topic tags derived from the content.

## Default Section Logic

- `Summary`: High-signal synthesis in 3-5 sentences or one dense paragraph.
- `Key Takeaways`: The ideas worth remembering without replaying the video.
- `Timeline`: Include only when timestamps are available or useful.
- `Notes`: Group by themes, frameworks, examples, or claims.
- `Links`: Always include the source URL.
