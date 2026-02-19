#!/usr/bin/env bun
// ~/.claude/hooks/load-core-context.ts
// SessionStart hook: Inject IDENTITY and PROJECTS into Claude's context
// Auto-creates symlinks if ai-brain is found but ~/.claude/pai/ doesn't exist

import { existsSync, readFileSync, mkdirSync, symlinkSync } from 'fs';
import { join } from 'path';
import { homedir } from 'os';

interface SessionStartPayload {
  session_id: string;
  [key: string]: any;
}

const PAI_FILES = ['IDENTITY.md', 'PROJECTS.md', 'DAIDENTITY.md'];

function isSubagentSession(): boolean {
  return process.env.CLAUDE_CODE_AGENT !== undefined ||
         process.env.SUBAGENT === 'true';
}

function getLocalTimestamp(): string {
  const date = new Date();
  const tz = process.env.TIME_ZONE || Intl.DateTimeFormat().resolvedOptions().timeZone;

  try {
    const localDate = new Date(date.toLocaleString('en-US', { timeZone: tz }));
    const year = localDate.getFullYear();
    const month = String(localDate.getMonth() + 1).padStart(2, '0');
    const day = String(localDate.getDate()).padStart(2, '0');
    const hours = String(localDate.getHours()).padStart(2, '0');
    const minutes = String(localDate.getMinutes()).padStart(2, '0');

    return `${year}-${month}-${day} ${hours}:${minutes}`;
  } catch {
    return new Date().toISOString();
  }
}

function findAiBrainPath(): string | null {
  // Check AI_BRAIN_PATH environment variable first
  if (process.env.AI_BRAIN_PATH) {
    const envPath = join(process.env.AI_BRAIN_PATH, 'pai');
    if (existsSync(join(envPath, 'IDENTITY.md'))) {
      return envPath;
    }
  }

  // Check standard location: ~/ai-brain/pai/
  const standardPath = join(homedir(), 'ai-brain', 'pai');
  if (existsSync(join(standardPath, 'IDENTITY.md'))) {
    return standardPath;
  }

  return null;
}

interface SetupResult {
  success: boolean;
  message: string;
  sourcePath?: string;
}

function ensurePaiSymlinks(paiDir: string): SetupResult {
  // Check if pai directory exists and has at least one file
  const hasExistingFiles = existsSync(paiDir) &&
    PAI_FILES.some(file => existsSync(join(paiDir, file)));

  if (hasExistingFiles) {
    return { success: true, message: '' }; // Already set up
  }

  // Try to find ai-brain
  const sourcePath = findAiBrainPath();

  if (!sourcePath) {
    return {
      success: false,
      message: '⚠️ PAI: Contexto não carregado. ai-brain não encontrado em ~/ai-brain/. Clone o repo ou defina AI_BRAIN_PATH.'
    };
  }

  // Create ~/.claude/pai/ directory
  try {
    if (!existsSync(paiDir)) {
      mkdirSync(paiDir, { recursive: true });
    }

    // Create symlinks for each PAI file
    for (const file of PAI_FILES) {
      const sourceFile = join(sourcePath, file);
      const targetFile = join(paiDir, file);

      if (existsSync(sourceFile) && !existsSync(targetFile)) {
        symlinkSync(sourceFile, targetFile);
      }
    }

    return {
      success: true,
      message: `PAI: Symlinks criados automaticamente a partir de ${sourcePath}/`,
      sourcePath
    };
  } catch (error) {
    return {
      success: false,
      message: `⚠️ PAI: Erro ao criar symlinks: ${error}`
    };
  }
}

async function main() {
  try {
    if (isSubagentSession()) {
      process.exit(0);
    }

    const stdinData = await Bun.stdin.text();
    if (!stdinData.trim()) {
      process.exit(0);
    }

    const payload: SessionStartPayload = JSON.parse(stdinData);

    const claudeDir = join(homedir(), '.claude');
    const paiDir = join(claudeDir, 'pai');

    // Auto-setup symlinks if needed
    const setupResult = ensurePaiSymlinks(paiDir);

    if (!setupResult.success) {
      console.log(setupResult.message);
      process.exit(0);
    }

    const identityPath = join(paiDir, 'IDENTITY.md');
    const projectsPath = join(paiDir, 'PROJECTS.md');

    const hasIdentity = existsSync(identityPath);
    const hasProjects = existsSync(projectsPath);

    if (!hasIdentity && !hasProjects) {
      console.log('⚠️ PAI: Symlinks existem mas arquivos estão vazios.');
      process.exit(0);
    }

    const daIdentityPath = join(paiDir, 'DAIDENTITY.md');
    const hasDaIdentity = existsSync(daIdentityPath);

    // Read available files
    let contextContent = '';

    if (hasDaIdentity) {
      const daIdentity = readFileSync(daIdentityPath, 'utf-8');
      contextContent += daIdentity + '\n\n---\n\n';
    }

    if (hasIdentity) {
      const identity = readFileSync(identityPath, 'utf-8');
      contextContent += identity + '\n\n---\n\n';
    }

    if (hasProjects) {
      const projects = readFileSync(projectsPath, 'utf-8');
      contextContent += projects;
    }

    // Build output with setup message if symlinks were just created
    const loadedParts = [
      hasDaIdentity ? 'AI_IDENTITY' : null,
      hasIdentity ? 'IDENTITY' : null,
      hasProjects ? 'PROJECTS' : null,
    ].filter(Boolean).join(' + ');
    let statusMessage = `PAI Context loaded (${loadedParts})`;
    if (setupResult.message) {
      statusMessage = setupResult.message + '\n' + statusMessage;
    }

    const output = `<system-reminder>
PAI CONTEXT (Auto-loaded at Session Start)

${getLocalTimestamp()}

${contextContent}

---
Context loaded from ~/.claude/pai/
</system-reminder>

${statusMessage}`;

    console.log(output);

  } catch (error) {
    console.error('Context loading error:', error);
  }

  process.exit(0);
}

main();
