# AI Brain - Contexto para Claude

Este é um hub central de conhecimento e projetos pessoais.

## Estrutura

```
ai-brain/
├── sources/           ← Conhecimento capturado
├── projects/          ← Projetos em andamento
├── templates/         ← Templates
├── scripts/           ← Scripts de captura
└── CONTEXT.md         ← Guia de autores
```

## Como trabalhar

Ao iniciar uma conversa:
1. Ler `CONTEXT.md` para entender os autores e seus domínios
2. Se for sobre um projeto, ler o `README.md` do projeto
3. Identificar o estágio (Exploração, Definição, Execução)
4. Adaptar abordagem conforme o estágio

Ao finalizar uma conversa produtiva:
1. Atualizar o `README.md` do projeto se houve decisões
2. Adicionar entrada no Histórico com data e mudança

## Comandos de Captura

| Comando | Script |
|---------|--------|
| /capture youtube <url> | python3 scripts/capture_youtube.py |
| /capture playlist <url> | python3 scripts/capture_playlist.py |
| /capture article <url> | python3 scripts/capture_article.py |
| /capture epub <file> | python3 scripts/capture_epub.py |
| /capture course | python3 scripts/capture_course.py |
| /capture manual | Usar template templates/CAPTURE-MANUAL.md |

## Criar novo projeto

```bash
cp templates/PROJECT-EXPLORATION.md projects/nome-do-projeto/README.md
```

## Guia rápido de autores

- **Direção/Marketing** → Seth Godin
- **Filosofia/Clareza** → Derek Sivers
- **IA/Execução** → Nate
- **Emocional/Bloqueios** → Joe Hudson
- **Marca pessoal** → Bruno Perini

## Usuário

- **Nome:** Ale
- **Contexto:** Construindo empresa de uma pessoa só, baseada em IA
- **Trabalha em:** Duke Beach Hotel (liberdade para criar soluções)
- **Objetivo:** Sistemas que mostrem que "trabalho pode ser bacana"
