#!/bin/bash
# Sync PAI config from ai-brain (WSL) to Windows .claude/
# Run this from WSL after changing config in ai-brain.
#
# Unlike setup-pai.sh (which creates symlinks for WSL),
# this COPIES files because Windows can't follow WSL symlinks.

set -e

REPO_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
WIN_CLAUDE="/mnt/c/Users/Alejandro/.claude"
CONFIG_SRC="$REPO_DIR/.claude-config"
PAI_SRC="$REPO_DIR/pai"

echo "🔄 Syncing PAI config → Windows .claude/"
echo "   Source: $REPO_DIR"
echo "   Target: $WIN_CLAUDE"
echo ""

# --- CLAUDE.md (global) ---
# This one is special: we inline the PAI identity into it
# because hooks may not be available on Windows (no bun).
echo "📝 Building CLAUDE.md with inline PAI identity..."

CLAUDE_MD="$CONFIG_SRC/CLAUDE.md"
IDENTITY="$PAI_SRC/IDENTITY.md"
PROJECTS="$PAI_SRC/PROJECTS.md"

if [ -f "$CLAUDE_MD" ]; then
    # Start with the base CLAUDE.md
    cp "$CLAUDE_MD" "$WIN_CLAUDE/CLAUDE.md"

    # Append PAI identity inline
    echo "" >> "$WIN_CLAUDE/CLAUDE.md"
    echo "---" >> "$WIN_CLAUDE/CLAUDE.md"
    echo "" >> "$WIN_CLAUDE/CLAUDE.md"

    if [ -f "$IDENTITY" ]; then
        cat "$IDENTITY" >> "$WIN_CLAUDE/CLAUDE.md"
        echo "" >> "$WIN_CLAUDE/CLAUDE.md"
        echo "---" >> "$WIN_CLAUDE/CLAUDE.md"
        echo "" >> "$WIN_CLAUDE/CLAUDE.md"
    fi

    if [ -f "$PROJECTS" ]; then
        # Compact version of projects (just the essentials)
        echo "## Projetos Ativos" >> "$WIN_CLAUDE/CLAUDE.md"
        echo "" >> "$WIN_CLAUDE/CLAUDE.md"
        echo "### 1. Duke (Obrigação)" >> "$WIN_CLAUDE/CLAUDE.md"
        echo "- Soluções solicitadas no Duke Beach Hotel" >> "$WIN_CLAUDE/CLAUDE.md"
        echo "- Repo: sistema-os / concierge-platform" >> "$WIN_CLAUDE/CLAUDE.md"
        echo "" >> "$WIN_CLAUDE/CLAUDE.md"
        echo "### 2. AI-PMS (Visão)" >> "$WIN_CLAUDE/CLAUDE.md"
        echo "- PMS AI-native como produto (futura empresa)" >> "$WIN_CLAUDE/CLAUDE.md"
        echo "- Repo: ai-brain (exploração) → sistema-os (produção)" >> "$WIN_CLAUDE/CLAUDE.md"
        echo "" >> "$WIN_CLAUDE/CLAUDE.md"
        echo "### 3. AI-Brain (Capacidade)" >> "$WIN_CLAUDE/CLAUDE.md"
        echo "- PAI/TELOS, workflows de aumento de potencial humano" >> "$WIN_CLAUDE/CLAUDE.md"
        echo "- Repo: ai-brain" >> "$WIN_CLAUDE/CLAUDE.md"
    fi

    echo "   ✅ CLAUDE.md"
else
    echo "   ⚠️  CLAUDE.md not found in $CONFIG_SRC"
fi

# --- settings.json ---
echo "⚙️  Syncing settings.json (permissions only, no hooks)..."
# We build a Windows-specific settings.json without hooks
# since hooks require bun which may not be installed on Windows.
# If bun IS installed, the hooks section can be added manually.
python3 -c "
import json, sys

# Read source settings
with open('$CONFIG_SRC/settings.json') as f:
    settings = json.load(f)

# Keep permissions and deny rules
win_settings = {
    'permissions': {
        'allow': [
            'Read(**)', 'Write(**)', 'Edit(**)', 'Glob(**)', 'Grep(**)',
            'WebSearch', 'WebFetch(*)', 'Skill(*)', 'Task(*)', 'Bash(*)',
            'mcp__plugin_supabase_supabase__*',
            'mcp__plugin_playwright_playwright__*'
        ],
        'deny': settings.get('permissions', {}).get('deny', [])
    },
    'enabledPlugins': settings.get('enabledPlugins', {}),
    'language': settings.get('language', 'PT-BR'),
    'alwaysThinkingEnabled': settings.get('alwaysThinkingEnabled', True)
}

with open('$WIN_CLAUDE/settings.json', 'w') as f:
    json.dump(win_settings, f, indent=2)
    f.write('\n')
" 2>/dev/null && echo "   ✅ settings.json" || echo "   ⚠️  Python failed, using existing settings.json"

# --- PAI files (for future hook use) ---
echo "📄 Syncing PAI context files..."
mkdir -p "$WIN_CLAUDE/pai"
if [ -d "$PAI_SRC" ]; then
    cp "$PAI_SRC"/*.md "$WIN_CLAUDE/pai/" 2>/dev/null
    echo "   ✅ pai/"
fi

# --- Hooks (for future bun installation) ---
echo "🪝 Syncing hooks (requires bun on Windows to work)..."
mkdir -p "$WIN_CLAUDE/hooks/lib"
if [ -d "$CONFIG_SRC/hooks" ]; then
    cp "$CONFIG_SRC/hooks"/*.ts "$WIN_CLAUDE/hooks/" 2>/dev/null
    cp "$CONFIG_SRC/hooks/lib"/*.ts "$WIN_CLAUDE/hooks/lib/" 2>/dev/null
    echo "   ✅ hooks/ (inactive until bun is installed)"
fi

echo ""
echo "✅ Sync complete!"
echo ""
echo "To activate hooks on Windows, install bun:"
echo "   powershell -c \"irm bun.sh/install.ps1 | iex\""
echo "Then add hooks section to settings.json."
