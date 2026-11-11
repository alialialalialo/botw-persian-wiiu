import sys; sys.path.insert(0,"/tmp/claude-0/-home-claude/e3988272-a021-590f-b21b-178f594b23ac/scratchpad/ext/GTX-Extractor"); sys.path.insert(0,"/tmp/claude-0/-home-claude/e3988272-a021-590f-b21b-178f594b23ac/scratchpad/tools")
import struct, numpy as np
from addrlib import addrlib as A
from tex import bc4_decode, bc4_encode
STRIDE_PAD=1   # real stride of a glyph cell in the texture = header cell size + 1
def parse(d):
    hs=struct.unpack('>H',d[6:8])[0]; nb=struct.unpack('>H',d[16:18])[0]
    p=hs; secs=[]
    for _ in range(nb):
        m=d[p:p+4]; sz=struct.unpack('>I',d[p+4:p+8])[0]; secs.append((m,p,sz)); p+=sz
    F={'cwdh':[],'cmap':[],'secs':secs}
    for m,p,sz in secs:
        if m==b'FINF':
            ft,h,w,asc,lf,alt=struct.unpack('>BBBBHH',d[p+8:p+16]); dl,dg,dc,enc=struct.unpack('>bBBB',d[p+16:p+20])
            F['finf']=dict(type=ft,height=h,width=w,ascent=asc,linefeed=lf,alter=alt,defw=(dl,dg,dc),enc=enc)
        elif m==b'TGLP':
            cw,ch,sn,mcw=struct.unpack('BBBB',d[p+8:p+12]); ssz,base,fmt,cols,rows,sw,sh,doff=struct.unpack('>IHHHHHHI',d[p+12:p+32])
            F['tglp']=dict(cellw=cw,cellh=ch,sheets=sn,maxcw=mcw,sheetsize=ssz,baseline=base,fmt=fmt,cols=cols,rows=rows,sw=sw,sh=sh,doff=doff)
        elif m==b'CWDH':
            s,en,nxt=struct.unpack('>HHI',d[p+8:p+16]); F['cwdh'].append((s,en,[struct.unpack('>bBB',d[p+16+3*i:p+19+3*i]) for i in range(en-s+1)]))
        elif m==b'CMAP':
            cb,ce,ty,_,nxt=struct.unpack('>HHHHI',d[p+8:p+20]); q=p+20; mp={}
            if ty==0:
                off=struct.unpack('>H',d[q:q+2])[0]
                for c in range(cb,ce+1): mp[c]=off+c-cb
            elif ty==1:
                for i in range(ce-cb+1):
                    v=struct.unpack('>H',d[q+2*i:q+2*i+2])[0]
                    if v!=0xffff: mp[cb+i]=v
            else:
                n=struct.unpack('>H',d[q:q+2])[0]; q+=2
                for i in range(n):
                    c,g=struct.unpack('>HH',d[q+4*i:q+4*i+4]); mp[c]=g
            F['cmap'].append((cb,ce,ty,mp))
    return F
def glyphs(F):
    g={}
    for s,e,ent in F['cwdh']:
        for i,t in enumerate(ent): g[s+i]=t
    return g
def codes(F):
    cm={}
    for cb,ce,ty,mp in F['cmap']: cm.update(mp)
    return cm
def swz(k): return (k&3)<<9
def decode_sheets(d,F):
    t=F['tglp']; out=[]; W,H=t['sw'],t['sh']
    for s in range(t['sheets']):
        raw=d[t['doff']+s*t['sheetsize']:t['doff']+(s+1)*t['sheetsize']]
        assert len(raw)==t['sheetsize']
        if t['fmt']==0xc:
            so=A.getSurfaceInfo(0x34,W,H,1,1,4,0,0); lin=A.deswizzle(W,H,1,0x34,0,1,4,swz(s),so.pitch,64,0,0,raw); img=bc4_decode(lin,W,H)
        elif t['fmt']==8:
            so=A.getSurfaceInfo(0x1,W,H,1,1,4,0,0); lin=A.deswizzle(W,H,1,0x1,0,1,4,swz(s),so.pitch,8,0,0,raw); img=np.frombuffer(lin,dtype=np.uint8).reshape(H,so.pitch)[:,:W].copy()
        else: raise Exception("fmt %x"%t['fmt'])
        out.append(img[::-1].copy())
    return out
def encode_sheet(vis,fmt,k,expect):
    H,W=vis.shape; img=np.ascontiguousarray(vis[::-1])
    if fmt==0xc:
        so=A.getSurfaceInfo(0x34,W,H,1,1,4,0,0); out=A.swizzle(W,H,1,0x34,0,1,4,swz(k),so.pitch,64,0,0,bc4_encode(img))
    else:
        so=A.getSurfaceInfo(0x1,W,H,1,1,4,0,0); pad=np.zeros((H,so.pitch),dtype=np.uint8); pad[:,:W]=img
        out=A.swizzle(W,H,1,0x1,0,1,4,swz(k),so.pitch,8,0,0,pad.tobytes())
    assert len(out)==expect,("sheet size changed",len(out),expect)
    return out
def cell_of(F,gi,pad=STRIDE_PAD):
    t=F['tglp']; per=t['cols']*t['rows']; s=gi//per; c=gi%per
    return s,(c%t['cols'])*(t['cellw']+pad),(c//t['cols'])*(t['cellh']+pad)
