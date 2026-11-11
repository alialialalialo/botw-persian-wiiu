import unicodedata
ZWNJ,ZWJ=0x200c,0x200d
# joining classes: D dual, R right-only
R_ONLY=set(map(ord,'آأإاةدذرزژوؤى')); 
DUAL=set(map(ord,'بپتثجچحخسشصضطظعغفقکگلمنهیئكي'))
TAGJ='U'
def jtype(c):
    if c==0xFFFF: return TAGJ
    if c==0x640: return 'D'
    if 0x64b<=c<=0x65f or c==0x670: return 'T'
    if c==ZWJ: return 'J'
    if c in R_ONLY: return 'R'
    if c in DUAL: return 'D'
    return 'U'
# presentation tables (isolated, final, initial, medial) from Unicode data
FORM={}
for cp in list(range(0xfb50,0xfe00))+list(range(0xfe70,0xff00)):
    dc=unicodedata.decomposition(chr(cp))
    if dc.startswith('<') and ' ' in dc:
        t=dc.split(' '); k=t[0].strip('<>')
        if len(t)==2 and k in('isolated','final','initial','medial'): FORM[(int(t[1],16),k)]=cp
CANON={0x6a9:0x643}
def canon(c): return CANON.get(c,c)
def unshape_char(c):
    if 0xfb50<=c<=0xfdff or 0xfe70<=c<=0xfeff:
        dc=unicodedata.decomposition(chr(c))
        if dc.startswith('<'):
            parts=dc.split(' ')[1:]
            if len(parts)==1: return [canon(int(parts[0],16))]
            return [canon(int(p,16)) for p in parts]   # ligatures (lam-alef)
    return [canon(c)]
def unshape(cs):
    out=[]
    for c in cs:
        if c==ZWJ: continue
        out+=unshape_char(c)
    return out
LAMALEF={0x622:'FEF5',0x623:'FEF7',0x625:'FEF9',0x627:'FEFB'}
def glyph(c,form):   # form: iso fin ini med
    k={'iso':'isolated','fin':'final','ini':'initial','med':'medial'}[form]
    if c==0x6cc:     # Persian yeh: Farsi forms only isolated/final, Arabic yeh forms joined to next
        if form in('iso','fin'): return [FORM[(0x6cc,k)]]
        return [FORM[(0x64a,k)]]
    if c==0x6a9: return [FORM[(0x643,k)]]
    if c==0x686:
        out=[0x686]
        if form in('ini','med'): out.append(ZWJ)
        if form in('fin','med'): out.insert(0,ZWJ)
        return out
    cp=FORM.get((c,k))
    if cp is None: cp=FORM.get((c,'isolated'))
    return [cp] if cp else [c]
def reshape(cs):
    # cs: list of base codepoints (canon); returns list of output codepoints. Items that are None are transparent (tags) -> caller handles
    n=len(cs); out=[]; i=0
    jt=[jtype(c) for c in cs]
    def prevj(i):
        j=i-1
        while j>=0 and jt[j]=='T': j-=1
        return j
    def nextj(i):
        j=i+1
        while j<n and jt[j]=='T': j+=1
        return j
    def joins_prev(i):
        j=prevj(i)
        if j<0: return False
        return jt[j] in('D','J')
    def joins_next(i):
        j=nextj(i)
        if j>=n: return False
        return jt[j] in('D','R','J')
    skip=set()
    res=[]
    for i,c in enumerate(cs):
        if i in skip: continue
        t=jt[i]
        if t=='T':
            res.append([c]); continue
        if t=='U':
            res.append([] if c==0xFFFF else [FORM.get((c,'isolated'),c) if c==0x621 else c]); continue
        if t=='J': continue
        # lam + alef ligature
        if c==0x644 and nextj(i)<n and cs[nextj(i)] in (0x622,0x623,0x625,0x627):
            a=cs[nextj(i)]; base=int(LAMALEF[a],16); fin=joins_prev(i)
            res.append([base+1 if fin else base]); skip.add(nextj(i)); continue
        jp=joins_prev(i) and t in('D','R'); jn=joins_next(i) and t=='D'
        # a letter before a right-only letter cannot join if prev is R-only
        if jp and jt[prevj(i)]=='R': jp=False
        form='med' if (jp and jn) else 'fin' if jp else 'ini' if jn else 'iso'
        res.append(glyph(c,form))
    return [x for r in res for x in r]

def reshape_items(items):
    """items: list of ('c',code) / tags. Shapes each maximal text run (between tags) separately like the source tool."""
    out=[]; run=[]
    def flush():
        nonlocal run
        if run:
            for c in reshape(unshape(run)): out.append(('c',c))
            run=[]
    for it in items:
        if it[0]=='c' and it[1]!=0: run.append(it[1])
        else: flush(); out.append(it)
    flush(); return out
