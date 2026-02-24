#!/usr/bin/env bun
// Status line for Claude Code (cross-platform)
// Shows: Model | Git Branch | Cost | Context Usage

import { execSync } from 'child_process';

interface StatusInput {
  model?: { display_name?: string };
  context_window?: { context_window_size?: number; current_usage?: { input_tokens?: number; cache_creation_input_tokens?: number; cache_read_input_tokens?: number } };
  cost?: { total_cost_usd?: number };
}

async function main() {
  const stdinData = await Bun.stdin.text();
  if (!stdinData.trim()) {
    process.exit(0);
  }

  const input: StatusInput = JSON.parse(stdinData);

  const model = input.model?.display_name ?? 'Claude';

  // Format cost
  const cost = input.cost?.total_cost_usd ?? 0;
  const costFormatted = cost < 0.01 && cost > 0 ? cost.toFixed(4) : cost.toFixed(2);

  // Calculate context percentage
  let percentUsed = 0;
  const usage = input.context_window?.current_usage;
  const contextSize = input.context_window?.context_window_size;
  if (usage && contextSize && contextSize > 0) {
    const currentTokens = (usage.input_tokens ?? 0) + (usage.cache_creation_input_tokens ?? 0) + (usage.cache_read_input_tokens ?? 0);
    percentUsed = Math.round((currentTokens * 100) / contextSize);
  }

  // Color context percentage (ANSI)
  let contextColor: string;
  if (percentUsed < 50) {
    contextColor = '\x1b[32m'; // Green
  } else if (percentUsed < 80) {
    contextColor = '\x1b[33m'; // Yellow
  } else {
    contextColor = '\x1b[31m'; // Red
  }
  const reset = '\x1b[0m';

  // Git branch
  let gitBranch = '';
  try {
    const branch = execSync('git branch --show-current', { encoding: 'utf-8', timeout: 2000, stdio: ['pipe', 'pipe', 'pipe'] }).trim();
    if (branch) gitBranch = `🌿 ${branch}`;
  } catch { /* not in a git repo */ }

  // Build status line
  const parts = [`[${model}]`];
  if (gitBranch) parts.push(gitBranch);
  parts.push(`💰 $${costFormatted}`);
  parts.push(`${contextColor}📊 ${percentUsed}%${reset}`);

  console.log(parts.join(' | '));
}

main();
