#!/usr/bin/env bun
// session-capture.ts
// SessionEnd hook: Capture session summary to MEMORY/sessions/
// CENTRALIZED: All sessions go to ai-brain/MEMORY/sessions/ regardless of cwd
// Reads Claude Code JSONL to extract real content (summaries, files, tools)
// v2: Adds minimum session filter + intelligent summary via Haiku

import { writeFileSync, readFileSync, mkdirSync, existsSync, statSync } from 'fs';
import { join, basename } from 'path';
import { homedir } from 'os';
import { callHaiku, SESSION_SUMMARY_PROMPT } from './lib/haiku-client';

const MAX_JSONL_BYTES = 2 * 1024 * 1024; // 2MB cap for reading
const AI_BRAIN_MEMORY = join(homedir(), 'ai-brain', 'MEMORY', 'sessions');
const MIN_INTERACTIONS = 2; // Minimum interactions to save session

interface SessionPayload {
  session_id: string;
  cwd?: string;
  [key: string]: any;
}

interface SessionData {
  summaries: string[];
  firstUserMessage: string;
  filesModified: string[];
  toolsUsed: string[];
  userMessageCount: number;
  project: string;
  branch: string;
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
    const seconds = String(localDate.getSeconds()).padStart(2, '0');
    return `${year}-${month}-${day}T${hours}:${minutes}:${seconds}`;
  } catch {
    return new Date().toISOString();
  }
}

function getDateString(): string {
  const date = new Date();
  const year = date.getFullYear();
  const month = String(date.getMonth() + 1).padStart(2, '0');
  const day = String(date.getDate()).padStart(2, '0');
  return `${year}-${month}-${day}`;
}

function getFilenameTimestamp(): string {
  const date = new Date();
  const year = date.getFullYear();
  const month = String(date.getMonth() + 1).padStart(2, '0');
  const day = String(date.getDate()).padStart(2, '0');
  const hours = String(date.getHours()).padStart(2, '0');
  const minutes = String(date.getMinutes()).padStart(2, '0');
  const seconds = String(date.getSeconds()).padStart(2, '0');
  return `${year}-${month}-${day}_${hours}-${minutes}-${seconds}`;
}

function cwdToProjectDir(cwd: string): string {
  // Claude Code maps /home/marketing/ai-brain → -home-marketing-ai-brain
  return cwd.replace(/\//g, '-');
}

function getJsonlPath(cwd: string, sessionId: string): string | null {
  const projectDir = cwdToProjectDir(cwd);
  const jsonlPath = join(homedir(), '.claude', 'projects', projectDir, `${sessionId}.jsonl`);
  if (existsSync(jsonlPath)) {
    return jsonlPath;
  }
  return null;
}

function extractUserText(content: any): string {
  if (typeof content === 'string') return content;
  if (Array.isArray(content)) {
    for (const block of content) {
      if (block?.type === 'text' && block.text) {
        return block.text;
      }
    }
  }
  return '';
}

function extractFromJsonl(jsonlPath: string): SessionData {
  const data: SessionData = {
    summaries: [],
    firstUserMessage: '',
    filesModified: [],
    toolsUsed: [],
    userMessageCount: 0,
    project: '',
    branch: '',
  };

  try {
    const fileSize = statSync(jsonlPath).size;
    let rawContent: string;

    if (fileSize > MAX_JSONL_BYTES) {
      // For large files, read first 1MB + last 500KB
      const buf = Buffer.alloc(MAX_JSONL_BYTES);
      const fd = Bun.file(jsonlPath);
      rawContent = readFileSync(jsonlPath, { encoding: 'utf-8', flag: 'r' }).substring(0, MAX_JSONL_BYTES);
    } else {
      rawContent = readFileSync(jsonlPath, 'utf-8');
    }

    const lines = rawContent.split('\n');
    const filesSet = new Set<string>();
    const toolsSet = new Set<string>();

    for (const line of lines) {
      if (!line.trim()) continue;

      try {
        const obj = JSON.parse(line);
        const type = obj.type;

        // Extract summaries
        if (type === 'summary' && obj.summary) {
          data.summaries.push(obj.summary);
        }

        // Extract first user message and count
        if (type === 'user' && obj.message?.role === 'user') {
          data.userMessageCount++;
          if (!data.firstUserMessage) {
            const text = extractUserText(obj.message.content);
            // Clean up system-reminder tags and truncate
            const cleaned = text.replace(/<system-reminder>[\s\S]*?<\/system-reminder>/g, '').trim();
            data.firstUserMessage = cleaned.substring(0, 300);
          }
          // Extract branch from first available
          if (!data.branch && obj.gitBranch) {
            data.branch = obj.gitBranch;
          }
        }

        // Extract tools and files from assistant messages
        if (type === 'assistant' && Array.isArray(obj.message?.content)) {
          for (const block of obj.message.content) {
            if (block?.type === 'tool_use' && block.name) {
              toolsSet.add(block.name);
              // Track file modifications
              if (['Write', 'Edit', 'NotebookEdit'].includes(block.name)) {
                const fp = block.input?.file_path || block.input?.filePath || '';
                if (fp) filesSet.add(fp);
              }
            }
          }
        }

        // Extract branch from any record
        if (!data.branch && obj.gitBranch) {
          data.branch = obj.gitBranch;
        }
      } catch {
        // Skip malformed lines
        continue;
      }
    }

    data.filesModified = [...filesSet];
    data.toolsUsed = [...toolsSet].sort();
  } catch (error) {
    console.error('[PAI] JSONL extraction error:', error);
  }

  return data;
}

/**
 * Verifica se a sessão é mínima (deve ser ignorada)
 * Sessões com poucas interações E sem arquivos modificados são descartadas
 */
function isMinimalSession(data: SessionData): boolean {
  // Se tem arquivos modificados, sempre salvar
  if (data.filesModified.length > 0) {
    return false;
  }
  // Se tem poucas interações e nenhum arquivo, é mínima
  return data.userMessageCount < MIN_INTERACTIONS;
}

/**
 * Gera resumo inteligente via Haiku quando não há summary do Claude
 */
async function generateSmartSummary(data: SessionData): Promise<string | null> {
  // Se já tem summary do Claude, usar
  if (data.summaries.length > 0) {
    return null; // Usar o que já existe
  }

  // Sessão muito curta para resumo inteligente
  if (data.userMessageCount < 3 && data.filesModified.length === 0) {
    return null;
  }

  // Construir contexto para Haiku
  const context = `
Primeira mensagem do usuário: ${data.firstUserMessage || 'N/A'}
Arquivos modificados: ${data.filesModified.join(', ') || 'nenhum'}
Ferramentas usadas: ${data.toolsUsed.join(', ') || 'nenhuma'}
Total de interações: ${data.userMessageCount}
Projeto: ${data.project || 'desconhecido'}
  `.trim();

  try {
    const result = await callHaiku(
      SESSION_SUMMARY_PROMPT,
      context,
      200
    );

    if (result?.content) {
      return result.content;
    }
  } catch (error) {
    console.error('[PAI] Smart summary generation failed:', error);
  }

  return null;
}

function buildContent(
  sessionId: string,
  shortId: string,
  dateStr: string,
  timestamp: string,
  cwd: string,
  projectName: string,
  data: SessionData
): string {
  const topic = data.summaries.length > 0
    ? data.summaries[data.summaries.length - 1]
    : `Session with ${data.userMessageCount} interactions`;

  const branch = data.branch || 'unknown';

  let content = `---
session_id: ${sessionId}
timestamp: ${timestamp}
project: ${projectName}
cwd: ${cwd}
branch: ${branch}
interactions: ${data.userMessageCount}
---

# Session ${shortId}

**Date:** ${dateStr} | **Project:** ${projectName}

## Topic

${topic}
`;

  // Initial context
  if (data.firstUserMessage) {
    content += `
## Initial Context

${data.firstUserMessage}
`;
  }

  // What happened (summary evolution)
  if (data.summaries.length > 1) {
    content += `
## What Happened

`;
    // Deduplicate similar summaries, keep unique ones
    const seen = new Set<string>();
    for (const s of data.summaries) {
      if (!seen.has(s)) {
        seen.add(s);
        content += `- ${s}\n`;
      }
    }
  }

  // Files modified
  if (data.filesModified.length > 0) {
    content += `
## Files Modified

`;
    for (const f of data.filesModified) {
      content += `- ${f}\n`;
    }
  }

  // Tools used
  if (data.toolsUsed.length > 0) {
    content += `
## Tools Used

${data.toolsUsed.join(', ')}
`;
  }

  content += `
---
*Auto-generated from session JSONL by session-capture.ts*
`;

  return content;
}

function buildFallbackContent(
  sessionId: string,
  shortId: string,
  dateStr: string,
  timestamp: string,
  cwd: string,
  projectName: string
): string {
  return `---
session_id: ${sessionId}
timestamp: ${timestamp}
project: ${projectName}
cwd: ${cwd}
interactions: 0
---

# Session ${shortId}

**Date:** ${dateStr} | **Project:** ${projectName}

## Topic

Session without JSONL data (short session or JSONL not found)

---
*Auto-generated by session-capture.ts (no JSONL available)*
`;
}

async function main() {
  try {
    const stdinData = await Bun.stdin.text();
    if (!stdinData.trim()) {
      process.exit(0);
    }

    const payload: SessionPayload = JSON.parse(stdinData);
    const cwd = payload.cwd || process.cwd();
    const sessionId = payload.session_id || 'unknown';
    const shortId = sessionId.substring(0, 8);
    const dateStr = getDateString();
    const timestamp = getLocalTimestamp();
    const filenameTs = getFilenameTimestamp();
    const filename = `${filenameTs}_${shortId}.md`;
    const projectName = basename(cwd);

    // Always write to ai-brain MEMORY (centralized)
    if (!existsSync(AI_BRAIN_MEMORY)) {
      mkdirSync(AI_BRAIN_MEMORY, { recursive: true });
    }

    const filepath = join(AI_BRAIN_MEMORY, filename);

    // If file already exists (created by /fim skill), append metadata section
    if (existsSync(filepath)) {
      const jsonlPath = getJsonlPath(cwd, sessionId);
      if (jsonlPath) {
        const data = extractFromJsonl(jsonlPath);
        let appendContent = `\n\n## Auto-Metadata\n\n`;
        appendContent += `- **Interactions:** ${data.userMessageCount}\n`;
        appendContent += `- **Branch:** ${data.branch || 'unknown'}\n`;
        if (data.toolsUsed.length > 0) {
          appendContent += `- **Tools:** ${data.toolsUsed.join(', ')}\n`;
        }
        if (data.filesModified.length > 0) {
          appendContent += `- **Files:** ${data.filesModified.join(', ')}\n`;
        }
        appendContent += `\n---\n*Metadata appended by session-capture.ts*\n`;

        const existing = readFileSync(filepath, 'utf-8');
        writeFileSync(filepath, existing + appendContent);
      }
      console.error(`[PAI] Session metadata appended: ${filename}`);
      process.exit(0);
    }

    // Try to extract from JSONL
    const jsonlPath = getJsonlPath(cwd, sessionId);

    if (jsonlPath) {
      const data = extractFromJsonl(jsonlPath);
      data.project = projectName;

      // FILTRO: Ignorar sessões mínimas
      if (isMinimalSession(data)) {
        console.error(`[PAI] Session ${shortId} skipped (minimal: ${data.userMessageCount} interactions, ${data.filesModified.length} files)`);
        process.exit(0);
      }

      // RESUMO INTELIGENTE: Gerar via Haiku se não tem summary
      const smartSummary = await generateSmartSummary(data);
      if (smartSummary) {
        data.summaries.push(smartSummary);
      }

      const content = buildContent(sessionId, shortId, dateStr, timestamp, cwd, projectName, data);
      writeFileSync(filepath, content);
      console.error(`[PAI] Session captured (JSONL): ${filename} [${data.summaries.length} summaries, ${data.filesModified.length} files]`);
    } else {
      // Fallback: no JSONL found - também aplicar filtro (sessão sem dados = mínima)
      console.error(`[PAI] Session ${shortId} skipped (no JSONL data)`);
      process.exit(0);
    }

  } catch (error) {
    console.error('[PAI] Session capture error:', error);
  }

  process.exit(0);
}

main();
