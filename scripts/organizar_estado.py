#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Organiza um zip BRUTO de orcamentos do Cilia conforme o METODO (por estado/operador).
Requer: pip install pymupdf   (e lib_classificacao.py na mesma pasta)

Uso:
    python organizar_estado.py <ESTADO> "<zip_bruto>" "<pasta_saida>"

ESTADO (sigla):
    MT  MS  CE  PE  PB  AL  MA  PA  PI  RN  BA  SE

Regras completas: ver METODO-ORGANIZACAO-ORCAMENTOS.md
Cada PDF: extraimos a CIDADE da oficina e o TIPO (CARRO/MOTO/CAMINHAO). Sprinter=CAMINHAO.
Destino None = APAGAR (nao entra na saida).
"""
import sys, os, glob, shutil, zipfile, tempfile
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import fitz
from lib_classificacao import norm, classify, city_of
from collections import Counter

# nome do estado p/ regex de cidade ("- CIDADE - <Estado> CEP")
NOME = {
 'MT':'Mato Grosso', 'MS':'Mato Grosso do Sul', 'CE':'Cear[aá]', 'PE':'Pernambuco',
 'PB':'Para[ií]ba', 'AL':'Alagoas', 'MA':'Maranh[aã]o', 'PA':'Par[aá]',
 'PI':'Piau[ií]', 'RN':'Rio Grande do Norte', 'BA':'Bahia', 'SE':'Sergipe',
}

# conjuntos de cidades (sempre em MAIUSCULO, sem acento)
FORTALEZA='FORTALEZA'; SOBRAL='SOBRAL'; PETROLINA='PETROLINA'; PICOS='PICOS'
SAO_LUIS='SAO LUIS'; IMPERATRIZ='IMPERATRIZ'
BA_JAIME={'BRUMADO','GUANAMBI'}
BA_BRUNO={'FEIRA DE SANTANA','SANTO ANTONIO DE JESUS'}
BA_IVAN={'SENHOR DO BONFIM'}

def destino(ESTADO, tipo, city):
    """Retorna o caminho relativo de destino (lista de pastas) ou None para APAGAR."""
    E=ESTADO
    if E in ('MT','MS'):
        return ['CAMINHAO' if tipo=='CAMINHAO' else 'PEQUENOS']
    if E=='CE':
        if tipo=='CAMINHAO': return ['VIDAL', city]
        if city==FORTALEZA:
            return ['JOEL'] if tipo=='MOTO' else None          # carro de Fortaleza = APAGAR
        if city==SOBRAL: return ['AMORIM', tipo]               # CARRO/MOTO
        return ['IVANILSON', city]                             # interior: so por cidade
    if E=='PE':
        if tipo=='CAMINHAO':
            return None if city==PETROLINA else ['ANDRE', city]  # caminhao Petrolina = APAGAR
        if city==PETROLINA: return ['IVANILSON', tipo]           # CARRO/MOTO
        return ['GUTO', city]
    if E=='PB':
        return ['ANDRE', city] if tipo=='CAMINHAO' else ['GUTO', city]
    if E=='AL':
        return ['ANDRE', city] if tipo=='CAMINHAO' else ['CRISTIANO', city]
    if E=='MA':
        if city==SAO_LUIS: return ['FELIPE', tipo]
        if city==IMPERATRIZ: return ['JUNIOR', tipo]
        return None                                            # resto = APAGAR
    if E=='PA':
        return ['JONAS', tipo, city]
    if E=='PI':
        if city==PICOS:
            return None if tipo=='CAMINHAO' else ['AMORIM', tipo]  # caminhao Picos = APAGAR
        return ['RUAN', tipo, city]
    if E=='RN':
        return ['ANDRE', city] if tipo=='CAMINHAO' else ['NIVARDO', city]
    if E=='BA':
        if tipo=='CAMINHAO': return None                       # caminhao BA = APAGAR
        if city in BA_JAIME: return ['JAIME']                  # tudo junto numa pasta
        if city in BA_BRUNO: return ['BRUNO', tipo]            # CARRO/MOTO
        if city in BA_IVAN: return ['IVANILSON', tipo]         # CARRO/MOTO
        return ['BRUNO RALF', city]
    if E=='SE':
        return None if tipo=='CAMINHAO' else ['BRUNO RALF', city]
    raise SystemExit('Estado nao reconhecido: '+E)

def main():
    if len(sys.argv)!=4:
        raise SystemExit('Uso: python organizar_estado.py <ESTADO> "<zip>" "<saida>"')
    ESTADO, ZIP, OUT = sys.argv[1].upper(), sys.argv[2], sys.argv[3]
    if ESTADO not in NOME: raise SystemExit('ESTADO invalido. Use: '+', '.join(NOME))
    src=tempfile.mkdtemp()
    with zipfile.ZipFile(ZIP) as z: z.extractall(src)
    pdfs=sorted(glob.glob(os.path.join(src,'**','*.pdf'),recursive=True))
    if os.path.exists(OUT): shutil.rmtree(OUT)

    tc=Counter(); apagados=0; semcidade=0; total=0
    for f in pdfs:
        d=fitz.open(f); t=norm(d[0].get_text()); d.close()
        tipo=classify(t); city=city_of(t, NOME[ESTADO]); base=os.path.basename(f)
        if city=='SEM CIDADE': semcidade+=1
        rel=destino(ESTADO, tipo, city)
        total+=1
        if rel is None:
            apagados+=1; continue
        dest=os.path.join(OUT, *rel)
        os.makedirs(dest, exist_ok=True)
        shutil.copy2(f, os.path.join(dest, base))
        tc[tipo]+=1

    print('ESTADO:', ESTADO)
    print('total lidos:', total, '| organizados:', sum(tc.values()),
          '| apagados(regra):', apagados, '| sem_cidade:', semcidade)
    print('tipos organizados:', dict(tc))

if __name__=='__main__':
    main()
