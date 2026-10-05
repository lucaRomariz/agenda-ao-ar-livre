# Planejamento e rastreabilidade
Agenda ao Ar Livre | Luca Romariz e Miguel Silva

## Situação e marcos
Prazo da Entrega 1 informado pelo grupo: 05/10/2026 às 08h (horário de Brasília). A revisão e a publicação devem ocorrer antes desse horário. O prazo da fase 2 não foi informado: as semanas de M2 a M6 são uma estimativa relativa à semana de entrega da fase 1, a ajustar ao calendário da disciplina.

| Marco | Prazo relativo | Resultado verificável |
| --- | --- | --- |
| M1 - Fase 1 | Até 05/10/2026, 08h | Revisar pacote, publicar repositório derivado do material oficial, contribuições da dupla e tag. |
| M2 - Base | Semana 2 | Django, PostgreSQL, usuário customizado, migrations e escolha de hospedagem. |
| M3 - Negócio | Semana 3 | Locais, atividades, busca e inscrições com concorrência testada. |
| M4 - Integrações | Semana 4 | API REST, meteorologia, relatório e interface responsiva. |
| M5 - Qualidade | Semana 5 | Testes, publicação, SAST/DAST, correções e nova verificação. |
| M6 - Fase 2 | Semana 6 | Revisão final, demonstração ensaiada e tag final. |

## Backlog e responsabilidades propostas
São atribuições sugeridas, não comprovação de trabalho já realizado. Ambos devem revisar o conjunto e produzir contribuições identificáveis em suas contas.

| ID | Tarefa / responsável | Aceite e dependência |
| --- | --- | --- |
| B01 | Visão e requisitos / Luca | RF/RN revisados por Miguel; M1. |
| B02 | Casos de uso / Miguel | Fluxos e exceções alinhados aos RF; depende B01. |
| B03 | Dados e arquitetura / Luca | DER e componentes revisados; depende B01-B02. |
| B04 | Protótipos e identidade / Miguel | Telas e estados em desktop/celular; depende B02. |
| B05 | Contratos e plano / ambos | API e rastreabilidade consistentes; depende B03-B04. |
| B06 | GitHub e revisão da entrega / ambos | Template, colaboradores, commits reais e tag; depende B01-B05. |
| B07 | Django, auth e banco / Luca | Migrações, login e validações; depende M1. |
| B08 | Locais/atividades e templates / Miguel | CRUD e permissões; depende B07. |
| B09 | Inscrições e concorrência / Luca | Última vaga segura; depende B08. |
| B10 | API e Open-Meteo / Luca | Contrato e falhas testados; depende B08. |
| B11 | Relatório e responsividade / Miguel | Filtros e CSV coerentes; depende B09. |
| B12 | Deploy e testes integrados / ambos | HTTPS e roteiro reproduzível; depende B10-B11. |
| B13 | SAST e correções / Luca | Bandit e análise de dependências, triagem e reteste; depende B12. |
| B14 | DAST e correções / Miguel | ZAP apenas no sistema autorizado, triagem e reteste; depende B12. |
| B15 | Apresentação / ambos | Demonstração e explicação individual; depende B13-B14. |

## Rastreabilidade
| Requisito | Casos de uso / dados | Evidência prevista |
| --- | --- | --- |
| RF01 | UC01 / Usuario | Tela acesso; testes de sessão e e-mail único. |
| RF02 | UC04 / Local, Usuario | Tela locais; validações e PROTECT. |
| RF03 | UC05 / Atividade, Local, Categoria | Formulário/gestão; testes de autorização. |
| RF04 | UC02 / Atividade, Local, Categoria | Catálogo e GET /atividades/. |
| RF05 | UC06 / Inscricao, Atividade | Detalhe; teste PostgreSQL concorrente. |
| RF06 | UC07-UC08 / Inscricao | Minhas inscrições; isolamento entre contas. |
| RF07 | UC09 / Atividade, Inscricao | Gestão/cancelamento transacional. |
| RF08 | UC03 / Local, Atividade, cache técnico | Detalhe; GET /atividades/{id}/previsao/. |
| RF09 | UC10 / Atividade, Inscricao | Relatório restrito e CSV. |
| RF10 | UC11 / Atividade, Local, Categoria | OpenAPI; catálogo/detalhe/categorias/previsão. |
| RF11 | UC01-UC10 / apresentação | Protótipos e teste em 360 px. |

## Fórmulas do relatório
Filtro considera a data local de inicio da atividade, inclusive nos dois limites, e situação opcional. Toda consulta é limitada ao organizador da sessão.

Total de atividades = quantidade de atividades filtradas. Publicadas/canceladas = contagens por situação persistida (publicadas encerradas continuam publicadas). Inscrições confirmadas/canceladas = registros únicos atuais ligados às atividades filtradas. Não mede presença nem histórico de tentativas.

Ocupação = 100 * confirmadas em atividades publicadas filtradas / soma da capacidade dessas atividades. Denominador zero produz null, exibido como "não se aplica". Rascunhos e canceladas não entram no denominador. Exportar uma linha por atividade com id, título, início, situação, capacidade, confirmadas, canceladas e ocupação (vazia para não publicadas). Totais na tela derivam dessas linhas. Neutralizar fórmulas em campos textuais do CSV.

## Estratégia de execução
Usar tarefas pequenas, branches docs/ ou feat/, revisão do outro integrante e integração frequente. Atualizar documentos quando mudar regra ou escopo; registrar motivo no histórico. Priorizar fluxo completo: cadastro -> atividade -> busca -> inscrição -> cancelamento -> relatório; depois consolidar API e estados de falha.

## Riscos e resposta
| Risco | Responsável e ação |
| --- | --- |
| Prazo insuficiente | Ambos: concluir revisão/publicação antes de 05/10/2026, 08h; ajustar marcos da fase 2 quando informada. |
| API externa falha | Luca: cache, timeout, mocks e demonstração com data dentro da janela. |
| Interface inconsistente | Miguel: revisar protótipos e fluxo no celular. |
| Vazamento entre contas | Ambos: testar acesso com dois usuários e ids trocados. |
| Hospedagem suspensa | Luca: monitorar manualmente disponibilidade até fim da avaliação. |
| Commit concentrado | Ambos: contribuições próprias ao longo do trabalho, sem atribuição fictícia. |

## Roteiro de validação na fase 2
1. Usuário A cadastra local e atividade; B não consegue editá-los.
2. B pesquisa, consulta previsão e se inscreve; nova tentativa não duplica.
3. Duas requisições disputam última vaga: só uma confirma.
4. B cancela; vaga retorna; reinscrição reativa o registro.
5. A cancela atividade: todas as inscrições confirmadas são canceladas atomicamente.
6. API oculta rascunhos e e-mails; valida filtros e paginação.
7. Previsão falha/fica fora de horizonte: inscrições continuam funcionando.
8. Relatório/CSV mostram mesmos registros, filtrados pelo dono.
9. Validar teclado, 360 px, SAST/DAST, produção sem DEBUG e segredos fora do Git.

## Pendências para submissão da fase 1
- Instituição, curso, turma e prazo da Entrega 1 preenchidos. Informar matrículas apenas se exigidas e confirmar o prazo da fase 2.
- Repositório publicado: https://github.com/lucaRomariz/agenda-ao-ar-livre. Conferir os colaboradores da dupla.
- Cada integrante revisar e contribuir com sua conta; este pacote não fabrica autoria individual.
- Verificar acesso do professor e revisar atribuições propostas.
- URL registrada acima; registrar o hash/tag final após enviar a revisão documental.
