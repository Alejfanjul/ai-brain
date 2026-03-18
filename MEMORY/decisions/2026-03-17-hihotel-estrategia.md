# HiHotel — Estratégia e Identidade

**Data:** 2026-03-17
**Status:** Em formação

Ale e Matheus estão construindo a **HiHotel**, empresa de tecnologia hoteleira.

## Produtos
- **SID** (repo: sistema-os) — Sistema de orquestração hoteleira ("sistema nervoso do hotel"). Três camadas: operacional, tático, estratégico. Já tem módulos em produção no Duke. Visão: 3ª geração de IA (Seth Godin) — conectar pessoas, informação certa na hora certa pro funcionário fazer seu melhor trabalho. Efeito de rede interno.
- **Concierge Platform** (repo: concierge-platform) — Launcher Android TV + backend (Go WS gateway + Laravel API + PostgreSQL). MVP em desenvolvimento. IP da HiHotel. "Cavalo de Tróia" — mais fácil de vender (gera receita visível pro hotel).

## Sócios
- **Ale** — Estratégia & Produto. Background: BRF (marketing, transformação cultural), consultoria, Four Seasons, UFSC.
- **Matheus** — Tecnologia & Infraestrutura. Dev Pleno, Scrum Master, Azure Certified, autor de apostilas.

## Cliente / Proposta
- Apresentaram proposta ao **Diego** e **Heiko** do Duke Beach Hotel (sistema-os/docs/proposta-pj/apresentacao-v7.html).
- Proposta é transição de CLT para PJ — parceria tecnológica com escopo definido.
- Próximo passo: proposta financeira e técnica detalhada.
- Heiko pode ter papel na expansão para outros hotéis (termos a definir).

## Decisões estratégicas (sessão 2026-03-17)

### Modelo de negócio
- **Concierge** = produto com licença (IP da HiHotel). Escalável, SaaS, vendável.
- **SID** = serviço de alto valor. O SID do Duke é do Duke (foi construído CLT). Mas o conhecimento/playbook é da HiHotel.
- Código não é o IP — domínio e expertise são. IA torna código barato de produzir; o valor está em saber O QUE construir.

### Estrutura de receita por hotel
1. Concierge Platform → licença mensal (recorrente, escalável)
2. Setup + Implementação → fee único (cada vez mais rápido com playbook + IA)
3. Orquestração tipo SID → contrato mensal de evolução (upsell)

### Visão de longo prazo
- Concierge com base instalada = SaaS com múltiplo de valuation (empresa vendável)
- Conhecimento acumulado de operação hoteleira = moat
- Rede de hotéis no Concierge = efeito de rede
- Não é empresa de software puro nem consultoria pura — é domain experts + IA

### Proposta pro Duke (estrutura acordada)
- Concierge: projeto à parte, IP da HiHotel, licença de uso pro Duke
- SID: contrato de manutenção e evolução, sistema é do Duke
- Migração CMNET: projeto pontual com escopo fechado

## Referências intelectuais
- **Nate** (newsletter): Jevons Paradox — quando custo de execução cai 10x, expandir ambição, não cortar. Domain experts viram builders. → `sources/2026-03-14-nate-ai-cut-execution-cost-by-10x-the-companies-cutting.md`
- **Seth Godin**: 3ª geração de IA = criar valor conectando pessoas. Ferramentas que melhoram quando mais pessoas usam. → `sources/2026-02-15-seth-godin-the-next-generation-of-ai-businesses.md`

## Próximos passos
- [ ] Montar proposta financeira/técnica pro Duke (separando Concierge, SID, CMNET)
- [ ] Alinhar com Matheus sobre identidade e modelo de negócio
- [ ] Definir pricing
