#!/bin/bash
# Build the book inside a container (no local pandoc/LaTeX needed).
# Requires docker or podman. Fonts are mounted read-only from the host.
set -e

cd "$(dirname "$0")/.."

IMAGE="zh-esp-book-builder"
ENGINE="${CONTAINER_ENGINE:-docker}"
if ! command -v "$ENGINE" &> /dev/null; then
    if command -v podman &> /dev/null; then ENGINE=podman; else
        echo "Error: neither docker nor podman found."; exit 1
    fi
fi

# Build the image once (cached afterwards)
if ! $ENGINE image exists "$IMAGE" 2>/dev/null && ! $ENGINE image inspect "$IMAGE" &>/dev/null; then
    echo "Building container image $IMAGE (first time only, needs network)..."
    $ENGINE build -t "$IMAGE" .
fi

FONT_MOUNTS=""
for d in /usr/share/fonts /usr/local/share/fonts "$HOME/.fonts" "$HOME/.local/share/fonts"; do
    [ -d "$d" ] && FONT_MOUNTS="$FONT_MOUNTS -v $d:/usr/share/fonts/host/$(echo $d | tr / _):ro,z"
done

# Pass through: build.sh [pdf|html] [glob]
SCRIPT=scripts/build.sh


$ENGINE run --rm -v "$PWD:/data:z" $FONT_MOUNTS -w /data --entrypoint sh "$IMAGE" \
    -c "fc-cache -f >/dev/null 2>&1; bash $SCRIPT $*"
