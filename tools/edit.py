import sys,re,struct
sys.path.insert(0,"/tmp/claude-0/-home-claude/e3988272-a021-590f-b21b-178f594b23ac/scratchpad/tools")
from textfix import *
import shape
VIEWCANON={0x64a:0x6cc,0x649:0x6cc}
OK_EXTRA=set(range(0x20,0x7f))|{0xa0,0xab,0xbb,0x60c,0x61b,0x61f,0x200c,0x2026,0xa}
def supported(cs):
    for c in cs:
        if 0x600<=c<=0x6ff and not (c in(0x60c,0x61b,0x61f,0x640) or 0x621<=c<=0x63a or 0x641<=c<=0x64a or 0x64b<=c<=0x652 or c in(0x67e,0x686,0x698,0x6a9,0x6af,0x6cc,0x649)): return False
    return True
def to_view(u):
    its=items_of(u); out=[]; tags=[]
    for it in its:
        if it[0]=='c':
            c=it[1]
            if c==0: out.append('\0'); continue
            for b in shape.unshape([c]):
                out.append(chr(VIEWCANON.get(b,b)))
        else:
            out.append('⟦%d⟧'%len(tags)); tags.append(it)
    return ''.join(out),tags
def from_view(view,tags):
    parts=re.split(r'(⟦\d+⟧)',view); items=[]
    for p in parts:
        m=re.fullmatch(r'⟦(\d+)⟧',p)
        if m: items.append(('M',int(m.group(1))))
        else: items+= [('C',ord(ch)) for ch in p]
    cs=[0xFFFF if x[0]=='M' else x[1] for x in items]
    # shape per line (newline breaks)
    out=[]; cur=[]
    def flush():
        nonlocal cur
        sh=shape.reshape([c for c in cur]) if cur else []
        out.extend(sh); cur=[]
    # reshape keeps marker positions? handle markers by segmenting
    segs=[]; 
    res=[]
    i=0
    line=[]; lineidx=[]
    for k,x in enumerate(items):
        if x[0]=='C' and x[1]==10: segs.append(('L',line)); segs.append(('N',None)); line=[]
        else: line.append(x)
    segs.append(('L',line))
    final=[]
    for kind,line in segs:
        if kind=='N': final.append(('c',10)); continue
        cs=[0xFFFF if x[0]=='M' else x[1] for x in line]
        # shape with markers as breakers: insert sentinel; reshape drops them, so shape piecewise
        piece=[]; 
        # shape whole line with sentinels then re-insert markers: do by shaping each char group between markers using lookahead context
        shaped=shape.reshape(cs)
        # re-align: markers positions = count of output glyphs before them; compute by shaping prefixes (cheap)
        pos=0; mk=[]
        for j,x in enumerate(line):
            if x[0]=='M':
                mk.append((len(shape.reshape(cs[:j])),x[1]))
        # reshape of prefix may differ in last form; use shaping of prefix up to marker and total, markers act as breakers so consistent
        last=0
        for (p,idx) in mk:
            final+= [('c',g) for g in shaped[last:p]]; final.append(tags[idx]); last=p
        final+= [('c',g) for g in shaped[last:]]
    return final
def pack_items(final):
    b=bytearray()
    for it in final: b+=pk(it)
    return bytes(b)
