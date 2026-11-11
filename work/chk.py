import sys,pickle,struct; sys.path.insert(0,'tools')
from botw_min import *
import bffnt,fontbuild,numpy as np
from render import render
used=pickle.load(open('used.pkl','rb'))
U="/root/.claude/uploads/e3988272-a021-590f-b21b-178f594b23ac/"
e,wl=sarc_parse(maybe(open(U+"6fa730f3-Font_EU.sbfarc",'rb').read()))
R="sw/The Legend Of Zelda Breath Of The Wild/atmosphere/contents/01007EF00011E000/Romfs/Font/Font_EU.sbfarc"
e2,sl=sarc_parse(maybe(open(R,'rb').read()))
import swfont
def check(n,r):
    od=wl[n+'_00.bffnt']; nd,i=fontbuild.build(od,sl[n+'_00.bffnt'],used,r,n)
    Fo=bffnt.parse(od); Fn=bffnt.parse(nd)
    go,gn=bffnt.glyphs(Fo),bffnt.glyphs(Fn); co,cn=bffnt.codes(Fo),bffnt.codes(Fn)
    assert all(gn[k]==v for k,v in go.items()); assert all(cn[k]==v for k,v in co.items())
    assert struct.unpack('>I',nd[12:16])[0]==len(nd)
    print(n,'ok glyphs+',len(gn)-len(go),'codes+',len(cn)-len(co),'sheets',Fn['tglp']['sheets'],'oy',i['oy'],'len',len(od),'->',len(nd))
    so=bffnt.decode_sheets(od,Fo); sn=bffnt.decode_sheets(nd,Fn)
    per=Fo['tglp']['cols']*Fo['tglp']['rows']
    # old cells unchanged
    bad=0
    for g in list(go)[::7]:
        s,x,y=bffnt.cell_of(Fo,g); a=so[s][y:y+Fo['tglp']['cellh']+1,x:x+Fo['tglp']['cellw']+1]; b=sn[s][y:y+Fo['tglp']['cellh']+1,x:x+Fo['tglp']['cellw']+1]
        if np.abs(a.astype(int)-b.astype(int)).max()>0: bad+=1
    print(' old cells differing (sampled):',bad)
    return nd,i,Fn,sn,gn,cn
