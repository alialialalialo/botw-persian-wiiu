import json,re,sys
n=sys.argv[1]; c={str(x['id']):x for x in json.load(open('review/ar_c%s.json'%n))}; o=json.load(open('review/ar_o%s.json'%n))
mk=lambda s:re.findall(r'⟦\d+⟧',s); bad=0
for k,x in c.items():
    if k not in o: print('missing',k); bad+=1; continue
    v=o[k]
    if mk(v)!=mk(x['fa']): print('markers',k); bad+=1
    elif v.count('\n')!=x['fa'].count('\n'): print('nl',k,v.count('\n'),x['fa'].count('\n')); bad+=1
    else:
        mx=max(len(re.sub(r'⟦\d+⟧','',l)) for l in x['en'].split('\n'))
        if any(len(re.sub(r'⟦\d+⟧','',l))>mx+2 for l in v.split('\n')): print('long',k); bad+=1
    if re.search(r'[ةىأإ]',v): print('arabic left',k); bad+=1
print('problems',bad,'of',len(c))
