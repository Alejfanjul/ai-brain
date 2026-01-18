#!/bin/bash
# Setup PAI (Personal AI Infrastructure) from ai-brain repo
# Run this on a new PC after cloning ai-brain

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_DIR="$(dirname "$SCRIPT_DIR")"
CLAUDE_DIR="$HOME/.claude"
CONFIG_SRC="$REPO_DIR/.claude-config"

echo "🚀 Setting up PAI..."

# Check if config exists in repo
if [ ! -d "$CONFIG_SRC" ]; then
    echo "❌ .claude-config not found in ai-brain repo"
    exit 1
fi

# Create .claude directory if needed
mkdir -p "$CLAUDE_DIR"

# Copy skills
if [ -d "$CONFIG_SRC/skills" ]; then
    echo "📦 Installing skills..."
    cp -r "$CONFIG_SRC/skills" "$CLAUDE_DIR/"
    echo "   ✅ Skills installed"
fi

# Copy hooks
if [ -d "$CONFIG_SRC/hooks" ]; then
    echo "🪝 Installing hooks..."
    cp -r "$CONFIG_SRC/hooks" "$CLAUDE_DIR/"
    echo "   ✅ Hooks installed"
fi

# Copy settings (backup existing first)
if [ -f "$CONFIG_SRC/settings.json" ]; then
    if [ -f "$CLAUDE_DIR/settings.json" ]; then
        echo "⚠️  Backing up existing settings.json..."
        cp "$CLAUDE_DIR/settings.json" "$CLAUDE_DIR/settings.json.bak"
    fi
    echo "⚙️  Installing settings..."
    cp "$CONFIG_SRC/settings.json" "$CLAUDE_DIR/"
    echo "   ✅ Settings installed"
fi

# Check for bun (required for hooks)
if ! command -v bun &> /dev/null; then
    echo ""
    echo "⚠️  Bun not found. Install with:"
    echo "   curl -fsSL https://bun.sh/install | bash"
fi

# Check for Python deps
echo ""
echo "📋 Python dependencies needed:"
echo "   pip install pypdf ebooklib beautifulsoup4 markdownify"

# Reminder about .env
echo ""
echo "🔐 Don't forget to create ~/.claude/.env with:"
echo "   SUPABASE_URL=..."
echo "   SUPABASE_ANON_KEY=..."

echo ""
echo "✅ PAI setup complete!"
echo "   Restart Claude Code to load the new configuration."
