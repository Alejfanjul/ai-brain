---
name: Frontend
description: Frontend patterns for sistema-os (vanilla JS/HTML/CSS, no framework). USE WHEN writing page scripts, fixing UI bugs, modal issues, API calls from frontend, browser APIs, or localStorage.
---

# Frontend

Padroes de frontend para o sistema-os do Duke Beach Hotel. Vanilla JS sem framework. 7 regras extraidas de bugs reais.

## Rules

Antes de implementar qualquer pagina, componente, ou script frontend, ler `Rules.md` neste diretorio.

## Examples

**Example 1: Nova pagina**
```
User: "Criar pagina de listagem de produtos"
-> Le Rules.md
-> Aplica Rule 5 (normalizar resposta API)
-> Aplica Rule 7 (script non-module, sem type="module")
-> Gera HTML + JS seguindo padroes existentes
```

**Example 2: Bug em modal**
```
User: "Checkbox no modal nao funciona direito"
-> Le Rules.md
-> Verifica Rule 3 (event bubbling — usar onchange no checkbox, nao onclick no pai)
```

**Example 3: Integracao com API externa**
```
User: "Adicionar login com Google"
-> Le Rules.md
-> Aplica Rule 2 (debounce para callbacks externos)
-> Aplica Rule 4 (solicitar permissao do browser)
```
