# Citation Format — Discriminated Union by Source Kind

When the user wants to quote a passage from a book during analysis (especially in ARQ extracts and Polya log entries), use a unified citation schema. The schema discriminates by source kind so future books (audio, EPUB, HTML) drop in without redesign.

## Inline compact form

Embedded in the chapter note body where the citation occurs:

```
[<book-slug> <locator-compact> #<quote-id>]
```

Examples:
- `[arq §7 p.138 #rc-3]`
- `[polya II/auxprob ¶3 #ap-1]`
- `[polya I/§7 ¶3]`
- `[feynman-vol-1 ch.5 §5.2 #5-2-1]`
- `[mill-on-liberty ch.2 ¶12]`

Single regex extracts book / locator / quote_id from any citation:

```regex
\[(\S+) ([^\]]+) #(\S+)\]
```

## Full form (entry-end YAML appendix)

For each `quote_id` referenced in body, append a full entry at the end:

```yaml
citations:
  - quote_id: rc-3
    book: arq
    source_kind: pdf
    api_type: page_location           # Anthropic Citations API type if used
    file_path: ~/wiki/tmp_books/arq.pdf
    document_index: 0                 # for Citations API
    start_page: 142                   # PDF page index
    end_page: 143
    printed_page: "p.138"             # printed page differs from PDF page (front matter)
    chapter: "Ch.7 Are There Rival Causes?"
    cited_text: "..."
```

## Source kinds

| source_kind | locator structure | api_type (if Anthropic Citations API) | example inline |
|-------------|-------------------|--------------------------------------|----------------|
| `pdf` | `{start_page, end_page, printed_page, chapter}` | `page_location` | `[arq §7 p.138 #qid]` |
| `chapter_split` | `{part, section, section_number, para}` | `content_block_location` | `[polya II/auxprob ¶3 #qid]` |
| `html` | `{section, url_fragment, heading}` | `char_location` | `[htdp §1.2.3 #qid]` |
| `epub` | `{chapter, para, cfi}` | `char_location` (after conversion) | `[book Ch.4 ¶12 #qid]` |
| `audio` | `{chapter_index, start_ms, end_ms}` | `none` | `[book ch.7 17:14 #qid]` |

## Critical gotchas

### PDF page ≠ printed page

Most books have front matter (cover, copyright, TOC, preface) before the first numbered page. PDF page 1 is usually not printed page 1.

When citing, capture both:
- `start_page` (PDF page index — what the Read tool returns)
- `printed_page` (the page number as printed in the book — what a reader expects to see)

The `printed_page_offset` (PDF − printed) is fixed per book; store in books.yml:

```yaml
arq:
  path: ...
  printed_page_offset: -4   # PDF page 5 = printed page 1
```

When recording a citation, compute and store both. Display compact form uses printed page (`p.138`) since that's what humans look up.

### Citations API structured-outputs incompatibility

If skill uses Anthropic Citations API for automated quote extraction: citations + structured outputs returns 400 errors. Capture citations from streaming `citations_delta` or in a separate non-structured turn.

### Scanned PDFs

PDFs without text layer can't be cited. If chapter PDF is scanned, surface to user:

> 이 PDF는 scanned (text layer 없음). citation 불가. OCR 필요:
> `ocrmypdf input.pdf output.pdf`

### EPUB → PDF conversion preserves structure

After pandoc/calibre EPUB→PDF, internal structure (chapter boundaries, page numbers) is preserved enough for `pdf` kind. Use `printed_page` from the converted PDF — it usually matches the EPUB's intended page numbering.

## Quote ID discipline

`quote_id` is a stable slug for a specific cited passage. Pattern: `<short-tag>-<n>` within a chapter.

Examples:
- `rc-3` (Rival Causes, third citation in chapter)
- `ap-1` (Auxiliary Problem, first citation)
- `eq-5-2-1` (Equation 5.2.1)

The slug must be unique within a chapter note; not globally unique.

If the same passage is cited multiple times, reuse the quote_id. Avoid re-quoting different passages with the same id.

## Inline self-decoding

Inline compact form is *self-decoding* — given just `[arq §7 p.138 #rc-3]`, a future LLM (or grep) can identify the source without scanning the citation appendix:

- `arq` = book slug
- `§7` = chapter 7
- `p.138` = page (printed)
- `#rc-3` = quote_id

This makes partial-context retrieval work. If the next session reads only the body of the chapter note (not the appendix), citations remain interpretable.

## Footnote pattern — DO NOT use

Markdown footnote `[^1]` style is rejected because:
- Requires resolving the footnote table to identify the source
- Ambiguous in partial context (grep result missing the footnote table)
- Tied to one book / one source — doesn't generalize across kinds

Use inline compact form.

## Capturing from Anthropic Citations API

If citations are produced via Citations API (when document is loaded with `cache_control` and `citations.enabled`), Claude returns a structured citation object. Map to the schema:

```python
# pseudocode
def capture_citation(api_citation, book_meta):
    return {
        "quote_id": slugify(api_citation["cited_text"][:40]),
        "book": book_meta["slug"],
        "source_kind": book_meta["source_kind"],
        "api_type": api_citation["type"],
        "file_path": book_meta["path"],
        "document_index": api_citation["document_index"],
        "cited_text": api_citation["cited_text"],
        "locator": build_locator(api_citation, book_meta),  # source_kind-specific
    }
```

When skill is running natively in Claude Code (Read tool, no Citations API), citations are captured manually:

1. User pastes a passage they want to cite
2. Skill asks for the page number (or the user provides it)
3. Skill verifies by Read tool with `pages: <page>` and matching the passage
4. Inserts inline compact form + appends to YAML appendix

## Cross-references

- `references/methods/arq.md` — citations are produced inside ARQ extracts
- `references/chapter-template.md` — appendix location
- `references/setup.md` — `printed_page_offset` is captured during setup per book
