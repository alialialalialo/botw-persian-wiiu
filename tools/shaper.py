import sys,unicodedata,collections
sys.path.insert(0,"/tmp/claude-0/-home-claude/e3988272-a021-590f-b21b-178f594b23ac/scratchpad/tools")
ZWJ='‍'; ZWNJ='‌'
CANON={'ك':'ک','ي':'ی','ى':'ی','ۀ':'ۀ'}
DUAL=set('بپتثجچحخسشصضطظعغفقکگلمنهیئـ')
RIGHT=set('اآأإدذرزژوؤةء')
TRANSP=set(chr(c) for c in range(0x64b,0x660))|{'ٰ','ٔ','ٕ'}
LIGA={'ا':'ا','آ':'آ','أ':'أ','إ':'إ'}
def canon(c): return CANON.get(c,c)
def form_of(code):
    d=unicodedata.decomposition(chr(code))
    for t in ('initial','medial','final','isolated'):
        if d.startswith('<%s>'%t): return t
    return None
def learn(texts):
    tab=collections.defaultdict(collections.Counter)
    for t in texts:
        n=len(t)
        for i,ch in enumerate(t):
            c=ord(ch)
            if 0xfb50<=c<=0xfdff or 0xfe70<=c<=0xfeff:
                f=form_of(c)
                if not f: continue
                base=unicodedata.normalize('NFKC',ch)
                if len(base)==2 and base[0]=='ل': key=('لا' if base[1]=='ا' else 'ل'+base[1],f)
                elif len(base)==1: key=(canon(base),f)
                else: continue
                tab[key][ch]+=1
            elif 0x621<=c<=0x6ff and ch not in TRANSP and ch!='ـ' and (ch in DUAL or ch in RIGHT or canon(ch) in DUAL):
                nxt=t[i+1] if i+1<n else ''
                prevf=None
                if i>0:
                    p=ord(t[i-1]); prevf=form_of(p) if (0xfb50<=p<=0xfeff) else None
                pj=prevf in('initial','medial')
                if nxt==ZWJ:
                    f='medial' if pj else 'initial'; tab[(canon(ch),f)][ch+ZWJ]+=1
                else:
                    f='final' if pj else 'isolated'; tab[(canon(ch),f)][ch]+=1
    return {k:v.most_common(1)[0][0] for k,v in tab.items()}
def shape(s,table):
    out=[]; n=len(s)
    def cls(ch):
        ch=canon(ch)
        if ch in DUAL: return 'D'
        if ch in RIGHT: return 'R'
        return None
    # logical letters list (skip transparent for join calc)
    idx=[i for i,ch in enumerate(s) if ch not in TRANSP]
    pos={i:k for k,i in enumerate(idx)}
    res=[None]*n
    i=0
    while i<n:
        ch=s[i]
        if ch in TRANSP or cls(ch) is None: res[i]=ch; i+=1; continue
        k=pos[i]
        prev=s[idx[k-1]] if k>0 else ''
        pj = cls(prev)=='D' if prev else False
        # lam-alef
        nxt=s[idx[k+1]] if k+1<len(idx) else ''
        if canon(ch)=='ل' and nxt in LIGA:
            key=('ل'+nxt if nxt!='ا' else 'لا','final' if pj else 'isolated')
            g=table.get(key)
            if g:
                res[i]=g; j=idx[k+1]; 
                for m in range(i+1,j+1): res[m]=''
                i=j+1; continue
        nj = cls(ch)=='D' and nxt!='' and cls(nxt) is not None
        f='medial' if (pj and nj) else 'initial' if nj else 'final' if pj else 'isolated'
        g=table.get((canon(ch),f))
        if g is None:
            # standard unicode fallback
            g=ch
            for c in list(range(0xfb50,0xfe00))+list(range(0xfe70,0xff00)):
                if form_of(c)==f and unicodedata.normalize('NFKC',chr(c))==canon(ch)  : g=chr(c); break
        res[i]=g; i+=1
    return ''.join(r for r in res if r is not None)
