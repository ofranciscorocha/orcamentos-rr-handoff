# Método de Organização de Orçamentos — Recicladora Rocha (Cilia / Bradesco)

Regra única para emitir e organizar os orçamentos por estado. **Entrega = 1 zip por estado.**
Dentro do zip, as **pastas de primeiro nível são os operadores** (ou os tipos, quando há um
operador só). Valem os 6 tipos de conclusão "emitíveis" (4× Autorizado + Finalização
Automática + Supervisão); o resto não entra.

Classificação de veículo: CARRO / MOTO / CAMINHÃO. **Mercedes Sprinter = CAMINHÃO.**

Convenções:
- "Dividir por carro e moto" = pastas **CARRO** e **MOTO**.
- "Por cidade" = subpastas por cidade.
- Quando vale os dois, a ordem é **TIPO → cidade** (tipo primeiro, cidade dentro).

---

## Carlinhos — Mato Grosso (MT) e Mato Grosso do Sul (MS)
Operador único: **Carlinhos** (cobre os dois estados). **Não divide por cidade.**

- `MATO GROSSO/PEQUENOS` — carros + motos
- `MATO GROSSO/CAMINHAO` — só caminhão (Sprinter = caminhão)
- `MATO GROSSO DO SUL/PEQUENOS` — carros + motos
- `MATO GROSSO DO SUL/CAMINHAO` — só caminhão

---

## Ceará (CE)
- `VIDAL/` — **todos os caminhões** do CE, **por cidade**
- `JOEL/` — **motos de Fortaleza**
- `AMORIM/` — **Sobral**, dividido em **CARRO** e **MOTO**
- `IVANILSON/` — carro + moto do CE inteiro **exceto Fortaleza e Sobral**, **só por cidade**
  (não separa carro/moto)
- **Carros de Fortaleza → APAGAR.**

---

## Pernambuco (PE) e Paraíba (PB)
- `GUTO/` — PE + PB **carro e moto**, **por cidade**, **exceto Petrolina**
- `ANDRE/` — PE + PB **caminhão**, **por cidade**, **exceto Petrolina**
- `IVANILSON/` — **Petrolina**, dividido em **CARRO** e **MOTO**
- **Caminhão de Petrolina → APAGAR.**

---

## Alagoas (AL)
- `CRISTIANO/` — AL **carro e moto**, **por cidade**
- `ANDRE/` — AL **caminhão**, **por cidade**

---

## Maranhão (MA)
- `FELIPE/` — **São Luís**, dividido em **CARRO / MOTO / CAMINHAO**
- `JUNIOR/` — **Imperatriz**, dividido em **CARRO / MOTO / CAMINHAO**
- **Resto do Maranhão (fora de São Luís e Imperatriz) → APAGAR.**

---

## Pará (PA)
- `JONAS/` — Pará inteiro, **CARRO / MOTO / CAMINHAO**, **por cidade**

---

## Piauí (PI)
- `RUAN/` — Piauí **exceto Picos**, **CARRO / MOTO / CAMINHAO**, **por cidade**
- `AMORIM/` — **Picos**, dividido em **CARRO** e **MOTO**
- **Caminhão de Picos → APAGAR.**

---

## Rio Grande do Norte (RN)
- `NIVARDO/` — RN **carro e moto**, **por cidade**
- `ANDRE/` — RN **caminhão**, **por cidade**

---

## Bahia (BA)
- `BRUNO RALF/` — Bahia inteira **carro e moto**, **por cidade**, **exceto** as cidades abaixo
- `JAIME/` — **Brumado** e **Guanambi**, carro e moto **numa pasta só** (sem separar tipo, sem cidade)
- `BRUNO/` — **Feira de Santana** e **Santo Antônio de Jesus**, dividido em **CARRO** e **MOTO**
- `IVANILSON/` — **Senhor do Bonfim**, dividido em **CARRO** e **MOTO**
- **Caminhão da Bahia → APAGAR.**

---

## Sergipe (SE)
- `BRUNO RALF/` — SE **carro e moto**, **por cidade**
- **Caminhão de Sergipe → APAGAR.**

---

# Operadores que se repetem (referência)
- **André** — caminhão de PE/PB, AL e RN
- **Ivanilson** — CE (interior), Petrolina (PE), Senhor do Bonfim (BA)
- **Amorim** — Sobral (CE), Picos (PI)
- **Bruno Ralf** — Bahia e Sergipe

Entrega sempre **por estado** (1 zip por estado, com as pastas dos operadores dentro).
