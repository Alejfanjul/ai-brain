# Interview Process Pattern

Pattern para documentar processos operacionais através de entrevistas com funcionários.

## Conceito

Diferente de patterns de extração (como `extract_wisdom`), este é um pattern de **entrevista ativa**:

- O funcionário narra o processo (áudio ou texto)
- A IA identifica gaps no PROCESS SCHEMA
- A IA faz perguntas específicas para completar
- No final, gera documentação em 4 formatos

## Uso Direto (CLI)

```bash
# Com arquivo de áudio transcrito
cat transcricao.txt | fabric -p interview_process

# Interativo (se o modelo suportar)
fabric -p interview_process --stream
```

## Uso via Telegram Bot (planejado)

```
Funcionário: [envia áudio]
Bot: [transcreve com Whisper]
Bot: [processa com este pattern]
Bot: [responde com perguntas ou documentação final]
```

## Schema de Processo

Todo processo documentado terá:

| Elemento | Pergunta-chave |
|----------|---------------|
| Trigger | O que inicia? |
| Pré-requisitos | O que precisa antes? |
| Passos | Como faz? |
| Decisões | E se X? |
| Exceções | O que pode dar errado? |
| Handoff | Para onde vai depois? |
| Ferramentas | O que usa? |
| Métricas | Como saber se deu certo? |

## Outputs Gerados

1. **SOP** - Documento formal completo
2. **Checklist** - Lista para uso diário
3. **FAQ** - Perguntas de funcionário novo
4. **Ficha Resumo** - Referência rápida (1 página)

## Exemplo de Conversa

Ver `example_conversation.md`

## Próximos Passos

- [ ] Criar bot Telegram
- [ ] Integrar Whisper para transcrição
- [ ] Testar com processo real (check-in)
- [ ] Iterar no pattern baseado em feedback
