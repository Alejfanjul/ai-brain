#!/usr/bin/env bun
/**
 * haiku-client.ts
 * Cliente leve para chamadas Haiku via API Anthropic
 * Usado pelos hooks para classificação e resumos inteligentes
 */

import { existsSync, readFileSync } from 'fs';
import { join } from 'path';
import { homedir } from 'os';

const ANTHROPIC_API_URL = 'https://api.anthropic.com/v1/messages';
const DEFAULT_MODEL = 'claude-3-5-haiku-20241022';
const DEFAULT_MAX_TOKENS = 500;

/**
 * Carrega variáveis do .env do ~/.claude/ se existir
 */
function loadEnvFile(): void {
  const envPath = join(homedir(), '.claude', '.env');
  if (existsSync(envPath)) {
    const content = readFileSync(envPath, 'utf-8');
    for (const line of content.split('\n')) {
      const trimmed = line.trim();
      if (trimmed && !trimmed.startsWith('#')) {
        const [key, ...valueParts] = trimmed.split('=');
        const value = valueParts.join('=').replace(/^["']|["']$/g, '');
        if (key && value && !process.env[key]) {
          process.env[key] = value;
        }
      }
    }
  }
}

// Carregar .env na inicialização
loadEnvFile();

export interface HaikuResponse {
  classification?: string;
  confidence?: number;
  phase?: string | null;
  reasoning?: string;
  learning_summary?: string | null;
  content?: string;
  raw?: string;
}

/**
 * Chama Haiku para classificação/processamento
 * @param systemPrompt - Instruções do sistema
 * @param userMessage - Conteúdo a processar
 * @param maxTokens - Limite de tokens de saída (default: 500)
 * @returns HaikuResponse parseado ou null em caso de erro
 */
export async function callHaiku(
  systemPrompt: string,
  userMessage: string,
  maxTokens: number = DEFAULT_MAX_TOKENS
): Promise<HaikuResponse | null> {
  const apiKey = process.env.ANTHROPIC_API_KEY;

  if (!apiKey) {
    console.error('[PAI] ANTHROPIC_API_KEY not set - skipping Haiku call');
    return null;
  }

  try {
    const response = await fetch(ANTHROPIC_API_URL, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'x-api-key': apiKey,
        'anthropic-version': '2023-06-01'
      },
      body: JSON.stringify({
        model: DEFAULT_MODEL,
        max_tokens: maxTokens,
        system: systemPrompt,
        messages: [{ role: 'user', content: userMessage }]
      })
    });

    if (!response.ok) {
      console.error('[PAI] Haiku API error:', response.status, response.statusText);
      return null;
    }

    const data = await response.json();
    const text = data.content?.[0]?.text || '';

    // Tentar parsear como JSON
    try {
      // Limpar possíveis marcadores de código
      const cleanText = text
        .replace(/^```json\s*/i, '')
        .replace(/^```\s*/i, '')
        .replace(/\s*```$/i, '')
        .trim();

      return JSON.parse(cleanText);
    } catch {
      // Se não for JSON válido, retornar como content
      return {
        content: text.trim(),
        raw: text
      };
    }
  } catch (error) {
    console.error('[PAI] Haiku call failed:', error);
    return null;
  }
}

/**
 * Classificação de learning com prompt pré-definido
 */
export const LEARNING_CLASSIFICATION_PROMPT = `You are a learning classifier for a developer's personal knowledge system.

Analyze the AI assistant's response and classify it:

1. "learning" - Contains a reusable insight, pattern, discovery, or technique that:
   - Could help in future similar situations
   - Is not project-specific
   - Contains generalizable knowledge

2. "work" - Normal productive work (code changes, file edits, research) without extractable learning

3. "empty" - Trivial responses (greetings, acknowledgments, errors, simple questions)

If "learning", also identify the phase:
- OBSERVE: Discoveries about codebase, system, or domain
- THINK: Analysis conclusions, hypotheses confirmed/rejected
- PLAN: Strategic decisions, architectural choices
- BUILD: Implementation patterns, code techniques
- EXECUTE: Operational learnings, deployment insights
- VERIFY: Testing insights, validation patterns

Respond ONLY with JSON (no markdown, no explanation):
{
  "classification": "learning" | "work" | "empty",
  "confidence": 0.0-1.0,
  "phase": "OBSERVE" | "THINK" | "PLAN" | "BUILD" | "EXECUTE" | "VERIFY" | null,
  "reasoning": "brief explanation",
  "learning_summary": "extracted learning in Portuguese if classification=learning, else null"
}`;

/**
 * Prompt para resumo de sessão
 */
export const SESSION_SUMMARY_PROMPT = `Generate a concise session summary in Portuguese (Brazilian).
Focus on: what was accomplished, key decisions made, main outcomes.
Tone: technical, factual, no filler.
Output: 1-2 sentences only.`;

// Se executado diretamente (para testes)
if (import.meta.main) {
  const testResult = await callHaiku(
    'Respond with JSON: {"status": "ok", "message": "Haiku client working"}',
    'Test connection',
    100
  );
  console.log('Test result:', JSON.stringify(testResult, null, 2));
}
