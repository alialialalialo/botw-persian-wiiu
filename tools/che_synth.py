import numpy as np,cv2,swfont
def cellimg(S,ssh,sg,sc,code):
    g=sc[code]; l,gw,adv=sg[g]; st=S['tglp']; s,x,y=swfont.cell_of(S,g)
    return g,(l,gw,adv),ssh[s][y+1:y+1+st['cellh'],x+1:x+1+max(gw,1)].copy()
def comps(im):
    m=(im>128).astype(np.uint8); n,lab,stats,cent=cv2.connectedComponentsWithStats(m,connectivity=8); return n,lab,stats,cent
NORMAL=None
def synth(S,ssh,sg,sc):
    """FB7A..FB7D = jeem bodies without their dot; meta (cx,cy,dw,dh) = position of the removed dot (Switch px)"""
    out={}
    for code,src in ((0xfb7a,0xfe9d),(0xfb7b,0xfe9e),(0xfb7c,0xfe9f),(0xfb7d,0xfea0)):
        _,m,T=cellimg(S,ssh,sg,sc,src); n,lab,st,ce=comps(T)
        big=1+int(np.argmax(st[1:,4])); cand=[k for k in range(1,n) if k!=big]
        k=max(cand,key=lambda k:ce[k][1]) if cand else None
        if k is None: meta=(T.shape[1]/2,T.shape[0]*0.8,8,8)
        else:
            meta=(float(ce[k][0]),float(ce[k][1]),int(st[k,2]),int(st[k,3])); T=T.copy(); T[lab==k]=0
        out[code]=(m[0],m[1],m[2],T,meta)
    return out
def draw_dots(im,cx,cy,d):
    """three dots (one over two) of size d centred on (cx,cy)"""
    H,W=im.shape; gap=1 if d<4 else 2
    top=(cx-d/2.0,cy-d-gap/2.0-d/2.0+d/2.0)
    pts=[(cx-d/2.0,cy-d-gap/2.0),(cx-d-gap/2.0,cy+gap/2.0),(cx+gap/2.0,cy+gap/2.0)]
    for x,y in pts:
        x0=int(round(x)); y0=int(round(y)); x1=min(W,x0+d); y1=min(H,y0+d)
        x0=max(0,x0); y0=max(0,y0)
        if x1>x0 and y1>y0: im[y0:y1,x0:x1]=255
    return im
