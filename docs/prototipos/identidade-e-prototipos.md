# Identidade visual e protótipos
Agenda ao Ar Livre | Fase 1

## Conceito
Uma agenda para encontrar pessoas e ocupar espaços abertos. Assinatura: "Seu próximo encontro começa lá fora." O símbolo original combina montanha/trilha e sol dentro de um calendário; SVG vetorial editável em images/logo.svg. Não utiliza imagens externas ou marca de terceiros.

## Paleta e tipografia
| Token | Cor e uso |
| --- | --- |
| Verde principal | #174C3C: títulos, botões e navegação. |
| Verde suave | #E8F1E9: estados positivos e superfícies. |
| Fundo | #F7F6F0: base da página. |
| Texto | #20312B: texto principal. |
| Texto secundário | #52615A: metadados. |
| Acento solar | #F2C66D: ilustrações e destaque com texto escuro. |
| Erro | #A12828: borda e texto de falha, sempre com mensagem. |

Tipografia: pilha system-ui, -apple-system, Segoe UI, sans-serif; sem download externo de fontes. Base 16 px, títulos 28-48 px, espaçamento múltiplo de 4/8 px, cantos de 12-20 px. Foco visível e botões com altura mínima 44 px. Cor não substitui rótulos.

## Telas essenciais
| Tela | Casos / propósito |
| --- | --- |
| Explorar | UC02: filtros, cartões e resultado vazio. |
| Detalhe | UC02-UC03-UC06: informações, previsão diária, vagas e inscrição. |
| Entrar / criar conta | UC01: formulário e validação de campos. |
| Minhas inscrições | UC07-UC08: lista, estado e cancelamento. |
| Organizar | UC05-UC09: lista de atividades e ações do dono. |
| Nova atividade | UC05: local, categoria, horários, capacidade e publicação. |
| Locais | UC04: cadastro de endereço e coordenadas. |
| Relatórios | UC10: período, situação, indicadores e CSV. |

## Arquivos e modo de uso
Abrir index.html em navegador. Fontes editáveis: index.html, styles.css e app.js. A galeria telas.md reúne as oito capturas PNG, também incluídas ao final deste PDF. Protótipo com dados fictícios e interações em memória; não implementa autenticação, backend Django, persistência ou acesso real à previsão. Atualizar a página reinicia a demonstração.

O protótipo simula inscrição/cancelamento, navegação, filtros, cadastro de atividade e exportação demonstrativa. Controles de estados permitem visualizar indisponibilidade meteorológica, fora de horizonte e lotação. Não interpretar a simulação como evidência da fase 2.

## Estados e acessibilidade
Formulários com labels; feedback em região aria-live; foco visível; contraste adequado; grids empilham no celular. Detalhe diferencia publicada, cancelada e lotada. Previsão diferencia disponível, indisponível e fora do horizonte; botão de inscrição permanece disponível quando apenas a previsão falha.

Erros do servidor planejados devem aparecer próximos aos campos e no resumo. Listas vazias explicam a próxima ação. Exclusão/cancelamento exigem confirmação. As telas de referência apresentam dados fictícios e a mesma identidade visual dos documentos.
