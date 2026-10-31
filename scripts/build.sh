#!/bin/bash
# Build the whole book: Markdown -> Pandoc (+ Lua filter) -> XeLaTeX -> PDF.
# Usage: scripts/build.sh            -> output/chino-espanol.pdf
#        scripts/build.sh html       -> output/chino-espanol.html
#        scripts/build.sh pdf "00[0-9]"   -> only files matching src/chapters/<glob>-*.md
# Without local xelatex, use scripts/build-docker.sh (same arguments).
set -e
cd "$(dirname "$0")/.."

FORMAT="${1:-pdf}"
PATTERN="${2:-[0-9][0-9][0-9]}"
SRC=src; OUT=output; META="$SRC/metadata.yaml"
mkdir -p "$OUT"

command -v pandoc >/dev/null || { echo "pandoc not found; use scripts/build-docker.sh"; exit 1; }

FILES=$(ls $SRC/chapters/${PATTERN}-*.md 2>/dev/null | sort)
[ -n "$FILES" ] || { echo "No files match $SRC/chapters/${PATTERN}-*.md"; exit 1; }
NAME=chino-espanol
[ "$PATTERN" != "[0-9][0-9][0-9]" ] && NAME=test

# Each chapter has its own YAML title; force the book metadata with -M or the
# document would inherit the last chapter's title.
BOOK_META=()
for key in title subtitle author date; do
    v=$(sed -n "s/^$key:[[:space:]]*\"\(.*\)\"[[:space:]]*$/\1/p" "$META" | head -1)
    [ -n "$v" ] && BOOK_META+=(-M "$key=$v")
done

OPTS=(--from markdown+pipe_tables+footnotes+fenced_divs-smart
      --lua-filter="$SRC/filters/paralelo.lua"
      --toc --toc-depth=1 --metadata-file="$META" "${BOOK_META[@]}")

if [ "$FORMAT" = html ]; then
    pandoc $FILES "${OPTS[@]}" --standalone --css="$SRC/templates/style.css" \
        --embed-resources -o "$OUT/$NAME.html"
    echo "Wrote $OUT/$NAME.html"
else
    if ! command -v xelatex >/dev/null || [ -z "$(kpsewhich xeCJK.sty 2>/dev/null)" ]; then
        echo "xelatex/xeCJK not available locally: building inside the container"
        exec scripts/build-docker.sh "$FORMAT" "$PATTERN"
    fi
    pandoc $FILES "${OPTS[@]}" --pdf-engine=xelatex \
        --template="$SRC/templates/bilingual.tex" -o "$OUT/$NAME.pdf"
    echo "Wrote $OUT/$NAME.pdf ($(du -h "$OUT/$NAME.pdf" | cut -f1))"
fi
