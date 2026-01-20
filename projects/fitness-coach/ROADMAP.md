# Fitness Coach - Roadmap

## Fase 1: Fundação (MVP)
> Visibilidade básica - "estou no caminho certo?"

### 1.1 Estrutura de dados
- [x] Criar estrutura do projeto
- [x] Definir formato weight.csv
- [x] Definir formato cardio.csv
- [x] Importar wendler.csv (Five3One export)

### 1.2 Dashboard básico
- [x] Mostrar peso atual vs média semanal
- [x] Mostrar tendência de peso (subindo/descendo/estável)
- [x] Mostrar frequência de treino (Wendler + Cardio)
- [x] Output ASCII (como Daily Goals)

### 1.3 Input simples
- [x] Comando para registrar peso: `python3 coach.py log-weight 81.5`
- [x] Comando para registrar cardio: `python3 coach.py log-cardio "5km 31min corrida"`
- [x] Comando para registrar metcon: `python3 coach.py log-metcon "AMRAP 15min burpees+kb"`

**Entrega:** `python3 coach.py` mostra dashboard com tendências ✅

---

## Fase 2: Análise visual
> Progresso que você VÊ

### 2.1 Sistema de fotos
- [ ] Estrutura para fotos semanais (data no nome)
- [ ] Comando para comparar fotos lado a lado
- [ ] Análise via Claude Vision (qualitativo)

### 2.2 % Gordura
- [ ] Adicionar coluna gordura no weight.csv
- [ ] Mostrar tendência de gordura (com disclaimer de imprecisão)
- [ ] Correlacionar com fotos

**Entrega:** Comparação visual semanal + tendência de composição

---

## Fase 3: Coaching inteligente
> Feedback e sugestões

### 3.1 Alertas
- [ ] Peso subindo por 2+ semanas → alerta
- [ ] Cardio < 2x/semana → alerta
- [ ] Gap > 5 dias no Wendler → alerta

### 3.2 Sugestões
- [ ] Baseado em dados, sugerir ajustes
- [ ] "Peso estável há 3 semanas, considere aumentar cardio ou reduzir calorias"
- [ ] "Ótima consistência no Wendler, força mantida"

### 3.3 Relatório semanal
- [ ] Resumo automático domingo à noite
- [ ] Comparação semana atual vs anterior
- [ ] Próximos passos sugeridos

**Entrega:** Coach que dá feedback acionável

---

## Fase 4: Integrações
> Facilitar input

### 4.1 Skill PAI
- [ ] `/coach` ou `/fitness` para ver dashboard
- [ ] `/log-weight 81.5` para registrar

### 4.2 Histórico Wendler
- [ ] Parser do CSV Five3One
- [ ] Análise de PRs ao longo do tempo
- [ ] Detecção de platô

---

## Status Atual

**Fase:** 1 completa ✅ (MVP funcional)
**Última atualização:** 2026-01-20

**Próximo:** Fase 2 - Análise visual (fotos + tendência gordura)
