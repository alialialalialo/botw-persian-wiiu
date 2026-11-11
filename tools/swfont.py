import struct, numpy as np
from tex import bc4_decode
def tegra_offsets(wb,hb,bpp,bh):
    pitch=((wb*bpp+63)//64)*64
    ys,xs=np.mgrid[0:hb,0:wb]; x=xs*bpp
    gob=(ys//(8*bh))*512*bh*(pitch//64)+(x//64)*512*bh+((ys%(8*bh))//8)*512
    xx=x%64; yy=ys%8
    return gob+((xx%64)//32)*256+((yy%8)//2)*64+((xx%32)//16)*32+(yy%2)*16+(xx%16)
def tegra_deswizzle(data,wb,hb,bpp,bh):
    off=tegra_offsets(wb,hb,bpp,bh); a=np.frombuffer(data,dtype=np.uint8)
    return a[(off[:,:,None]+np.arange(bpp)[None,None,:])].reshape(-1).tobytes()
def parse(d):
    hs=struct.unpack('<H',d[6:8])[0]; nb=struct.unpack('<H',d[16:18])[0]; p=hs; secs=[]
    for _ in range(nb):
        m=d[p:p+4]; sz=struct.unpack('<I',d[p+4:p+8])[0]; secs.append((m,p,sz)); p+=sz
    F={'cwdh':[],'cmap':[]}
    for m,p,sz in secs:
        if m==b'FINF':
            ft,h,w,asc,lf,alt=struct.unpack('<BBBBHH',d[p+8:p+16]); F['finf']=dict(height=h,width=w,ascent=asc,linefeed=lf)
        elif m==b'TGLP':
            cw,ch,sn,mcw=struct.unpack('BBBB',d[p+8:p+12]); ssz,base,fmt,cols,rows,sw,sh,doff=struct.unpack('<IHHHHHHI',d[p+12:p+32])
            F['tglp']=dict(cellw=cw,cellh=ch,sheets=sn,maxcw=mcw,sheetsize=ssz,baseline=base,fmt=fmt,cols=cols,rows=rows,sw=sw,sh=sh,doff=doff)
        elif m==b'CWDH':
            s,en,nxt=struct.unpack('<HHI',d[p+8:p+16]); F['cwdh'].append((s,en,[struct.unpack('bBB',d[p+16+3*i:p+19+3*i]) for i in range(en-s+1)]))
        elif m==b'CMAP':
            cb,ce,ty,_,nxt=struct.unpack('<IIHHI',d[p+8:p+24]); q=p+24; mp={}
            if ty==0:
                off=struct.unpack('<H',d[q:q+2])[0]
                for c in range(cb,ce+1): mp[c]=off+c-cb
            elif ty==1:
                for i in range(ce-cb+1):
                    v=struct.unpack('<H',d[q+2*i:q+2*i+2])[0]
                    if v!=0xffff: mp[cb+i]=v
            else:
                n=struct.unpack('<H',d[q:q+2])[0]; q+=4
                for i in range(n):
                    c,g=struct.unpack('<IHH',d[q+8*i:q+8*i+8])[:2]; mp[c]=g
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
def sheets(d,F):
    t=F['tglp']; b=d[t['doff']:]
    i=b.index(b'BRTI'); r=b[i:i+0x40]
    w,h=struct.unpack('<II',r[0x24:0x2c]); arr=struct.unpack('<I',r[0x30:0x34])[0]; bhl=struct.unpack('<I',r[0x34:0x38])[0]
    j=b.index(b'BRTD')+0x10; wb,hb=w//4,h//4; layer=wb*hb*8; out=[]
    for k in range(arr):
        lin=tegra_deswizzle(b[j+k*layer:j+(k+1)*layer],wb,hb,8,1<<bhl)
        out.append(bc4_decode(lin,w,h)[::-1].copy())
    return out
def cell_of(F,gi,pad=1):
    t=F['tglp']; per=t['cols']*t['rows']; s=gi//per; c=gi%per
    return s,(c%t['cols'])*(t['cellw']+pad),(c//t['cols'])*(t['cellh']+pad)
