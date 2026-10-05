# Plano de integração externa
Agenda ao Ar Livre | Open-Meteo | Consulta documental em 04/10/2026

## Finalidade
Apresentar resumo meteorológico diário na página da atividade e pela API própria. O organizador usa essa informação para decidir manualmente se mantém ou cancela a atividade. Participantes consultam o mesmo resumo para se planejar. Não calcular previsão nem inventar dados ausentes.

## Serviço e documentação
Provedor: Open-Meteo. Endpoint HTTPS: https://api.open-meteo.com/v1/forecast. Documentação: https://open-meteo.com/en/docs. Termos: https://open-meteo.com/en/terms. Acesso gratuito não comercial sem chave; reavaliar condições antes da publicação e atribuir a fonte com link em toda exibição.

A documentação permite solicitar até 16 dias (padrão: 7). A implementação adotará deliberadamente horizonte conservador de 7 dias, incluindo hoje (hoje a hoje+6), verificando se a data efetivamente veio na resposta. Fora dessa janela retorna fora_do_horizonte sem chamada. Atividades passadas não usam previsão histórica.

## Requisição planejada
GET /v1/forecast com latitude e longitude do Local, daily=temperature_2m_min,temperature_2m_max,precipitation_probability_max,weather_code, timezone=America/Sao_Paulo, forecast_days=7, temperature_unit=celsius.

Exemplo ilustrativo de coordenadas de local público, não localização de usuário:

```text
https://api.open-meteo.com/v1/forecast?latitude=-23.5874&longitude=-46.6576&daily=temperature_2m_min,temperature_2m_max,precipitation_probability_max,weather_code&timezone=America%2FSao_Paulo&forecast_days=7&temperature_unit=celsius
```

## Dados utilizados
| Campo externo | Uso no sistema |
| --- | --- |
| daily.time | Selecionar exatamente a data local da atividade. |
| temperature_2m_min / max | Exibir mínima e máxima diária em graus Celsius. |
| precipitation_probability_max | Exibir probabilidade máxima diária de precipitação, em porcentagem. |
| weather_code | Traduzir código WMO para condição; código desconhecido produz descrição não disponível. |
| daily_units | Validar unidades esperadas antes de exibir. |

Os valores correspondem ao dia inteiro, não especificamente ao horário do encontro. consultado_em é o horário de obtenção pelo nosso servidor, não o horário de geração do modelo meteorológico. Respostas de exemplo nos documentos e protótipos são fictícias.

## Robustez
1. Validar coordenadas no cadastro e usar URL fixa do provedor, nunca URL informada pelo cliente.
2. Consultar cache por latitude, longitude, data e fuso; TTL de 1.800 segundos.
3. Em falta de cache, usar timeout de conexão de 2 s e leitura de 3 s; sem retry automático no mesmo pedido. Tempo total alvo 5 s; configurar também prazo de resposta no servidor.
4. Validar HTTP, JSON, arrays de mesmo tamanho, data desejada, unidades e números finitos; rejeitar mínimo maior que máximo e probabilidade fora de 0..100.
5. Valores nulos ou incompletos geram indisponivel; manter a página e todas as operações de inscrição acessíveis.
6. Erros 429 respeitam Retry-After quando válido; aplicar cache negativo de pelo menos 60 s, sem dormir na requisição. Timeout/5xx/JSON inválido também usam 60 s de cache negativo.
7. Cache expirado não é apresentado como previsão atual; sem resposta nova, mostrar indisponível.
8. Registrar tipo de erro e duração; não registrar credenciais ou dados de participantes.

## Limites e licença
Na consulta de 04/10/2026, os termos gratuitos indicam menos de 10.000 chamadas/dia, 5.000/hora e 600/minuto; a tabela também indica 300.000/mês. Uso não comercial e atribuição CC BY 4.0. O projeto adotará orçamento operacional inferior aos limites, com cache e contagem de chamadas; revisar termos no deploy.

Atribuição na interface: Dados meteorológicos: Open-Meteo (CC BY 4.0), com links ao provedor e à licença https://creativecommons.org/licenses/by/4.0/. O resumo é uma transformação dos campos originais.

## Testes planejados
Resposta válida; data ausente; horizonte excedido; JSON inválido; campo nulo; arrays inconsistentes; timeout; 429; 5xx; cache hit; expiração. Usar mocks determinísticos para erros e uma demonstração real da integração na fase 2. Esta fase verificou documentação, não comprova execução do serviço integrado.
