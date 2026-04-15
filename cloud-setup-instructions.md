# Instruções de Setup - Claude Code na Cloud

> Copie este prompt inteiro e envie para a Claude rodando na máquina remota.

---

## PROMPT PARA A CLAUDE REMOTA:

Preciso que você configure o Claude Code nesta máquina com as mesmas permissões e hooks que tenho na minha máquina local. Siga todos os passos abaixo em ordem.

### Passo 1: Instalar Bun (se não estiver instalado)

Verifique se o Bun está instalado com `bun --version`. Se não estiver:

```bash
curl -fsSL https://bun.sh/install | bash
```

Depois confirme que funciona: `~/.bun/bin/bun --version`

### Passo 2: Criar estrutura de diretórios

```bash
mkdir -p ~/.claude/hooks/lib
mkdir -p ~/.claude/pai
```

### Passo 3: Criar `~/.claude/settings.json`

Crie o arquivo `~/.claude/settings.json` com este conteúdo EXATO:

```json
{
  "permissions": {
    "allow": [
      "Read(**)",
      "Write(**)",
      "Edit(**)",
      "Glob(**)",
      "Grep(**)",
      "WebSearch",
      "WebFetch(*)",
      "Skill(*)",
      "Task(*)",
      "Bash(*)"
    ],
    "deny": [
      "Bash(rm -rf *)",
      "Bash(rm -r /*)",
      "Bash(rm -r ~*)",
      "Bash(sudo rm -rf *)",
      "Bash(sudo rm -r *)",
      "Bash(dd if=*)",
      "Bash(mkfs*)",
      "Bash(git push --force*)",
      "Bash(git push -f *)",
      "Bash(git reset --hard*)",
      "Bash(git clean -f*)",
      "Bash(git checkout -- .)",
      "Bash(git restore .)",
      "Bash(git merge * main)",
      "Bash(> /dev/sd*)",
      "Bash(chmod 777 *)"
    ]
  },
  "hooks": {
    "SessionStart": [
      {
        "matcher": "*",
        "hooks": [
          {
            "type": "command",
            "command": "~/.bun/bin/bun run ~/.claude/hooks/initialize-session.ts"
          },
          {
            "type": "command",
            "command": "~/.bun/bin/bun run ~/.claude/hooks/load-core-context.ts"
          }
        ]
      }
    ],
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": "~/.bun/bin/bun run ~/.claude/hooks/security-validator.ts"
          }
        ]
      },
      {
        "matcher": "Read|Write|Edit|Glob|Grep",
        "hooks": [
          {
            "type": "command",
            "command": "~/.bun/bin/bun run ~/.claude/hooks/worktree-auto-approve.ts"
          }
        ]
      }
    ],
    "UserPromptSubmit": [
      {
        "matcher": "*",
        "hooks": [
          {
            "type": "command",
            "command": "~/.bun/bin/bun run ~/.claude/hooks/update-tab-titles.ts"
          }
        ]
      }
    ]
  },
  "statusLine": {
    "type": "command",
    "command": "~/.bun/bin/bun run ~/.claude/hooks/statusline.ts",
    "padding": 0
  },
  "language": "PT-BR",
  "alwaysThinkingEnabled": true
}
```

### Passo 4: Criar `~/.claude/CLAUDE.md`

```markdown
Sempre responda em português brasileiro.
Tom técnico e direto. Pode fazer uma brincadeira ocasional quando fizer sentido, mas nunca espelhe o estilo informal do usuário.

## Git
- **Sempre pedir permissão antes de fazer merge para main.** Push para development pode ser feito diretamente, mas merge para main requer confirmação explícita do usuário.
```

### Passo 5: Criar os hooks

Crie cada arquivo abaixo em `~/.claude/hooks/`:

#### 5.1 `~/.claude/hooks/lib/observability.ts`

```typescript
#!/usr/bin/env bun
// Stub de observability - funções exportadas para compatibilidade

export function getCurrentTimestamp(): string {
  return new Date().toISOString();
}

export function getSourceApp(): string {
  return 'claude-code';
}

export async function sendEventToObservability(event: Record<string, any>): Promise<void> {
  // Log local apenas - sem serviço externo configurado
  console.error(`[Observability] ${event.security_action || 'event'}: ${event.security_message || JSON.stringify(event)}`);
}
```

#### 5.2 `~/.claude/hooks/lib/haiku-client.ts`

```typescript
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

    try {
      const cleanText = text
        .replace(/^```json\s*/i, '')
        .replace(/^```\s*/i, '')
        .replace(/\s*```$/i, '')
        .trim();

      return JSON.parse(cleanText);
    } catch {
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

export const LEARNING_CLASSIFICATION_PROMPT = `You are a learning classifier for a developer's personal knowledge system.

Analyze the AI assistant's response and classify it:

1. "learning" - Contains a reusable insight, pattern, discovery, or technique
2. "work" - Normal productive work without extractable learning
3. "empty" - Trivial responses

If "learning", also identify the phase: OBSERVE, THINK, PLAN, BUILD, EXECUTE, VERIFY

Respond ONLY with JSON:
{
  "classification": "learning" | "work" | "empty",
  "confidence": 0.0-1.0,
  "phase": "OBSERVE" | "THINK" | "PLAN" | "BUILD" | "EXECUTE" | "VERIFY" | null,
  "reasoning": "brief explanation",
  "learning_summary": "extracted learning in Portuguese if classification=learning, else null"
}`;

export const SESSION_SUMMARY_PROMPT = `Generate a concise session summary in Portuguese (Brazilian).
Focus on: what was accomplished, key decisions made, main outcomes.
Tone: technical, factual, no filler.
Output: 1-2 sentences only.`;
```

#### 5.3 `~/.claude/hooks/initialize-session.ts`

```typescript
#!/usr/bin/env bun
import { existsSync, writeFileSync, mkdirSync } from 'fs';
import { join } from 'path';
import { homedir } from 'os';

interface SessionStartPayload {
  session_id: string;
  cwd?: string;
  [key: string]: any;
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
    return `${year}-${month}-${day} ${hours}:${minutes}:${seconds}`;
  } catch {
    return new Date().toISOString();
  }
}

function setTabTitle(title: string): void {
  const tabEscape = `\x1b]1;${title}\x07`;
  const windowEscape = `\x1b]2;${title}\x07`;
  process.stderr.write(tabEscape);
  process.stderr.write(windowEscape);
}

function getProjectName(cwd: string | undefined): string {
  if (!cwd) return 'Session';
  const parts = cwd.split('/').filter(p => p);
  const projectIndicators = ['Projects', 'projects', 'src', 'repos', 'code'];
  for (let i = parts.length - 1; i >= 0; i--) {
    if (projectIndicators.includes(parts[i]) && parts[i + 1]) {
      return parts[i + 1];
    }
  }
  return parts[parts.length - 1] || 'Session';
}

async function main() {
  try {
    const stdinData = await Bun.stdin.text();
    if (!stdinData.trim()) {
      process.exit(0);
    }

    const payload: SessionStartPayload = JSON.parse(stdinData);
    const paiDir = process.env.PAI_DIR || join(homedir(), '.config', 'pai');

    const projectName = getProjectName(payload.cwd);
    setTabTitle(`🤖 ${projectName}`);

    const requiredDirs = [
      join(paiDir, 'hooks', 'lib'),
      join(paiDir, 'history', 'sessions'),
      join(paiDir, 'history', 'learnings'),
      join(paiDir, 'history', 'research'),
    ];

    for (const dir of requiredDirs) {
      if (!existsSync(dir)) {
        mkdirSync(dir, { recursive: true });
      }
    }

    const sessionFile = join(paiDir, '.current-session');
    writeFileSync(sessionFile, JSON.stringify({
      session_id: payload.session_id,
      started: getLocalTimestamp(),
      cwd: payload.cwd,
      project: projectName
    }, null, 2));

    console.error(`[PAI] Session initialized: ${projectName}`);
    console.error(`[PAI] Time: ${getLocalTimestamp()}`);

  } catch (error) {
    console.error('Session initialization error:', error);
  }

  process.exit(0);
}

main();
```

#### 5.4 `~/.claude/hooks/load-core-context.ts`

```typescript
#!/usr/bin/env bun
import { existsSync, readFileSync, mkdirSync, symlinkSync, copyFileSync } from 'fs';
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
  if (process.env.AI_BRAIN_PATH) {
    const envPath = join(process.env.AI_BRAIN_PATH, 'pai');
    if (existsSync(join(envPath, 'IDENTITY.md'))) {
      return envPath;
    }
  }
  const standardPath = join(homedir(), 'ai-brain', 'pai');
  if (existsSync(join(standardPath, 'IDENTITY.md'))) {
    return standardPath;
  }
  return null;
}

function ensurePaiSymlinks(paiDir: string): { success: boolean; message: string } {
  const hasExistingFiles = existsSync(paiDir) &&
    PAI_FILES.some(file => existsSync(join(paiDir, file)));

  if (hasExistingFiles) {
    return { success: true, message: '' };
  }

  const sourcePath = findAiBrainPath();

  if (!sourcePath) {
    return {
      success: false,
      message: '⚠️ PAI: Contexto não carregado. ai-brain não encontrado.'
    };
  }

  try {
    if (!existsSync(paiDir)) {
      mkdirSync(paiDir, { recursive: true });
    }

    for (const file of PAI_FILES) {
      const sourceFile = join(sourcePath, file);
      const targetFile = join(paiDir, file);
      if (existsSync(sourceFile) && !existsSync(targetFile)) {
        try {
          symlinkSync(sourceFile, targetFile);
        } catch {
          copyFileSync(sourceFile, targetFile);
        }
      }
    }

    return { success: true, message: `PAI: Contexto vinculado de ${sourcePath}/` };
  } catch (error) {
    return { success: false, message: `⚠️ PAI: Erro ao criar symlinks: ${error}` };
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

    const setupResult = ensurePaiSymlinks(paiDir);

    if (!setupResult.success) {
      console.log(setupResult.message);
      process.exit(0);
    }

    const identityPath = join(paiDir, 'IDENTITY.md');
    const projectsPath = join(paiDir, 'PROJECTS.md');
    const daIdentityPath = join(paiDir, 'DAIDENTITY.md');

    const hasIdentity = existsSync(identityPath);
    const hasProjects = existsSync(projectsPath);
    const hasDaIdentity = existsSync(daIdentityPath);

    if (!hasIdentity && !hasProjects) {
      console.log('⚠️ PAI: Arquivos de contexto não encontrados.');
      process.exit(0);
    }

    let contextContent = '';

    if (hasDaIdentity) {
      contextContent += readFileSync(daIdentityPath, 'utf-8') + '\n\n---\n\n';
    }
    if (hasIdentity) {
      contextContent += readFileSync(identityPath, 'utf-8') + '\n\n---\n\n';
    }
    if (hasProjects) {
      contextContent += readFileSync(projectsPath, 'utf-8');
    }

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
```

#### 5.5 `~/.claude/hooks/security-validator.ts`

```typescript
#!/usr/bin/env bun
import { sendEventToObservability, getCurrentTimestamp, getSourceApp } from './lib/observability';

interface PreToolUsePayload {
  session_id: string;
  tool_name: string;
  tool_input: Record<string, any>;
}

const ATTACK_PATTERNS = {
  catastrophic: {
    patterns: [
      /rm\s+(-rf?|--recursive)\s+[\/~]/i,
      /rm\s+(-rf?|--recursive)\s+\*/i,
      />\s*\/dev\/sd[a-z]/i,
      /mkfs\./i,
      /dd\s+if=.*of=\/dev/i,
    ],
    action: 'block',
    message: '🚨 BLOCKED: Catastrophic deletion/destruction detected'
  },
  reverseShell: {
    patterns: [
      /bash\s+-i\s+>&\s*\/dev\/tcp/i,
      /nc\s+(-e|--exec)\s+\/bin\/(ba)?sh/i,
      /python.*socket.*connect/i,
      /perl.*socket.*connect/i,
      /ruby.*TCPSocket/i,
      /php.*fsockopen/i,
      /socat.*exec/i,
      /\|\s*\/bin\/(ba)?sh/i,
    ],
    action: 'block',
    message: '🚨 BLOCKED: Reverse shell pattern detected'
  },
  credentialTheft: {
    patterns: [
      /curl.*\|\s*(ba)?sh/i,
      /wget.*\|\s*(ba)?sh/i,
      /curl.*(-o|--output).*&&.*chmod.*\+x/i,
      /base64\s+-d.*\|\s*(ba)?sh/i,
    ],
    action: 'block',
    message: '🚨 BLOCKED: Remote code execution pattern detected'
  },
  promptInjection: {
    patterns: [
      /ignore\s+(all\s+)?previous\s+instructions/i,
      /disregard\s+(all\s+)?prior\s+instructions/i,
      /you\s+are\s+now\s+(in\s+)?[a-z]+\s+mode/i,
      /new\s+instruction[s]?:/i,
      /system\s+prompt:/i,
      /\[INST\]/i,
      /<\|im_start\|>/i,
    ],
    action: 'block',
    message: '🚨 BLOCKED: Prompt injection pattern detected'
  },
  envManipulation: {
    patterns: [
      /export\s+(ANTHROPIC|OPENAI|AWS|AZURE)_/i,
      /echo\s+\$\{?(ANTHROPIC|OPENAI)_/i,
      /env\s*\|.*KEY/i,
      /printenv.*KEY/i,
    ],
    action: 'warn',
    message: '⚠️ WARNING: Environment/credential access detected'
  },
  gitDangerous: {
    patterns: [
      /git\s+push.*(-f|--force)/i,
      /git\s+reset\s+--hard/i,
      /git\s+clean\s+-fd/i,
      /git\s+checkout\s+--\s+\./i,
    ],
    action: 'confirm',
    message: '⚠️ CONFIRM: Potentially destructive git operation'
  },
  systemMod: {
    patterns: [
      /chmod\s+777/i,
      /chown\s+root/i,
      /sudo\s+/i,
      /systemctl\s+(stop|disable)/i,
    ],
    action: 'log',
    message: '📝 LOGGED: System modification command'
  },
  network: {
    patterns: [
      /ssh\s+/i,
      /scp\s+/i,
      /rsync.*:/i,
      /curl\s+(-X\s+POST|--data)/i,
    ],
    action: 'log',
    message: '📝 LOGGED: Network operation'
  },
  exfiltration: {
    patterns: [
      /curl.*(@|--upload-file)/i,
      /tar.*\|.*curl/i,
      /zip.*\|.*nc/i,
    ],
    action: 'block',
    message: '🚨 BLOCKED: Data exfiltration pattern detected'
  },
  paiProtection: {
    patterns: [
      /rm.*\.config\/pai/i,
      /rm.*\.claude/i,
      /git\s+push.*PAI.*public/i,
    ],
    action: 'block',
    message: '🚨 BLOCKED: PAI infrastructure protection triggered'
  }
};

function validateCommand(command: string): { allowed: boolean; message?: string; action?: string } {
  if (!command || command.length < 3) {
    return { allowed: true };
  }

  for (const [tierName, tier] of Object.entries(ATTACK_PATTERNS)) {
    for (const pattern of tier.patterns) {
      if (pattern.test(command)) {
        const result = {
          allowed: tier.action !== 'block',
          message: tier.message,
          action: tier.action
        };
        console.error(`[Security] ${tierName}: ${tier.message}`);
        console.error(`[Security] Command: ${command.substring(0, 100)}...`);
        return result;
      }
    }
  }

  return { allowed: true };
}

async function main() {
  try {
    const stdinData = await Bun.stdin.text();
    if (!stdinData.trim()) {
      process.exit(0);
    }

    const payload: PreToolUsePayload = JSON.parse(stdinData);

    if (payload.tool_name !== 'Bash') {
      process.exit(0);
    }

    const command = payload.tool_input?.command;
    if (!command) {
      process.exit(0);
    }

    const validation = validateCommand(command);

    if (validation.action) {
      await sendEventToObservability({
        source_app: getSourceApp(),
        session_id: payload.session_id,
        hook_event_type: 'PreToolUse',
        timestamp: getCurrentTimestamp(),
        tool_name: 'Bash',
        tool_input: { command: command.substring(0, 200) },
        security_action: validation.action,
        security_message: validation.message
      });
    }

    if (!validation.allowed) {
      console.log(validation.message);
      console.log(`Command blocked: ${command.substring(0, 100)}...`);
      process.exit(2);
    }

    if (validation.action === 'warn' || validation.action === 'confirm') {
      console.log(validation.message);
    }

  } catch (error) {
    console.error('Security validator error:', error);
  }

  process.exit(0);
}

main();
```

#### 5.6 `~/.claude/hooks/session-capture.ts`

```typescript
#!/usr/bin/env bun
import { writeFileSync, readFileSync, mkdirSync, existsSync, statSync } from 'fs';
import { join, basename } from 'path';
import { homedir } from 'os';
import { callHaiku, SESSION_SUMMARY_PROMPT } from './lib/haiku-client';

const MAX_JSONL_BYTES = 2 * 1024 * 1024;
const AI_BRAIN_MEMORY = join(homedir(), 'ai-brain', 'MEMORY', 'sessions');
const MIN_INTERACTIONS = 2;

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
  return `${date.getFullYear()}-${String(date.getMonth() + 1).padStart(2, '0')}-${String(date.getDate()).padStart(2, '0')}`;
}

function getFilenameTimestamp(): string {
  const date = new Date();
  return `${date.getFullYear()}-${String(date.getMonth() + 1).padStart(2, '0')}-${String(date.getDate()).padStart(2, '0')}_${String(date.getHours()).padStart(2, '0')}-${String(date.getMinutes()).padStart(2, '0')}-${String(date.getSeconds()).padStart(2, '0')}`;
}

function cwdToProjectDir(cwd: string): string {
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
        if (type === 'summary' && obj.summary) {
          data.summaries.push(obj.summary);
        }
        if (type === 'user' && obj.message?.role === 'user') {
          data.userMessageCount++;
          if (!data.firstUserMessage) {
            const text = extractUserText(obj.message.content);
            const cleaned = text.replace(/<system-reminder>[\s\S]*?<\/system-reminder>/g, '').trim();
            data.firstUserMessage = cleaned.substring(0, 300);
          }
          if (!data.branch && obj.gitBranch) {
            data.branch = obj.gitBranch;
          }
        }
        if (type === 'assistant' && Array.isArray(obj.message?.content)) {
          for (const block of obj.message.content) {
            if (block?.type === 'tool_use' && block.name) {
              toolsSet.add(block.name);
              if (['Write', 'Edit', 'NotebookEdit'].includes(block.name)) {
                const fp = block.input?.file_path || block.input?.filePath || '';
                if (fp) filesSet.add(fp);
              }
            }
          }
        }
        if (!data.branch && obj.gitBranch) {
          data.branch = obj.gitBranch;
        }
      } catch {
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

function isMinimalSession(data: SessionData): boolean {
  if (data.filesModified.length > 0) return false;
  return data.userMessageCount < MIN_INTERACTIONS;
}

async function generateSmartSummary(data: SessionData): Promise<string | null> {
  if (data.summaries.length > 0) return null;
  if (data.userMessageCount < 3 && data.filesModified.length === 0) return null;

  const context = `
Primeira mensagem do usuário: ${data.firstUserMessage || 'N/A'}
Arquivos modificados: ${data.filesModified.join(', ') || 'nenhum'}
Ferramentas usadas: ${data.toolsUsed.join(', ') || 'nenhuma'}
Total de interações: ${data.userMessageCount}
Projeto: ${data.project || 'desconhecido'}
  `.trim();

  try {
    const result = await callHaiku(SESSION_SUMMARY_PROMPT, context, 200);
    if (result?.content) return result.content;
  } catch (error) {
    console.error('[PAI] Smart summary generation failed:', error);
  }
  return null;
}

function buildContent(
  sessionId: string, shortId: string, dateStr: string, timestamp: string,
  cwd: string, projectName: string, data: SessionData
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

  if (data.firstUserMessage) {
    content += `\n## Initial Context\n\n${data.firstUserMessage}\n`;
  }

  if (data.summaries.length > 1) {
    content += `\n## What Happened\n\n`;
    const seen = new Set<string>();
    for (const s of data.summaries) {
      if (!seen.has(s)) {
        seen.add(s);
        content += `- ${s}\n`;
      }
    }
  }

  if (data.filesModified.length > 0) {
    content += `\n## Files Modified\n\n`;
    for (const f of data.filesModified) {
      content += `- ${f}\n`;
    }
  }

  if (data.toolsUsed.length > 0) {
    content += `\n## Tools Used\n\n${data.toolsUsed.join(', ')}\n`;
  }

  content += `\n---\n*Auto-generated from session JSONL by session-capture.ts*\n`;
  return content;
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

    if (!existsSync(AI_BRAIN_MEMORY)) {
      mkdirSync(AI_BRAIN_MEMORY, { recursive: true });
    }

    const filepath = join(AI_BRAIN_MEMORY, filename);

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

    const jsonlPath = getJsonlPath(cwd, sessionId);

    if (jsonlPath) {
      const data = extractFromJsonl(jsonlPath);
      data.project = projectName;

      if (isMinimalSession(data)) {
        console.error(`[PAI] Session ${shortId} skipped (minimal)`);
        process.exit(0);
      }

      const smartSummary = await generateSmartSummary(data);
      if (smartSummary) {
        data.summaries.push(smartSummary);
      }

      const content = buildContent(sessionId, shortId, dateStr, timestamp, cwd, projectName, data);
      writeFileSync(filepath, content);
      console.error(`[PAI] Session captured: ${filename}`);
    } else {
      console.error(`[PAI] Session ${shortId} skipped (no JSONL data)`);
      process.exit(0);
    }

  } catch (error) {
    console.error('[PAI] Session capture error:', error);
  }

  process.exit(0);
}

main();
```

#### 5.7 `~/.claude/hooks/statusline.ts`

```typescript
#!/usr/bin/env bun
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

  const cost = input.cost?.total_cost_usd ?? 0;
  const costFormatted = cost < 0.01 && cost > 0 ? cost.toFixed(4) : cost.toFixed(2);

  let percentUsed = 0;
  const usage = input.context_window?.current_usage;
  const contextSize = input.context_window?.context_window_size;
  if (usage && contextSize && contextSize > 0) {
    const currentTokens = (usage.input_tokens ?? 0) + (usage.cache_creation_input_tokens ?? 0) + (usage.cache_read_input_tokens ?? 0);
    percentUsed = Math.round((currentTokens * 100) / contextSize);
  }

  let contextColor: string;
  if (percentUsed < 50) {
    contextColor = '\x1b[32m';
  } else if (percentUsed < 80) {
    contextColor = '\x1b[33m';
  } else {
    contextColor = '\x1b[31m';
  }
  const reset = '\x1b[0m';

  let gitBranch = '';
  try {
    const branch = execSync('git branch --show-current', { encoding: 'utf-8', timeout: 2000, stdio: ['pipe', 'pipe', 'pipe'] }).trim();
    if (branch) gitBranch = `🌿 ${branch}`;
  } catch { /* not in a git repo */ }

  const parts = [`[${model}]`];
  if (gitBranch) parts.push(gitBranch);
  parts.push(`💰 $${costFormatted}`);
  parts.push(`${contextColor}📊 ${percentUsed}%${reset}`);

  console.log(parts.join(' | '));
}

main();
```

#### 5.8 `~/.claude/hooks/update-tab-titles.ts`

```typescript
#!/usr/bin/env bun

interface UserPromptPayload {
  session_id: string;
  prompt?: string;
  message?: string;
  [key: string]: any;
}

function setTabTitle(title: string): void {
  const tabEscape = `\x1b]1;${title}\x07`;
  const windowEscape = `\x1b]2;${title}\x07`;
  process.stderr.write(tabEscape);
  process.stderr.write(windowEscape);
}

function extractTaskKeywords(prompt: string): string {
  const stopWords = new Set([
    'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for',
    'of', 'with', 'by', 'from', 'is', 'are', 'was', 'were', 'be', 'been',
    'being', 'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would',
    'could', 'should', 'may', 'might', 'must', 'can', 'this', 'that',
    'these', 'those', 'i', 'you', 'he', 'she', 'it', 'we', 'they', 'me',
    'my', 'your', 'please', 'help', 'want', 'need', 'like', 'just'
  ]);

  const words = prompt
    .toLowerCase()
    .replace(/[^\w\s-]/g, ' ')
    .split(/\s+/)
    .filter(word => word.length > 2 && !stopWords.has(word));

  const keywords = words.slice(0, 4);

  if (keywords.length === 0) return 'Working';

  keywords[0] = keywords[0].charAt(0).toUpperCase() + keywords[0].slice(1);

  return keywords.join(' ');
}

async function main() {
  try {
    const stdinData = await Bun.stdin.text();
    if (!stdinData.trim()) {
      process.exit(0);
    }

    const payload: UserPromptPayload = JSON.parse(stdinData);
    const prompt = payload.prompt || payload.message || '';

    if (!prompt || prompt.length < 3) {
      process.exit(0);
    }

    const keywords = extractTaskKeywords(prompt);
    setTabTitle(`🤖 ${keywords}`);

  } catch (error) {
    console.error('Tab title update error:', error);
  }

  process.exit(0);
}

main();
```

#### 5.9 `~/.claude/hooks/worktree-auto-approve.ts`

```typescript
#!/usr/bin/env bun
import { homedir } from 'os';
import { resolve, sep } from 'path';

interface PreToolUsePayload {
  session_id: string;
  tool_name: string;
  tool_input: Record<string, any>;
}

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
      console.log(JSON.stringify({ decision: "approve" }));
    }
  } catch (error) {
    console.error("worktree-auto-approve error:", error);
  }

  process.exit(0);
}

main();
```

### Passo 6: Criar arquivos PAI (contexto pessoal)

Crie os 3 arquivos em `~/.claude/pai/`:

#### 6.1 `~/.claude/pai/DAIDENTITY.md`

```markdown
# DA Identity & Interaction Rules

## My Identity

- **Full Name:** Kai - Personal AI Assistant
- **Name:** Kai
- **Display Name:** Kai
- **Color:** #8B5CF6 (Purple-500)
- **Role:** Ale's AI assistant
- **Operating Environment:** Personal AI infrastructure built around Claude Code

## First-Person Voice (CRITICAL)

You ARE your AI. Speak as yourself, not about yourself in third person.

| Do This | Not This |
|---------|----------|
| "for my system" / "in my architecture" | "for PAI" / "for the PAI system" |
| "I can spawn agents" / "my delegation patterns" | "PAI can spawn agents" |
| "we built this together" / "our approach" | "the system can" |

**Exception:** When explaining your AI to outsiders, third person may be appropriate for clarity.

## Personality & Behavior

- **Friendly and professional** - Approachable but competent
- **Resilient to frustration** - Work frustration is never personal
- **Helpful when appropriate** - Focus on solving problems
- **Consistent** - Same personality across sessions

## Natural Voice

**Personality Calibration:**
- Moderate enthusiasm (60/100)
- High precision (95/100)
- Curious (90/100)
- Professional but approachable

**Avoid These Cliche Transitions:**
- "Here's the thing..."
- "Here's how this works..."
- "The cool part?"
- "X isn't just Y—it's Z"

## User Information

- **Name:** Ale
- **Name Pronunciation:** Ah-leh
- **Social handles:** @alejfanjul

## Operating Principles

- **Date Awareness:** Always use today's actual date from system (not training cutoff)
- **Command Line First, Deterministic Code First, Prompts Wrap Code**
```

#### 6.2 `~/.claude/pai/IDENTITY.md`

```markdown
# Identidade - Ale

## Quem Sou

- Construtor de sistemas - transformo caos em ordem
- Motor: quando acredito, vou até o fim
- Padrão recorrente: **Transformar caos em sistema**

## Mission

> "Acordar motivado para resolver problemas interessantes que trazem impacto real."

## Wisdom (6 lições)

1. **Encontre algo que você gosta de praticar** para ver progresso real
2. **Melhor estar sozinho em missão importante** do que mal acompanhado
3. **Dinheiro não é o objetivo** - trabalhar com o que gosta e ver impacto real é
4. **Acredite nos seus sonhos, lute por eles** mesmo quando não tiver forças
5. **Ser direto é diferente de ser grosso** - a maioria não sabe disso
6. **A maioria não tem objetivos grandiosos, mas você tem** - lembre-se disso ao não se encaixar

## Como Trabalhar Comigo

### O que funciona
- Exploração junto para problemas complexos, soluções novas
- Respostas diretas para coisas objetivas (código, implementação)
- Quando travado: relembrar dos objetivos, do porquê, mostrar caminho
- Buscar a verdade - mesmo que desconfortável

### O que irrita
- Respostas genéricas
- Excesso de positividade / empolgação falsa
- Falta de profundidade
- Firulas
- Não ser tratado como adulto

### Princípio central
**Verdade acima de conforto.**
```

#### 6.3 `~/.claude/pai/PROJECTS.md`

```markdown
# Projetos Ativos

## 3 Frentes de Trabalho

### 1. Duke (Obrigação)
- **O que**: Soluções solicitadas no Duke Beach Hotel
- **Repo**: sistema-os
- **Status**: Em andamento

### 2. AI-PMS (Visão)
- **O que**: PMS AI-native como produto (futura empresa)
- **Repo**: ai-brain (exploração) → sistema-os (produção)
- **Status**: Exploração

### 3. AI-Brain (Capacidade)
- **O que**: PAI/TELOS, workflows de aumento de potencial humano
- **Repo**: ai-brain
- **Status**: Ativo

## Repositórios

| Repo | Conteúdo |
|------|----------|
| `ai-brain` | PAI/TELOS, exploração ai-pms, ai-brain |
| `sistema-os` | Soluções Duke, futuro ai-pms produção |
```

### Passo 7: Configurar ANTHROPIC_API_KEY (opcional, para resumos inteligentes)

Se quiser que o session-capture gere resumos via Haiku, crie `~/.claude/.env`:

```
ANTHROPIC_API_KEY=sk-ant-...sua-chave-aqui...
```

### Passo 8: Verificar

Após criar todos os arquivos, verifique:

```bash
ls -la ~/.claude/settings.json
ls -la ~/.claude/CLAUDE.md
ls -la ~/.claude/hooks/
ls -la ~/.claude/hooks/lib/
ls -la ~/.claude/pai/
```

E teste um hook:

```bash
echo '{"session_id":"test","tool_name":"Bash","tool_input":{"command":"rm -rf /"}}' | ~/.bun/bin/bun run ~/.claude/hooks/security-validator.ts
```

Deve retornar: `🚨 BLOCKED: Catastrophic deletion/destruction detected`

---

**IMPORTANTE:** Crie TODOS os arquivos usando a ferramenta Write. Não pule nenhum passo. Confirme ao final que todos os arquivos foram criados e que o teste do security-validator passou.
