# Contrato inicial da API REST
Agenda ao Ar Livre | v1 | Proposta para fase 2

## Escopo e autenticação
API própria pública de consulta, implementada com Django REST Framework. Base local prevista: http://localhost:8000/api/v1/. URL de produção ainda não definida. Arquivo legível por ferramentas: openapi.json (OpenAPI 3.0.3).

Não é necessário login ou token para GET. Escritas de conta, local, atividade e inscrição serão feitas pelas views web com sessão e CSRF; elas não são rotas da API pública v1. Essa decisão atende ao requisito de consulta por terceiros e reduz exposição.

## Endpoints
| Método e rota | Finalidade |
| --- | --- |
| GET /atividades/ | Catálogo paginado; exclui rascunhos, inclui publicada/cancelada. |
| GET /atividades/{id}/ | Detalhe público, sem dados pessoais de participantes. |
| GET /atividades/{id}/previsao/ | Resumo diário ou estado fora_do_horizonte/indisponivel. |
| GET /categorias/ | Lista de categorias, ordenada por nome; sem paginação nesta versão. |

Paths relativos à base /api/v1/. Barras finais fazem parte do contrato. Métodos de escrita retornam 405; HEAD e OPTIONS seguem suporte padrão do framework.

## Filtros e paginação
Catálogo: q (texto até 120 caracteres em título/descrição), cidade (texto até 120, correspondência sem diferenciar maiúsculas), categoria (id inteiro positivo), data_inicio e data_fim (YYYY-MM-DD, limites inclusivos sobre a data de início em America/Sao_Paulo), situacao (publicada ou cancelada), page (>=1), page_size (1..100, padrão 20). Filtros combinados por AND. Sem datas, inclui eventos passados e futuros; sem situação, inclui ambas as públicas. Ordenação fixa: inicio, id.

Data inicial maior que final ou formato inválido: 400. Categoria válida sem resultados: lista vazia. Página positiva além da última: 404, exceto page=1 sem registros, que retorna lista vazia. Parâmetro desconhecido: 400 para evitar consultas silenciosamente incorretas.

## Exemplo de consulta
```text
GET /api/v1/atividades/?cidade=São%20Paulo&data_inicio=2026-10-01&data_fim=2026-10-31&page=1&page_size=20
Accept: application/json
```

```json
{"count":1,"next":null,"previous":null,"results":[{"id":1,"titulo":"Caminhada no parque","descricao":"Encontro gratuito para caminhada leve.","inicio":"2026-10-10T08:00:00-03:00","termino":"2026-10-10T10:00:00-03:00","capacidade":20,"vagas":8,"situacao":"publicada","encerrada":false,"motivo_cancelamento":"","categoria":{"id":1,"nome":"Caminhada"},"local":{"id":1,"nome":"Parque Ibirapuera","endereco":"Av. Pedro Álvares Cabral, portão de encontro a confirmar","cidade":"São Paulo","uf":"SP","latitude":-23.5874,"longitude":-46.6576}}]}
```

Dados acima são exemplos fictícios, não evento real. O detalhe retorna o mesmo objeto de results, sem envelope. next/previous são URLs ou null. Datas incluem offset; encerrada deriva de termino <= agora. Não serializar organizador, e-mail, senha, lista de inscritos nem campos técnicos.

## Exemplo de previsão normalizada
```json
{"atividade_id":1,"data":"2026-10-10","estado":"disponivel","min_c":17.0,"max_c":26.0,"probabilidade_chuva_pct":30,"codigo_wmo":2,"descricao":"Parcialmente nublado","consultado_em":"2026-10-04T14:00:00-03:00","fonte":"Open-Meteo","url_fonte":"https://open-meteo.com/","mensagem":"Resumo do dia inteiro; não representa apenas o horário da atividade."}
```

Nos estados indisponivel ou fora_do_horizonte, todos os campos meteorológicos e consultado_em são null; mensagem explica o motivo. Mantêm-se atividade_id, data, fonte e url_fonte. A resposta é 200 porque o estado da previsão foi consultado corretamente. Atividade inexistente ou rascunho retorna 404.

## Erros e códigos HTTP
| Código | Significado |
| --- | --- |
| 200 | Consulta concluída, inclusive lista vazia ou previsão indisponível. |
| 400 | Filtros, formato, parâmetros desconhecidos ou valores inválidos. |
| 404 | Atividade pública inexistente, id inacessível ou página fora do intervalo. |
| 405 | Método não aceito; incluir cabeçalho Allow. |
| 429 | Limite de consulta excedido; incluir Retry-After em segundos. |
| 500 | Falha interna genérica; não expor traceback. |

```json
{"erro":{"codigo":"parametros_invalidos","mensagem":"Revise os filtros informados.","campos":{"data_fim":["Deve ser igual ou posterior à data inicial."]}}}
```

Outros códigos de erro: nao_encontrado, metodo_nao_permitido, limite_excedido, erro_interno. campos é um objeto vazio quando não há erro de campo. Implementar exception handler DRF para esse envelope; não presumir que seja formato padrão do framework.

## Condições de uso
Limite inicial proposto: 60 requisições/minuto por IP, ajustável no ambiente. Não há SLA. Usar cache local no cliente e respeitar Retry-After. Content-Type application/json; UTF-8; não configurar CORS amplo por padrão. CORS não impede clientes servidor-servidor. Um cliente web de outro domínio exigirá decisão explícita na fase 2.

## Verificação futura
Importar openapi.json em ferramenta compatível; verificar catálogo, filtros, paginação, rascunho inacessível, erro uniforme, limite e indisponibilidade meteorológica. Os endpoints estão especificados, ainda não implementados.
