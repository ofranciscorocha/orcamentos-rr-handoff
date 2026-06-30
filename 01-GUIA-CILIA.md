# Guia Técnico — Cilia (Bradesco Seguros)

Acessamos o Cilia como empresa terceirizada para coletar os orçamentos de sinistro
automotivo das oficinas credenciadas. Login é manual (com MFA). A sessão expira por
inatividade e diariamente por volta das 19h — quando cai, refazer o login.

## 1. Enumeração (API JSON)
`GET https://sistema.cilia.com.br/api/surveys/search.json` (com os cookies da sessão), parâmetros:

```
page=1                                            # ~20 itens por página; paginar até vir vazio
search_filters[date_type]=scheduling              # data de Agendamento
search_filters[date_range][start_date]=01/06/2026 # dd/mm/aaaa
search_filters[date_range][end_date]=28/06/2026
search_filters[order_option]=scheduling_older
search_filters[state_id][]=20                     # ID do estado (ver tabela)
search_filters[status_ids][]=analyzed             # status "Analisado"
```

Cada item traz: `surveyable_id`, `insurer_budget.number_with_version` (nº do orçamento),
`insurer_budget.license_plate`, `insurer_budget.workshop_name`,
`insurer_budget.current_conclusion_title`, `current_status`.

### ARMADILHA IMPORTANTE (resolvida)
NÃO mande `search_filters[conclusion_type_ids][]=...` na query — com esse filtro o
servidor **estoura o tempo (timeout)** em consultas grandes. Em vez disso:
- consulte só com `status_ids=analyzed` (rápido),
- e **filtre os tipos de conclusão NO CLIENTE** pelo campo `current_conclusion_title`.

### Os 6 tipos de conclusão que "emitimos"
4 variantes de "Autorizado" + "CILIA - Finalização Automática" + "Supervisão".
Regra (sobre o título, maiúsculo/sem acento de comparação):
```
título começa com "AUTORIZADO"  OU  contém "FINALIZAÇÃO AUTOMÁTICA"  OU  == "SUPERVISÃO"
```
Tudo o que fica de fora (Indenização Integral, Cancelado, Não Realizada, Não Autorizado,
Abaixo da Franquia, Constatação, Acordo, etc.) NÃO entra.

## 2. PDF do orçamento
`GET https://sistema.cilia.com.br/budgets/{surveyable_id}/report.pdf` → PDF do orçamento.
(O `/report` sem `.pdf` devolve HTML — não use; use sempre `.pdf`.)
PDF válido começa com `%PDF` e tem > 20 KB (abaixo disso = página de login/sessão caída).

## 3. Fotos da vistoria (quando preciso)
`GET https://sistema.cilia.com.br/budgets/{surveyable_id}/photos.json` → array de fotos.
As fotos NÃO são rotuladas, então não dá para separar automaticamente — precisa olhar.

## 4. IDs dos estados
AC=1 AL=2 AP=3 AM=4 BA=5 CE=6 DF=7 ES=8 GO=9 MA=10 MT=11 MS=12 MG=13 PA=14 PB=15
PR=16 PE=17 PI=18 RJ=19 RN=20 RS=21 RO=22 RR=23 SC=24 SP=25 SE=26 TO=27

## 5. Limite de requisições (rate limit) — lições aprendidas
- O endpoint `report.pdf` devolve **HTTP 429** sob carga. Use **concorrência baixa (2)**
  com backoff (espera crescente). Concorrência alta = quase tudo 429.
- Há um limite **cumulativo por sessão/IP**: depois de ~1.200–2.400 PDFs numa sessão,
  o servidor passa a segurar. **Refazer o login** (sessão nova) reseta o limite.
- O `search.json` também trava se for martelado; espace as tentativas.
- Volume típico: Ceará ~400–500, Bahia ~1.800–2.600, Sergipe ~300, Piauí ~120–180,
  RN ~90–180, Maranhão ~160–230, Pará ~150–250 (varia com o período).

## 6. Como o zip chega ao organizador
O navegador monta **1 zip "bruto"** e baixa para a pasta Downloads. Depois você roda o
`organizar_estado.py` apontando para esse zip (ver GUIA-COMPLETO-WINDOWS.md).
