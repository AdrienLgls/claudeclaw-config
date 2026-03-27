#!/bin/bash
# Install claudeclaw-config into a bot's .claude directory
# Usage: ./install.sh [TARGET_CLAUDE_DIR]
# Default target: $HOME/.claude

set -eu

REPO_DIR="$(cd "$(dirname "$0")" && pwd)"
CLAUDE_DIR="${1:-$HOME/.claude}"

echo "=== claudeclaw-config installer ==="
echo "Repo:   $REPO_DIR"
echo "Target: $CLAUDE_DIR"
echo ""

mkdir -p "$CLAUDE_DIR"

# Symlink shared directories
ITEMS=(skills commands agents)

for item in "${ITEMS[@]}"; do
  target="$CLAUDE_DIR/$item"
  source="$REPO_DIR/$item"

  if [ -L "$target" ]; then
    echo "  [skip] $item (already linked)"
  elif [ -e "$target" ]; then
    echo "  [warn] $item exists and is not a symlink — skipping"
  else
    ln -s "$source" "$target"
    echo "  [link] $item"
  fi
done

# Copy hooks (not symlinked — each bot may customize)
mkdir -p "$CLAUDE_DIR/hooks"
for hook in "$REPO_DIR/hooks/"*; do
  fname="$(basename "$hook")"
  target="$CLAUDE_DIR/hooks/$fname"
  if [ -e "$target" ]; then
    echo "  [skip] hooks/$fname (already exists)"
  else
    cp "$hook" "$target"
    echo "  [copy] hooks/$fname"
  fi
done

echo ""
echo "=== Done ==="
echo "Config installed to $CLAUDE_DIR"
