import struct,os,subprocess,tempfile
def yaz0_dec(d):
    size=struct.unpack('>I',d[4:8])[0]; out=bytearray(); i=16
    while len(out)<size:
        code=d[i]; i+=1
        for b in range(8):
            if len(out)>=size: break
            if code&(0x80>>b): out.append(d[i]); i+=1
            else:
                b1,b2=d[i],d[i+1]; i+=2
                dist=((b1&15)<<8|b2)+1; n=b1>>4
                if n==0: n=d[i]+18; i+=1
                else: n+=2
                for _ in range(n): out.append(out[-dist])
    return bytes(out)
def maybe(d): return yaz0_dec(d) if d[:4]==b'Yaz0' else d
_YC=os.path.join(os.path.dirname(os.path.abspath(__file__)),'yaz0c')
def yaz0_comp(data):
    with tempfile.TemporaryDirectory() as t:
        a=os.path.join(t,'a'); b=os.path.join(t,'b'); open(a,'wb').write(data)
        subprocess.run([_YC,a,b],check=True); return open(b,'rb').read()
def sum_hash(n,m=101):
    h=0
    for ch in n.encode(): h=(h*m+ch)&0xffffffff
    return h
def sarc_parse(d):
    e='<' if d[6:8]==b'\xff\xfe' else '>'
    hl,=struct.unpack(e+'H',d[4:6]); fsize,dataoff=struct.unpack(e+'II',d[8:16])
    s=hl; cnt=struct.unpack(e+'H',d[s+6:s+8])[0]
    nodes=[struct.unpack(e+'IIII',d[s+12+16*i:s+28+16*i]) for i in range(cnt)]
    sf=s+12+16*cnt; ns=sf+8; files={}
    for h,no,b,en in nodes:
        o=(no&0xffffff)*4+ns; e0=d.index(b'\0',o); files[d[o:e0].decode()]=d[dataoff+b:dataoff+en]
    return e,files
def sarc_build(files,e='>',align=4,hmul=101):
    names=sorted(files,key=lambda n:sum_hash(n,hmul))
    sfnt=b''; offs={}
    for n in names:
        offs[n]=len(sfnt)//4; sfnt+=n.encode()+b'\0'; sfnt+=b'\0'*((-len(sfnt))%4)
    data=b''; nodes=[]
    for n in names:
        data+=b'\0'*((-len(data))%align); b=len(data); data+=files[n]; nodes.append((sum_hash(n,hmul),0x01000000|offs[n],b,len(data)))
    hl=0x14; sfat=b'SFAT'+struct.pack(e+'HHI',0xc,len(names),hmul)+b''.join(struct.pack(e+'IIII',*x) for x in nodes)
    sfn=b'SFNT'+struct.pack(e+'HH',8,0)+sfnt
    do=hl+len(sfat)+len(sfn); do+=(-do)%align
    hdr=b'SARC'+struct.pack(e+'H',hl)+(b'\xfe\xff' if e=='>' else b'\xff\xfe')+struct.pack(e+'II',do+len(data),do)+struct.pack(e+'HH',0x100,0)
    body=hdr+sfat+sfn; body+=b'\0'*(do-len(body))
    return body+data

# ---------- MSBT ----------
def msbt_sections(d):
    e='<' if d[8:10]==b'\xff\xfe' else '>'
    n=struct.unpack(e+'H',d[0x0e:0x10])[0]; p=0x20; secs=[]
    for _ in range(n):
        m=d[p:p+4]; sz=struct.unpack(e+'I',d[p+4:p+8])[0]
        secs.append((m,d[p+16:p+16+sz])); p+=16+((sz+15)//16)*16
    return e,d[:0x20],secs
def txt2_units(body,e):
    cnt=struct.unpack(e+'I',body[:4])[0]
    offs=list(struct.unpack(e+'%dI'%cnt,body[4:4+4*cnt]))+[len(body)]
    return [body[offs[k]:offs[k+1]] for k in range(cnt)]
def tokenize(b,e):
    u=struct.unpack(e+'%dH'%(len(b)//2),b); i=0; out=[]; cur=[]
    while i<len(u):
        c=u[i]
        if c==0x0E:
            if cur: out.append(('t',cur)); cur=[]
            g,t,sz=u[i+1],u[i+2],u[i+3]; out.append(('tag',g,t,b[(i+4)*2:(i+4)*2+sz])); i+=4+(sz+1)//2
        elif c==0x0F:
            if cur: out.append(('t',cur)); cur=[]
            out.append(('end',u[i+1],u[i+2])); i+=3
        else: cur.append(c); i+=1
    if cur: out.append(('t',cur))
    return out
def lbl1(body,e):
    ng=struct.unpack(e+'I',body[:4])[0]; res={}
    for g in range(ng):
        c,o=struct.unpack(e+'II',body[4+8*g:12+8*g]); p=o
        for _ in range(c):
            l=body[p]; name=body[p+1:p+1+l].decode('ascii','replace'); idx=struct.unpack(e+'I',body[p+1+l:p+5+l])[0]
            res[name]=idx; p+=5+l
    return res
def build_msbt(header,secs,e):
    out=bytearray(header)
    for m,b in secs:
        out+=m+struct.pack(e+'I',len(b))+b'\0'*8+b; out+=b'\xab'*((-len(b))%16)
    out[0x12:0x16]=struct.pack(e+'I',len(out)); return bytes(out)
def build_txt2(strs,e):
    n=len(strs); off=4+4*n; offs=[]; body=b''
    for s in strs: offs.append(off+len(body)); body+=s
    return struct.pack(e+'I',n)+struct.pack(e+'%dI'%n,*offs)+body
def swap2(b): return b''.join(b[i:i+2][::-1] for i in range(0,len(b),2))
def pack_units(u,e): return struct.pack(e+'%dH'%len(u),*u)
def _rev4(b): return b''.join(b[i:i+4][::-1] for i in range(0,len(b)-len(b)%4,4))+b[len(b)-len(b)%4:]
def _keep2(b): return swap2(b[:-2])+b[-2:] if len(b)>=2 else b
def default_tf(g,ty,p):
    if g==1: return _rev4(p) if (ty,len(p))==(0,4) else _keep2(p)
    if g==0: return swap2(p)
    return p
def convert_entry(sw_bytes,wii_bytes,stats):
    st=tokenize(sw_bytes,'<'); wt=[t for t in tokenize(wii_bytes,'>') if t[0]=='tag']
    used=[False]*len(wt); out=bytearray()
    for t in st:
        if t[0]=='t': out+=pack_units(t[1],'>')
        elif t[0]=='end': out+=pack_units([0x0F,t[1],t[2]],'>')
        else:
            _,g,ty,p=t; pick=None
            for c in [p,swap2(p),_rev4(p),_keep2(p)]:
                for i,w in enumerate(wt):
                    if not used[i] and w[1]==g and w[2]==ty and w[3]==c: pick=i;break
                if pick is not None: break
            if pick is None:
                for i,w in enumerate(wt):
                    if not used[i] and w[1]==g and w[2]==ty and len(w[3])==len(p): pick=i;stats['positional']+=1;break
            if pick is not None: used[pick]=True; params=wt[pick][3]
            else: params=default_tf(g,ty,p); stats['fallback']+=1
            out+=pack_units([0x0E,g,ty,len(params)],'>')+params
            if len(params)%2: out+=b'\0'
    return bytes(out)
