import sys,struct,re,collections,pickle,zipfile,io; sys.path.insert(0,'tools'); sys.path.insert(0,'work')
from botw_min import *
import textfix as T, bffnt, rstb, newtext, shape
from apply_edits import *
Z=zipfile.ZipFile('out/BOTW_Persian_v2.1.1.zip'); names=Z.namelist(); print('FILES',[n for n in names if not n.endswith('/')])
rules=Z.read('BOTW_Persian/rules.txt').decode(); print(rules)
pack=Z.read('BOTW_Persian/content/Pack/Bootup_EUen.pack'); font=Z.read('BOTW_Persian/content/Font/Font_EU.sbfarc'); rs=Z.read('BOTW_Persian/content/System/Resource/ResourceSizeTable.product.srsizetable')
o,fl=sarc_parse(maybe(pack)); raw=maybe(fl[list(fl)[0]]); _,m=sarc_parse(raw)
base=rstb.maybe(open('/root/.claude/uploads/e3988272-a021-590f-b21b-178f594b23ac/459a7954-ResourceSizeTable.product.srsizetable','rb').read()); new=rstb.maybe(rs)
print('RSTB entries same set:',struct.unpack('>I',base[4:8]),struct.unpack('>I',new[4:8]),'len',len(base),len(new))
bd=[k for k in range(struct.unpack('>I',new[4:8])[0]) if base[12+8*k:16+8*k]==new[12+8*k:16+8*k] and base[16+8*k:20+8*k]!=new[16+8*k:20+8*k]]
print('RSTB changed entries',len(bd),'msg actual',len(raw),'msg rstb',rstb.get(new,'Message/Msg_EUen.product.sarc'))
fe,fl2=sarc_parse(maybe(font)); fraw=len(maybe(font)); print('font files',list(fl2),'size',fraw,'rstb font',rstb.get(new,'Font/Font_EU.bfarc'))
mw,ow=newtext.load()
print('msbt in pack',len(m),'orig',len(ow),'missing',set(ow)-set(m),'extra',set(m)-set(ow))
# fonts mapping
fonts={}
for fn in ['Normal','NormalS','Caption','Special']:
    d=fl2[fn+'_00.bffnt']; d=maybe(d) if d[:4]==b'Yaz0' else d
    F=bffnt.parse(d); fonts[fn]=(bffnt.codes(F),bffnt.glyphs(F))
issues=collections.defaultdict(list); labelbad=0; unitn=0; allcodes=collections.Counter()
for n,b in m.items():
    if not n.endswith('.msbt'): continue
    eo,ho,so=msbt_sections(ow[n]); en,hn,sn=msbt_sections(b)
    do,dn=dict(so),dict(sn)
    for k in (b'LBL1',b'ATR1',b'NLI1',b'TSY1'):
        if (k in do)!=(k in dn) or (k in do and k!=b'ATR1' and do[k]!=dn[k]): labelbad+=1; issues['section_diff'].append((n,k))
    if b'ATR1' in do and do[b'ATR1']!=dn[b'ATR1']: issues['atr_diff'].append(n)
    eu=txt2_units(do[b'TXT2'],eo); nu=txt2_units(dn[b'TXT2'],en)
    if len(eu)!=len(nu): issues['count'].append(n); continue
    for i,(a,c) in enumerate(zip(eu,nu)):
        unitn+=1
        its=T.items_of(c); cs=[x[1] for x in its if x[0]=='c']
        for x in cs: allcodes[x]+=1
        s=''.join(chr(x) for x in cs if x!=0)
        ta=''.join(''.join(map(chr,t[1])) for t in tokenize(a,eo) if t[0]=='t').strip('\x00 \n\r')
        if ta and not s.strip(): issues['empty_vs_en'].append((n,i))
        if re.search(r'[⟦⟧]|<br>|</?color|\{[a-z]|&[a-z]+;',s): issues['leak'].append((n,i,s[:40]))
        if re.search('[ةىأإيك]',s) and False: pass
        if re.search(r'[ةىأإ]',s): issues['arabic_only'].append((n,i,s[:40]))
        if s.startswith('‍') or s.endswith('‍'): issues['zwj_edge'].append((n,i))
        if re.search(r'[\x01-\x08\x0b-\x1f]',s): issues['ctrl'].append((n,i))
        if '?' in s and re.search('[ﭐ-﻿]',s): issues['latin_qmark'].append((n,i,s[:40]))
        if ',' in s and re.search('[ﭐ-﻿]',s) and False: pass
cm=fonts['Normal'][0]
unm=[hex(c) for c in allcodes if c>=0x20 and c not in cm]; print('codes unmapped in Normal',unm)
for fn,(cm2,gl) in fonts.items():
    print(fn,'unmapped',[hex(c) for c in allcodes if c>=0x20 and c not in cm2][:10])
print('units',unitn,'labelbad',labelbad)
for k,v in issues.items(): print(k,len(v),v[:5])
