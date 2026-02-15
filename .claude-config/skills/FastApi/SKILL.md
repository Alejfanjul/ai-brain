---
name: FastApi
description: Backend patterns for sistema-os (FastAPI + SQLAlchemy). USE WHEN writing endpoints, fixing API bugs, WebSocket issues, Pydantic serialization, or scheduled scripts.
---

# FastApi

Padroes de backend para o sistema-os do Duke Beach Hotel. 7 regras extraidas de bugs reais em producao.

## Rules

Antes de implementar qualquer endpoint, WebSocket, ou script backend, ler `Rules.md` neste diretorio.

## Examples

**Example 1: Novo endpoint**
```
User: "Criar endpoint para listar OSs por departamento"
-> Le Rules.md
-> Aplica Rule 1 (retornar objeto completo com response_model)
-> Aplica Rule 2 (trailing slash para collection: /os/)
-> Gera endpoint seguindo padroes
```

**Example 2: Bug em WebSocket**
```
User: "WebSocket retorna 403 para admin"
-> Le Rules.md
-> Verifica Rule 3 (query params opcionais com fallback)
-> Verifica se departamento tem default para admin
```

**Example 3: Script agendado**
```
User: "Criar job de limpeza que roda via scheduler"
-> Le Rules.md
-> Aplica Rule 7 (nunca usar input(), detectar modo com sys.stdin.isatty())
-> Implementa com argumentos CLI ou valores padrao
```
