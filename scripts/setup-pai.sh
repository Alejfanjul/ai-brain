#!/bin/bash
# Setup PAI (Personal AI Infrastructure) from ai-brain repo
# Run this ONCE on each new machine after cloning ai-brain
#
# Creates symlinks so that git pull automatically updates everything.

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_DIR="$(dirname "$SCRIPT_DIR")"
CLAUDE_DIR="$HOME/.claude"
CONFIG_SRC="$REPO_DIR/.claude-config"
PAI_SRC="$REPO_DIR/pai"

echo "🚀 Setting up PAI (symlinks)..."
echo "   Repo: $REPO_DIR"
echo ""

# Check if config exists in repo
if [ ! -d "$CONFIG_SRC" ]; then
    echo "❌ .claude-config not found in ai-brain repo"
    exit 1
fi

# Create .claude directories if needed
mkdir -p "$CLAUDE_DIR/hooks"
mkdir -p "$CLAUDE_DIR/pai"

# Symlink hooks
echo "🪝 Linking hooks..."
for hook in "$CONFIG_SRC/hooks"/*.ts; do
    if [ -f "$hook" ]; then
        filename=$(basename "$hook")
        target="$CLAUDE_DIR/hooks/$filename"

        # Remove existing file/symlink
        rm -f "$target"

        # Create symlink
        ln -s "$hook" "$target"
        echo "   ✅ $filename"
    fi
done

# Symlink hooks/lib directory if exists
if [ -d "$CONFIG_SRC/hooks/lib" ]; then
    rm -rf "$CLAUDE_DIR/hooks/lib"
    ln -s "$CONFIG_SRC/hooks/lib" "$CLAUDE_DIR/hooks/lib"
    echo "   ✅ lib/"
fi

# Symlink settings.json
if [ -f "$CONFIG_SRC/settings.json" ]; then
    echo "⚙️  Linking settings..."
    rm -f "$CLAUDE_DIR/settings.json"
    ln -s "$CONFIG_SRC/settings.json" "$CLAUDE_DIR/settings.json"
    echo "   ✅ settings.json"
fi

# Symlink skills directory
echo "🧠 Linking skills..."
if [ -d "$CONFIG_SRC/skills" ]; then
    if [ -d "$CLAUDE_DIR/skills" ] && [ ! -L "$CLAUDE_DIR/skills" ]; then
        echo "   ⚠️  Backing up existing skills to skills.bak"
        mv "$CLAUDE_DIR/skills" "$CLAUDE_DIR/skills.bak-$(date +%Y%m%d)"
    fi
    rm -f "$CLAUDE_DIR/skills"
    ln -s "$CONFIG_SRC/skills" "$CLAUDE_DIR/skills"
    echo "   ✅ skills/"
fi

# Symlink PAI context files
echo "📄 Linking PAI context..."
for file in "$PAI_SRC"/*.md; do
    if [ -f "$file" ]; then
        filename=$(basename "$file")
        target="$CLAUDE_DIR/pai/$filename"

        rm -f "$target"
        ln -s "$file" "$target"
        echo "   ✅ $filename"
    fi
done

# Check for bun (required for hooks)
echo ""
if ! command -v bun &> /dev/null; then
    echo "⚠️  Bun not found. Install with:"
    echo "   curl -fsSL https://bun.sh/install | bash"
else
    echo "✅ Bun found: $(which bun)"
fi

echo ""
echo "✅ PAI setup complete!"
echo ""
echo "Symlinks created:"
ls -la "$CLAUDE_DIR/hooks/"*.ts 2>/dev/null | head -5
echo "..."
ls -la "$CLAUDE_DIR/skills" 2>/dev/null
ls -la "$CLAUDE_DIR/settings.json" 2>/dev/null
echo ""
echo "To verify: restart Claude Code and check if context loads."
