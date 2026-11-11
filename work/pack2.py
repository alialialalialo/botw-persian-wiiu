import sys,os,shutil,struct,pickle,collections; sys.path.insert(0,'tools')
from botw_min import *
import bffnt,swfont,fontbuild,rstb,textfix
U="/root/.claude/uploads/e3988272-a021-590f-b21b-178f594b23ac/"
mw=pickle.load(open('work/mw_edited.pkl','rb'))
# used codes from final text (after reorder: same code set + mirrored brackets already present)
used=collections.Counter()
for n,d in mw.items():
    for u in txt2_units(dict(msbt_sections(d)[2])[b'TXT2'],'>'):
        for it in textfix.items_of(u):
            if it[0]=='c': used[it[1]]+=1
e,wl=sarc_parse(maybe(open(U+"6fa730f3-Font_EU.sbfarc",'rb').read()))
R="sw/The Legend Of Zelda Breath Of The Wild/atmosphere/contents/01007EF00011E000/Romfs/Font/Font_EU.sbfarc"
e2,sl=sarc_parse(maybe(open(R,'rb').read()))
files=dict(wl); infos={}
for n,r in [('Normal',39/105),('NormalS',30/105),('Caption',22/49),('Special',71/52)]:
    nd,i=fontbuild.build(wl[n+'_00.bffnt'],sl[n+'_00.bffnt'],used,r,n)
    F=bffnt.parse(nd); cm=bffnt.codes(F)
    miss=[hex(c) for c in used if c>=0x20 and c not in cm]
    print(n,'new glyphs',i['M']-i['N'],'unmapped',miss)
    files[n+'_00.bffnt']=nd; infos[n]=i
    open('work/%s_new.bffnt'%n,'wb').write(nd)
fraw=sarc_build(files,'>',8192); fsb=yaz0_comp(fraw); assert maybe(fsb)==fraw
base_rstb=open("r2/BOTW_Persian_FULL/content/System/Resource/ResourceSizeTable.product.srsizetable",'rb').read()
newv=9191776+(len(fraw)-9183576)+0x10000
b2=rstb.setv(base_rstb,'Font/Font_EU.bfarc',newv)
b2=rstb.setv(b2,'Message/Msg_EUen.product.sarc',rstb.get(b2,'Message/Msg_EUen.product.sarc')+0x20000)
rs=yaz0_comp(b2)
eo,fl=sarc_parse(maybe(open("r2/BOTW_Persian_FULL/content/Pack/Bootup_EUen.pack",'rb').read())); n0=list(fl)[0]; ee,_=sarc_parse(maybe(fl[n0]))
m2={k:textfix.fix_msbt(v) for k,v in mw.items()}
inner=yaz0_comp(sarc_build(m2,ee,4)); outer=sarc_build({n0:inner},'>',128)
CREDITS=open('work/credits.txt',encoding='utf-8').read()
root='out/R4/Persian_Final'; shutil.rmtree('out/R4',ignore_errors=True)
for p in ['content/Font','content/Pack','content/System/Resource']: os.makedirs(root+'/'+p)
open(root+'/content/Font/Font_EU.sbfarc','wb').write(fsb)
open(root+'/content/System/Resource/ResourceSizeTable.product.srsizetable','wb').write(rs)
open(root+'/content/Pack/Bootup_EUen.pack','wb').write(outer)
open(root+'/README_Credits.txt','w',encoding='utf-8').write(CREDITS)
open(root+'/rules.txt','w').write("[Definition]\ntitleIds = 00050000101c9500\nname = Persian Final\npath = \"The Legend of Zelda: Breath of the Wild/Mods/Persian Final\"\ndescription = Persian translation by Majid Hoshyar (radoo.ir/author/majidh1), adapted for Wii U 1.5.0 EUen by ali123qp. Disable BCML.\nversion = 7\n")
print('built',len(fsb),len(outer))
