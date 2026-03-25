---
name: NanoBanana
description: Generate JSON prompts for Nano Banana Pro image editing. USE WHEN user wants to edit, expand, outpaint, or generate images for the sistema-os project (menus, pacotes, propostas) OR /nanobanana OR /banana.
---

# NanoBanana - Image Prompt Generator

Gera prompts JSON estruturados para o Nano Banana Pro, seguindo o schema `marketing_image` do JSON Prompt Translator.

## Context

O sistema-os usa fotos em propostas de eventos (menus, pacotes adicionais). As fotos aparecem no PDF em layout zigzag com proporcao **landscape ~4:3** (largura ~50% da pagina, altura 220-280px). Fotos verticais (portrait) ficam cortadas pelo `object-fit: cover`.

## Rules

Antes de gerar o prompt:

1. **Verificar a foto original** — ler o arquivo de imagem para entender o conteudo
2. **Verificar as proporcoes necessarias** — no zigzag do PDF, a foto precisa ser **landscape 4:3**
3. **Usar a foto original como referencia** — pedir outpaint/expand, nao geracao do zero
4. **Manter fidelidade** — `lock_subject_geometry: true`, `forbidden_changes` para preservar elementos-chave
5. **Sem elementos IA evidentes** — nunca adicionar props decorativos que possam parecer artificiais
6. **Formato de saida** — JSON puro seguindo o schema `marketing_image`

## Schema Reference

O arquivo de referencia do schema esta em:
`C:\Users\aleja\OneDrive\Desktop\Projetos\Imagens\# JSON Prompt Translator A Unified.txt`

Ler este arquivo para garantir que o JSON segue a spec correta.

## Proporcoes por uso

| Uso no PDF | Proporcao | Notas |
|------------|-----------|-------|
| Zigzag normal | 4:3 landscape | height: 280px, ~50% largura pagina |
| Zigzag compacto | 4:3 landscape | height: 220px |
| Capa | 16:9 landscape | Imagem de fundo da capa |

## Workflow

1. Usuario fornece foto original e descreve o que quer
2. Ler a foto e o schema de referencia
3. Gerar JSON `marketing_image` com:
   - `output_aspect_ratio` correto
   - `expand_direction` se for outpaint
   - `forbidden_changes` para preservar elementos originais
   - `controls.lock_subject_geometry: true`
4. Entregar o JSON pronto para colar no Nano Banana Pro

## Examples

**Example 1: Expandir foto portrait para landscape**
```
User: "Essa foto do garcon esta cortada no PDF, preciso expandir para 4:3"
-> Ler foto original
-> Gerar JSON com expand_direction: "outward, especially left and bottom"
-> output_aspect_ratio: "4:3"
```

**Example 2: Trocar fundo de foto de comida**
```
User: "Essa foto de pizza tem fundo ruim, quero um fundo de madeira rustica"
-> Ler foto original
-> Gerar JSON com background.material: "warm rustic wood table"
-> forbidden_changes: ["do_not_change_pizza_toppings"]
```

**Example 3: Gerar foto nova para categoria de menu**
```
User: "Preciso de uma foto para a categoria Sobremesas"
-> Perguntar que tipo de sobremesa
-> Gerar JSON completo sem foto de referencia
-> output_aspect_ratio: "4:3"
```
