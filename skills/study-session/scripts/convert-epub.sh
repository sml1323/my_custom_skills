#!/usr/bin/env bash
# Convert an EPUB file to PDF for use with the Read tool.
# Prefers Calibre (ebook-convert) over Pandoc (which needs LaTeX).
#
# Usage: convert-epub.sh <input.epub> [output.pdf]
# If output omitted, writes alongside input with .pdf extension.

set -euo pipefail

if [ "$#" -lt 1 ]; then
  echo "Usage: convert-epub.sh <input.epub> [output.pdf]" >&2
  exit 1
fi

INPUT="$1"
OUTPUT="${2:-${INPUT%.epub}.pdf}"

if [ ! -f "$INPUT" ]; then
  echo "Input file not found: $INPUT" >&2
  exit 1
fi

if [ ! "${INPUT##*.}" = "epub" ]; then
  echo "Input does not appear to be EPUB (extension): $INPUT" >&2
  exit 1
fi

# Prefer Calibre — handles EPUB → PDF natively, no LaTeX dependency.
if command -v ebook-convert >/dev/null 2>&1; then
  echo "Using Calibre (ebook-convert)..."
  ebook-convert "$INPUT" "$OUTPUT" \
    --paper-size letter \
    --pdf-page-numbers \
    --pretty-print
  echo "✓ Converted: $OUTPUT"
  exit 0
fi

# Fall back to Pandoc — requires LaTeX installed.
if command -v pandoc >/dev/null 2>&1; then
  if ! command -v pdflatex >/dev/null 2>&1; then
    echo "Pandoc found but LaTeX (pdflatex) missing." >&2
    echo "Install LaTeX:  brew install --cask basictex" >&2
    echo "Or install Calibre instead:  brew install --cask calibre" >&2
    exit 2
  fi
  echo "Using Pandoc..."
  pandoc "$INPUT" -o "$OUTPUT" --pdf-engine=pdflatex
  echo "✓ Converted: $OUTPUT"
  exit 0
fi

echo "No conversion tool found. Install one:" >&2
echo "  brew install --cask calibre   (recommended)" >&2
echo "  brew install pandoc && brew install --cask basictex" >&2
exit 1
