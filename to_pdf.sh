#!/usr/bin/env bash
set -euo pipefail

PREFIX="${1:-}"

if [[ -z "$PREFIX" ]]; then
    echo "usage: $0 100"
    exit 1
fi

NOTEBOOK_DIR="./notebooks"
PDF_DIR="./pdf"

mkdir -p "$PDF_DIR"

if command -v chromium >/dev/null 2>&1; then
    CHROME_BIN="chromium"
elif command -v chromium-browser >/dev/null 2>&1; then
    CHROME_BIN="chromium-browser"
elif command -v google-chrome >/dev/null 2>&1; then
    CHROME_BIN="google-chrome"
else
    echo "error: need chromium, chromium-browser, or google-chrome installed"
    exit 1
fi

TMP_DIR="$(mktemp -d)"
cleanup() {
    rm -rf "$TMP_DIR"
}
trap cleanup EXIT

shopt -s nullglob
files=( "$NOTEBOOK_DIR"/"${PREFIX}"-*.ipynb )

if (( ${#files[@]} == 0 )); then
    echo "error: no notebooks found matching ${NOTEBOOK_DIR}/${PREFIX}-*.ipynb"
    exit 1
fi

for nb in "${files[@]}"; do
    base="$(basename "$nb" .ipynb)"
    html="${TMP_DIR}/${base}.html"
    pdf="${PDF_DIR}/${base}.pdf"

    echo "converting: $nb -> $pdf"

    uvx --from nbconvert jupyter-nbconvert \
        --to html \
        --output "$html" \
        "$nb"

    python3 - "$html" <<'PY'
from pathlib import Path
import sys

path = Path(sys.argv[1])
s    = path.read_text(encoding="utf-8")

css  = """
<style>
@page {
    size: A4;
    margin: 8mm;
}

@media print {
    body {
        zoom: 0.75;
    }
}
</style>
"""

if "</head>" in s:
    s = s.replace("</head>", css + "\n</head>", 1)
else:
    s = css + s

path.write_text(s, encoding="utf-8")
PY

    "$CHROME_BIN" \
        --headless \
        --disable-gpu \
        --no-sandbox \
        --print-to-pdf="$pdf" \
        --print-to-pdf-no-header \
        "file://$html"
done

echo "done"