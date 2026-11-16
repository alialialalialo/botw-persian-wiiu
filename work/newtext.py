import sys,re,unicodedata
sys.path.insert(0,'tools')
from units import *
import shape
MIRS={'(':')',')':'(','[':']',']':'[','«':'»','»':'«','<':'>','>':'<','{':'}','}':'{'}
PAD=set(range(0x2000,0x200b))|{0xa0}
def isltr(c): return (0x6f0<=c<=0x6f9) or (0x660<=c<=0x669) or (0x30<=c<=0x39) or (0x41<=c<=0x5a) or (0x61<=c<=0x7a) or c in(0xe0,0xe9,0xf1)
def v2l(codes):
    # strip padding at both ends
    a=list(codes)
    while a and (a[0] in PAD or a[0]==0x20): a.pop(0)
    while a and (a[-1] in PAD or a[-1]==0x20): a.pop()
    a=[0x20 if c in PAD else c for c in a]
    r=a[::-1]
    # re-reverse LTR runs (alnum with inner . ' - , / space between alnum)
    out=[];i=0
    while i<len(r):
        if isltr(r[i]):
            j=i
            while j<len(r) and (isltr(r[j]) or (r[j] in (0x2e,0x27,0x2d,0x2c,0x2f,0x20,0x3a) and j+1<len(r) and isltr(r[j+1]) and j>i)): j+=1
            out+=r[i:j][::-1]; i=j
        else: out.append(r[i]); i+=1
    # mirror brackets
    out=[ord(MIRS.get(chr(c),chr(c))) if chr(c) in MIRS else c for c in out]
    # ZWNJ reconstruction on presentation forms
    res=[]
    for k,c in enumerate(out):
        res.append(c)
        if k+1<len(out):
            n=out[k+1]
            dc=unicodedata.decomposition(chr(c)) if (0xfb50<=c<=0xfdff or 0xfe70<=c<=0xfeff) else ''
            if dc.startswith('<final>') or dc.startswith('<isolated>'):
                base=shape.canon(int(dc.split(' ')[1],16)) if len(dc.split(' '))==2 else None
                if base in shape.DUAL or base==0x643:
                    if (0xfb50<=n<=0xfdff or 0xfe70<=n<=0xfeff or 0x621<=n<=0x6d3): res.append(0x200c)
    return ''.join(map(chr,shape.unshape(res)))
def unit_text(b,e):
    """returns (canonical logical text with ⟦j⟧ markers, tags list [(g,t)])"""
    out=[];tags=[]
    cur=[]
    def flush():
        nonlocal cur
        if cur:
            lines=[[]]
            for c in cur:
                if c==10: lines.append([])
                elif c: lines[-1].append(c)
            out.append('\n'.join(v2l(l) for l in lines)); cur=[]
    for t in tokenize(b,e):
        if t[0]=='t': cur+=t[1]
        else:
            flush(); tags.append((t[1],t[2])); out.append('⟦%d⟧'%(len(tags)-1))
    flush(); return ''.join(out),tags

def swap16(b): return b''.join(b[i:i+2][::-1] for i in range(0,len(b)-1,2))+(b[-1:] if len(b)%2 else b'')
def v2l_seg(codes):
    a=[0x20 if c in PAD else c for c in codes]
    r=a[::-1]; out=[];i=0
    while i<len(r):
        if isltr(r[i]):
            j=i
            while j<len(r) and (isltr(r[j]) or (r[j] in (0x2e,0x27,0x2d,0x2c,0x2f,0x20,0x3a) and j+1<len(r) and isltr(r[j+1]) and j>i)): j+=1
            out+=r[i:j][::-1]; i=j
        else: out.append(r[i]); i+=1
    out=[ord(MIRS[chr(c)]) if chr(c) in MIRS else c for c in out]
    res=[]
    for k,c in enumerate(out):
        res.append(c)
        if k+1<len(out):
            n=out[k+1]
            dc=unicodedata.decomposition(chr(c)) if (0xfb50<=c<=0xfdff or 0xfe70<=c<=0xfeff) else ''
            if dc.startswith('<final>') or dc.startswith('<isolated>'):
                p=dc.split(' ')
                base=shape.canon(int(p[1],16)) if len(p)==2 else None
                if base in shape.DUAL and (0xfb50<=n<=0xfdff or 0xfe70<=n<=0xfeff or 0x621<=n<=0x6d3): res.append(0x200c)
    return ''.join(map(chr,shape.unshape(res)))
BARRIER={(0,4),(1,0),(5,0),(5,1),(5,2)}
def convert(b,e,ours_tags):
    toks=tokenize(b,e); items=[]; ntags=[]
    for t in toks:
        if t[0]=='t': items+=[('c',c) for c in t[1] if c!=0]
        else: items.append(('tag',len(ntags),t[1],t[2])); ntags.append((t[1],t[2]))
    if ntags!=[(o[1],o[2]) for o in ours_tags]: return None
    # split into blocks at barriers
    blocks=[[]]
    for it in items:
        if it[0]=='tag' and (it[2],it[3]) in BARRIER: blocks.append(it); blocks.append([])
        else: blocks[-1].append(it)
    out=[]   # tokens: str | ('tag',idx,g,t)
    for blk in blocks:
        if isinstance(blk,tuple): out.append(blk); continue
        lines=[[]]
        for it in blk:
            if it[0]=='c' and it[1]==10: lines.append([])
            else: lines[-1].append(it)
        btoks=[]
        for li,line in enumerate(lines):
            if li: btoks.append('\n')
            ci=[k for k,x in enumerate(line) if x[0]=='c' or (x[2],x[3])==(0,3)]
            if not ci: btoks+=line; continue
            a0,b0=ci[0],ci[-1]
            while a0<=b0 and line[a0][0]=='c' and line[a0][1] in PAD: a0+=1
            while b0>=a0 and line[b0][0]=='c' and line[b0][1] in PAD: b0-=1
            lead=[x for x in line[:ci[0]] if x[0]=='tag']; trail=[x for x in line[ci[-1]+1:] if x[0]=='tag']
            core=line[a0:b0+1]
            segs=[[]]; tgs=[]
            for it in core:
                if it[0]=='c': segs[-1].append(it[1])
                else: tgs.append(it); segs.append([])
            L=[v2l_seg(x) for x in segs[::-1]]; tg=tgs[::-1]
            btoks+=lead; btoks.append(L[0])
            for k in range(len(tg)): btoks.append(tg[k]); btoks.append(L[k+1])
            btoks+=trail
        # pair fix for color tags (0,3): renumber ascending by logical position
        pos=[k for k,x in enumerate(btoks) if not isinstance(x,str) and (x[2],x[3])==(0,3)]
        idx=sorted(btoks[k][1] for k in pos)
        for k,ix in zip(pos,idx): btoks[k]=('tag',ix,0,3)
        out+=btoks
    r=''.join(x if isinstance(x,str) else '⟦%d⟧'%x[1] for x in out)
    r=re.sub(r'[ ]{2,}',' ',r); r=re.sub(r' *\n *','\n',r)
    return r
