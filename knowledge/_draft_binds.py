#!/usr/bin/env python3
"""s141 binds drafter — DRAFT ONLY, edits nothing. Writes reviews/BINDS-DRAFT-*.json."""
import json,glob,os,re,sys,datetime
ROOT='/sessions/gracious-focused-lamport/mnt/UX-design'
sys.path.insert(0,os.path.join(ROOT,'knowledge'))
import importlib.util
spec=importlib.util.spec_from_file_location('dtcg',os.path.join(ROOT,'knowledge','_validate_dtcg.py'))
dtcg=importlib.util.module_from_spec(spec); spec.loader.exec_module(dtcg)
files,_=dtcg.corpus_files(os.path.join(ROOT,'knowledge'))
TOKENS,GROUPS,_pf=dtcg.build_spine(files)
SPINE=set(TOKENS)|set(GROUPS)

# ---- VISUAL classification. Declared lists: a reader can disagree with the RULE. ----
VISUAL_NAMES={'size','width','height','fontsize','surface','state','status','variant','shape',
 'style','elevation','radius','opacity','fillalpha','glyph','sign','highcontrast','tone',
 'density','emphasis','scale','type','version','posture','visual','side','placement',
 'orientation','selected','open','disabled','error','breakpoint','mode','sticky','shimmer',
 'itemstate','handlestate','datecellstate','chiptype','bullettype','checkboxkind','control',
 'masked','redacted','image','tag','family','direction','delta','marker','markers'}
NONVISUAL_NAMES={'data','series','items','actions','title','label','message','content','help',
 'action','link','value','total','rows','columns','categories','ranges','slices','sessions',
 'bins','accounts','filters','pagesize','min','max','from/to','mindate/maxdate','index',
 'startindex','length','steps','totalsteps','currentstep','period','amount','currency','text',
 'body','detail','accept','maxsize','multiple','multiline','multilink','module','auth','form',
 'target','sort','selection','itemselection','reorder','predictive','resend','gate','version',
 'labelling','measure','outliers','trendline','secondaryaxis','intersection','xgrammar',
 'valuemode','tablepopover','legendfilter','errorsummary','pairrow','buttons','flyout',
 'backnavigation','asset','platform','element','optionalmarker','up','down','empty','date'}
NONVISUAL_TYPES={'function','mechanism','table','array','date'}

SLASHPATH=re.compile(r'(?<![\w/.-])([a-z][\w-]*(?:/[\w./-]+)+)')
def candidates(s):
    """token-ish slash paths mentioned in a tokens-map value, resolved against the spine."""
    out=[]
    for m in SLASHPATH.findall(s if isinstance(s,str) else ''):
        d=m.replace('/','.').rstrip('.')
        for cand in (d, d.replace('.','-',0)):
            if cand in SPINE and cand not in out: out.append(cand)
    return out


# ---- candidate FAMILIES for common visual prop names. NOT proposals: these are the
# ---- spine addresses that COULD be meant, offered so Dave can pick in the controller.
# ---- Every entry is resolved against the spine before it is offered.
CANDIDATE_FAMILIES={
 'size':['icon.xsmall','icon.small','icon.medium','icon.large','target.min','spacing'],
 'state':['text.default','text.disabled','form.background','form.border','button'],
 'status':['rag.success','rag.warning','rag.error','rag.neutral'],
 'variant':['button.primary','button.secondary','button.tertiary','button.quaternary'],
 'surface':['background.default','surface.raised','surface.subtle','surface.action'],
 'elevation':['elevation.functional','elevation.decorative','elevation.border'],
 'radius':['border-radius.control','border-radius.surface','border-radius.indicator'],
 'shape':['border-radius.control','border-radius.surface','border-radius.indicator'],
 'opacity':['alpha'],'fillalpha':['alpha'],
 'fontsize':['typography.font-size'],
 'width':['border-width.small','border-width.medium','border-width.large'],
 'highcontrast':['data.series-high-contrast'],
 'breakpoint':['breakpoint','scale'],
 'mode':['background.default'],
 'glyph':['icon.default','icon.default-reverse','icon.disabled'],
 'orientation':[],'sign':['rag.success','rag.error'],
}
def family_candidates(n):
    out=[]
    for c in CANDIDATE_FAMILIES.get(n,[]):
        if c in SPINE or any(k.startswith(c+'.') for k in SPINE): out.append(c)
    return out

def flat_tokens(v,pre=''):
    if isinstance(v,str): yield pre,v
    elif isinstance(v,dict):
        for k,x in v.items():
            if k.startswith('$'): continue
            yield from flat_tokens(x, (pre+'/'+k if pre else k))

def norm(s): return re.sub(r'[^a-z0-9]','',s.lower())

rows=[]; doubts=0; metas_with=set()
for f in sorted(glob.glob(os.path.join(ROOT,'knowledge','components','*.meta.json'))):
    b=os.path.basename(f)
    if b.startswith('EXAMPLE'): continue
    comp=b[:-len('.meta.json')]
    d=json.load(open(f))
    tmap=list(flat_tokens(d.get('tokens',{})))
    for p in d.get('props',[]):
        name=p['name']; n=norm(name); ptype=p.get('type','')
        row={'component':comp,'prop':name,'propType':ptype}
        if ptype in NONVISUAL_TYPES or n in {norm(x) for x in NONVISUAL_NAMES}:
            row['classification']='NON-VISUAL'; row['proposedBinds']=None
            row['rationale']='content/data/behaviour prop — no visual value to bind (s136-D1 axis A applies to VISUAL props only)'
            rows.append(row); continue
        if n not in {norm(x) for x in VISUAL_NAMES}:
            row['classification']='UNCLASSIFIED'; row['proposedBinds']=None
            row['$doubt']='prop name is in neither the declared VISUAL nor NON-VISUAL list — classification is a judgment, not a measurement'
            row['rationale']='unknown is never defaulted'
            rows.append(row); doubts+=1; continue
        row['classification']='VISUAL'
        # evidence: this meta's own tokens map
        by_prop=[(k,v) for k,v in tmap if norm(k)==n or n in norm(k) or norm(k) in n]
        vals=[str(x) for x in (p.get('values') or [])]
        by_value={}
        for val in vals:
            hits=[(k,v) for k,v in tmap if norm(k)==norm(val)]
            for k,v in hits:
                c=candidates(v)
                if c: by_value.setdefault(val,[]).extend(c)
        cand=[]
        for k,v in by_prop: cand.extend(candidates(v))
        cand=list(dict.fromkeys(cand))
        if by_value and len(by_value)>=2:
            row['proposedBinds']={k:(v[0] if len(v)==1 else v) for k,v in by_value.items()}
            row['bindsShape']='intent map (s140-D1 hybrid)'
            row['rationale']='per-value bindings recovered from this meta\'s own tokens map; every path resolves in the spine'
            metas_with.add(comp)
        elif len(cand)==1:
            row['proposedBinds']=cand[0]; row['bindsShape']='single token name (s140-D1 hybrid)'
            row['rationale']='sole resolving token path in this meta\'s tokens map entry matching the prop name'
            metas_with.add(comp)
        elif len(cand)>1:
            row['proposedBinds']=cand; row['bindsShape']='array (s140-D1 hybrid)'
            row['rationale']='multiple resolving token paths matched the prop name in this meta\'s tokens map; ARRAY drafted, but which subset the prop actually drives is unproven'
            row['$doubt']='array drafted from co-mentioned paths — Dave to confirm the set is the prop\'s, not the component\'s'
            doubts+=1; metas_with.add(comp)
        else:
            raw=[v for k,v in by_prop] or [v for k,v in tmap if norm(k)==n]
            row['proposedBinds']=None
            fc=family_candidates(n)
            if fc: row['spineCandidates']=fc
            row['$doubt']=('no token path in this meta resolves for this prop — '
                + ('the tokens-map entry is prose, not a path: %r'%(raw[0][:160],) if raw
                   else 'the meta declares no tokens entry for this prop at all'))
            row['rationale']='a token NAME is not an ADDRESS — refusing to invent one'
            doubts+=1
        rows.append(row)

out={'$schema':'s141 binds draft (DRAFT — no meta.json was edited)',
 'ruling':'s136-D1 axis A + s140-D1 bindsShape (hybrid)','date':str(datetime.date.today()),
 'method':{'classification':'declared VISUAL / NON-VISUAL name lists + non-visual types; anything in neither list is UNCLASSIFIED and gets a $doubt, never a guess',
  'sourceOfBindings':"each meta's OWN tokens map — slash paths extracted and RESOLVED against the live spine index built by knowledge/_validate_dtcg.py; an unresolved path is never proposed",
  'spineCandidates':'offered on $doubt rows ONLY as a pick-list of resolvable spine addresses — an offer is not a proposal',
  'notARuling':'this file proposes; Dave rules; the conductor enacts'},
 'summary':{'metas':len({r['component'] for r in rows}),
   'props':len(rows),
   'visual':sum(1 for r in rows if r['classification']=='VISUAL'),
   'nonVisual':sum(1 for r in rows if r['classification']=='NON-VISUAL'),
   'unclassified':sum(1 for r in rows if r['classification']=='UNCLASSIFIED'),
   'propsWithProposedBinds':sum(1 for r in rows if r.get('proposedBinds')),
   'metasThatWouldCarryAtLeastOneBinds':len(metas_with),
   'doubtRows':doubts,
   'doubtRowsCarryingSpineCandidates':sum(1 for r in rows if r.get('spineCandidates'))},
 'metasThatWouldCarryBinds':sorted(metas_with),
 'rows':rows}
p=os.path.join(ROOT,'reviews','BINDS-DRAFT-2026-08-09-s141-v1.json')
json.dump(out,open(p,'w'),indent=2,ensure_ascii=False)
print(json.dumps(out['summary'],indent=1)); print('->',p)
