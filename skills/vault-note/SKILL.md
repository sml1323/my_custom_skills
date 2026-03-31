---
name: vault-note
description: Convert Claude conversation sessions or research topics into structured Obsidian notes with YAML frontmatter, GitHub-compatible callouts, and [[]] vault links. Use when the user wants to save a conversation as a note, research a topic and create a note, or organize knowledge into the Obsidian vault. Trigger on phrases like "정리해줘", "노트로 만들어줘", "리서치해줘", or "vault에 저장".
---

# Vault Note

Create a structured Obsidian note from a conversation session or a research topic. The note includes YAML frontmatter, GitHub-compatible callouts, and [[]] wiki-links to existing vault notes.

## Workflow

### 1. Determine input mode

Decide the mode based on what the user provides:

- **Session mode (기본)**: 사용자가 "정리해줘", "노트로 만들어줘", "vault에 저장" 등을 말하면, **현재 대화의 전체 컨텍스트를 자동으로 분석**한다. 대화 내용을 붙여넣을 필요 없이, 이 스킬이 호출되기 전까지의 모든 대화 내역을 읽고 정리한다.
- **Research mode**: The user provides a topic to research, like "파이썬 데코레이터 리서치해줘" or "Kubernetes networking 조사해줘". Use WebSearch to gather information first.

If ambiguous, ask: "이 대화를 정리할까요, 아니면 주제를 리서치해서 노트를 만들까요?"

### 2. Gather and extract content

**Session mode:**
- 현재 Claude Code 세션의 대화 내역 전체를 자동으로 읽는다. 사용자가 별도로 붙여넣을 필요 없다.
- 대화에서 추출할 것: 핵심 주제, 개념, 결정사항, 코드 스니펫, 인사이트, 미해결 질문, 액션 아이템.
- 사용자가 특정 부분만 정리를 원하면 (예: "마지막 디버깅 부분만 정리해줘"), 해당 부분에 집중한다.
- Compress repetitive passages. Prefer thematic synthesis over source paraphrase.
- Never invent claims, quotes, or facts not present in the conversation.

**Research mode:**
- Use WebSearch to research the given topic. Run 2-3 searches with different angles.
- Synthesize search results into structured content.
- Track all sources (title + URL) for the Sources section.
- Mark uncertainty explicitly when search results are ambiguous or conflicting.

### 3. Scan vault for related notes

Before writing the note, scan the vault for existing notes that may be related:

1. Use the Glob tool to list all `.md` files in the vault root directory.
2. If the glob returns more than 500 files, skip link resolution and warn: "볼트 파일이 500개를 초과하여 자동 링크를 건너뜁니다."
3. Extract topic names and entity names from the content you analyzed in step 2.
4. Match these against vault filenames (case-insensitive). A match means the filename contains the topic/entity name or vice versa.
5. Build a list of matching note names for use in `related:` frontmatter and `## Related Notes` section.

### 4. Determine output path and filename

- Default output directory: `notes/concepts/` (개념/학습 노트), `notes/sources/` (외부 소스 기반), `notes/projects/` (프로젝트 관련). 내용에 맞는 디렉토리를 자동 선택한다.
- If the user specifies a different path (e.g., "inbox/에 저장해줘"), use that path instead.
- Filename: sanitize the note title to a filesystem-safe slug. Use the title as-is if it's already safe. Add `.md` extension.
- Before writing, check if a file already exists at the target path. If it does, ask the user: "이미 같은 이름의 파일이 있습니다. 덮어쓸까요, 아니면 타임스탬프를 붙여서 새로 만들까요?"

### 5. Write the note

- Start with YAML frontmatter following [references/frontmatter-schema.md](references/frontmatter-schema.md).
- Use `# <note title>` as the document heading (same as the frontmatter `title`).
- Follow the section structure in [references/output-template.md](references/output-template.md).
- Only use callouts from [references/github-callouts.md](references/github-callouts.md): NOTE, TIP, IMPORTANT, WARNING, CAUTION.
- Insert `[[note name]]` wiki-links for related vault notes found in step 3.
- Match the user's language. If the input is Korean, write Korean. If English, write English.
- Omit sections that have no content (e.g., skip "Open Questions" if there are none).

### 6. Save and confirm

- Use the Write tool to save the note to the determined path.
- After saving, report to the user:
  - The file path where the note was saved
  - A brief summary of what was captured
  - Any related notes that were linked

## Quality Bar

- Preserve factual fidelity to the conversation context (session mode) or search results (research mode).
- Prefer fewer clear sections over exhaustive prose.
- Mark uncertainty explicitly when content is ambiguous.
- All frontmatter scalar string values must be quoted. No exceptions.
- Use lowercase kebab-case for tags (e.g., `python-decorators`, not `Python Decorators`).
- Do not use Obsidian-only callout types. Only the five GitHub-compatible types are allowed.
- Every [[]] link in the note must correspond to an actual file found in the vault scan. Do not create links to non-existent notes.

## References

- Use [references/frontmatter-schema.md](references/frontmatter-schema.md) for the frontmatter field definitions and quoting rules.
- Use [references/output-template.md](references/output-template.md) for the section structure and adaptive content guidelines.
- Use [references/github-callouts.md](references/github-callouts.md) for the allowed callout types and formatting rules.
- See [references/examples/](references/examples/) for a sample input/output pair demonstrating correct formatting.
