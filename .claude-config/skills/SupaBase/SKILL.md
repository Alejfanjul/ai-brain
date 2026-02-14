---
name: SupaBase
description: Database operations for sistema-os (Duke Beach Hotel). USE WHEN user asks for SQL query, database query, consulta no banco, quantas reservas, lista hospedes, cria migration, altera tabela, novo enum, schema change OR /supabase.
---

# SupaBase

Operacoes de banco de dados para o sistema-os do Duke Beach Hotel. Gera queries SQL corretas e migrations seguindo convencoes do projeto.

## Workflow Routing

| Workflow | Trigger | File |
|----------|---------|------|
| **Query** | Consultar dados, gerar SQL, "quantas reservas", "lista hospedes", "me da uma query" | `Workflows/Query.md` |
| **Migrate** | Criar migration, alterar tabela, novo enum, adicionar coluna, schema change | `Workflows/Migrate.md` |

## Examples

**Example 1: Consulta simples**
```
User: "Quantas reservas confirmadas temos para fevereiro?"
-> Invokes Query workflow
-> Le Rules.md e consulta schema
-> Gera SQL com WHERE deleted_at IS NULL e enum lowercase ('confirmada')
-> Entrega query pronta ou executa via MCP
```

**Example 2: Consulta com joins**
```
User: "Lista as OSs do hospede Joao com os itens e produtos"
-> Invokes Query workflow
-> Identifica join: hospedes -> ordens_servico -> os_itens -> produtos
-> Gera SQL com eager joins e soft delete em todas as tabelas
```

**Example 3: Nova migration**
```
User: "Preciso adicionar um campo 'observacoes' na tabela reservas"
-> Invokes Migrate workflow
-> Le Rules.md, consulta schema atual
-> Gera migration SQL idempotente em ~/sistema-os/scripts/migrations/
-> Atualiza model SQLAlchemy correspondente
```

## Quick Reference — Tabelas Principais

| Tabela | Colunas-chave | FK |
|--------|--------------|-----|
| `hospedes` | id, nome_completo, cpf (numero_documento), email, celular, status_cadastro | — |
| `reservas` | id, numero, status, checkin, checkout, plano_tarifario | — |
| `reserva_hospedes` | id, reserva_id, hospede_id, tipo_vinculo | reservas, hospedes |
| `reserva_apartamentos` | id, reserva_id, apartamento_id, apartamento_principal | reservas, apartamentos |
| `apartamentos` | id, numero, categoria, status | — |
| `ordens_servico` | id, numero, tipo, status, hospede_id, reserva_id, data_servico | hospedes, reservas |
| `os_itens` | id, os_id, produto_id, quantidade, valor_unitario | ordens_servico, produtos |
| `produtos` | id, nome, categoria, preco_venda, tipo | — |
| `contas` | id, hospede_id, reserva_id, status, tipo, valor_total | hospedes, reservas |
| `tarefas` | id, os_id, tipo, status, responsavel, apartamento | ordens_servico |
| `usuarios` | id, nome, email, nivel | — |

**Schema completo:** `~/sistema-os/docs/schemas/supabase_full_schema_*.sql`
**Enums:** `~/sistema-os/app/models/enums.py` (28 enums, TODOS lowercase)
