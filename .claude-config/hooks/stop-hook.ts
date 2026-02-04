#!/usr/bin/env bun
/**
 * stop-hook.ts
 * Hook para evento Stop - analisa cada resposta e extrai learnings
 * Dispara após cada resposta do Claude (não da sessão inteira)
 */

import { writeFileSync, readFileSync, mkdirSync, existsSync, statSync } from 'fs';
import { join, basename } from 'path';
import { homedir } from 'os';
import { callHaiku, LEARNING_CLASSIFICATION_PROMPT } from './lib/haiku-client';

const AI_BRAIN = join(homedir(), 'ai-brain');
const LEARNINGS_DIR = join(AI_BRAIN, 'MEMORY', 'learnings');
const MAX_JSONL_BYTES = 500 * 1024; // 500KB para leitura do JSONL

interface StopPayload {
  session_id: string;
  cwd?: string;
  [key: string]: any;
}

/**
 * Converte cwd para o path do projeto no Claude
 */
function cwdToProjectDir(cwd: string): string {
  return cwd.replace(/\//g, '-');
}

/**
 * Encontra o arquivo JSONL da sessão
 */
function getJsonlPath(cwd: string, sessionId: string): string | null {
  const projectDir = cwdToProjectDir(cwd);
  const jsonlPath = join(homedir(), '.claude', 'projects', projectDir, `${sessionId}.jsonl`);
  if (existsSync(jsonlPath)) {
    return jsonlPath;
  }
  return null;
}

/**
 * Extrai a última resposta do assistant do JSONL
 */
function extractLastAssistantResponse(jsonlPath: string): string | null {
  try {
    const fileSize = statSync(jsonlPath).size;
    let content: string;

    if (fileSize > MAX_JSONL_BYTES) {
      // Para arquivos grandes, ler apenas os últimos 500KB
      const buffer = Buffer.alloc(MAX_JSONL_BYTES);
      const fd = Bun.file(jsonlPath);
      content = readFileSync(jsonlPath, 'utf-8').slice(-MAX_JSONL_BYTES);
    } else {
      content = readFileSync(jsonlPath, 'utf-8');
    }

    const lines = content.split('\n').filter(l => l.trim());

    // Percorrer de trás para frente buscando última resposta do assistant
    for (let i = lines.length - 1; i >= 0; i--) {
      try {
        const obj = JSON.parse(lines[i]);
        if (obj.type === 'assistant' && obj.message?.content) {
          // Extrair texto das respostas
          const contentBlocks = obj.message.content;
          if (Array.isArray(contentBlocks)) {
            const textParts = contentBlocks
              .filter((b: any) => b.type === 'text' && b.text)
              .map((b: any) => b.text)
              .join('\n');
            if (textParts.length > 50) {
              return textParts;
            }
          }
        }
      } catch {
        continue;
      }
    }
    return null;
  } catch (error) {
    console.error('[PAI] Error reading JSONL:', error);
    return null;
  }
}

/**
 * Salva um learning extraído
 */
function saveLearning(
  phase: string,
  summary: string,
  sessionId: string,
  confidence: number
): void {
  const phaseDir = join(LEARNINGS_DIR, phase);
  if (!existsSync(phaseDir)) {
    mkdirSync(phaseDir, { recursive: true });
  }

  const now = new Date();
  const year = now.getFullYear();
  const month = String(now.getMonth() + 1).padStart(2, '0');
  const day = String(now.getDate()).padStart(2, '0');
  const hours = String(now.getHours()).padStart(2, '0');
  const minutes = String(now.getMinutes()).padStart(2, '0');
  const seconds = String(now.getSeconds()).padStart(2, '0');
  const hash = sessionId.substring(0, 6) || Math.random().toString(36).substring(2, 8);
  const filename = `${year}-${month}-${day}_${hours}-${minutes}-${seconds}_${hash}.md`;

  const content = `---
timestamp: ${now.toISOString()}
session_id: ${sessionId}
phase: ${phase}
confidence: ${confidence}
---

# Learning: ${phase}

${summary}

---
*Auto-extracted by stop-hook.ts*
`;

  writeFileSync(join(phaseDir, filename), content);
  console.error(`[PAI] Learning captured: ${phase}/${filename}`);
}

async function main() {
  try {
    const stdinData = await Bun.stdin.text();
    if (!stdinData.trim()) {
      process.exit(0);
    }

    const payload: StopPayload = JSON.parse(stdinData);
    const cwd = payload.cwd || process.cwd();
    const sessionId = payload.session_id || 'unknown';

    // Encontrar JSONL da sessão
    const jsonlPath = getJsonlPath(cwd, sessionId);
    if (!jsonlPath) {
      // Sem JSONL, não há o que analisar
      process.exit(0);
    }

    // Extrair última resposta do assistant
    const lastResponse = extractLastAssistantResponse(jsonlPath);
    if (!lastResponse || lastResponse.length < 100) {
      // Resposta muito curta, provavelmente trivial
      process.exit(0);
    }

    // Truncar para evitar tokens excessivos
    const truncatedResponse = lastResponse.substring(0, 4000);

    // Classificar com Haiku
    const result = await callHaiku(
      LEARNING_CLASSIFICATION_PROMPT,
      `ASSISTANT RESPONSE:\n${truncatedResponse}`,
      400
    );

    if (!result) {
      console.error('[PAI] Classification failed, skipping');
      process.exit(0);
    }

    // Se for learning, salvar
    if (
      result.classification === 'learning' &&
      result.phase &&
      result.learning_summary
    ) {
      saveLearning(
        result.phase,
        result.learning_summary,
        sessionId,
        result.confidence || 0.5
      );
    } else {
      // Log para debug (comentar em produção)
      // console.error(`[PAI] Classified as ${result.classification}: ${result.reasoning?.substring(0, 50)}`);
    }
  } catch (error) {
    console.error('[PAI] Stop hook error:', error);
  }

  process.exit(0);
}

main();
