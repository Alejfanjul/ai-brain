# Regras de Frontend — Sistema OS

7 regras extraidas de bugs reais no `~/sistema-os/docs/LEARNINGS.md`. Seguir ao implementar paginas, componentes, e scripts.

---

## 1. Template literals: sempre com parenteses

Chamadas de funcao com template literals exigem parenteses.

```javascript
// ERRADO — tagged template literal, nao chamada de funcao
await api.post`/tarefas/${id}/iniciar`, {}

// CORRETO — parenteses envolvendo template literal
await api.post(`/tarefas/${id}/iniciar`, {})
```

---

## 2. Debounce para callbacks de terceiros

APIs externas (Google OAuth, Stripe, etc) podem chamar callbacks multiplas vezes. Usar flag de protecao.

```javascript
let isAuthenticating = false;

async function handleCredentialResponse(response) {
    if (isAuthenticating) {
        console.log('Ignorando callback duplicado');
        return;
    }
    isAuthenticating = true;

    try {
        // ... logica de login
    } finally {
        isAuthenticating = false;
    }
}
```

---

## 3. Event bubbling: checkbox dentro de container

Checkbox dentro de div com onclick causa evento duplo. Usar onchange no checkbox.

```html
<!-- ERRADO — evento dispara 2x -->
<div onclick="toggle()">
  <input type="checkbox" />
</div>

<!-- CORRETO — evento unico -->
<div>
  <input type="checkbox" onchange="toggle()" />
</div>
```

---

## 4. Solicitar permissao do browser antes de usar APIs

APIs do browser (Notification, Geolocation, Camera) exigem permissao explicita.

```javascript
// ERRADO — permissao nunca solicitada, Notification.permission === 'default'
function showNotification(title, body) {
    if (Notification.permission === 'granted') {
        new Notification(title, { body });
    }
}

// CORRETO — solicitar ao conectar/inicializar
function init() {
    if ('Notification' in window && Notification.permission === 'default') {
        Notification.requestPermission();
    }
}
```

Checklist:
1. Verificar se API existe (`'Notification' in window`)
2. Verificar permissao atual
3. Solicitar permissao ANTES de usar

---

## 5. Normalizar resposta da API

Backend pode retornar array direto ou objeto com array. Sempre normalizar.

```javascript
// Backend inconsistente:
// GET /tarefas/ -> [{...}, {...}]
// GET /os/      -> {ordens: [{...}], total: 5}

// CORRETO — normalizar no frontend
const data = await api.get('/tarefas/');
const tarefas = data.tarefas || data || [];
```

---

## 6. localStorage: objeto unico JSON

Usar um unico objeto JSON no localStorage. Limpar apos mudancas estruturais.

```javascript
// ERRADO — multiplas chaves
localStorage.setItem('user_name', name);
localStorage.setItem('user_departamento', depto);

// CORRETO — objeto unico
localStorage.setItem('user', JSON.stringify({
    id, email, nome_completo, nivel, departamentos
}));

// Ao ler, validar estrutura
const user = JSON.parse(localStorage.getItem('user') || '{}');
if (!user.id) { /* redirect to login */ }
```

---

## 7. Scripts de pagina sao non-module

No sistema-os, scripts de pagina usam `<script>` sem `type="module"`. O unico modulo ES6 e `api.js`.

```html
<!-- CORRETO — script de pagina -->
<script src="/js/pages/os.js"></script>

<!-- api.js e o unico module -->
<script type="module" src="/js/api.js"></script>
```

Cada pagina tem sua propria copia de utilitarios (escapeHtml, API_URL, etc). Nao importar de outros scripts de pagina.
