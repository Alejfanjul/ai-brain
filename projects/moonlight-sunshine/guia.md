# Guia de Implementação: Sunshine + Moonlight (Game Streaming)

> Documento-base escrito com ChatGPT. Referência técnica — o plano real de execução e status está em [plano-testes.md](plano-testes.md) e [log.md](log.md).

## Contexto do Setup

- **PC (Casa 1):** RTX 5060, dois monitores (ultrawide 32" e 27" normal)
- **TV (Casa 2):** TCL 50" P7K (Google TV)
- **Objetivo:** Jogar games do PC na TV com baixa latência (substituindo Steam Link)
- **Cabo físico:** já existe entre as duas casas

### Topologia de rede alvo (longo prazo)

```
Roteador (Casa 2)
├── [cabo entre casas] → PC (Casa 1)  ← CRÍTICO: PC deve estar no cabo
└── [Wi-Fi direto]    → TV TCL P7K    ← sem repetidor
```

> O RE200 (repetidor) seria REMOVIDO na topologia final. TV conectaria direto ao roteador — ou via cabo caso compre um roteador novo pro lugar do RE200.

---

## Parte 1 — Sunshine (Servidor, instalar no PC)

### 1.1 Download e instalação

- Site oficial: https://github.com/LizardByte/Sunshine/releases
- Ou via winget: `winget install LizardByte.Sunshine`
- Roda como serviço em background

### 1.2 Interface de configuração

Após instalar, acessar pelo browser do PC:
```
https://localhost:47990
```
Criar usuário e senha na primeira vez.

### 1.3 Configurações recomendadas (Audio/Video)

```
Codec:       AV1 (NVENC)       ← aproveita RTX 5060 (NVENC 8ª geração)
Resolution:  1920x1080          ← Full HD é suficiente, mais estável que 4K via stream
FPS:         60
Bitrate:     30 Mbps (ponto de partida via cabo; 20 Mbps via Wi-Fi)
```

> **Por que AV1?** A RTX 5060 tem encoder AV1 de última geração. Menos artefatos em cenas de movimento rápido. A TCL P7K suporta decodificação AV1 por hardware.

### 1.4 Configuração do monitor de captura

**Problema:** O Sunshine captura um monitor físico. Com ultrawide (21:9) sendo capturado numa TV 16:9, a imagem fica distorcida ou com bordas pretas.

**Solução: Monitor Virtual (IddSampleDriver)**

1. Baixar: https://github.com/ge9/IddSampleDriver/releases
2. Instalar o driver
3. Criar um display virtual: **1920x1080 @ 60Hz**
4. No Sunshine → Configuration → Audio/Video → `Output Name`: selecionar o monitor virtual

> Resultado: TV recebe exatamente 1920x1080, proporção correta. Monitores físicos continuam disponíveis.

---

## Parte 2 — Moonlight (Cliente, instalar na TV)

### 2.1 Instalação na TCL P7K (Google TV)

1. Abrir a **Google Play Store** na TV
2. Buscar: `Moonlight Game Streaming`
3. Instalar (app oficial, gratuito)

### 2.2 Pareamento com o Sunshine

1. Abrir o Moonlight na TV
2. Auto-discovery (mesma subnet) — ou adicionar PC manualmente pelo IP
3. PIN aparece na TV → inserir em `https://localhost:47990 → PIN`
4. Pareamento concluído

### 2.3 Configurações no Moonlight

```
Resolution:  1920x1080
FPS:         60
Bitrate:     30 Mbps (ajustar)
Codec:       AV1
```

---

## Parte 3 — Wake on LAN (fase futura)

### 3.1 BIOS do PC
- `Wake on LAN` habilitado
- `Power on by PCI-E` (ou similar)

### 3.2 Windows
```
Gerenciador de Dispositivos → Adaptadores de Rede → [placa] → Propriedades
→ Gerenciamento de Energia: ✅ Permitir acordar o computador
→ Configurações Avançadas: Wake on Magic Packet → Enabled
```

### 3.3 IP fixo no roteador
Reservar IP por MAC address.

### 3.4 Ferramentas de envio
| Origem | Ferramenta |
|--------|-----------|
| TV (mesma rede) | Moonlight nativo |
| Celular (rede local) | Depicus WoL / Wol Wake On Lan |
| Celular (fora de casa) | Tailscale + app WoL |

---

## Referências

- Sunshine: https://github.com/LizardByte/Sunshine
- Moonlight: https://moonlight-stream.org
- IddSampleDriver: https://github.com/ge9/IddSampleDriver
- Tailscale: https://tailscale.com
