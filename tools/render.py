import numpy as np
from PIL import Image
def render(lines,F,sheets,cmap,gl,cell_of,scale=1,bg=255,pad=1,margin=6,gap=4):
    t=F['tglp']; cw,ch=t['cellw'],t['cellh']
    imgs=[]
    for codes in lines:
        W=margin*2+sum(gl.get(cmap.get(c,0),(0,0,0))[2] for c in codes)+40; H=ch+margin*2
        im=np.zeros((H,W),dtype=np.float32); x=margin
        for c in codes:
            g=cmap.get(c,0); l,gw,adv=gl.get(g,(0,0,0))
            s,x0,y0=cell_of(F,g)
            cell=sheets[s][y0+1:y0+1+ch, x0+1:x0+1+cw].astype(np.float32)
            xs=x+l
            for i in range(min(cw,gw+2)):
                xx=xs+i
                if 0<=xx<W and i<cell.shape[1]:
                    im[margin:margin+ch,xx]=np.maximum(im[margin:margin+ch,xx],cell[:,i]) if i<gw else im[margin:margin+ch,xx]
            x+=adv
        imgs.append(im)
    Wm=max(i.shape[1] for i in imgs); out=np.zeros((sum(i.shape[0] for i in imgs),Wm),dtype=np.float32); y=0
    for i in imgs: out[y:y+i.shape[0],:i.shape[1]]=i; y+=i.shape[0]
    a=(255-out).astype(np.uint8)
    im=Image.fromarray(a)
    if scale!=1: im=im.resize((im.width*scale,im.height*scale),Image.NEAREST)
    return im
