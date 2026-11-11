import sys,re,json,collections,struct
sys.path.insert(0,"/tmp/claude-0/-home-claude/e3988272-a021-590f-b21b-178f594b23ac/scratchpad/tools")
from units import *
MK=re.compile(r'⟦(\d+)⟧')
def build_items(text,tags,trail_zeros,trail_ws):
    its=[]; pos=0
    def addtext(s):
        for ch in s: its.append(('c',10 if ch=='\n' else ord(ch)))
    for m in MK.finditer(text):
        addtext(text[pos:m.start()]); its.append(tags[int(m.group(1))]); pos=m.end()
    addtext(text[pos:])
    # keep trailing whitespace the original had (e.g. \r / space)
    cs=''.join(chr(c[1]) for c in its if c[0]=='c')
    if trail_ws and not cs.endswith(trail_ws): addtext(trail_ws)
    its=shape.reshape_items(its)
    its+= [('c',0)]*trail_zeros
    return its
def pk_items(its):
    return b''.join(pk(i) for i in its)
def apply(mw,edits_by_text):
    """edits_by_text: {old_canonical_text: new_text}"""
    new={}; n=0
    for name,d in mw.items():
        e,hdr,secs=msbt_sections(d); ns=[]
        for m_,b in secs:
            if m_==b'TXT2':
                us=txt2_units(b,e); out=[]
                for u in us:
                    its=items_of(u)
                    t,tags=plain_marked(its)
                    if t in edits_by_text:
                        tz=0
                        k=len(its)
                        while k>0 and its[k-1]==('c',0): tz+=1; k-=1
                        ws=''
                        mm=re.search(r'[ \r\t]+$',t)
                        if mm: ws=mm.group(0)
                        u=pk_items(build_items(edits_by_text[t],tags,tz,ws)); n+=1
                    out.append(u)
                b=build_txt2(out,e)
            ns.append((m_,b))
        new[name]=build_msbt(hdr,ns,e)
    return new,n
def fix_yeh(mw):
    new={}
    for name,d in mw.items():
        e,hdr,secs=msbt_sections(d); ns=[]
        for m_,b in secs:
            if m_==b'TXT2':
                out=[]
                for u in txt2_units(b,e):
                    its=items_of(u); ch=False; r=[]
                    for i in its:
                        if i[0]=='c' and i[1] in (0xfef1,0xfef2): i=('c',{0xfef1:0xfbfc,0xfef2:0xfbfd}[i[1]]); ch=True
                        r.append(i)
                    out.append(pk_items(r) if ch else u)
                b=build_txt2(out,e)
            ns.append((m_,b))
        new[name]=build_msbt(hdr,ns,e)
    return new
