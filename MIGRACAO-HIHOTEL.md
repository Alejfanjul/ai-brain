# Migração ai-brain ↔ HiHotel — Painel de Trabalho

**Criado:** 2026-04-17
**Status:** Fase 1 concluída (Cat 3 em exceção) · Fase 2 concluída · próxima: Fase 3

## Regras combinadas

- **Objetivo:** zero duplicidade entre `ai-brain` e `HiHotel`. Cada arquivo mora num lugar só.
- **Crivo de lixo (Fase 1 e 2):** A1 (inequivocamente morto) + A2 (nunca usado). A3 (obsoleto mas teve valor) **não** é lixo — vai pra Fase 3 decidir se sintetiza/migra/descarta.
- **Política de deleção:** hard delete (`git rm`). História fica no git.
- **Aprovação:** por categoria, com commit por categoria aprovada.
- **Status na coluna "Decisão":** ⬜ pendente / ✅ aprovado / ⚠️ exceção (mantém com motivo).

## Fases

| Fase | Escopo | Estado |
|---|---|---|
| 1 | Lixo do `ai-brain` | 🟢 Cat 1, 2, 4 executadas (8 arquivos + edit README). Cat 3 em exceção. |
| 2 | Lixo do `HiHotel` | 🟢 concluída — 1 arquivo deletado + 2 TIPs criados |
| 3 | Estratégia de migração (original × síntese × fragmento) | ⚪ a fazer |
| 4 | Executar migração | ⚪ a fazer |

---

# Fase 1 — Lixo do `ai-brain`

## Categoria 1 — Arquivos soltos por acidente (A1)

Arquivos criados por engano no shell (nomes suspeitos, conteúdo irrelevante).

| Arquivo | Motivo | Decisão |
|---|---|---|
| `=0.18` | Output de `pip install "ebooklib>=0.18"` sem aspas. 794B de texto de instalação. | ✅ |

## Categoria 2 — HTMLs duplicados de `.md` (A1)

Exportados HTML de documentos cuja versão `.md` é canônica.

| Arquivo | Motivo | Decisão |
|---|---|---|
| `projects/hihotel/proposta/2026-04-12-proposta-hihotel-duke-v2.html` | Duplicata HTML do `.md` irmão. | ✅ |
| `projects/hihotel/proposta/2026-04-12-changelog-v1-v2.html` | Duplicata HTML do `.md` irmão. | ✅ |
| `projects/hihotel/proposta/2026-04-02-proposta-hihotel-duke.html` | HTML de versão v1 já superada. | ✅ |

## Categoria 3 — Versões superadas (A1)

Documentos substituídos por versão posterior que já existe em outro lugar.

| Arquivo | Superado por | Decisão |
|---|---|---|
| `projects/hihotel/proposta/proposta-hihotel-duke.md` | `proposta/2026-04-12-proposta-hihotel-duke-v2.md` (e hoje pela proposta-vigente em HiHotel). | ⚠️ | Tendo em vista que ainda temos que fazer a proposta final, acho valido manter o arquivo
| `projects/hihotel/proposta/2026-04-12-proposta-hihotel-duke-v2.md` | `HiHotel/clientes/duke/proposta-vigente.md` — versão mais nova, tem seção "Transição de TI". | ⚠️ | Tendo em vista que ainda temos que fazer a proposta final, acho valido manter o arquivo

## Categoria 4 — Templates nunca seguidos (A2)

Templates prescritivos que nenhum projeto adotou (verificado via grep nos READMEs de projetos reais).

| Arquivo | Motivo | Decisão |
|---|---|---|
| `templates/PROJECT-DEFINITION.md` | Nenhum projeto usa a seção `## Estágio: Definição`. | ✅ |
| `templates/PROJECT-EXPLORATION.md` | Idem — `## Estágio: Exploração`. | ✅ |
| `templates/PROJECT-EXECUTION.md` | Idem — `## Estágio: Execução`. | ✅ |
| `templates/CAPTURE-MANUAL.md` | Captura hoje é via skills (`/capture-*`); template manual redundante. | ✅ |

**Ação complementar:** ajustar `README.md` (raiz) removendo as linhas 11 e 81 que referenciam esses templates. --> OTIMO!

**Exceção conhecida:** `templates/patterns/interview_process/` **não** entra aqui. É A2 (nunca testado) mas tem valor de migração pro HiHotel → vai pra Fase 3.

---

# Itens fora do crivo (vão pra Fase 3, não Fase 1)

Por coerência com a regra A1+A2 (e não A3), estes **não** são lixo — são conteúdo que teve valor pontual e merecem decisão consciente de síntese/migração/descarte:

- `projects/hihotel/proposta/memoria-claude.md` — memória de sessão de março/2026
- `projects/hihotel/proposta/2026-04-09-notas-hihotel.txt` — notas soltas
- `projects/hihotel/proposta/roteiro-conversa-heiko.md` + `roteiro-conversa-heiko-v2.md` — roteiros de conversa já ocorrida
- `projects/hihotel/proposta/estrutura-apresentacao-gestores.md` — apresentação pontual
- `projects/hihotel/proposta/2026-04-08-feedback-heijo-hihotel0chatgpt-original.md` — feedback bruto (typo no nome)
- `projects/hihotel/proposta/2026-04-08-feedback-heiko-hihotel-chatgpt.md` — feedback processado
- `projects/hihotel/proposta/2026-03-17-apresentacao-inicial-heiko-diego.html` — apresentação histórica
- `projects/hihotel/proposta/rascunho-contexto.md` — contexto da gênese da empresa
- `projects/hihotel/proposta/hotel_blueprint.png` + `mapa_virtual_hotel.png` — imagens (verificar uso)
- `projects/hihotel/genese-visao-dez2024.md` — visão original dez/2024
- `projects/hihotel/plano-estudo-fundamentos.md` + `artefatos/*` — estudo pessoal (provável "fica no ai-brain")
- `cloud-setup-instructions.md` (40KB na raiz) — guia de setup já executado; zero referências externas, mas é A3
- `projects/hihotel/quadro-estrutura-prioridades-2026-04-16.md` — duplicado da nota em HiHotel (foi criado hoje nesta sessão)

---

# Fora de escopo (fica no ai-brain sem discussão)

Projetos/pastas que não têm relação com HiHotel:

- `projects/ai-brain/` (meta-projeto PAI)
- `projects/ai-brand/` (marca pessoal)
- `projects/fitness-coach/`
- `projects/moonlight-sunshine/`
- `projects/speech-to-text/`
- `MEMORY/`, `pai/`, `scripts/`, `tools/`, `sources/`, `.github/`, `.claude-config/`, `.claude/`
- Arquivos-raiz de configuração: `.gitignore`, `requirements.txt`, `CLAUDE.md`, `README.md`

Podem virar candidatos a lixo em futuros passes, mas hoje estão vivos.

---

# Log de execução — Fase 1

| Data | Categoria | Commit | Itens |
|---|---|---|---|
| 2026-04-17 | Cat 1 — Arquivos soltos | `4012c06` | 1 arquivo (`=0.18`) |
| 2026-04-17 | Cat 2 — HTMLs duplicados | `dde0972` | 3 arquivos |
| 2026-04-17 | Cat 4 — Templates + README | `071b308` | 4 arquivos + edit README |
| — | Cat 3 — Versões superadas | — | ⚠️ exceção: manter como referência pra próxima proposta (reavaliar em Fase 4, possivelmente mover pra `HiHotel/clientes/duke/historico/`) |

# Log de execução — Fase 2

Varredura do HiHotel praticamente zero lixo (repo disciplinado).

| Data | Ação | Commit (HiHotel) | Detalhe |
|---|---|---|---|
| 2026-04-17 | Deletar `.gitkeep` órfão em `notas/` | `fb41f63` | Pasta já tem conteúdo real |
| 2026-04-17 | Criar 2 TIPs (tipo ideia) | `29639e8` | `2026-04-17-avaliar-condensacao-identidade.md`, `2026-04-17-consolidar-claude-readme-overlap.md` |
