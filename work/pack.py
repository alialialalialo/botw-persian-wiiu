import sys,os,shutil,struct,zipfile,pickle; sys.path.insert(0,'tools')
from botw_min import *
import rstb, textfix
U="/root/.claude/uploads/e3988272-a021-590f-b21b-178f594b23ac/"
e,wl=sarc_parse(maybe(open(U+"6fa730f3-Font_EU.sbfarc",'rb').read()))
files=dict(wl)
for n in ['Normal','NormalS','Caption']: files[n+'_00.bffnt']=open('work/%s_new.bffnt'%n,'rb').read()
fraw=sarc_build(files,'>',8192); 
# sanity
_,chk=sarc_parse(fraw); assert all(chk[k]==files[k] for k in files)
fsb=yaz0_comp(fraw); assert maybe(fsb)==fraw
print('font sarc',len(fraw),len(fsb))
base_rstb=open("r2/BOTW_Persian_FULL/content/System/Resource/ResourceSizeTable.product.srsizetable",'rb').read()
newv=9191776+(len(fraw)-9183576)+0x10000
b2=rstb.setv(base_rstb,'Font/Font_EU.bfarc',newv)
b2=rstb.setv(b2,'Message/Msg_EUen.product.sarc',rstb.get(b2,'Message/Msg_EUen.product.sarc')+0x10000)
rs=yaz0_comp(b2); print('rstb font entry',newv)
eo,fl=sarc_parse(maybe(open("r2/BOTW_Persian_FULL/content/Pack/Bootup_EUen.pack",'rb').read())); n0=list(fl)[0]; ee,mw=sarc_parse(maybe(fl[n0]))
def text_pack(visual):
    m2={k:(textfix.fix_msbt(v) if visual else v) for k,v in mw.items()}
    pass
    inner=yaz0_comp(sarc_build({n0:None} if False else m2,ee,4))
    outer=sarc_build({n0:inner},'>',128)
    return outer
def mk(name,visual,desc):
    root='out/R3/'+name; shutil.rmtree(root,ignore_errors=True)
    for p in ['content/Font','content/Pack','content/System/Resource']: os.makedirs(root+'/'+p)
    open(root+'/content/Font/Font_EU.sbfarc','wb').write(fsb)
    open(root+'/content/System/Resource/ResourceSizeTable.product.srsizetable','wb').write(rs)
    open(root+'/content/Pack/Bootup_EUen.pack','wb').write(text_pack(visual))
    open(root+'/README_Credits.txt','w',encoding='utf-8').write(CREDITS)
    open(root+'/rules.txt','w').write("[Definition]\ntitleIds = 00050000101c9500\nname = %s\npath = \"The Legend of Zelda: Breath of the Wild/Mods/%s\"\ndescription = %s\nversion = 7\n"%(name.replace('_',' '),name.replace('_',' '),desc))
CREDITS='''Persian translation of The Legend of Zelda: Breath of the Wild
ترجمهٔ فارسی بازی زلدا: نفس وحش

Original Persian translation (Switch version) by Majid Hoshyar (مجید هوشیار).
مترجم و سازندهٔ ترجمهٔ فارسی اصلی: آقای مجید هوشیار
https://www.radoo.ir/author/majidh1/

Wii U adaptation / تطبیق نسخهٔ Wii U: ali123qp (Telegram)

This graphic pack only adapts that translation (text order, fonts, control codes)
for the Wii U 1.5.0 (EU) version running in Cemu. All translation credit belongs to the original author.
این گرافیک‌پک فقط ترجمهٔ ایشان را برای نسخهٔ Wii U (1.5.0 اروپا) در Cemu سازگار می‌کند؛ همهٔ اعتبار ترجمه متعلق به سازندهٔ اصلی است.
'''
mk('Persian_Final',True,'Persian translation by Majid Hoshyar (radoo.ir/author/majidh1), adapted for Wii U 1.5.0 EUen. Disable BCML.')
