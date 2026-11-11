import sys,collections; sys.path.insert(0,'tools')
from textfix import *
import shape
e,fl=sarc_parse(maybe(open("r2/BOTW_Persian_FULL/content/Pack/Bootup_EUen.pack",'rb').read())); n0=list(fl)[0]; ee,mw=sarc_parse(maybe(fl[n0]))
def run(tagmode,show=0):
    shape.TAGJ=tagmode
    tot=bad=0; diffc=collections.Counter(); ex=collections.defaultdict(list)
    def chk(cs,n):
        nonlocal tot,bad
        base=shape.unshape(cs); re_=shape.reshape(base); orig=[c for c in cs if c!=0xFFFF]; tot+=1
        if re_!=orig:
            bad+=1
            for i,(a,b) in enumerate(zip(re_,orig)):
                if a!=b:
                    k=('%04x'%a,'%04x'%b); diffc[k]+=1
                    if len(ex[k])<3: ex[k].append((n.split('/')[-1],' '.join('%04x'%x for x in orig[max(0,i-4):i+5])))
                    break
            else: diffc['len']+=1
    for n,d in mw.items():
        for u in txt2_units(dict(msbt_sections(d)[2])[b'TXT2'],'>'):
            its=items_of(u); allcs=[]
            for it in its: allcs.append(it[1] if it[0]=='c' else 0xFFFF)
            lines=[[]]
            for c in allcs:
                if c==10: lines.append([])
                else: lines[-1].append(c)
            for cs in lines:
                if not any(0x600<=c<=0x6ff or 0xfb50<=c<=0xfeff for c in cs): continue
                if is_visual([c for c in cs if c!=0xFFFF]): continue
                chk(cs,n)
    print(tagmode,tot,bad)
    for k,v in diffc.most_common(show): print(' ',k,v,ex[k])
    return
    for n,d in mw.items():
        for u in []:
            cs=[]
            base=shape.unshape(cs); re_=[c for c in shape.reshape(base)]; orig=[c for c in cs if c!=0xFFFF]; tot+=1
            if re_!=orig:
                bad+=1
                for i,(a,b) in enumerate(zip(re_,orig)):
                    if a!=b:
                        k=('%04x'%a,'%04x'%b); diffc[k]+=1
                        if len(ex[k])<2: ex[k].append((n.split('/')[-1],' '.join('%04x'%x for x in orig[max(0,i-3):i+4])))
                        break
    print(tagmode,tot,bad)
    for k,v in diffc.most_common(show): print(' ',k,v,ex[k])
run('U',12)
