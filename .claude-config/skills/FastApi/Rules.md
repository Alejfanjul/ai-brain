# Regras de Backend — Sistema OS

7 regras extraidas de bugs reais no `~/sistema-os/docs/LEARNINGS.md`. Seguir ao implementar endpoints, WebSockets, e scripts.

---

## 1. Retornar objeto completo quando response_model definido

Endpoint com `response_model` deve retornar o objeto completo, nao apenas o ID.

```python
# ERRADO — FastAPI tenta serializar int como objeto
@router.post("/os/", response_model=OSResponse)
async def criar_os(...):
    os_id = await service.criar(data)
    return os_id  # Erro de validacao!

# CORRETO — buscar objeto completo apos criar
@router.post("/os/", response_model=OSResponse)
async def criar_os(...):
    os_id = await service.criar(data)
    os_criada = await service.buscar(os_id)
    return os_criada
```

---

## 2. Trailing slash: padrao de URLs

FastAPI tem comportamento nao-obvio com trailing slash.

```python
# Collections (lista): COM trailing slash
GET /api/v1/tarefas/     # 200 OK
GET /api/v1/tarefas      # 404 Not Found

# Items (detalhe): SEM trailing slash
GET /api/v1/tarefas/1    # 200 OK
GET /api/v1/tarefas/1/   # 307 Redirect

# Actions: SEM trailing slash
POST /api/v1/tarefas/1/iniciar    # 200 OK
POST /api/v1/tarefas/1/iniciar/   # 307 Redirect
```

---

## 3. WebSocket query params opcionais com fallback

Query params em WebSocket devem ser opcionais. Usar `Query(None)` com fallback.

```python
# ERRADO — obrigatorio, retorna 403 se ausente
@router.websocket("/ws")
async def websocket(ws: WebSocket, departamento: str = Query(...)):
    ...

# CORRETO — opcional com fallback
@router.websocket("/ws")
async def websocket(ws: WebSocket, departamento: str = Query(None)):
    dept = departamento or 'admin'
    ...
```

Frontend deve sempre enviar valor:
```javascript
const dept = user.nivel === 'admin' ? 'admin' : user.departamentos[0];
const url = `${WS_URL}?departamento=${dept}`;
```

---

## 4. Refresh apos UPDATE

SQLAlchemy mantem objeto em cache. Apos UPDATE, fazer refresh ou re-query.

```python
# ERRADO — retorna dados em cache
await db.execute(update(OS).where(OS.id == id).values(status='confirmada'))
await db.commit()
return os_obj  # Dados antigos!

# CORRETO — refresh apos commit
await db.execute(update(OS).where(OS.id == id).values(status='confirmada'))
await db.commit()
await db.refresh(os_obj)
return os_obj
```

---

## 5. Pydantic para JSON: model_dump(mode='json')

`model_dump()` nao converte datetime para string. Usar `mode='json'`.

```python
# ERRADO — "Object of type datetime is not JSON serializable"
await manager.enviar(dept, notif.model_dump())

# CORRETO — serializa datetime como string ISO
await manager.enviar(dept, notif.model_dump(mode='json'))
```

---

## 6. Cancelamento em cascata: transacao atomica

Operacoes destrutivas que afetam multiplos registros devem ser transacionais.

```python
# CORRETO — tudo ou nada
async with db.begin():
    # Cancelar tarefas
    await db.execute(update(Tarefa).where(...).values(status='cancelada'))
    # Cancelar OS
    await db.execute(update(OS).where(...).values(status='cancelada'))
    # Commit automatico ou rollback em caso de erro
```

UI deve solicitar confirmacao explicita do impacto antes de executar.

---

## 7. Scripts agendados: nunca usar input()

Scripts executados via scheduler/cron nao tem terminal. `input()` trava o processo indefinidamente.

```python
# ERRADO — bloqueia quando nao ha terminal
response = input("Deseja retomar? [s/N]: ")

# CORRETO — detectar modo de execucao
if not sys.stdin.isatty():
    # Modo nao-interativo: tomar decisao automatica
    resuming = True
else:
    # Modo interativo: pode perguntar
    response = input("Deseja retomar? [s/N]: ")
```

Alternativas: argumentos CLI (`--yes`, `--resume`) ou valor padrao seguro.
