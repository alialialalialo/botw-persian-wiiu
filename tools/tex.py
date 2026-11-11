import numpy as np
def bc4_decode(data,w,h):
    bw,bh=w//4,h//4
    a=np.frombuffer(data,dtype=np.uint8)[:bw*bh*8].reshape(bh,bw,8)
    e0=a[:,:,0].astype(np.float32); e1=a[:,:,1].astype(np.float32)
    bits=np.zeros((bh,bw),dtype=np.uint64)
    for i in range(6): bits|=a[:,:,2+i].astype(np.uint64)<<np.uint64(8*i)
    pal=np.zeros((bh,bw,8),dtype=np.float32); pal[:,:,0]=e0; pal[:,:,1]=e1
    m=(e0>e1)
    for k in range(6):
        p8=((6-k)*e0+(k+1)*e1)/7.0
        p6=((5-k)*e0+(k+1)*e1)/5.0 if k<4 else (0 if k==4 else 255)
        pal[:,:,2+k]=np.where(m,p8,p6)
    out=np.zeros((h,w),dtype=np.uint8)
    for py in range(4):
        for px in range(4):
            idx=((bits>>np.uint64(3*(py*4+px)))&np.uint64(7)).astype(np.int64)
            v=np.take_along_axis(pal,idx[:,:,None],axis=2)[:,:,0]
            out[py::4,px::4]=np.clip(np.rint(v),0,255).astype(np.uint8)
    return out
def bc4_encode(img):
    h,w=img.shape; bw,bh=w//4,h//4
    blk=img.reshape(bh,4,bw,4).transpose(0,2,1,3).reshape(bh,bw,16).astype(np.float32)
    mx=blk.max(axis=2); mn=blk.min(axis=2)
    e0=mx.copy(); e1=mn.copy()
    same=(e0==e1); e0=np.where(same,np.minimum(e0+1,255),e0); e1=np.where(same&(mx==255),254,e1)
    pal=np.stack([e0,e1]+[((6-k)*e0+(k+1)*e1)/7.0 for k in range(6)],axis=2)
    idx=np.abs(blk[:,:,:,None]-pal[:,:,None,:]).argmin(axis=3).astype(np.uint64)
    bits=np.zeros((bh,bw),dtype=np.uint64)
    for i in range(16): bits|=idx[:,:,i]<<np.uint64(3*i)
    out=np.zeros((bh,bw,8),dtype=np.uint8); out[:,:,0]=e0; out[:,:,1]=e1
    for i in range(6): out[:,:,2+i]=((bits>>np.uint64(8*i))&np.uint64(255)).astype(np.uint8)
    return out.tobytes()
