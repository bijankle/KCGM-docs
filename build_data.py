import openpyxl,re,json,sys
src=sys.argv[1]
wb=openpyxl.load_workbook(src,read_only=True,data_only=True)
rows=list(wb.worksheets[0].iter_rows(values_only=True))[1:]
folders={};F=[]
out=[]
for r in rows:
    name,url,_,num,rev,st,title=(list(r)+[None]*7)[:7]
    s=lambda v:'' if v is None else str(v).strip()
    url=s(url); fi=-1; tail=''
    if url:
        f,_,t=url.rpartition('/')
        if f not in folders: folders[f]=len(F); F.append(f)
        fi=folders[f]; tail='' if t==s(name) else t
    out.append([s(name),fi,tail,s(num),s(rev),s(st),s(title)])
json.dump({'folders':F,'rows':out,'source':src.split('/')[-1]},open('data.json','w'),ensure_ascii=False,separators=(',',':'))
import os;print(len(out),len(F),os.path.getsize('data.json'))
