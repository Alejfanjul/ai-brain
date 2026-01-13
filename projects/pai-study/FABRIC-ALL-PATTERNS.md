# Fabric - Guia Completo de Todos os 234 Patterns

> Catálogo completo de todos os patterns disponíveis no Fabric

## O que é o Fabric?

Fabric é uma coleção crowdsourced de prompts (patterns) para resolver problemas específicos. Cada pattern é um prompt testado e refinado pela comunidade.

**Localização:** `/home/marketing/fabric-reference/data/patterns/`

**Uso típico:**
```bash
cat input.txt | fabric -p nome_do_pattern
```

---

## Índice por Categoria

| Categoria | Qtd | Descrição |
|-----------|-----|-----------|
| [Análise](#análise-analyze) | 35 | Analisar conteúdos diversos |
| [Criação](#criação-create) | 55 | Criar conteúdos e artefatos |
| [Extração](#extração-extract) | 42 | Extrair informações específicas |
| [Resumo](#resumo-summarize) | 16 | Resumir conteúdos |
| [Escrita](#escrita-write) | 8 | Escrever documentos |
| [Melhoria](#melhoria-improve) | 5 | Melhorar conteúdos existentes |
| [TELOS](#telos-t_) | 16 | Trabalhar com contexto pessoal |
| [Código](#código) | 10 | Desenvolvimento de software |
| [Segurança](#segurança) | 15 | Cibersegurança e threat modeling |
| [Explicação](#explicação-explain) | 5 | Explicar conceitos |
| [Avaliação](#avaliação-rate) | 6 | Avaliar e classificar |
| [Utilidades](#utilidades) | 21 | Ferramentas diversas |

---

## Análise (analyze_*)

35 patterns para analisar diferentes tipos de conteúdo.

### Análise de Conteúdo

| Pattern | O que faz | Útil para |
|---------|-----------|-----------|
| `analyze_answers` | Analisa respostas de entrevistas/questionários | Processar pesquisas |
| `analyze_claims` | Analisa afirmações e verifica veracidade | Fact-checking |
| `analyze_comments` | Analisa comentários de redes sociais | Entender feedback |
| `analyze_debate` | Analisa debates e argumentos | Estudar retórica |
| `analyze_presentation` | Analisa apresentações | Melhorar slides |
| `analyze_prose` | Analisa qualidade de escrita | Melhorar textos |
| `analyze_prose_json` | Analisa prosa (output JSON) | Integração com sistemas |
| `analyze_prose_pinker` | Analisa escrita estilo Steven Pinker | Clareza de escrita |
| `analyze_spiritual_text` | Analisa textos espirituais/religiosos | Estudo de textos |

### Análise de Negócios

| Pattern | O que faz | Útil para |
|---------|-----------|-----------|
| `analyze_bill` | Analisa projetos de lei/legislação | Entender leis |
| `analyze_bill_short` | Versão resumida de análise de lei | Quick overview |
| `analyze_candidates` | Analisa candidatos políticos | Eleições |
| `analyze_product_feedback` | Analisa feedback de produto | **Hotelaria - reviews** |
| `analyze_proposition` | Analisa proposições/propostas | Decisões de negócio |
| `analyze_sales_call` | Analisa chamadas de vendas | Treinar equipe |
| `analyze_risk` | Analisa riscos de negócio | **Planejamento hotel** |

### Análise Técnica

| Pattern | O que faz | Útil para |
|---------|-----------|-----------|
| `analyze_cfp_submission` | Analisa submissões para conferências | Avaliar propostas |
| `analyze_email_headers` | Analisa headers de email | Segurança/spam |
| `analyze_incident` | Analisa incidentes de segurança | Resposta a incidentes |
| `analyze_interviewer_techniques` | Analisa técnicas de entrevistador | Melhorar entrevistas |
| `analyze_logs` | Analisa logs de sistema | Debug |
| `analyze_malware` | Analisa malware | Segurança |
| `analyze_patent` | Analisa patentes | Pesquisa de mercado |
| `analyze_terraform_plan` | Analisa planos Terraform | DevOps |
| `analyze_threat_report` | Analisa relatórios de ameaças | Segurança |
| `analyze_threat_report_cmds` | Extrai comandos de relatórios | Segurança |
| `analyze_threat_report_trends` | Analisa tendências de ameaças | Segurança |

### Análise Intelectual

| Pattern | O que faz | Útil para |
|---------|-----------|-----------|
| `analyze_mistakes` | Analisa erros e como evitá-los | Aprendizado |
| `analyze_military_strategy` | Analisa estratégias militares | Estudo de estratégia |
| `analyze_paper` | Analisa artigos acadêmicos | Pesquisa |
| `analyze_paper_simple` | Versão simplificada de análise | Quick overview |
| `analyze_personality` | Analisa personalidade de alguém | **Criar TELOS** |
| `analyze_tech_impact` | Analisa impacto de tecnologias | Decisões tech |

---

## Criação (create_*)

55 patterns para criar diferentes tipos de conteúdo.

### Criação de Conteúdo

| Pattern | O que faz | Útil para |
|---------|-----------|-----------|
| `create_5_sentence_summary` | Cria resumo em 5 frases | Quick summary |
| `create_academic_paper` | Cria estrutura de paper | Pesquisa |
| `create_aphorisms` | Cria aforismos/frases de efeito | Conteúdo de marca |
| `create_art_prompt` | Cria prompts para arte IA | Geração de imagens |
| `create_better_frame` | Reformula frames negativos em positivos | **Criar TELOS** |
| `create_diy` | Cria tutoriais DIY | Conteúdo educacional |
| `create_flash_cards` | Cria flashcards para estudo | Aprendizado |
| `create_formal_email` | Cria emails formais | Comunicação |
| `create_keynote` | Cria estrutura de keynote | Apresentações |
| `create_logo` | Descreve conceito de logo | Branding |
| `create_micro_summary` | Cria micro resumo | Social media |
| `create_mnemonic_phrases` | Cria frases mnemônicas | Memorização |
| `create_newsletter_entry` | Cria entrada de newsletter | Email marketing |
| `create_npc` | Cria personagem NPC para jogos | RPG/Games |
| `create_quiz` | Cria quiz/questionário | Educação |
| `create_reading_plan` | Cria plano de leitura | **Estudo pessoal** |
| `create_recursive_outline` | Cria outline recursivo | Estruturar ideias |
| `create_show_intro` | Cria intro para shows/podcasts | Mídia |
| `create_story_about_people_interaction` | Cria história sobre interação | Storytelling |
| `create_story_about_person` | Cria história sobre pessoa | Biografia |
| `create_story_explanation` | Cria explicação narrativa | Educação |
| `create_tags` | Cria tags para conteúdo | Organização |
| `create_video_chapters` | Cria capítulos para vídeo | YouTube |

### Criação para Negócios

| Pattern | O que faz | Útil para |
|---------|-----------|-----------|
| `create_ai_jobs_analysis` | Analisa impacto de IA em empregos | Planejamento |
| `create_hormozi_offer` | Cria oferta irresistível (Alex Hormozi) | **Vendas hotel** |
| `create_idea_compass` | Estrutura ideia em 8 dimensões | **Planejamento** |
| `create_loe_document` | Cria documento de estimativa de esforço | Projetos |
| `create_prd` | Cria Product Requirements Document | Produto |
| `create_prediction_block` | Cria bloco de predições | Planejamento |
| `create_user_story` | Cria user stories | Desenvolvimento |

### Criação de Visualizações

| Pattern | O que faz | Útil para |
|---------|-----------|-----------|
| `create_conceptmap` | Cria mapa conceitual | Visualização |
| `create_excalidraw_visualization` | Cria diagrama Excalidraw | Diagramas |
| `create_graph_from_input` | Cria gráfico de dados | Data viz |
| `create_investigation_visualization` | Visualiza investigações | Análise |
| `create_markmap_visualization` | Cria mindmap (Markmap) | Mindmaps |
| `create_mermaid_visualization` | Cria diagrama Mermaid | Fluxogramas |
| `create_mermaid_visualization_for_github` | Mermaid para GitHub | Documentação |
| `create_visualization` | Cria visualização geral | Data viz |

### Criação para Segurança

| Pattern | O que faz | Útil para |
|---------|-----------|-----------|
| `create_cyber_summary` | Cria resumo de cibersegurança | Relatórios |
| `create_network_threat_landscape` | Cria mapa de ameaças de rede | Segurança |
| `create_report_finding` | Cria finding de relatório | Pentest |
| `create_security_update` | Cria atualização de segurança | Comunicação |
| `create_sigma_rules` | Cria regras SIGMA | Detecção |
| `create_stride_threat_model` | Cria threat model STRIDE | Arquitetura |
| `create_threat_scenarios` | Cria cenários de ameaça | Planejamento |
| `create_ttrc_graph` | Cria gráfico TTRC | Métricas |
| `create_ttrc_narrative` | Cria narrativa TTRC | Relatórios |
| `create_upgrade_pack` | Cria pacote de upgrade | Manutenção |

### Criação para Desenvolvimento

| Pattern | O que faz | Útil para |
|---------|-----------|-----------|
| `create_coding_feature` | Cria feature de código | Desenvolvimento |
| `create_coding_project` | Cria estrutura de projeto | Novos projetos |
| `create_command` | Cria comando CLI | Automação |
| `create_design_document` | Cria documento de design | Arquitetura |
| `create_git_diff_commit` | Cria commit a partir de diff | Git |
| `create_pattern` | Cria novo pattern do Fabric | Meta |
| `create_summary` | Cria resumo estruturado | Documentação |

### Criação RPG/Jogos

| Pattern | O que faz | Útil para |
|---------|-----------|-----------|
| `create_rpg_summary` | Cria resumo de sessão RPG | Jogos |

---

## Extração (extract_*)

42 patterns para extrair informações específicas.

### Extração de Sabedoria/Ideias

| Pattern | O que faz | Útil para |
|---------|-----------|-----------|
| `extract_wisdom` | Extrai sabedoria estruturada | **Processar conteúdos** |
| `extract_wisdom_agents` | Extrai sabedoria (versão agentes) | Automação |
| `extract_wisdom_dm` | Extrai sabedoria (Daniel Miessler) | Estilo DM |
| `extract_wisdom_nometa` | Extrai sabedoria sem meta-info | Clean output |
| `extract_article_wisdom` | Extrai sabedoria de artigo | Artigos |
| `extract_ideas` | Extrai ideias principais | Brainstorm |
| `extract_insights` | Extrai insights | **Análise** |
| `extract_insights_dm` | Extrai insights (Daniel Miessler) | Estilo DM |
| `extract_core_message` | Extrai mensagem central | Resumo |
| `extract_main_idea` | Extrai ideia principal | Quick summary |

### Extração de Livros/Conteúdo

| Pattern | O que faz | Útil para |
|---------|-----------|-----------|
| `extract_book_ideas` | Extrai ideias de livro | **Processar leituras** |
| `extract_book_recommendations` | Extrai recomendações de livros | Curadoria |
| `extract_characters` | Extrai personagens | Análise literária |
| `extract_jokes` | Extrai piadas | Entretenimento |
| `extract_song_meaning` | Extrai significado de música | Análise |
| `extract_sponsors` | Extrai patrocinadores de conteúdo | Análise de mídia |
| `extract_videoid` | Extrai ID de vídeo YouTube | Automação |
| `extract_latest_video` | Extrai vídeo mais recente | Monitoramento |

### Extração para Negócios

| Pattern | O que faz | Útil para |
|---------|-----------|-----------|
| `extract_business_ideas` | Extrai ideias de negócio | **Oportunidades** |
| `extract_primary_problem` | Extrai problema principal | **Criar TELOS** |
| `extract_primary_solution` | Extrai solução principal | Análise |
| `extract_product_features` | Extrai features de produto | Produto |
| `extract_predictions` | Extrai predições | Planejamento |
| `extract_recommendations` | Extrai recomendações | Curadoria |
| `extract_main_activities` | Extrai atividades principais | Análise de processo |

### Extração Técnica

| Pattern | O que faz | Útil para |
|---------|-----------|-----------|
| `extract_algorithm_update_recommendations` | Extrai recomendações de update | Manutenção |
| `extract_ctf_writeup` | Extrai writeup de CTF | Segurança |
| `extract_domains` | Extrai domínios de texto | Segurança |
| `extract_instructions` | Extrai instruções | Documentação |
| `extract_mcp_servers` | Extrai servidores MCP | Integração |
| `extract_patterns` | Extrai patterns de código | Análise |
| `extract_poc` | Extrai proof of concept | Segurança |
| `extract_questions` | Extrai perguntas | FAQ |
| `extract_recipe` | Extrai receitas | Culinária |
| `extract_references` | Extrai referências | Pesquisa |
| `extract_skills` | Extrai skills mencionadas | RH |

### Extração de Opiniões

| Pattern | O que faz | Útil para |
|---------|-----------|-----------|
| `extract_alpha` | Extrai insights únicos/controversos | Análise |
| `extract_controversial_ideas` | Extrai ideias controversas | Debate |
| `extract_extraordinary_claims` | Extrai claims extraordinárias | Fact-checking |
| `extract_most_redeeming_thing` | Extrai melhor aspecto | Análise balanceada |

---

## Resumo (summarize_*)

16 patterns para resumir diferentes tipos de conteúdo.

| Pattern | O que faz | Útil para |
|---------|-----------|-----------|
| `summarize` | Resumo geral | **Uso frequente** |
| `summarize_board_meeting` | Resumo de reunião de board | Governança |
| `summarize_debate` | Resumo de debate | Política |
| `summarize_git_changes` | Resumo de mudanças Git | Desenvolvimento |
| `summarize_git_diff` | Resumo de diff Git | Code review |
| `summarize_lecture` | Resumo de palestra | **Processar aulas** |
| `summarize_legislation` | Resumo de legislação | Legal |
| `summarize_meeting` | Resumo de reunião | **Operações hotel** |
| `summarize_micro` | Micro resumo (tweet-size) | Social media |
| `summarize_newsletter` | Resumo de newsletter | Curadoria |
| `summarize_paper` | Resumo de paper acadêmico | Pesquisa |
| `summarize_prompt` | Resumo de prompt | Meta |
| `summarize_pull-requests` | Resumo de PRs | Desenvolvimento |
| `summarize_rpg_session` | Resumo de sessão RPG | Jogos |
| `youtube_summary` | Resumo de vídeo YouTube | **Processar vídeos** |

---

## Escrita (write_*)

8 patterns para escrever documentos.

| Pattern | O que faz | Útil para |
|---------|-----------|-----------|
| `write_essay` | Escreve ensaio | Conteúdo |
| `write_essay_pg` | Escreve ensaio estilo Paul Graham | Blog |
| `write_hackerone_report` | Escreve relatório HackerOne | Bug bounty |
| `write_latex` | Escreve em LaTeX | Acadêmico |
| `write_micro_essay` | Escreve micro ensaio | Social media |
| `write_nuclei_template_rule` | Escreve regra Nuclei | Segurança |
| `write_pull-request` | Escreve descrição de PR | Desenvolvimento |
| `write_semgrep_rule` | Escreve regra Semgrep | Segurança |

---

## Melhoria (improve_*)

5 patterns para melhorar conteúdos.

| Pattern | O que faz | Útil para |
|---------|-----------|-----------|
| `improve_academic_writing` | Melhora escrita acadêmica | Papers |
| `improve_prompt` | Melhora prompts | **Meta-prompting** |
| `improve_report_finding` | Melhora findings de relatório | Segurança |
| `improve_writing` | Melhora escrita geral | **Comunicação** |

---

## TELOS (t_*)

16 patterns para trabalhar com contexto pessoal.

> Ver guia completo: `FABRIC-TELOS-PATTERNS.md`

| Pattern | O que faz |
|---------|-----------|
| `t_analyze_challenge_handling` | Avalia progresso nos desafios |
| `t_check_dunning_kruger` | Avalia vieses de competência |
| `t_check_metrics` | Verifica KPIs |
| `t_create_h3_career` | Planeja carreira Human 3.0 |
| `t_create_opening_sentences` | Cria frases de apresentação |
| `t_describe_life_outlook` | Descreve perspectiva de vida |
| `t_extract_intro_sentences` | Extrai intro sobre você |
| `t_extract_panel_topics` | Sugere painéis para participar |
| `t_find_blindspots` | Encontra pontos cegos |
| `t_find_negative_thinking` | Encontra pensamentos negativos |
| `t_find_neglected_goals` | Encontra metas negligenciadas |
| `t_give_encouragement` | Dá encorajamento |
| `t_red_team_thinking` | Ataca seu próprio pensamento |
| `t_threat_model_plans` | Modela ameaças ao plano de vida |
| `t_visualize_mission_goals_projects` | Visualiza alinhamento |
| `t_year_in_review` | Review anual |

---

## Código

10 patterns para desenvolvimento de software.

| Pattern | O que faz | Útil para |
|---------|-----------|-----------|
| `coding_master` | Assistente de código avançado | Desenvolvimento |
| `explain_code` | Explica código | Onboarding |
| `explain_project` | Explica projeto | Documentação |
| `generate_code_rules` | Gera regras de código | Linting |
| `review_code` | Revisa código | Code review |
| `review_design` | Revisa design de sistema | Arquitetura |
| `refine_design_document` | Refina documento de design | Arquitetura |
| `fix_typos` | Corrige typos em código | Limpeza |

---

## Segurança

15 patterns para cibersegurança.

| Pattern | O que faz | Útil para |
|---------|-----------|-----------|
| `ask_secure_by_design_questions` | Perguntas de security by design | Arquitetura |
| `greybeard_secure_prompt_engineer` | Prompt engineer seguro | Segurança de IA |
| `analyze_malware` | Analisa malware | Resposta a incidentes |
| `analyze_incident` | Analisa incidentes | SOC |
| `analyze_threat_report` | Analisa relatórios de ameaça | Intel |
| `create_stride_threat_model` | Cria threat model STRIDE | Design |
| `create_threat_scenarios` | Cria cenários de ameaça | Planning |
| `create_sigma_rules` | Cria regras SIGMA | Detecção |
| `extract_ctf_writeup` | Extrai writeup CTF | Aprendizado |
| `extract_poc` | Extrai proof of concept | Pesquisa |

---

## Explicação (explain_*)

5 patterns para explicar conceitos.

| Pattern | O que faz | Útil para |
|---------|-----------|-----------|
| `explain_code` | Explica código | Desenvolvimento |
| `explain_docs` | Explica documentação | Onboarding |
| `explain_math` | Explica matemática | Educação |
| `explain_project` | Explica projeto | Documentação |
| `explain_terms` | Explica termos técnicos | Glossário |

---

## Avaliação (rate_*)

6 patterns para avaliar e classificar.

| Pattern | O que faz | Útil para |
|---------|-----------|-----------|
| `rate_ai_response` | Avalia resposta de IA | Quality check |
| `rate_ai_result` | Avalia resultado de IA | Quality check |
| `rate_content` | Avalia qualidade de conteúdo | Curadoria |
| `rate_value` | Avalia valor de algo | Decisão |
| `label_and_rate` | Classifica e avalia | Organização |
| `judge_output` | Julga output | Quality check |

---

## Utilidades

21 patterns para tarefas diversas.

### Transformação de Texto

| Pattern | O que faz | Útil para |
|---------|-----------|-----------|
| `clean_text` | Limpa texto | Pré-processamento |
| `convert_to_markdown` | Converte para Markdown | Formatação |
| `sanitize_broken_html_to_markdown` | Sanitiza HTML quebrado | Limpeza |
| `translate` | Traduz texto | Internacionalização |
| `humanize` | Torna texto mais humano | Comunicação |
| `fix_typos` | Corrige erros de digitação | Limpeza |

### Interação/Diálogo

| Pattern | O que faz | Útil para |
|---------|-----------|-----------|
| `dialog_with_socrates` | Diálogo socrático | Reflexão |
| `ask_uncle_duke` | Pergunta ao "Uncle Duke" | Aconselhamento |
| `model_as_sherlock_freud` | Analisa como Sherlock+Freud | Análise profunda |
| `heal_person` | Conversa terapêutica | Bem-estar |

### Recomendações

| Pattern | O que faz | Útil para |
|---------|-----------|-----------|
| `recommend_artists` | Recomenda artistas | Curadoria |
| `recommend_pipeline_upgrades` | Recomenda upgrades de pipeline | DevOps |
| `recommend_talkpanel_topics` | Recomenda tópicos de painel | Eventos |
| `recommend_yoga_practice` | Recomenda prática de yoga | Bem-estar |
| `find_female_life_partner` | Ajuda a encontrar parceira | Relacionamentos |

### Outros

| Pattern | O que faz | Útil para |
|---------|-----------|-----------|
| `agility_story` | Cria história ágil | Scrum |
| `ai` | Prompt genérico de IA | Base |
| `answer_interview_question` | Responde pergunta de entrevista | Preparação |
| `apply_ul_tags` | Aplica tags Unsupervised Learning | Categorização |
| `capture_thinkers_work` | Captura trabalho de pensadores | Pesquisa |
| `check_agreement` | Verifica acordo/consenso | Negociação |
| `compare_and_contrast` | Compara e contrasta | Análise |
| `concall_summary` | Resumo de conference call | Reuniões |
| `enrich_blog_post` | Enriquece post de blog | Conteúdo |
| `export_data_as_csv` | Exporta dados como CSV | Dados |
| `find_hidden_message` | Encontra mensagens ocultas | Análise |
| `find_logical_fallacies` | Encontra falácias lógicas | Debate |
| `get_wow_per_minute` | Calcula "wow" por minuto | Entretenimento |
| `identify_dsrp_*` | Identifica distinções/relações/sistemas | Pensamento sistêmico |
| `identify_job_stories` | Identifica job stories | Produto |
| `md_callout` | Cria callouts Markdown | Formatação |
| `official_pattern_template` | Template oficial de pattern | Meta |
| `predict_person_actions` | Prediz ações de pessoa | Análise |
| `prepare_7s_strategy` | Prepara estratégia 7S | Estratégia |
| `provide_guidance` | Fornece orientação | Aconselhamento |
| `raw_query` | Query raw sem processamento | Debug |
| `suggest_pattern` | Sugere pattern para tarefa | Meta |
| `to_flashcards` | Converte para flashcards | Aprendizado |
| `transcribe_minutes` | Transcreve ata de reunião | Reuniões |
| `tweet` | Cria tweet | Social media |

---

## Patterns Mais Úteis para Hotelaria

| Pattern | Uso no Hotel |
|---------|--------------|
| `analyze_product_feedback` | Analisar reviews de hóspedes |
| `analyze_risk` | Análise de riscos operacionais |
| `create_hormozi_offer` | Criar ofertas irresistíveis |
| `summarize_meeting` | Resumir reuniões de equipe |
| `improve_writing` | Melhorar comunicação com hóspedes |
| `create_formal_email` | Emails profissionais |
| `extract_business_ideas` | Identificar oportunidades |
| `translate` | Comunicação internacional |

---

## Patterns Mais Úteis para TELOS Pessoal

| Pattern | Uso para TELOS |
|---------|----------------|
| `extract_primary_problem` | Definir PROBLEMS |
| `create_better_frame` | Reformular crenças |
| `analyze_personality` | Entender perfil |
| `extract_wisdom` | Processar conteúdos |
| `create_idea_compass` | Estruturar ideias |
| `create_reading_plan` | Plano de aprendizado |
| `dialog_with_socrates` | Reflexão profunda |

---

## Como Usar

### Instalação do Fabric

```bash
# Via Go
go install github.com/danielmiessler/fabric@latest

# Configurar
fabric --setup
```

### Uso Básico

```bash
# Processar arquivo
cat arquivo.txt | fabric -p nome_do_pattern

# Processar URL (YouTube)
fabric -y "https://youtube.com/..." -p extract_wisdom

# Listar patterns disponíveis
fabric --list
```

### Uso com Claude Code

Você pode usar os patterns diretamente como prompts, copiando o conteúdo de `system.md` de cada pattern.

---

## Localização

```
/home/marketing/fabric-reference/data/patterns/
├── analyze_*/
├── create_*/
├── extract_*/
├── summarize_*/
├── write_*/
├── improve_*/
├── t_*/
├── explain_*/
├── rate_*/
└── [utilidades]/
```

Cada pattern tem a estrutura:
```
pattern_name/
└── system.md    ← O prompt completo
```
