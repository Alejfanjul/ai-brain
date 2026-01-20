# Fitness Coach

> **Meta:** Perder 4-6kg de gordura mantendo força. Coach pessoal baseado em dados.

---

## Por que este projeto

- Gordura abdominal incomoda (escondendo definição)
- Treino de força já está consistente (5/3/1)
- Falta visibilidade do progresso real
- Preciso de accountability nos dados

---

## O que o Coach faz

### Tracking
- **Peso**: Tendência semanal (não o número diário)
- **Gordura**: Tendência via bioimpedância + fotos
- **Treino**: Wendler (CSV) + Corrida (manual) + Metcons (manual)

### Análise
- Dashboard com métricas principais
- Comparação de fotos (visual progress)
- Alertas de inconsistência

### Coaching
- Feedback baseado em dados
- Ajustes sugeridos (déficit, cardio, etc.)

---

## Fontes de dados

| Dado | Fonte | Input |
|------|-------|-------|
| Peso/Gordura | Balança bioimpedância | Manual (diário/semanal) |
| Fotos | Câmera celular | Upload semanal |
| Wendler | App Five3One | CSV export |
| Corrida | Strava | Copy/paste manual |
| Metcons | - | Descrição manual |

---

## Estrutura

```
fitness-coach/
├── README.md           ← Este arquivo
├── ROADMAP.md          ← Fases de implementação
├── data/
│   ├── weight.csv      ← Log peso/gordura
│   ├── cardio.csv      ← Corridas + metcons
│   ├── wendler.csv     ← Export do Five3One
│   └── photos/         ← Fotos de progresso
└── scripts/
    └── coach.py        ← Dashboard principal
```

---

## Princípios

1. **Dados > Sensação** - Decisões baseadas em tendências, não em como me sinto
2. **Simples > Completo** - Mínimo viável que funciona
3. **Tendência > Número** - Média semanal importa, dia a dia não
4. **Consistência > Perfeição** - Melhor dado imperfeito que nenhum dado

---

## Links

- Metas de saúde: `projects/ai-brain/metas/SAUDE.md`
- Histórico Wendler: `data/wendler.csv` (export Five3One)
