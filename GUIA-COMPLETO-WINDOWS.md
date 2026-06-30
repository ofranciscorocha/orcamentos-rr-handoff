# Guia Completo — Emitir e Organizar Orçamentos do Cilia no Windows

Este guia ensina, do zero, a fazer no **Windows** o mesmo processo que rodamos: emitir os
orçamentos do Cilia e organizá-los pelas regras de cada estado (ver
`METODO-ORGANIZACAO-ORCAMENTOS.md`).

Há **dois caminhos**. Escolha um:
- **Caminho A (recomendado): manual + script.** Funciona em qualquer Windows, só precisa do
  Chrome e do Python. É o mais simples e confiável.
- **Caminho B: com o Claude Desktop (Cowork) + extensão Claude in Chrome.** O Claude dirige
  o navegador e roda o organizador sozinho, como fizemos. Exige plano pago do Claude.

---

## Pré-requisitos (uma vez só)

### 1. Google Chrome
Instale o Chrome no Windows. É nele que você loga no Cilia.

### 2. Python 3 + biblioteca de PDF
1. Baixe o Python em https://www.python.org/downloads/windows/ e instale
   **marcando a opção "Add python.exe to PATH"**.
2. Abra o **Prompt de Comando** (tecla Windows → digite `cmd` → Enter) e rode:
   ```
   pip install pymupdf
   ```

### 3. Esta pasta
Descompacte este pacote numa pasta fácil, por exemplo `C:\orcamentos`. Dentro tem:
```
METODO-ORGANIZACAO-ORCAMENTOS.md   <- as regras (a fonte da verdade)
01-GUIA-CILIA.md                   <- detalhes técnicos do Cilia
GUIA-COMPLETO-WINDOWS.md           <- este arquivo
scripts\cilia_emitir_navegador.js  <- emissor (cola no console do Chrome)
scripts\organizar_estado.py        <- organizador (roda no Python)
scripts\lib_classificacao.py       <- classificador de veículo/cidade
```

---

## CAMINHO A — Manual + Script (recomendado)

### Passo 1 — Logar no Cilia
No Chrome, acesse **https://sistema.cilia.com.br** e faça login (com o MFA).
A sessão cai por inatividade e ~19h; se cair, relogar.

### Passo 2 — Abrir o Console do Chrome
Com a aba do Cilia aberta, aperte **F12** (ou `Ctrl+Shift+J`) e vá na aba **Console**.

> Se aparecer um aviso vermelho de "não cole nada aqui", digite `allow pasting` e Enter
> uma vez — aí o Chrome libera colar.

### Passo 3 — Carregar o emissor
Abra `scripts\cilia_emitir_navegador.js` no Bloco de Notas, **copie tudo**, cole no Console
e aperte **Enter**. Deve aparecer: `Pronto. Ex.: emitirCilia(...)`.

### Passo 4 — Emitir o estado
Cole o comando do estado/período e Enter. Exemplos:
```js
emitirCilia(20, "01/06/2026", "28/06/2026", "RIO GRANDE DO NORTE")
emitirCilia(6,  "01/06/2026", "28/06/2026", "CEARA")
emitirCilia(5,  "01/06/2026", "28/06/2026", "BAHIA")
```
(IDs dos estados estão no `01-GUIA-CILIA.md`. **MT=11, MS=12, CE=6, PE=17, PB=15, AL=2,
MA=10, PA=14, PI=18, RN=20, BA=5, SE=26**.)

Acompanhe digitando `window.__job` e Enter (repita). As fases são
`enum → download → zip → done`. Quando chegar em **done**, o zip
`<ESTADO> dd.mm.aaaa - dd.mm.aaaa (bruto).zip` baixa sozinho na pasta **Downloads**.

> Se aparecer muito `fail` ou erro no `enum`, a sessão caiu — relogue e rode de novo.

### Passo 5 — Organizar
No Prompt de Comando, vá até a pasta dos scripts e rode (troque a sigla do estado e os
caminhos). A sigla é a do **METODO** (MT, MS, CE, PE, PB, AL, MA, PA, PI, RN, BA, SE):
```
cd C:\orcamentos\scripts
python organizar_estado.py RN "C:\Users\SEU_USUARIO\Downloads\RIO GRANDE DO NORTE 01.06.2026 - 28.06.2026 (bruto).zip" "C:\orcamentos\saida\RN"
```
O script imprime um resumo (tipos, apagados pela regra, sem_cidade) e cria a pasta
`saida\RN` já organizada pelos operadores. Confira e zipe a pasta `saida\RN` para enviar.

> Atenção: o `organizar_estado.py` aplica a regra do estado automaticamente (quem recebe o
> quê, o que é apagado). Se uma regra mudar, ajuste primeiro o `METODO` e depois o script.

---

## CAMINHO B — Claude Desktop (Cowork) + extensão Claude in Chrome

Exige: app **Claude Desktop** (Windows) com **modo Cowork** (plano Pro/Max/Team/Enterprise)
e a extensão **Claude in Chrome** instalada e conectada.

1. Logue no Cilia no Chrome (Passo 1 acima).
2. No Claude Desktop (Cowork), conecte esta pasta como pasta de trabalho e diga, por exemplo:
   *"Emita o RN de 01/06 a 28/06 pelo Cilia e organize pela regra do RN."*
3. O Claude usa a extensão para enumerar/baixar os PDFs na sua sessão logada, você **sobe o
   zip bruto** no chat (ou aponta a pasta Downloads), e ele roda o `organizar_estado.py`
   e devolve o zip organizado.

> Observação importante: o app do Claude **não** existe no iPad/celular com Cowork — só em
> Windows e macOS. No iPad o Chrome não aceita extensão. Por isso este processo é de desktop.

---

## Checklist rápido por emissão
1. Logado no Cilia? (senão, relogar)
2. Console aberto → emissor carregado → `emitirCilia(ID, inicio, fim, "NOME")`
3. `window.__job` chegou em `done`, 0/poucos fails?
4. `python organizar_estado.py <SIGLA> "<zip bruto>" "<saida>"`
5. Conferir o resumo e a árvore de pastas → zipar a saída → enviar.
