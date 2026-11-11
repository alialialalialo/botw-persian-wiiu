import sys,json,collections
sys.path.insert(0,"/tmp/claude-0/-home-claude/e3988272-a021-590f-b21b-178f594b23ac/scratchpad/tools")
from textfix import *
import shape
U="/root/.claude/uploads/e3988272-a021-590f-b21b-178f594b23ac/"
def load():
    e,fl=sarc_parse(maybe(open("r2/BOTW_Persian_FULL/content/Pack/Bootup_EUen.pack",'rb').read())); ee,mw=sarc_parse(maybe(list(fl.values())[0]))
    e2,f2=sarc_parse(maybe(open(U+"658d3269-Bootup_EUen.pack",'rb').read())); _,ow=sarc_parse(maybe(list(f2.values())[0]))
    return mw,ow
def lines_of(items):
    lines=[[]]
    for it in items:
        if it[0]=='c' and it[1]==10: lines.append([])
        else: lines[-1].append(it)
    return lines
def plain_marked(items):
    """canonical Persian text; tags -> ⟦i⟧ markers; returns (text,tags)"""
    tags=[]; out=[]; run=[]
    def fl():
        nonlocal run
        if run: out.append(''.join(map(chr,shape.unshape(run)))); run=[]
    for it in items:
        if it[0]=='c':
            if it[1]==0: continue
            if it[1]==10: fl(); out.append('\n')
            else: run.append(it[1])
        else:
            fl(); tags.append(it); out.append('⟦%d⟧'%(len(tags)-1))
    fl(); return ''.join(out),tags
def en_plain(items):
    return ''.join('\n' if it[1]==10 else chr(it[1]) for it in items if it[0]=='c' and it[1]!=0)
