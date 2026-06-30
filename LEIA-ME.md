# Orçamentos Cilia — Pacote de Handoff (Windows)

Pacote para **emitir e organizar os orçamentos do Cilia (Bradesco)** num desktop Windows,
seguindo as regras da Recicladora Rocha.

## Por onde começar
1. Leia o **GUIA-COMPLETO-WINDOWS.md** — passo a passo de instalação e uso (do zero).
2. **METODO-ORGANIZACAO-ORCAMENTOS.md** — as regras de organização por estado/operador
   (a fonte da verdade; o organizador segue exatamente isto).
3. **01-GUIA-CILIA.md** — detalhes técnicos do Cilia (API, filtros, IDs, rate limit).

## Conteúdo
```
LEIA-ME.md
GUIA-COMPLETO-WINDOWS.md
METODO-ORGANIZACAO-ORCAMENTOS.md
01-GUIA-CILIA.md
scripts/
  cilia_emitir_navegador.js   - cola no Console do Chrome (logado no Cilia): baixa 1 zip bruto
  organizar_estado.py         - organiza o zip bruto pela regra do estado
  lib_classificacao.py        - classifica veículo (CARRO/MOTO/CAMINHÃO) e extrai a cidade
```

## Resumo de 1 minuto
1. Logar no Cilia no Chrome (tem MFA).
2. Console do Chrome → colar `cilia_emitir_navegador.js` → rodar
   `emitirCilia(ID, "inicio", "fim", "NOME")` → baixa o zip bruto.
3. `python organizar_estado.py <SIGLA> "<zip bruto>" "<saida>"` → pasta organizada.

## Siglas dos estados (organizador) e IDs (emissor)
| Estado | Sigla (script) | ID (emitirCilia) |
|---|---|---|
| Mato Grosso | MT | 11 |
| Mato Grosso do Sul | MS | 12 |
| Ceará | CE | 6 |
| Pernambuco | PE | 17 |
| Paraíba | PB | 15 |
| Alagoas | AL | 2 |
| Maranhão | MA | 10 |
| Pará | PA | 14 |
| Piauí | PI | 18 |
| Rio Grande do Norte | RN | 20 |
| Bahia | BA | 5 |
| Sergipe | SE | 26 |

> O Claude **não** tem login no Cilia — quem baixa os PDFs é o navegador, na sua sessão
> logada. Depois o organizador roda localmente no Python.
