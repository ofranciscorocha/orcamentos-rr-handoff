import fitz, unicodedata, re, os, shutil
def norm(s): return unicodedata.normalize('NFKC', s or '')
def deac(s): return ''.join(c for c in unicodedata.normalize('NFD',s) if unicodedata.category(c)!='Mn')
TRUCK_BRANDS={'SCANIA','MAN','DAF','IVECO','IVECO/FIAT','FACCHINI','RANDON','LIBRELATO','GUERRA','NOMA','ROSSETTI','AGRALE'}
PURE_MOTO={'YAMAHA','BAJAJ','ROYAL ENFIELD','AVELLOZ','NIU','SHINERAY','DAFRA','HAOJUE','KASINSKI','KAWASAKI','KTM','HARLEY-DAVIDSON','DUCATI','TRIUMPH','MOTTU','HUSQVARNA','TRAXX','MALAGUTI','APRILIA','VOGE','MOTORINO'}
HONDA_CAR={'HR-V','HRV','WR-V','WRV','CITY','FIT','CIVIC','CR-V','CRV','ACCORD','ZR-V','ZRV'}
SUZUKI_CAR={'S-CROSS','JIMNY','VITARA','SWIFT','SX4','GRAND'}
VOLVO_PRE=('VM','FH','FM','FMX','VNL','NL','NH','FE','FL')
MB_TRUCK=('ATEGO','ACCELO','AXOR','ACTROS','AROCS','ATRON','LINHA L','L-','O-500','OF ','OH ')
def veic_line(t):
    L=t.split('\n')
    for i,l in enumerate(L):
        if l.strip()=='Placa' and i>0: return L[i-1].strip()
    return ''
def classify(t):
    v=veic_line(t);U=v.upper();FU=t.upper();p=[x.strip() for x in v.split(' - ')]
    ma=(p[1] if len(p)>1 else '?').upper().replace('*','').strip();mo=(p[2] if len(p)>2 else '').upper().replace('*','').strip()
    if 'SPRINTER' in FU: return 'CAMINHAO'
    if re.search(r'CAMINH|CARRETA|SEMI-?REBOQUE|\bREBOQUE\b|BASCULANTE|GRANELEIRO|\bPIPA\b',U): return 'CAMINHAO'
    if ma in TRUCK_BRANDS: return 'CAMINHAO'
    if ma=='VOLVO': return 'CAMINHAO' if (mo.split() and mo.split()[0].startswith(VOLVO_PRE)) else 'CARRO'
    if ma in ('MERCEDES-BENZ','MERCEDES','MERCEDES BENZ'): return 'CAMINHAO' if any(mo.startswith(k) or k in mo for k in MB_TRUCK) else 'CARRO'
    if ma in ('VOLKSWAGEN','VW'):
        if any(k in mo for k in ('CONSTELLATION','DELIVERY','WORKER','METEOR','VOLKSBUS')) or re.match(r'\d{1,2}\.\d{3}',mo): return 'CAMINHAO'
        return 'CARRO'
    if 'MOTOCICLETA' in FU: return 'MOTO'
    if ma in PURE_MOTO: return 'MOTO'
    if ma=='HONDA': return 'CARRO' if any(mo.startswith(k) for k in HONDA_CAR) else 'MOTO'
    if ma=='SUZUKI': return 'CARRO' if any(mo.startswith(k) for k in SUZUKI_CAR) else 'MOTO'
    if ma=='BMW': return 'MOTO' if re.match(r'^(G|R|F|S|K|C)\s?\d',mo) else 'CARRO'
    return 'CARRO'
def city_of(t, state_name):
    rx=re.compile(r'-\s*([^-\n]+?)\s*-\s*'+state_name+r'\s+CEP', re.IGNORECASE)
    m=rx.search(' '.join(t.split('\n')))
    c=deac(m.group(1).strip()).upper().strip() if m else 'SEM CIDADE'
    return re.sub(r'\s+',' ',c) or 'SEM CIDADE'
