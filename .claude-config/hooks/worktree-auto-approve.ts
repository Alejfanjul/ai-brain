#!/usr/bin/env bun
// $PAI_DIR/hooks/worktree-auto-approve.ts
// PreToolUse hook: Auto-approves file operations on git worktrees
// matching the pattern: sistema-os-wt-*

import { homedir } from 'os';
import { resolve, sep } from 'path';

interface PreToolUsePayload {
  session_id: string;
  tool_name: string;
  tool_input: Record<string, any>;
}

// Pattern: any directory under home matching sistema-os-wt-{name}
const HOME = homedir();

function isWorktreePath(filePath: string): boolean {
  const normalized = resolve(filePath);
  const homePrefix = HOME + sep;
  if (!normalized.startsWith(homePrefix)) return false;
  const relative = normalized.slice(homePrefix.length);
  return /^sistema-os-wt-[^/\\]+/.test(relative);
}

function extractPath(toolName: string, toolInput: Record<string, any>): string | null {
  switch (toolName) {
    case "Read":
    case "Write":
    case "Edit":
      return toolInput.file_path ?? null;
    case "Glob":
    case "Grep":
      return toolInput.path ?? null;
    default:
      return null;
  }
}

async function main() {
  try {
    const stdinData = await Bun.stdin.text();
    if (!stdinData.trim()) {
      process.exit(0);
    }

    const payload: PreToolUsePayload = JSON.parse(stdinData);

    const targetTools = ["Read", "Write", "Edit", "Glob", "Grep"];
    if (!targetTools.includes(payload.tool_name)) {
      process.exit(0);
    }

    const path = extractPath(payload.tool_name, payload.tool_input);
    if (!path) {
      process.exit(0);
    }

    if (isWorktreePath(path)) {
      // Auto-approve: bypass permission prompt
      console.log(JSON.stringify({ decision: "approve" }));
    }
  } catch (error) {
    // Never crash — fail open
    console.error("worktree-auto-approve error:", error);
  }

  process.exit(0);
}

main();
