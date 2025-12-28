# AI Brain

Repositório de conhecimento para alimentar conversas com Claude.

## Propósito

Capturar conhecimento de diversas fontes (newsletters, vídeos, artigos, cursos) em formato que Claude possa acessar e usar para ajudar em projetos e decisões.

## Estrutura

```
ai-brain/
├── sources/          ← Conteúdo capturado (raw + metadata)
├── scripts/          ← Scripts de captura automática
│   ├── capture_youtube.py
│   ├── capture_article.py
│   └── email_capture.py
├── notes/            ← Minhas reflexões e conexões
├── TEMPLATE.md       ← Template para capturas manuais
└── README.md
```

## Dependências

Os scripts de captura automática requerem:

```bash
pip install -r requirements.txt
```

**Incluído:**
- `yt-dlp` - Download de vídeos/transcrições YouTube
- `requests`, `beautifulsoup4`, `markdownify` - Extração de artigos web

## Como usar

### Captura Automática

#### YouTube

```bash
python3 scripts/capture_youtube.py <URL>
```

**Exemplo:**
```bash
python3 scripts/capture_youtube.py "https://www.youtube.com/watch?v=..."
```

**O que faz:**
- Extrai metadata do vídeo (título, canal, duração)
- **Detecta automaticamente o idioma original do vídeo**
- Baixa transcript/legendas no idioma original (melhor qualidade)
- Funciona com qualquer idioma (fallback para inglês se necessário)
- Cria arquivo em `sources/` com nome `YYYY-MM-DD-titulo.md`
- Faz commit automático

#### Artigo/Blog/Newsletter

```bash
python3 scripts/capture_article.py <URL>
```

**Exemplo:**
```bash
python3 scripts/capture_article.py "https://seths.blog/..."
```

**O que faz:**
- Extrai título e autor
- Converte conteúdo HTML para Markdown
- Cria arquivo em `sources/`
- Faz commit automático

### Captura Manual (Interativa)

Usar a skill Claude:

```
/capture manual
```

**Fluxo guiado que:**
- Pergunta título, tipo, autor, URL
- Pede para colar conteúdo
- Cria arquivo e commit automático

### Captura Manual (TEMPLATE)

Quando os scripts não funcionam ou para conteúdo copiado:

1. Copiar `TEMPLATE.md` para `sources/`
2. Nomear: `YYYY-MM-DD-titulo-slug.md`
3. Preencher metadata e colar conteúdo
4. Commit manual

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