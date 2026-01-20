# AI Brain - Roadmap

> Última atualização: 2026-01-20 (Migração para modelo file-based)

## Visão geral dos Marcos

| Marco | Descrição | Status |
|-------|-----------|--------|
| 1 | Audit Trail | ✅ Concluído |
| 2 | Persistência de Conversas | ✅ Concluído |
| 3 | Memória Semântica | ⚡ Migrado para file-based |
| 4 | Proatividade | 📋 Futuro |
| 5 | Contexto Profundo (TELOS) | 🔄 Em progresso |

---

## Marco 1: Audit Trail ✅

**Objetivo:** Registrar tudo automaticamente via hooks.

**Resultado:**
- Hooks do Claude Code configurados
- Toda interação salva

---

## Marco 2: Persistência de Conversas ✅

**Objetivo:** Manter histórico completo de conversas.

**Resultado:**
- Sessões salvas em MEMORY/sessions/
- Session ID para continuar conversas

---

## Marco 3: Memória Semântica ⚡ MIGRADO

**Status anterior:** Sistema baseado em Supabase + embeddings + pgvector.

**Migração (2026-01-20):** Substituído por modelo file-based (PAI-style).

### Por que migrar

| Antes (Supabase) | Depois (File-based) |
|------------------|---------------------|
| Requer scripts externos para busca | Claude lê nativamente |
| Embeddings exigem processamento | Sem processamento |
| Infraestrutura externa | Zero infraestrutura |
| Cron jobs para manter atualizado | Hooks simples |

### Nova arquitetura

```
MEMORY/
├── sessions/     → Captura automática via hook
├── decisions/    → Decisões importantes
├── learnings/    → Aprendizados por fase (OBSERVE/THINK/PLAN/BUILD/EXECUTE/VERIFY)
├── State/        → Estado ativo
└── Signals/      → Padrões e falhas
```

### Backup do sistema anterior

Arquivos do sistema Supabase/embeddings salvos em:
```
~/ai-brain-backup-YYYYMMDD/
```

---

## Marco 4: Proatividade 📋

**Objetivo:** Sistema que trabalha proativamente, não só quando acionado.

**Features planejadas:**
- Morning overview automático
- Acompanhamento de projetos (perguntar evolução)
- Detecção de padrões → sugestão de automações
- Weekly review automática

---

## Marco 5: Contexto Profundo (TELOS) 🔄

**Objetivo:** Dar contexto profundo para a IA sobre quem sou e o que quero.

> "Once the AI sees everything—purpose, goals, challenges, strategies, KPIs—now we can start asking questions." - Daniel Miessler

### Fases

| Fase | Descrição | Status |
|------|-----------|--------|
| 5.1 | TELOS pessoal (Ale) | ✅ Concluído |
| 5.2 | TELOS hotel (Duke Beach) | 📋 Pendente |
| 5.3 | Patterns FABRIC validados | 📋 Pendente |
| 5.4 | Skills estruturados | 📋 Pendente |

### Fase 5.1: TELOS Pessoal ✅

**Resultado:**
- ✅ Conversas 01-03 realizadas (Propósito, Camada profunda, Pilares)
- ✅ `telos/TELOS-ALE.md` consolidado (2026-01-17)
- ✅ Guias de patterns criados (`guides/`)

**Documentos:**
- `telos/TELOS-ALE.md` - TELOS pessoal consolidado
- `guides/FABRIC-ALL-PATTERNS.md` - 234 patterns disponíveis
- `guides/FABRIC-TELOS-PATTERNS.md` - 16 patterns para manutenção do TELOS

### Fase 5.2: TELOS Hotel 📋

**Objetivo:** Criar contexto profundo do Duke Beach Hotel.

**Entregável:**
- [ ] `telos/TELOS-HOTEL.md`
- [ ] Missão, metas, KPIs, desafios sazonais, perfil de hóspedes

### Fase 5.3: Patterns FABRIC 📋

**Objetivo:** Validar patterns resolvendo problemas reais.

> "Só automatize o que já validou manualmente"

**Entregável:**
- [ ] 3-5 patterns testados no dia a dia
- [ ] 1 pattern customizado para o hotel

### Fase 5.4: Skills Estruturados 📋

**Objetivo:** Transformar patterns validados em skills do PAI.

**Entregável:**
- [ ] Primeiro skill (ex: HotelOperations)
- [ ] 1 workflow funcional
- [ ] 1 tool em TypeScript

---

## Decisões técnicas

### Princípio fundamental
> "Não quero me distanciar de modelos de ponta. Quero que meu app incorpore novas funcionalidades rapidamente."

**Implicações:**
- Sem frameworks intermediários (LangChain, CrewAI)
- Claude Code CLI direto
- Código próprio para controle total
- **File-based > Embeddings externos** (Claude já lê arquivos nativamente)

### Validação externa
Alex Hillman (JFDI System), Nate (Second Brain 2026) e Daniel Miessler (PAI) construíram sistemas muito similares. Ver [REFERENCES.md](./REFERENCES.md).

---

## Fases Futuras (pós-migração)

- Hook de extração de learnings (classifica por fase automaticamente)
- Busca local em MEMORY/ (grep-based ou fzf)
- Cleanup automático de sessions antigas (rolling 90 dias)
- Integração com extractwisdom do Fabric para sources/
