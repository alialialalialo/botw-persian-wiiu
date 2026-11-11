import sys,pickle,re; sys.path.insert(0,'tools')
from apply_edits import *
L=r'[ء-ۓ]'
N=r'(?<!%s)'%L; E=r'(?!%s)'%L
R=[(N+r'مولدور[اآ][جگ]يك'+E,'مولدوگا'),
 (N+r'روجو'+E,'ريجو'),
 (N+r'تِ?ری'+E,'بيدل'),
 (N+r'واسا[شچ]'+E,'واساك')]
R=[(re.compile(a),b) for a,b in R]
ed={}
for f,i,fa,en in pickle.load(open('work/pairs.pkl','rb')):
    t=fa
    for rx,b in R: t=rx.sub(b,t)
    if t!=fa: ed[fa]=t
print(len(ed))
mw=pickle.load(open('work/mw_edited.pkl','rb'))
pickle.dump(mw,open('work/mw_before_d11.pkl','wb'))
mw,n=apply(mw,ed); mw=fix_yeh(mw); print('applied',n)
pickle.dump(mw,open('work/mw_edited.pkl','wb'))
