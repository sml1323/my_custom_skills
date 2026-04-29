#!/usr/bin/env bash
# Detect EPUB conversion tools. Print which is available and how to install if none.

found_pandoc=""
found_calibre=""
found_latex=""

if command -v pandoc >/dev/null 2>&1; then
  found_pandoc="$(command -v pandoc)"
fi

if command -v ebook-convert >/dev/null 2>&1; then
  found_calibre="$(command -v ebook-convert)"
fi

if command -v pdflatex >/dev/null 2>&1; then
  found_latex="$(command -v pdflatex)"
fi

echo "EPUB conversion tools:"
echo "  pandoc:       ${found_pandoc:-NOT FOUND}"
echo "  ebook-convert: ${found_calibre:-NOT FOUND}"
echo "  pdflatex:     ${found_latex:-NOT FOUND}"
echo ""

if [ -n "$found_calibre" ]; then
  echo "✓ Calibre available — preferred for EPUB → PDF (no LaTeX needed)."
  exit 0
fi

if [ -n "$found_pandoc" ] && [ -n "$found_latex" ]; then
  echo "✓ Pandoc + LaTeX available — EPUB → PDF works directly."
  exit 0
fi

if [ -n "$found_pandoc" ] && [ -z "$found_latex" ]; then
  echo "△ Pandoc found but LaTeX missing. Two options:"
  echo "  A) Install LaTeX:        brew install --cask basictex"
  echo "  B) Install Calibre:      brew install --cask calibre  (recommended)"
  exit 2
fi

echo "✗ No EPUB conversion tool found. Install one:"
echo ""
echo "  Option A — Calibre (recommended):"
echo "    brew install --cask calibre"
echo ""
echo "  Option B — Pandoc + LaTeX:"
echo "    brew install pandoc"
echo "    brew install --cask basictex"
echo ""
echo "Re-run after installation."
exit 1
