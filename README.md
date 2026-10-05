# Agenda ao Ar Livre

![Assinatura visual](images/logo.svg)

**Seu próximo encontro começa lá fora.** Plataforma proposta para organizar atividades gratuitas, controlar inscrições e consultar a previsão do tempo no local do evento.

**Instituição:** CEUB.  
**Curso:** Análise e Desenvolvimento de Sistemas (ADS).  
**Disciplina:** Desenvolvimento Web.  
**Turma:** A.  
**Prazo da Entrega 1:** 05/10/2026 às 08h (horário de Brasília), informado pelo grupo.  
**Professor:** Felippe Pires Ferreira.  
**Status:** Fase 1 - documentação e protótipos; aplicação Django ainda não implementada.

## Sumário
1. [Descrição](#1-descrição-do-projeto)
2. [Funcionalidades](#2-funcionalidades)
3. [Demonstração](#3-demonstração)
4. [Tecnologias](#4-tecnologias-utilizadas)
5. [Arquitetura](#5-arquitetura)
6. [Diretórios](#6-organização-dos-diretórios)
7. [Participantes](#7-participantes)
8. [Como executar](#8-como-executar)
9. [Configuração](#9-configuração)
10. [Testes](#10-testes)
11. [Uso de IA](#11-uso-de-inteligência-artificial)
12. [Contribuição](#12-contribuição-e-fluxo-de-trabalho)
13. [Versões](#13-histórico-de-versões)
14. [Limitações](#14-limitações-e-próximos-passos)
15. [Referências](#15-licença-referências-e-contato)

## 1. Descrição do projeto
Pequenos grupos precisam reunir informações sobre atividades externas, vagas, inscrições e cancelamentos. Agenda ao Ar Livre propõe centralizar essas informações e associar a previsão diária do local à atividade.

O público-alvo são organizadores de caminhadas, treinos e encontros gratuitos e seus participantes. O objetivo é oferecer cadastro, busca, controle de vagas, relatórios, API pública e integração meteorológica útil. A hipótese de problema ainda não foi validada em pesquisa de campo.

[Documento de Visão](docs/visao/visao.md) · [PDF consolidado da entrega](docs/entrega-1.pdf)

## 2. Funcionalidades
| Funcionalidade | Situação |
| --- | --- |
| Conta, login e logout | Planejada |
| CRUD de locais e atividades próprias | Planejado |
| Busca por texto, cidade, categoria e período | Planejada |
| Inscrição, cancelamento e controle de vagas | Planejados |
| Relatório filtrado e exportação CSV | Planejados |
| API REST pública de leitura | Contrato documentado |
| Previsão diária Open-Meteo | Integração planejada |
| Identidade e telas responsivas | Protótipo demonstrativo preparado |

Requisitos não funcionais: Python/Django, PostgreSQL, validação no servidor, autorização por dono, interface a partir de 360 px e HTTPS na fase 2. Metas e critérios estão na visão.

## 3. Demonstração
[Protótipo navegável](docs/prototipos/index.html) · [Galeria de telas](docs/prototipos/telas.md) · [Identidade visual](docs/prototipos/identidade-e-prototipos.md)

Abrir o HTML localmente; GitHub mostra o código-fonte e não executa o protótipo. Inclui explorar, detalhe, acesso, inscrições, gestão, formulário de atividade, locais e relatório. Dados fictícios, interações em memória e previsão simulada; não há backend ou autenticação real.

## 4. Tecnologias utilizadas
**Nesta fase:** Markdown, PDF, diagrams.net (.drawio), SVG, OpenAPI 3.0.3, HTML/CSS/JavaScript e Git. PDFs gerados com ReportLab; pacote consolidado com pypdf.

**Previstas para fase 2:** Python 3.12, Django 5.2 LTS, Django REST Framework, PostgreSQL, requests, Gunicorn e WhiteNoise. Versões corretivas compatíveis serão fixadas ao iniciar a implementação. Não há requirements de aplicação fictício nesta entrega.

## 5. Arquitetura
Monólito modular Django com templates e API REST de leitura. Serviços de domínio centralizam validações e transações; ORM acessa PostgreSQL; cliente meteorológico acessa Open-Meteo com timeout e cache.

[Arquitetura](docs/arquitetura/arquitetura.md) · [Componentes UML](docs/arquitetura/componentes.svg) · [Modelo de dados](docs/modelagem/banco-de-dados/modelo-logico.md)

| Método | Rota prevista |
| --- | --- |
| GET | /api/v1/atividades/ |
| GET | /api/v1/atividades/{id}/ |
| GET | /api/v1/atividades/{id}/previsao/ |
| GET | /api/v1/categorias/ |

[Contrato da API](docs/api/contrato-api.md) · [OpenAPI](docs/api/openapi.json) · [Integração externa](docs/api/integracao-externa.md)

## 6. Organização dos diretórios
```text
README.md
docs/
  README.md / README.pdf / entrega-1.pdf
  visao/
  modelagem/
    casos-de-uso/
    classes/
    banco-de-dados/
  arquitetura/
  api/
  prototipos/
  planejamento/
images/
  logo.svg
  semaforo.png
```

A estrutura existente do template foi preservada, incluindo os caminhos dos quatro PDFs de modelagem e a imagem institucional. As demais pastas cobrem entregáveis adicionais exigidos. Cada diagrama tem .drawio e .svg junto do documento correspondente. src/backend/ e testes serão criados na fase 2.

## 7. Participantes
| Nome | Matrícula | Responsabilidade proposta |
| --- | --- | --- |
| Luca Romariz | 22504651 | Backend, dados, API, integração e SAST; revisão conjunta. |
| Miguel Silva | Não informada | Casos de uso, interface, relatório e DAST; revisão conjunta. |

Divisão sujeita à confirmação da dupla; não representa evidência de execução individual. Professor responsável: Felippe Pires Ferreira.

## 8. Como executar
**Protótipo:** abrir docs/prototipos/index.html no navegador; não requer instalação. Alternativa, na raiz da pasta:

```bash
python3 -m http.server 8000
```

Acessar http://localhost:8000/docs/prototipos/. O servidor acima serve arquivos estáticos e não é a aplicação Django.

**Aplicação publicada:** ainda não existe; prevista para fase 2. Hospedagem a definir. Instruções reais de Django e migrations serão acrescentadas quando implementadas.

## 9. Configuração
As variáveis abaixo são previstas para a fase 2; o protótipo não requer configuração.

| Variável | Uso |
| --- | --- |
| DJANGO_SECRET_KEY | Chave gerada localmente; nunca versionar valor real. |
| DJANGO_DEBUG | False em produção. |
| DJANGO_ALLOWED_HOSTS | Hosts autorizados. |
| DJANGO_CSRF_TRUSTED_ORIGINS | Origens HTTPS exatas da produção. |
| DATABASE_URL | Conexão PostgreSQL, definida no ambiente. |
| OPEN_METEO_CONNECT_TIMEOUT | Timeout de conexão, 2 s. |
| OPEN_METEO_READ_TIMEOUT | Timeout de leitura, 3 s. |
| WEATHER_CACHE_TTL | Cache meteorológico, 1800 s. |
| API_RATE_LIMIT | Limite inicial de consulta, 60/min. |

Open-Meteo gratuita não comercial não exige chave. Não publicar .env, senhas ou banco com dados pessoais.

## 10. Testes
Esta entrega contém documentação e um protótipo. Não há testes de backend nem evidências SAST/DAST executadas. A verificação desta fase cobre integridade de arquivos, consistência documental, validade JSON/XML, renderização dos PDFs e navegação do protótipo.

[Roteiro de validação da fase 2](docs/planejamento/planejamento.md) inclui autorização entre contas, concorrência, falhas da integração, relatórios e API. A cobertura do código de aplicação ainda não se aplica.

## 11. Uso de inteligência artificial
Este repositório preserva a política de uso de IA do template da disciplina:

![Política de uso de IA - semáforo](images/semaforo.png)

| Situação | Significado |
| --- | --- |
| Vermelho - proibido | Atividades de autonomia intelectual, conforme a disciplina. |
| Amarelo - limitado | Ferramenta auxiliar com declaração de uso. |
| Verde - permitido | Uso permitido conforme as orientações da atividade. |

**Houve uso de IA:** sim, ChatGPT/Codex, para sugestões/revisão dos documentos, modelos e protótipos. O tema Agenda ao Ar Livre foi escolhido por Luca Romariz. A validação e a adoção das propostas cabem aos integrantes.

## 12. Contribuição e fluxo de trabalho
main guarda a versão para avaliação. Usar branches docs/nome, feat/nome e fix/nome. Cada integrante faz suas alterações com a própria conta e pede revisão ao colega. Exemplos: docs: revisa regras de inscrição; feat: adiciona cadastro de locais.

[Backlog](docs/planejamento/backlog.csv) · [Planejamento](docs/planejamento/planejamento.md) · [Checklist de submissão](docs/planejamento/submissao.md)

Repositório do grupo: [Agenda ao Ar Livre](https://github.com/lucaRomariz/agenda-ao-ar-livre), preparado a partir do template oficial. Cada integrante deve registrar suas contribuições reais e conferir o acesso dos colaboradores antes da entrega.

## 13. Histórico de versões
| Versão | Data | Descrição |
| --- | --- | --- |
| 0.1 - proposta | 2026-10-04 | Pacote de documentação e protótipos da fase 1; revisão humana e publicação pendentes. |
| 0.1 - revisão documental | 2026-10-05 | Matrícula de Luca, declaração de assistência e remoção dos arquivos auxiliares de preparação. |

## 14. Limitações e próximos passos
- Backend, persistência, integração real, deploy e segurança ainda não implementados.
- Protótipos usam dados fictícios e estado temporário.
- Sem pagamentos, mapas, chat, notificações, recorrência ou lista de espera.
- Confirmar contas GitHub, responsabilidades e prazo da fase 2; informar matrículas se exigidas.
- Revisar pacote com ambos, publicar, gerar contribuições reais e registrar tag da entrega.

## 15. Licença, referências e contato
Licença de redistribuição ainda não definida pelo grupo; nenhuma licença foi presumida para os materiais institucionais. Material preparado para avaliação acadêmica. Símbolo visual criado para este projeto com auxílio de IA; imagem semáforo preservada do template, de autoria externa.

### Documentação complementar
- [Índice em PDF](docs/README.pdf)
- [Visão](docs/visao/visao.pdf)
- [Casos de uso](docs/modelagem/casos-de-uso/especificacoes-casos-de-uso.pdf)
- [Arquitetura](docs/arquitetura/arquitetura.pdf)
- [Classes](docs/modelagem/classes/diagrama-de-classes.pdf)
- [DER](docs/modelagem/banco-de-dados/diagrama-er.pdf)
- [Modelo lógico](docs/modelagem/banco-de-dados/modelo-logico.pdf)
- [Contrato API](docs/api/contrato-api.pdf)
- [Integração externa](docs/api/integracao-externa.pdf)
- [Identidade/protótipos](docs/prototipos/identidade-e-prototipos.pdf)
- [Planejamento](docs/planejamento/planejamento.pdf)

### Referências
- [Template oficial de Felippe Pires Ferreira](https://github.com/Felippe-Pires/template_projects), commit ce21fdb96f2bebb6756dab70bc82ea39a1d93bd7.
- Enunciado "Desenvolvimento de Aplicação Web com Python e Django", fornecido pelo usuário.
- [Open-Meteo: documentação](https://open-meteo.com/en/docs) e [termos](https://open-meteo.com/en/terms), consultados em 04/10/2026.
- [Django](https://docs.djangoproject.com/) e [Django REST Framework](https://www.django-rest-framework.org/).
- [OpenAPI 3.0.3](https://spec.openapis.org/oas/v3.0.3).


