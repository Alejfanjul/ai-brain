# Setup PAI na Máquina do Trabalho

> Cole este conteúdo no Claude Code da máquina do trabalho.
> O Claude vai executar o setup automaticamente.

---

## Instruções para o Claude

Preciso que você configure o PAI (Personal AI Infrastructure) nesta máquina.

**Passos:**

1. Verifique se o repo ai-brain existe em `~/ai-brain`:
   ```bash
   ls ~/ai-brain/pai/
   ```

2. Se não existir, clone:
   ```bash
   git clone https://github.com/alejandrofjl/ai-brain.git ~/ai-brain
   ```

3. Se já existir, faça pull:
   ```bash
   cd ~/ai-brain && git pull
   ```

4. Execute o script de setup:
   ```bash
   cd ~/ai-brain && ./scripts/setup-pai.sh
   ```

5. Verifique se os symlinks foram criados:
   ```bash
   ls -la ~/.claude/pai/
   ls -la ~/.claude/hooks/load-core-context.ts
   ```

6. Teste o contexto (você vai precisar reiniciar o Claude Code depois):
   ```bash
   echo '{"session_id": "test"}' | bun ~/.claude/hooks/load-core-context.ts 2>&1 | tail -5
   ```

**Resultado esperado:** Deve mostrar "PAI Context loaded (IDENTITY + PROJECTS)"

---

## Após o Setup

Reinicie o Claude Code. Na próxima sessão, ao perguntar "quais são minhas 3 frentes de trabalho?", deve responder:
1. Duke (Obrigação)
2. AI-PMS (Visão)
3. AI-Brain (Capacidade)

---

## Troubleshooting

**Se Bun não estiver instalado:**
```bash
curl -fsSL https://bun.sh/install | bash
```

**Se o path do ai-brain for diferente de ~/ai-brain:**
```bash
export AI_BRAIN_PATH=/path/to/ai-brain
```
