---
name: jasoseo-draft-generator
description: Generate a grounded Korean self-introduction or cover-letter draft by combining a target folder's previous application letters, personal background or portfolio, and target company job-description or research files. Use when the user asks for 자소서 초안 작성, 지원동기 or 직무역량 draft generation, or wants folders such as 자소서들/, my_background/, and target_company/ synthesized into output/{회사}_{직무}_자소서초안.md.
---

# Jasoseo Draft Generator

## Overview

Create a first-pass Korean self-introduction draft from three input buckets: previous letters, personal background, and target company materials. Generate a source bundle first, then map JD keywords to candidate evidence, and write the final draft to the requested `output/` path.

## Expected Folder Layout

Prefer this structure inside one application root:

```text
지원폴더/
  자소서들/
    *.md
  my_background/          # or my_backgorund/
    background.md
    *.pdf
  target_company/
    jd.md
    research.md
  output/
```

Minimum viable input:
- `target_company/jd.md`
- one of `my_background/` or `my_backgorund/`
- at least one source file from either `자소서들/` or background materials

If the user has not organized files yet, tell them to create this structure first and name the expected files explicitly. Do not assume a random workspace layout is intentional.

## Folder Discovery

1. If the user explicitly names a folder or path such as `company2`, use that first.
2. If the user does not provide a path, search the current workspace for candidate roots that contain:
   - `target_company/`
   - at least one of `자소서들/`, `my_background/`, or `my_backgorund/`
3. Prefer the candidate that has all three directories.
4. If exactly one candidate exists, use it without asking.
5. If multiple plausible roots exist, ask one concise clarification question instead of guessing.
6. If no candidate exists, tell the user the exact folder structure to create.

## Workflow

1. Identify the root folder.
   Default to the user-provided application folder such as `company2`.
   If no folder was provided, perform the discovery flow above before asking a follow-up.
   Expect these directories when available:
   - `자소서들/`: previous letters
   - `my_background/` or `my_backgorund/`: background notes and portfolio
   - `target_company/`: `jd.md`, `research.md`, and related notes

2. Build the source bundle.
   Run:

   ```bash
   python3 scripts/prepare_jasoseo_bundle.py /abs/path/to/company2
   ```

   If the root is still ambiguous, run it from the workspace root without arguments:

   ```bash
   python3 scripts/prepare_jasoseo_bundle.py
   ```

   The script reads `.md`, `.txt`, and `.pdf`, creates `output/_jasoseo_source_bundle.md`, and suggests a final filename. It auto-discovers the application root when there is exactly one plausible candidate under the current working directory.

3. Read the generated bundle and [references/writing-checklist.md](references/writing-checklist.md).
   Use previous letters for narrative patterns and proof sources, not verbatim reuse.
   Use `target_company/jd.md` and `target_company/research.md` to extract the role, company needs, product context, and keywords.
   Use `my_background/background.md` and any extractable portfolio text to ground achievements.

4. Decide the section structure.
   If the target files contain explicit essay questions, keep those exact questions as headings and answer them directly.
   If explicit questions are missing, default to:
   - `1. 지원동기`
   - `2. 직무역량`
   - `3. 입사 후 포부`
   Use [assets/jasoseo-draft-template.md](assets/jasoseo-draft-template.md) as the starting skeleton if helpful.

5. Draft from evidence, not from vibes.
   Connect each section to:
   - a company need or product direction
   - a matching experience or project
   - a realistic contribution after joining
   Prefer one or two concrete episodes over adjective-heavy claims.
   If a fact appears only in `research.md`, treat it as company research and avoid overstating certainty beyond the source.

6. Save the draft.
   Write the final file to `output/{회사}_{직무}_자소서초안.md`.
   Use the script's suggested filename unless the user explicitly requested a different name.

7. Verify before finishing.
   Check that:
   - every major claim traces back to a source file
   - no metric, degree, certificate, or production experience was invented
   - tone stays in Korean business prose rather than marketing copy
   - previous letters were adapted instead of mechanically copied
   - filename and output path follow the convention

## Missing Data Rules

- If one folder is missing, continue with the available sources and mention the gap briefly.
- If `target_company/` is missing, stop and tell the user to add `jd.md` first.
- If the layout itself is missing or inconsistent, show the expected tree and name the missing folders explicitly.
- If PDF extraction fails, continue with markdown sources first. Do not block the draft on the portfolio PDF alone.
- If company name or role cannot be inferred confidently, use a conservative placeholder filename and state that assumption.

## Output Standard

- Keep the output in Korean unless the user asks otherwise.
- Prefer crisp paragraphs over bullet-heavy prose unless the target question explicitly asks for bullets.
- Optimize for a usable first draft that the user can revise, not a polished fiction piece.
- Preserve the user's demonstrated strengths and wording patterns, but rewrite them to fit the new company and role.
