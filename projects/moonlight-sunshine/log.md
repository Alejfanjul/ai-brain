# Log de Implementação

## 2026-04-14 — Setup inicial

### Estado descoberto
- Sunshine **já instalado** (v2025.924.154138, via winget). SunshineService rodando, porta 47990 escutando em `0.0.0.0`.
- Sem resíduo de IddSampleDriver / monitor virtual no Device Manager.
- Placas de vídeo: NVIDIA RTX 5060 (OK) + AMD Radeon 780M (erro — integrada, provavelmente desabilitada).
- **PC:** `192.168.1.69` (Wi-Fi 2, subnet `192.168.1.0/24`, máscara 255.255.255.0).
- Ethernet do PC desconectado (esperado — Fase 1 é Wi-Fi).

### Pendências imediatas (Fase 1)
- [ ] Descobrir IP da TV e confirmar se está na mesma subnet `192.168.1.0/24` (crítico pro auto-discovery do Moonlight).
- [ ] Acessar `https://localhost:47990` e concluir setup inicial do Sunshine (usuário/senha, se ainda não foi feito).
- [ ] Revisar config A/V (codec, resolução, bitrate 20 Mbps pra começar).
- [ ] Instalar Moonlight na TV (Play Store).
- [ ] Parear (PIN).
- [ ] Teste de fumaça capturando monitor físico.
- [ ] Se ok → instalar IddSampleDriver e migrar pra virtual.

### Fase 1 — resultados (2026-04-14)

#### Teste 1 — captura do ultrawide físico
**Setup:** Sunshine defaults, captura do monitor físico ultrawide 34" (21:9). PC e TV ambos no Wi-Fi 5GHz. TV via repetidor TP-Link RE200. Sem overlay de stats habilitado ainda.

**Resultado:** vídeo praticamente congelado, áudio oscilando, stream chegou a desconectar. Qualidade impraticável visualmente.

**Tese inicial (que depois foi derrubada):** gargalo de rede Wi-Fi + repetidor.

#### Teste 2 — overlay de stats ativado, captura do ultrawide
**Métricas do overlay na TV:**
- Transmissão: **1280x720 @ 63.85 FPS** (Moonlight pediu 720p — config default do app, não ajustado)
- Decodificador: OMX.amlogic.hevc.decoder (HEVC, não AV1)
- Taxa de quadros recebidos: 63.85 FPS / renderizando: 62.87 FPS
- **Quadros dropados pela rede: 0.00%**
- **Latência média da rede: 4 ms** (variação: 4 ms)
- Host processing latency: 1,5 / 3,2 / 2,0 ms
- Tempo de decodificação: 3,93 ms

**🔑 INSIGHT CRÍTICO:** a rede Wi-Fi com repetidor **NÃO é o gargalo**. Os números dizem que chega tudo praticamente sem perda. A qualidade ruim percebida no Teste 1 provavelmente foi **outra coisa** (captura do ultrawide 21:9 esticado pra TV 16:9 adicionando carga de rescaling? interferência momentânea no momento do teste?). Isso derruba a tese inicial — **pode ser que Fase 2 (cabo) nem seja necessária**.

#### Teste 3 — captura do monitor virtual VDD
**Setup:** VDD instalado via winget + driver via VDD Control (devcon.exe). Virtual configurado em 1920x1080@60. Sunshine apontado pra `\\.\DISPLAY7` (VDD by MTT). Testadas as configs avançadas:
- "Activate the display automatically and make it a primary display"
- "Deactivate other displays and activate only the specified display"

**Resultado em ambas:** tela PRETA na TV. Áudio picotado. Monitores físicos **não apagaram** mesmo com a opção "Deactivate others" selecionada + SunshineService reiniciado como admin.

#### Estado atual ao pausar
- Sunshine v2025.924.154138 rodando como service (SunshineService, automatic)
- VDD 25.7.23 instalado e conectado (confirmado via VDD Control pipe)
- Virtual display detectado em `\\.\DISPLAY7` (número suspeito: alto demais pra 3 monitores reais — provável resíduo de displays fantasma)
- PC IP: 192.168.1.69 | TV IP: 192.168.1.128 (mesma subnet, auto-discovery OK)

### Hipóteses em aberto (pra próxima sessão)

1. **Displays fantasma no Windows** — DISPLAY7 sugere lixo acumulado de tentativas anteriores. Limpar via Device Manager → View → Show hidden devices → remover "Monitor" entries desconectados.

2. **Sunshine rodando como SERVICE (SYSTEM) vs USER** — o fato da config "Deactivate other displays" não estar aplicando (monitores não apagam) sugere que o SunshineService (SYSTEM) não tem permissão pra alterar display config do user session. Solução candidata: reinstalar Sunshine em **modo user** (opção do instalador), não como service.

3. **Cross-GPU capture issue** — AMD Radeon 780M (iGPU) está com status "Error" no Device Manager. VDD é `ROOT\DISPLAY\0000` (genérico), mas pode estar roteando rendering pela iGPU quebrada. Sunshine captura via NVENC (RTX 5060). Se houver mismatch, resulta em frames pretos chegando com encode OK. **Vale investigar e possivelmente desabilitar a iGPU.**

4. **VDD bloat/config residual** — desinstalar VDD completamente, limpar `C:\VirtualDisplayDriver\`, remover displays fantasma, reinstalar do zero.

5. **Alternativa: Sunshine Virtual Monitor integration** — projeto que automatiza criação/destruição do virtual apenas durante o stream, reduz chance de lixo acumular. https://github.com/Cypresslin/Sunshine-Virtual-Monitor

### Próximos passos (ordem sugerida — superados pela sessão 2026-04-15)

- [x] ~~Investigar Sunshine user vs service~~ — abandonado: VDD removido por completo
- [x] ~~Limpar displays fantasma~~ — abandonado com remoção do VDD
- [ ] Investigar iGPU AMD 780M em erro (ainda aberto, mas não bloqueia streaming)
- [x] ~~Sunshine Virtual Monitor~~ — abandonado

---

## 2026-04-15 — Sessão de debug e validação final

### Mudança de abordagem
Amigo do Ale sugeriu eliminar o monitor virtual (complicação desnecessária). Decisão: **remover VDD completamente e capturar monitor físico.**

### Ações executadas
1. Sunshine revertido pra captura automática do primary (campo `output_name_windows` vazio)
2. VDD device removido via `devcon remove Root\MttVDD`
3. VDD desinstalado via `winget uninstall VirtualDrivers.Virtual-Display-Driver`
4. Pasta `C:\VirtualDisplayDriver\` restante (só XML de config — inofensiva)

### Testes de rede (todos em 1080p60)
| Cenário | Resolução/Codec | Latência | Drops | FPS recebidos | Veredicto |
|---------|-----------------|----------|-------|---------------|-----------|
| PC Wi-Fi (RE200) + TV Wi-Fi (RE200) | 1080p60 HEVC @ 20M | 28ms, var 12ms | 3.28% | ~58 | ruim |
| idem @ 15M | 1080p60 HEVC @ 15M | 37ms, var 55ms | 5.43% | ~60 | pior |
| PC cabo + TV Wi-Fi direto roteador | 1080p60 HEVC @ 20M | 11ms, var 16ms | 0% | 46.8 (!) | números ok, experiência ruim |
| PC cabo + TV cabo | 720p60 HEVC @ 20M | 1ms, var 0ms | 0% | 60.37 | **números perfeitos, experiência ruim** |
| PC cabo + TV cabo | 720p60 **H.264** @ 20M | 1ms, var 0ms | 0% | 60.37 | **funcionou!** |
| PC cabo + TV cabo | **1080p60 H.264 @ 100M** | ~1ms | 0% | 60 | **ideal validado** |
| PC Wi-Fi + TV cabo | 1080p60 H.264 @ ? | — | — | — | "rodou legal mas caiu um pouco a qualidade" |

### 🔑 Achado central da sessão
**NVENC HEVC da RTX 5060 produz stream inassistível mesmo com 1ms de latência e 0% de drops.** Não é rede — é bug/config do encoder na série 50 da NVIDIA. **Solução: usar H.264 como codec no Moonlight.**

Por que Steam Link parecia melhor antes: Steam Link usa H.264 por padrão.

### Configuração final funcional
- **Moonlight (na TV):** 1920x1080, 60fps, **H.264**, bitrate 100 Mbps (cabeado) ou ~30 Mbps (Wi-Fi no PC)
- **Sunshine:** defaults + `output_name_windows = \\.\DISPLAY2` (AOC 27B35H, o 27")
- **Topologia recomendada:** PC cabeado no roteador + TV cabeada no roteador (melhor qualidade absoluta)
- **Topologia aceitável:** PC Wi-Fi (direto roteador, sem RE200) + TV cabeada — funciona bem, pequena perda de qualidade

### Decisão de compra
Topologia ideal comprovada: **PC cabeado + TV cabeada**. Para isso é necessário:
- 1 cabo Ethernet longo (Casa 1 → Casa 2) para o PC
- 1 roteador novo no lugar do RE200 (pra dar Wi-Fi na Casa 2 + cabo pra TV)

Amigo do Ale virá 2026-04-16 ajudar a terminar o setup.

### Configuração multi-monitor
- Ultrawide LG (3440x1440 @ 160Hz) — DISPLAY1, primary por padrão (trabalho)
- AOC 27B35H (1920x1080 @ 60Hz) — DISPLAY2, capturado pelo Sunshine (streaming)
- **Fluxo de uso:** quando for jogar, trocar primary pro AOC manualmente (Win+I → Sistema → Tela → AOC → Tornar principal). Jogos abrem nele → chegam na TV via stream. Trocar de volta pro ultrawide quando terminar.

### Pendências
- [ ] Testar HEVC com driver NVIDIA atualizado numa sessão futura (pode ter corrigido)
- [ ] Investigar iGPU AMD 780M com Error no Device Manager (não bloqueia, mas é lixo)
- [ ] Considerar WoL (Parte 3 do guia) quando o setup estiver 100% físico

---

## Template para próximas fases

```
## YYYY-MM-DD — Fase N (nome)

### Setup
- Mudança de hardware/rede:
- Config Sunshine:
- Config Moonlight:

### Sessão de teste
- Jogo:
- Duração:

### Métricas
- Latência média (ms):
- Bitrate configurado vs efetivo:
- Frame drops:
- Artefatos visuais (0-3):
- Stutter de áudio (S/N):

### Notas subjetivas

### Decisão
```
