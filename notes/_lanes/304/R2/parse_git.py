#!/usr/bin/env python3
"""R2 helper: parse `git log` dump into commits.json (read-only; regenerable).
Dump made by: git --no-optional-locks log --date=iso-strict --format='%x1e%H%x1f%ad%x1f%s%x1f%b%x1d' --name-only > /tmp/r2/gitlog.raw
"""
import json,sys
raw=open(sys.argv[1],encoding='utf-8',errors='replace').read()
out=[]
for rec in raw.split('\x1e')[1:]:
    head,_,files=rec.partition('\x1d')
    sha,date,subj,body=(head.split('\x1f')+['','','',''])[:4]
    out.append({'sha':sha,'date':date,'subject':subj,'body':body,'files':[f for f in files.split('\n') if f.strip()]})
out.reverse()  # oldest first
json.dump(out,open(sys.argv[2],'w'),ensure_ascii=False)
print(len(out),'commits', out[0]['date'], '->', out[-1]['date'])
