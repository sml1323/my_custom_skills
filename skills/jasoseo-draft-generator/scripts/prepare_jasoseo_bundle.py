#!/usr/bin/env python3
"""
Bundle personal, company, and prior application materials into one markdown file.

Usage:
    python3 scripts/prepare_jasoseo_bundle.py /path/to/company2
    python3 scripts/prepare_jasoseo_bundle.py /path/to/company2 --output /tmp/bundle.md
"""

from __future__ import annotations

import argparse
import re
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path

try:
    from pypdf import PdfReader
except Exception:  # pragma: no cover - best-effort fallback
    PdfReader = None


GROUP_CANDIDATES = {
    "previous_letters": ["자소서들"],
    "background": ["my_background", "my_backgorund"],
    "target_company": ["target_company"],
}

GROUP_LABELS = {
    "previous_letters": "Previous Letters",
    "background": "My Background",
    "target_company": "Target Company",
}

SUPPORTED_SUFFIXES = {".md", ".txt", ".pdf"}


@dataclass
class SourceEntry:
    group: str
    path: Path
    relative_path: str
    status: str
    content: str
    note: str | None = None


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("root", type=Path, help="Application folder root such as company2")
    parser.add_argument(
        "--output",
        type=Path,
        help="Output markdown path. Defaults to <root>/output/_jasoseo_source_bundle.md",
    )
    return parser.parse_args()


def find_group_dir(root: Path, candidates: list[str]) -> Path | None:
    for candidate in candidates:
        path = root / candidate
        if path.is_dir():
            return path
    return None


def normalize_text(text: str) -> str:
    text = text.replace("\ufeff", "")
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def read_text_file(path: Path) -> tuple[str, str | None]:
    try:
        return normalize_text(path.read_text(encoding="utf-8", errors="replace")), None
    except Exception as exc:
        return "", f"Text extraction failed: {exc}"


def read_pdf_file(path: Path) -> tuple[str, str | None]:
    if PdfReader is None:
        return "", "pypdf is not available, so PDF text was skipped."

    try:
        reader = PdfReader(str(path))
        pages: list[str] = []
        for page_number, page in enumerate(reader.pages, start=1):
            page_text = normalize_text(page.extract_text() or "")
            if page_text:
                pages.append(f"[Page {page_number}]\n{page_text}")
        if not pages:
            return "", "No extractable text found in PDF."
        return "\n\n".join(pages), None
    except Exception as exc:
        return "", f"PDF extraction failed: {exc}"


def read_supported_file(path: Path) -> tuple[str, str | None]:
    suffix = path.suffix.lower()
    if suffix in {".md", ".txt"}:
        return read_text_file(path)
    if suffix == ".pdf":
        return read_pdf_file(path)
    return "", "Unsupported file type."


def collect_entries(root: Path) -> tuple[list[SourceEntry], list[str], dict[str, Path | None]]:
    entries: list[SourceEntry] = []
    warnings: list[str] = []
    group_dirs: dict[str, Path | None] = {}

    for group, candidates in GROUP_CANDIDATES.items():
        group_dir = find_group_dir(root, candidates)
        group_dirs[group] = group_dir
        if group_dir is None:
            warnings.append(f"Missing directory for {group}: expected one of {', '.join(candidates)}")
            continue

        matched_files = sorted(
            path
            for path in group_dir.rglob("*")
            if path.is_file() and path.suffix.lower() in SUPPORTED_SUFFIXES
        )
        if not matched_files:
            warnings.append(f"No supported files found in {group_dir}")
            continue

        for path in matched_files:
            content, note = read_supported_file(path)
            status = "ok" if content else "skipped"
            if note:
                warnings.append(f"{path.relative_to(root)}: {note}")
            entries.append(
                SourceEntry(
                    group=group,
                    path=path,
                    relative_path=str(path.relative_to(root)),
                    status=status,
                    content=content,
                    note=note,
                )
            )

    return entries, warnings, group_dirs


def first_nonempty_line(text: str) -> str:
    for line in text.splitlines():
        stripped = line.strip()
        if stripped:
            return stripped
    return ""


def clean_component(text: str) -> str:
    text = re.sub(r"\([^)]*\)", "", text)
    text = re.sub(r"\[[^\]]*\]", "", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip(" -")


def compact_filename_component(text: str, fallback: str) -> str:
    cleaned = re.sub(r"[^0-9A-Za-z가-힣]+", "", text)
    return cleaned or fallback


def infer_metadata(entries: list[SourceEntry], root: Path) -> dict[str, str]:
    jd_text = ""
    research_text = ""
    for entry in entries:
        filename = entry.path.name.lower()
        if filename == "jd.md":
            jd_text = entry.content
        elif filename == "research.md":
            research_text = entry.content

    team_name = ""
    role_name = ""
    jd_line = first_nonempty_line(jd_text)
    if jd_line:
        match = re.match(r"^\[(?P<tag>[^\]]+)\]\s*(?P<role>.+)$", jd_line)
        if match:
            team_name = clean_component(match.group("tag"))
            role_name = clean_component(match.group("role"))
        else:
            role_name = clean_component(jd_line)

    company_name = ""
    if research_text:
        company_match = re.search(r"^\s*([가-힣A-Za-z0-9&.+-]+)\s*\(", research_text)
        if company_match:
            company_name = clean_component(company_match.group(1))

    if not company_name and team_name:
        company_name = team_name
    if not company_name:
        company_name = root.name
    if not role_name:
        role_name = "직무미정"

    filename = (
        f"{compact_filename_component(company_name, '회사미정')}_"
        f"{compact_filename_component(role_name, '직무미정')}_자소서초안.md"
    )

    return {
        "company_name": company_name,
        "team_name": team_name,
        "role_name": role_name,
        "suggested_filename": filename,
    }


def build_summary(entries: list[SourceEntry], group_dirs: dict[str, Path | None]) -> list[str]:
    lines: list[str] = []
    for group, label in GROUP_LABELS.items():
        group_dir = group_dirs.get(group)
        matching = [entry for entry in entries if entry.group == group]
        dir_display = str(group_dir) if group_dir else "missing"
        lines.append(f"- {label}: {len(matching)} file(s) from `{dir_display}`")
    return lines


def render_bundle(
    root: Path,
    output_path: Path,
    entries: list[SourceEntry],
    warnings: list[str],
    metadata: dict[str, str],
    group_dirs: dict[str, Path | None],
) -> str:
    generated_at = datetime.now().astimezone().isoformat(timespec="seconds")
    suggested_output_path = output_path.parent / metadata["suggested_filename"]

    lines = [
        "# Jasoseo Source Bundle",
        "",
        f"- Generated at: `{generated_at}`",
        f"- Root folder: `{root}`",
        f"- Detected company: `{metadata['company_name']}`",
        f"- Detected team: `{metadata['team_name'] or 'n/a'}`",
        f"- Detected role: `{metadata['role_name']}`",
        f"- Suggested final output: `{suggested_output_path}`",
        "",
        "## Source Summary",
        *build_summary(entries, group_dirs),
        "",
        "## Warnings",
    ]

    if warnings:
        lines.extend(f"- {warning}" for warning in warnings)
    else:
        lines.append("- None")

    for group, label in GROUP_LABELS.items():
        group_entries = [entry for entry in entries if entry.group == group]
        lines.extend(["", f"## {label}"])
        if not group_entries:
            lines.append("")
            lines.append("_No supported files collected._")
            continue

        for entry in group_entries:
            lines.extend(
                [
                    "",
                    f"### {entry.relative_path}",
                    "",
                    f"- Status: `{entry.status}`",
                ]
            )
            if entry.note:
                lines.append(f"- Note: {entry.note}")
            lines.extend(["", "```text", entry.content or "[No extracted text]", "```"])

    return "\n".join(lines) + "\n"


def main() -> int:
    args = parse_args()
    root = args.root.expanduser().resolve()
    if not root.is_dir():
        raise SystemExit(f"Root directory not found: {root}")

    output_path = args.output.expanduser().resolve() if args.output else root / "output" / "_jasoseo_source_bundle.md"
    output_path.parent.mkdir(parents=True, exist_ok=True)

    entries, warnings, group_dirs = collect_entries(root)
    metadata = infer_metadata(entries, root)
    bundle = render_bundle(root, output_path, entries, warnings, metadata, group_dirs)
    output_path.write_text(bundle, encoding="utf-8")

    suggested_output_path = output_path.parent / metadata["suggested_filename"]
    print(f"Bundle written to: {output_path}")
    print(f"Suggested company: {metadata['company_name']}")
    print(f"Suggested role: {metadata['role_name']}")
    print(f"Suggested final output: {suggested_output_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
