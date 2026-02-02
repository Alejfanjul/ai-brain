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

# Symlink hooks directory
echo "🪝 Linking hooks..."
if [ -d "$CONFIG_SRC/hooks" ]; then
    if [ -d "$CLAUDE_DIR/hooks" ] && [ ! -L "$CLAUDE_DIR/hooks" ]; then
        echo "   ⚠️  Backing up existing hooks to hooks.bak"
        mv "$CLAUDE_DIR/hooks" "$CLAUDE_DIR/hooks.bak-$(date +%Y%m%d)"
    fi
    rm -f "$CLAUDE_DIR/hooks"
    ln -s "$CONFIG_SRC/hooks" "$CLAUDE_DIR/hooks"
    echo "   ✅ hooks/"
fi

# Symlink settings.json
if [ -f "$CONFIG_SRC/settings.json" ]; then
    echo "⚙️  Linking settings..."
    rm -f "$CLAUDE_DIR/settings.json"
    ln -s "$CONFIG_SRC/settings.json" "$CLAUDE_DIR/settings.json"
    echo "   ✅ settings.json"
fi

# Symlink global CLAUDE.md
if [ -f "$CONFIG_SRC/CLAUDE.md" ]; then
    echo "📝 Linking global CLAUDE.md..."
    rm -f "$CLAUDE_DIR/CLAUDE.md"
    ln -s "$CONFIG_SRC/CLAUDE.md" "$CLAUDE_DIR/CLAUDE.md"
    echo "   ✅ CLAUDE.md"
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

# Symlink PAI context directory
echo "📄 Linking PAI context..."
if [ -d "$PAI_SRC" ]; then
    if [ -d "$CLAUDE_DIR/pai" ] && [ ! -L "$CLAUDE_DIR/pai" ]; then
        echo "   ⚠️  Backing up existing pai to pai.bak"
        mv "$CLAUDE_DIR/pai" "$CLAUDE_DIR/pai.bak-$(date +%Y%m%d)"
    fi
    rm -f "$CLAUDE_DIR/pai"
    ln -s "$PAI_SRC" "$CLAUDE_DIR/pai"
    echo "   ✅ pai/"
fi

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
ls -la "$CLAUDE_DIR/hooks" 2>/dev/null
ls -la "$CLAUDE_DIR/skills" 2>/dev/null
ls -la "$CLAUDE_DIR/pai" 2>/dev/null
ls -la "$CLAUDE_DIR/settings.json" 2>/dev/null
ls -la "$CLAUDE_DIR/CLAUDE.md" 2>/dev/null
echo ""
echo "To verify: restart Claude Code and check if context loads."
