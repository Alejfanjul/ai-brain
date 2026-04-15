# Plano de Testes — 3 Fases de Rede

Objetivo: descobrir qual configuração de rede entrega streaming estável e decidir onde investir (cabo até o PC? roteador novo no lugar do RE200?).

## Hardware fixo
- **PC:** RTX 5060, Windows, Wi-Fi 2 @ 5GHz
- **TV:** TCL P7K 50" (Google TV)
- **Repetidor atual:** TP-Link RE200 (pega sinal do roteador via Wi-Fi, repete pra TV)
- **Roteador:** único, Casa 2

## Cenários

### Fase 1 — Ambos Wi-Fi (estado atual) 🎯
```
Roteador ─ Wi-Fi ─→ PC
Roteador ─ Wi-Fi ─→ RE200 ─ Wi-Fi ─→ TV
```
**Expectativa:** pior cenário. Dupla travessia Wi-Fi + repetidor.
**Bitrate inicial:** 20 Mbps (conservador pro Wi-Fi).
**Critério "funciona":** stream abre, imagem estável, latência tolerável pra jogos single-player.

### Fase 2 — PC no cabo, TV continua via RE200
```
Roteador ─ Cabo ─→ PC
Roteador ─ Wi-Fi ─→ RE200 ─ Wi-Fi ─→ TV
```
**Pré-requisito:** levar PC pra perto do roteador (teste físico) ou comprar cabo longo.
**Expectativa:** ganho grande no upload do PC (onde o stream nasce). Lado da TV continua sendo o gargalo.
**Bitrate alvo:** 30 Mbps.

### Fase 3 — PC e TV ambos no cabo (requer roteador novo)
```
Roteador ─ Cabo ─→ PC
Roteador(novo no lugar do RE200) ─ Cabo ─→ TV
```
**Pré-requisito:** comprar roteador pro lugar do RE200.
**Expectativa:** cenário ótimo. Validar se vale o investimento extra vs Fase 2.
**Bitrate alvo:** 40-50 Mbps.

## Métricas a coletar em cada fase

Registrar em [log.md](log.md):
- **Latência de input** (Moonlight mostra no overlay: `Ctrl+Alt+Shift+S` no PC, ou overlay do Moonlight na TV)
- **Bitrate efetivo** (vs configurado)
- **Frame drops / late frames** (overlay)
- **Artefatos visuais** (subjetivo: nenhum / leve / incômodo / inaceitável)
- **Stutter de áudio** (sim/não)
- **Jogo testado** (tipo: single-player calmo vs competitivo rápido)
- **Duração da sessão** (curta pega picos bons; longa revela instabilidade real)

## Decisão após cada fase

- **Fase 1 ruim + Fase 2 bom** → investir só no cabo até o PC (~R$ X)
- **Fase 2 ainda tem potencial** → avaliar Fase 3 (roteador novo)
- **Fase 2 já está ótimo** → parar, economizar
