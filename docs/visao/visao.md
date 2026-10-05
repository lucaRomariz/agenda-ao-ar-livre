# Documento de Visão
Agenda ao Ar Livre | Fase 1 | Versão 0.1 | 04/10/2026

## 1. Identificação e contexto
Integrantes: Luca Romariz e Miguel Silva. Instituição: CEUB. Curso: Análise e Desenvolvimento de Sistemas (ADS). Turma: A. Disciplina: Desenvolvimento Web. Professor: Felippe Pires Ferreira. Prazo da Entrega 1 informado pelo grupo: 05/10/2026 às 08h (horário de Brasília). Matrículas e prazo da fase 2 não informados.

Pequenos grupos organizam caminhadas, treinos e encontros em espaços públicos usando mensagens dispersas. Participantes podem perder informações sobre horários, endereço, vagas e cancelamentos. Organizadores precisam consolidar inscrições e consultar a previsão em outro serviço.

## 2. Problema e justificativa
A ausência de um registro central dificulta saber qual atividade está confirmada, quantas vagas existem e qual previsão corresponde à sua localização e data. A proposta reúne esses dados para reduzir consultas repetidas e apoiar decisões do organizador. O problema é uma hipótese de projeto, ainda sem pesquisa de campo; não se afirma validação com usuários reais.

## 3. Objetivos
Objetivo geral: planejar e implementar uma aplicação web Django que centralize atividades gratuitas ao ar livre, inscrições e previsão meteorológica.

- Permitir ao organizador manter locais e atividades de sua autoria.
- Permitir ao público pesquisar e consultar atividades publicadas.
- Controlar vagas e inscrições sem duplicidade nem exceder a capacidade.
- Apresentar previsão diária do local e data, sem prometer previsão fora do horizonte disponível.
- Gerar indicadores filtrados e exportar relatório CSV.
- Oferecer API REST de consulta pública e documentada.

## 4. Público-alvo e stakeholders
| Envolvido | Interesse / responsabilidade |
| --- | --- |
| Visitante | Descobrir atividades e consultar informações públicas. |
| Participante | Inscrever-se, consultar inscrições e cancelá-las. |
| Organizador | Publicar suas atividades, gerenciar vagas e obter relatórios. |
| Luca Romariz e Miguel Silva | Desenvolver, revisar e apresentar a solução. |
| Professor | Avaliar artefatos, consistência e participação individual. |
| Open-Meteo | Prover os dados meteorológicos sob suas condições de uso. |

Participante e organizador são papéis de uso da mesma conta: qualquer usuário autenticado pode organizar e participar. Não há escolha de perfil que conceda acesso a dados de outro organizador. A administração técnica usa Django Admin e não constitui uma funcionalidade de negócio adicional.

## 5. Escopo e requisitos funcionais
| ID | Requisito e critério de aceite |
| --- | --- |
| RF01 | Criar conta, entrar e sair. E-mail normalizado único; senha validada e armazenada com hash; falhas não revelam existência da conta. |
| RF02 | Manter locais próprios com nome, endereço e coordenadas válidas. Impedir exclusão de local referenciado. |
| RF03 | Criar, consultar, editar e excluir atividades próprias; exclusão física somente em rascunho e sem histórico de inscrição. |
| RF04 | Buscar atividades por texto, período de início, cidade e categoria; exibir resultado vazio claramente. |
| RF05 | Inscrever usuário em atividade publicada futura com vaga; impedir duplicidade e excesso em requisições concorrentes. |
| RF06 | Consultar minhas inscrições e cancelar inscrição confirmada antes do início, liberando vaga. |
| RF07 | Cancelar atividade própria futura, informar motivo e cancelar inscrições confirmadas na mesma transação. |
| RF08 | Exibir previsão diária do local/data e fonte; mostrar indisponibilidade e fora de horizonte sem impedir outras funções. |
| RF09 | Gerar relatório das próprias atividades por intervalo de início e situação; visualizar totais e exportar CSV equivalente. |
| RF10 | Expor catálogo, detalhes, categorias e previsão via API REST pública v1, sem divulgar participantes, e-mails ou rascunhos. |
| RF11 | Aplicar identidade visual e interface responsiva em telas essenciais. |

## 6. Regras de negócio
- RN01: cada atividade tem exatamente um organizador, local e categoria. Apenas o dono pode alterá-la; o local escolhido deve pertencer a esse organizador.
- RN02: início futuro na criação/publicação; término posterior ao início e no mesmo dia no fuso America/Sao_Paulo. Capacidade inteira entre 1 e 500. Escopo geográfico inicial: locais atendidos nesse fuso.
- RN03: estados da atividade: rascunho, publicada, cancelada. Evento encerrado é uma condição derivada de término <= agora, não uma quarta situação persistida. Cancelada não reabre.
- RN04: publicar exige todos os campos válidos. Atividade publicada não volta a rascunho; exclusão física somente de rascunho sem qualquer inscrição. As demais são canceladas e mantidas no histórico.
- RN05: inscrição única por usuário/atividade. Confirmada ocupa uma vaga; cancelada não ocupa. Reinscrição reativa o mesmo registro se ainda elegível; o relatório não conta tentativas como pessoas diferentes.
- RN06: a criação/reativação da inscrição, cancelamento da atividade e alterações da capacidade usam transação e bloqueio da linha da atividade. A verificação de vagas ocorre dentro desse bloqueio.
- RN07: atividade já iniciada não permite novas inscrições nem cancelamentos ou alterações de negócio. Antes do início, capacidade nunca fica abaixo do total confirmado. Com qualquer histórico de inscrição, local, categoria, início e término ficam imutáveis; alteração substancial exige cancelar e criar nova atividade.
- RN08: cancelamento de atividade exige motivo de 10 a 500 caracteres. Motivo é público. Inscrições confirmadas mudam para cancelada com motivo atividade_cancelada. Cancelamentos individuais anteriores são preservados.
- RN09: alterar endereço/coordenadas de local com qualquer atividade publicada ou com inscrição é bloqueado; deve-se cadastrar outro local. Assim se preserva a localização histórica.
- RN10: o dono da atividade não se inscreve nela. Visitante só vê publicada/cancelada; rascunho é privado. Inscrições e relatórios são restritos ao respectivo usuário/dono.
- RN11: previsão é informação de apoio, nunca cancela automaticamente. Sem coordenadas válidas, o cadastro do local não é salvo. Sem previsão válida, mostrar estado textual sem inventar números.
- RN12: vagas = capacidade - inscrições confirmadas. Não persistir vagas, percentuais ou contadores derivados.

## 7. Fora do escopo
Pagamentos, ingressos, chat, mapas interativos, geolocalização do participante, WhatsApp, envio de e-mails, recuperação de senha por e-mail, recorrência, lista de espera, presença/check-in, calendário externo, alertas automáticos e previsões históricas. Coordenadas são informadas manualmente pelo organizador. Não há garantia de reserva física do espaço público.

## 8. Restrições e requisitos não funcionais
- RNF01: Python, Django, Django REST Framework e banco PostgreSQL; frontend com templates Django, HTML e CSS. Evitar SPA para reduzir complexidade de duas pessoas.
- RNF02: validação no servidor, autenticação de sessão, proteção CSRF em operações de escrita e autorização por proprietário.
- RNF03: publicação HTTPS na fase 2, DEBUG desativado, segredos por ambiente e cookies seguros em produção.
- RNF04: páginas usáveis a partir de 360 px, teclado, foco visível, labels e mensagens que não dependam só de cor.
- RNF05: meta de 2 s para consultas locais em base de demonstração de 1.000 atividades, desconsiderando rede externa; medir na fase 2. Serviço meteorológico com tempo total alvo de até 5 s e cache de 30 min.
- RNF06: dependências fixadas e migrations versionadas na fase 2; testes de fluxo, autorização e concorrência no PostgreSQL.
- RNF07: o catálogo não expõe dados pessoais de participantes. Usar dados fictícios para demonstração, sem coletar CPF, telefone ou localização pessoal.

## 9. Premissas e riscos
Premissas: equipe com duas pessoas; acesso ao GitHub; uso educacional não comercial; conexão disponível. Entrega 1 até 05/10/2026 às 08h (horário de Brasília); horizonte da fase 2 ainda a confirmar. As responsabilidades propostas dependem de aceite do grupo.

| Risco | Impacto e resposta |
| --- | --- |
| API indisponível / limite | Preservar catálogo e inscrições; cache e mensagem explicativa; testar falhas simuladas. |
| Evento fora do horizonte | Mostrar que a previsão ainda não está disponível; não reutilizar outra data. |
| Escopo exceder o prazo | Priorizar RF01-RF10; manter exclusões; revisar backlog semanalmente. |
| Duas pessoas disputarem última vaga | Bloqueio transacional no PostgreSQL e teste concorrente. |
| Hospedagem interrompida | Definir provedor até marco M2 e verificar disponibilidade durante avaliação. |
| Documentos divergirem do código | Rastreabilidade por RF/UC e revisão a cada mudança. |
| Histórico concentrado em uma conta | Cada integrante revisa e altera seu trabalho com a própria conta; não simular commits. |

## 10. Critérios de sucesso
Fase 1: nove produtos obrigatórios legíveis, diagramas editáveis e exportados, requisitos rastreados, template preservado e repositório acessível ao professor com participação real da dupla.

Fase 2: demonstração de cadastro, busca, inscrição, cancelamento, relatório e APIs; última vaga protegida em teste concorrente; pessoa A não altera dados de B; falha meteorológica não impede inscrição; aplicação pública HTTPS, testes e evidências SAST/DAST do próprio sistema. Nenhuma dessas evidências de implementação é declarada concluída nesta fase.
