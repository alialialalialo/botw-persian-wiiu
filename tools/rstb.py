import struct,zlib,sys
sys.path.insert(0,"/tmp/claude-0/-home-claude/e3988272-a021-590f-b21b-178f594b23ac/scratchpad/tools")
from botw_min import maybe,yaz0_comp
def get(d,name):
    d=maybe(d); c=struct.unpack('>I',d[4:8])[0]; h=zlib.crc32(name.encode())
    for i in range(c):
        k,v=struct.unpack('>II',d[12+8*i:20+8*i])
        if k==h: return v
def setv(d,name,val):
    d=bytearray(maybe(d)); c=struct.unpack('>I',d[4:8])[0]; h=zlib.crc32(name.encode())
    for i in range(c):
        k,v=struct.unpack('>II',d[12+8*i:20+8*i])
        if k==h: d[16+8*i:20+8*i]=struct.pack('>I',val); return bytes(d)
    raise KeyError(name)
