# AI Brain

Repositório de conhecimento para alimentar conversas com Claude.

## Propósito

Capturar conhecimento de diversas fontes (newsletters, vídeos, artigos, cursos) em formato que Claude possa acessar e usar para ajudar em projetos e decisões.

## Estrutura

```
ai-brain/
├── sources/          ← Conteúdo capturado (raw + metadata)
├── notes/            ← Minhas reflexões e conexões
├── TEMPLATE.md       ← Template para novas capturas
└── README.md
```

## Como usar

### Capturar novo conteúdo

1. Copiar `TEMPLATE.md` para `sources/`
2. Nomear: `YYYY-MM-DD-titulo-slug.md`
3. Preencher metadata e colar conteúdo
4. Commit

### Consultar

Perguntar ao Claude no projeto que tem este repo como Knowledge.

## Fontes frequentes

- **Nate's Newsletter** - técnicas de IA, agents, prompts
- **Seth Godin** - marketing, posicionamento, filosofia de negócios
- **Cursos** - RM, operações hoteleiras, etc.

## Princípios

- **Raw over polished**: conteúdo original > resumos elaborados
- **Capture fast**: não deixar para depois
- **Claude does the work**: classificação e conexões acontecem na consulta, não na captura