# Query Workflow

Gera SQL correto para consultas no banco do sistema-os (Duke Beach Hotel).

## Steps

### 1. Carregar regras

Ler `Rules.md` (na raiz do skill). Aplicar TODAS as regras na query gerada.

### 2. Identificar tabelas e colunas

A partir do pedido do usuario:
- Identificar quais tabelas sao necessarias
- Consultar a quick reference no SKILL.md para colunas-chave e FKs
- Se houver duvida sobre nome exato de coluna ou tipo, consultar o schema:
  ```bash
  grep -A 30 "CREATE TABLE nome_tabela" ~/sistema-os/docs/schemas/supabase_full_schema_*.sql
  ```

### 3. Verificar enums envolvidos

Se a query filtra por status, tipo, categoria ou qualquer campo enum:
- Consultar `~/sistema-os/app/models/enums.py` para valores validos
- Usar SEMPRE o valor lowercase (ex: `'confirmada'`, nunca `'CONFIRMADA'`)

### 4. Gerar SQL

Montar a query respeitando:
- `WHERE deleted_at IS NULL` em TODAS as tabelas (Regra 3)
- Enum values SEMPRE lowercase (Regra 1)
- Nomes exatos de colunas conforme schema (Regra 2)
- IDs auto-increment — nao incluir em INSERTs (Regra 8)

### 5. Entregar

- Apresentar a query SQL formatada e pronta para uso
- Se o MCP Supabase estiver disponivel, oferecer executar direto
- Se executou, formatar resultado em tabela legivel

---

## Joins Comuns

### Hospede + Reservas
```sql
SELECT h.nome_completo, r.numero, r.status, r.checkin, r.checkout
FROM hospedes h
JOIN reserva_hospedes rh ON rh.hospede_id = h.id AND rh.deleted_at IS NULL
JOIN reservas r ON r.id = rh.reserva_id AND r.deleted_at IS NULL
WHERE h.deleted_at IS NULL;
```

### Reserva + Apartamentos
```sql
SELECT r.numero, r.status, a.numero AS apt_numero, a.categoria, ra.apartamento_principal
FROM reservas r
JOIN reserva_apartamentos ra ON ra.reserva_id = r.id AND ra.deleted_at IS NULL
JOIN apartamentos a ON a.id = ra.apartamento_id AND a.deleted_at IS NULL
WHERE r.deleted_at IS NULL;
```

### OS + Hospede + Itens + Produtos
```sql
SELECT os.numero, os.tipo, os.status, h.nome_completo,
       oi.quantidade, oi.valor_unitario, p.nome AS produto
FROM ordens_servico os
JOIN hospedes h ON h.id = os.hospede_id AND h.deleted_at IS NULL
JOIN os_itens oi ON oi.os_id = os.id AND oi.deleted_at IS NULL
JOIN produtos p ON p.id = oi.produto_id AND p.deleted_at IS NULL
WHERE os.deleted_at IS NULL;
```

### Conta + Hospede
```sql
SELECT c.id, c.tipo, c.status, c.valor_total, h.nome_completo
FROM contas c
JOIN hospedes h ON h.id = c.hospede_id AND h.deleted_at IS NULL
WHERE c.deleted_at IS NULL;
```

### Tarefas de uma OS
```sql
SELECT t.tipo, t.status, t.responsavel, t.apartamento, os.numero AS os_numero
FROM tarefas t
JOIN ordens_servico os ON os.id = t.os_id AND os.deleted_at IS NULL
WHERE t.deleted_at IS NULL;
```
