import sys,struct,unicodedata,re
sys.path.insert(0,"/tmp/claude-0/-home-claude/e3988272-a021-590f-b21b-178f594b23ac/scratchpad/tools")
from botw_min import *
import textfix, shaper
from textfix import items_of
PH0=0xE100   # private-use placeholders for tags
def unshape_char(ch):
    c=ord(ch)
    if 0xfb50<=c<=0xfdff or 0xfe70<=c<=0xfeff:
        n=unicodedata.normalize('NFKC',ch); return shaper.canon(n[0])+''.join(shaper.canon(x) for x in n[1:])
    return shaper.canon(ch)
def unshape(s):
    out=[]
    for i,ch in enumerate(s):
        if ch==shaper.ZWJ and out and 0x621<=ord(out[-1][-1])<=0x6ff: continue
        out.append(unshape_char(ch))
    return ''.join(out)
def extract(unit):
    its=items_of(unit); tags=[]; s=[]
    for it in its:
        if it[0]=='c':
            if it[1]==0: s.append('\x00')
            else: s.append(chr(it[1]))
        else:
            tags.append(it); s.append(chr(PH0+len(tags)-1))
    return unshape(''.join(s)),tags
def rebuild(clean,tags,table):
    sh=shaper.shape(clean,table); out=bytearray()
    for ch in sh:
        c=ord(ch)
        if PH0<=c<PH0+len(tags): out+=textfix.pk(tags[c-PH0])
        elif ch=='\x00': out+=struct.pack('>H',0)
        else:
            assert c<0x10000; out+=struct.pack('>H',c)
    return bytes(out)
