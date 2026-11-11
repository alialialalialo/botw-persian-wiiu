import sys,json,re
inp=json.load(open(sys.argv[1])); out=json.load(open(sys.argv[2]))
by={str(x['id']):x for x in inp}; bad=0
MK=re.compile(r'⟦\d+⟧')
def lens(t): return [len(MK.sub('',l)) for l in t.split('\n')]
for k,new in out.items():
    if k not in by: print('unknown id',k); bad+=1; continue
    old=by[k]['fa']
    if MK.findall(old)!=MK.findall(new): print(k,'markers differ (must be same markers, same order):',MK.findall(old),MK.findall(new)); bad+=1
    if old.count('\n')!=new.count('\n'): print(k,'line count differs',old.count('\n'),new.count('\n')); bad+=1; continue
    for a,b in zip(lens(old),lens(new)):
        pass
    mx=max(lens(old))
    for i,l in enumerate(lens(new)):
        if l>mx+2: print(k,'line',i,'too long',l,'>',mx); bad+=1
    lat=lambda t: sorted(re.findall(r'[A-Za-z0-9]+',MK.sub('',t)))
    if lat(old)!=lat(new): print(k,'latin/digit tokens changed',lat(old),lat(new)); bad+=1
print('checked',len(out),'problems',bad)
