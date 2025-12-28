# Capture Course

Captura conteúdo de cursos (Udemy, Coursera, etc) onde o usuário cola o transcript.

## Trigger

- `/capture course`
- "captura esse curso"
- "salva o transcript desse curso"

## Processo

Executar: `python3 scripts/capture_course.py`

O script vai perguntar interativamente:
1. Nome do curso
2. Autor/Instrutor
3. Plataforma
4. Número da seção
5. Título da seção
6. Transcript (colar e Enter 2x)

## Estrutura de Arquivo

Um arquivo por seção:
`YYYY-MM-DD-nome-do-curso-sX-titulo-secao.md`

## Exemplo

```
Nome do curso: AI-Powered Marketing
Autor: Seth Godin
Plataforma: Udemy
Número da seção: 2
Título da seção: Shifting our thinking about AI
[cola transcript]
```

Resultado: `2025-12-28-ai-powered-marketing-s2-shifting-our-thinking-about-ai.md`
