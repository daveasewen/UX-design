import re, sys, json, pathlib

SNIPPET = r'''
<!-- ===== DAVE'S DECISIONS & COMMENTS — added #289, self-contained, autosaves in this browser, exports markdown ===== -->
<style>
.dd-box{margin:var(--s4,2rem) 0 0;border:1px solid var(--grey-3,#D7D8D6);background:var(--white,#fff);color:var(--black,#000);
  font-family:"Helvetica Neue",Helvetica,Arial,sans-serif;font-size:14px;line-height:1.5;padding:1.25rem 1.5rem;
  border-left:4px solid var(--accent,#DA1A00)}
.dd-box.dd-has{border-left-color:var(--black,#000)}
.dd-head{display:flex;align-items:center;justify-content:space-between;gap:1rem;flex-wrap:wrap;margin-bottom:.75rem}
.dd-label{font-size:11px;font-weight:500;letter-spacing:.14em;text-transform:uppercase;color:var(--accent,#DA1A00)}
.dd-box.dd-has .dd-label{color:var(--grey-6,#767676)}
.dd-chips{display:flex;gap:.35rem;flex-wrap:wrap}
.dd-chip{font:inherit;font-size:11px;letter-spacing:.08em;text-transform:uppercase;padding:.25rem .6rem;border:1px solid var(--grey-3,#D7D8D6);
  background:var(--white,#fff);color:var(--grey-7,#545454);cursor:pointer;border-radius:0}
.dd-chip:hover{border-color:var(--black,#000);color:var(--black,#000)}
.dd-chip.on{background:var(--black,#000);color:var(--white,#fff);border-color:var(--black,#000)}
.dd-grid{display:grid;grid-template-columns:1fr 1fr;gap:1rem}
.dd-field{display:flex;flex-direction:column;gap:.3rem}
.dd-field span{font-size:11px;letter-spacing:.1em;text-transform:uppercase;color:var(--grey-6,#767676);font-weight:500}
.dd-field textarea{font:inherit;font-size:14px;line-height:1.5;color:var(--black,#000);background:var(--grey-1,#F3F3F3);border:0;
  border-bottom:1px solid var(--grey-3,#D7D8D6);padding:.6rem .75rem;min-height:4.5rem;resize:vertical;width:100%;border-radius:0}
.dd-field textarea:focus{outline:none;border-bottom-color:var(--accent,#DA1A00);background:var(--white,#fff);box-shadow:inset 0 0 0 1px var(--grey-3,#D7D8D6)}
.dd-stamp{font-size:11px;color:var(--grey-5,#9B9B9B);margin-top:.5rem;min-height:1em}
.dd-bar{position:fixed;left:0;right:0;bottom:0;z-index:99;background:var(--black,#000);color:var(--white,#fff);
  font-family:"Helvetica Neue",Helvetica,Arial,sans-serif;font-size:12px;letter-spacing:.04em}
.dd-bar .in{max-width:var(--max-width,var(--max,1200px));margin:0 auto;padding:.6rem 2rem;display:flex;align-items:center;gap:1.25rem;flex-wrap:wrap}
.dd-bar b{font-weight:500}
.dd-bar button{font:inherit;font-size:11px;letter-spacing:.1em;text-transform:uppercase;padding:.45rem .9rem;border:1px solid var(--grey-6,#767676);
  background:transparent;color:var(--white,#fff);cursor:pointer;border-radius:0}
.dd-bar button:hover{border-color:var(--white,#fff)}
.dd-bar button.pri{background:var(--accent,#DA1A00);border-color:var(--accent,#DA1A00)}
.dd-bar .msg{color:var(--grey-5,#9B9B9B);flex:1;min-width:0;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
body{padding-bottom:64px}
@media (max-width:820px){.dd-grid{grid-template-columns:1fr}.dd-bar .in{padding:.6rem 1rem;gap:.6rem}}
@media print{.dd-bar{display:none}body{padding-bottom:0}}
</style>
<script>
(function(){
  var CFG = __CFG__;
  var KEY = 'dave-decisions:' + CFG.page;
  var CHIPS = ['Inscribe','Do it','Later','No','Question'];
  var state = {}; try{ state = JSON.parse(localStorage.getItem(KEY)||'{}'); }catch(e){ state = {}; }
  function save(){ try{ localStorage.setItem(KEY, JSON.stringify(state)); }catch(e){} refresh(); }
  function txt(el){ return (el ? el.textContent : '').replace(/\s+/g,' ').trim(); }
  function esc(s){ return String(s||'').replace(/[&<>"]/g,function(c){return {'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c];}); }
  function now(){ var d=new Date(),p=function(n){return (n<10?'0':'')+n;}; return d.getFullYear()+'-'+p(d.getMonth()+1)+'-'+p(d.getDate())+' '+p(d.getHours())+':'+p(d.getMinutes()); }

  // ---- collect anchors -------------------------------------------------
  var items = [];
  CFG.targets.forEach(function(t){
    var nodes = document.querySelectorAll(t.sel);
    Array.prototype.forEach.call(nodes, function(el, i){
      if (t.skip && t.skip(el)) return;
      var id = el.id || (t.prefix + '-' + (i+1));
      var num = txt(el.querySelector(t.num||'.idx')) || (t.count ? String(i+1).padStart(2,'0') : '') || (t.fallbackNum ? txt(el.querySelector(t.fallbackNum)) : '');
      var title = txt(el.querySelector(t.title));
      items.push({ id:id, kind:t.kind, num:num, title:title, host: (typeof t.host==='function' ? t.host(el) : (t.host && el.querySelector(t.host))) || el.querySelector('.wrap') || el });
    });
  });
  items.push({ id:'page', kind:'Whole page', num:'', title:'Anything that belongs to the page rather than one section', host: document.querySelector(CFG.pageHost) });

  // ---- render ----------------------------------------------------------
  items.forEach(function(it){
    var s = state[it.id] || {};
    var box = document.createElement('div');
    box.className = 'dd-box'; box.dataset.id = it.id; box.id = 'dd-'+it.id;
    box.innerHTML =
      '<div class="dd-head"><span class="dd-label">Dave · '+esc(it.kind)+(it.num?' '+esc(it.num):'')+'</span>'+
      '<span class="dd-chips">'+CHIPS.map(function(c){return '<button type="button" class="dd-chip'+(s.verdict===c?' on':'')+'" data-v="'+c+'">'+c+'</button>';}).join('')+'</span></div>'+
      '<div class="dd-grid">'+
        '<label class="dd-field"><span>Decision — in your words</span><textarea data-f="decision" placeholder="What you rule, or what you want done.">'+esc(s.decision)+'</textarea></label>'+
        '<label class="dd-field"><span>Comment</span><textarea data-f="comment" placeholder="Anything else — a doubt, a question back, a reason.">'+esc(s.comment)+'</textarea></label>'+
      '</div><div class="dd-stamp">'+(s.at?'saved '+esc(s.at):'')+'</div>';
    it.host.appendChild(box);
    box.addEventListener('click', function(e){
      var b = e.target.closest('.dd-chip'); if(!b) return;
      var v = b.dataset.v; var cur = state[it.id]||{};
      cur.verdict = (cur.verdict===v) ? '' : v; cur.at = now(); state[it.id]=cur; save();
      box.querySelectorAll('.dd-chip').forEach(function(c){ c.classList.toggle('on', c.dataset.v===cur.verdict); });
    });
    box.addEventListener('input', function(e){
      var f = e.target.dataset && e.target.dataset.f; if(!f) return;
      var cur = state[it.id]||{}; cur[f]=e.target.value; cur.at=now(); state[it.id]=cur; save();
    });
  });

  function has(s){ return s && (s.verdict || (s.decision||'').trim() || (s.comment||'').trim()); }
  function refresh(){
    var n=0;
    items.forEach(function(it){
      var s=state[it.id], box=document.querySelector('.dd-box[data-id="'+it.id+'"]');
      if(has(s)) n++;
      if(box){ box.classList.toggle('dd-has', !!has(s)); box.querySelector('.dd-stamp').textContent = (s&&s.at)?'saved '+s.at:''; }
    });
    var c=document.getElementById('dd-count'); if(c) c.textContent = n+' of '+items.length+' answered';
  }

  // ---- export ----------------------------------------------------------
  function markdown(){
    var lines = ['# DAVE-RULINGS — '+CFG.title, '', 'source: `'+CFG.path+'`  ', 'exported: '+now()+'  ', 'status: his words, verbatim — quote, never paraphrase', ''];
    var n=0;
    items.forEach(function(it){
      var s=state[it.id]; if(!has(s)) return; n++;
      lines.push('## '+(it.num?it.num+' · ':'')+it.title+'  ');
      lines.push('<sub>'+it.kind+' · anchor `#dd-'+it.id+'` · saved '+s.at+'</sub>', '');
      if(s.verdict) lines.push('**Verdict:** '+s.verdict, '');
      if((s.decision||'').trim()) lines.push('**Decision, verbatim:**', '', '> '+s.decision.trim().replace(/\n/g,'\n> '), '');
      if((s.comment||'').trim()) lines.push('**Comment, verbatim:**', '', '> '+s.comment.trim().replace(/\n/g,'\n> '), '');
    });
    if(!n) lines.push('_Nothing answered yet._');
    lines.push('', '---', '', '<details><summary>machine copy</summary>', '', '```json', JSON.stringify({page:CFG.page, path:CFG.path, exported:now(), answers:state}, null, 2), '```', '', '</details>', '');
    return lines.join('\n');
  }
  function download(){
    var d=new Date(),p=function(n){return (n<10?'0':'')+n;};
    var name='DAVE-RULINGS-'+d.getFullYear()+'-'+p(d.getMonth()+1)+'-'+p(d.getDate())+'-'+CFG.page+'.md';
    var blob=new Blob([markdown()],{type:'text/markdown'}); var a=document.createElement('a');
    a.href=URL.createObjectURL(blob); a.download=name; document.body.appendChild(a); a.click(); a.remove();
    msg('Saved '+name+' to Downloads — drop it in notes/_lanes/289/');
  }
  function copy(){ var t=markdown(); (navigator.clipboard?navigator.clipboard.writeText(t):Promise.reject()).then(function(){msg('Copied — paste it into the chat');},function(){ var ta=document.createElement('textarea');ta.value=t;document.body.appendChild(ta);ta.select();document.execCommand('copy');ta.remove();msg('Copied — paste it into the chat'); }); }
  function clear(){ if(!confirm('Clear every decision and comment on this page?')) return; state={}; save(); document.querySelectorAll('.dd-box textarea').forEach(function(t){t.value='';}); document.querySelectorAll('.dd-chip.on').forEach(function(c){c.classList.remove('on');}); msg('Cleared'); }
  function msg(s){ var m=document.getElementById('dd-msg'); if(m){ m.textContent=s; } }

  var bar=document.createElement('div'); bar.className='dd-bar';
  bar.innerHTML='<div class="in"><b>Your decisions</b><span id="dd-count"></span><span class="msg" id="dd-msg">Autosaves as you type</span>'+
    '<button type="button" id="dd-copy">Copy as text</button><button type="button" class="pri" id="dd-dl">Export rulings .md</button><button type="button" id="dd-clear">Clear</button></div>';
  document.body.appendChild(bar);
  document.getElementById('dd-dl').onclick=download; document.getElementById('dd-copy').onclick=copy; document.getElementById('dd-clear').onclick=clear;
  refresh();
})();
</script>
'''

def inject(path, cfg):
    p = pathlib.Path(path); html = p.read_text()
    html = re.sub(r"\n<!-- ===== DAVE'S DECISIONS.*?</script>\n", '', html, flags=re.S)
    js = SNIPPET.replace('__CFG__', cfg)
    assert html.count('</body>') == 1
    html = html.replace('</body>', js + '\n</body>')
    p.write_text(html); print('injected', path, len(html))

STRAND = '''{
    page:'strand-map', title:'the strand map and the path to Friday the 25th', path:'notes/_STRAND-MAP-2026-09-19.html',
    pageHost:'footer .wrap',
    targets:[
      { sel:'section[id]', kind:'Section', num:'.idx', fallbackNum:'.label', title:'h2',
        host:function(el){ return el.classList.contains('dimension') ? el.querySelector('.wrap > div:last-child') : el.querySelector('.wrap'); },
        skip:function(el){ return el.classList.contains('hero') || el.id==='index'; } }
    ]
  }'''

REVIEW = '''{
    page:'template-quality-review', title:'the bento template — a quality review', path:'notes/_lanes/288/T/template-quality-review.html',
    pageHost:'footer .wrap',
    targets:[
      { sel:'section#verdict', kind:'Verdict', title:'h1, h2, .big', host:'.wrap', prefix:'verdict' },
      { sel:'.finding', kind:'Finding', num:'.idx', title:'h3', host:'.body', prefix:'finding' },
      { sel:'ol.q > li', kind:'Question', title:'h3', host:'.body', prefix:'question', count:true }
    ]
  }'''

PROP = '''{
    page:'proposal-story-v1', title:'the Apollo story, proposal v1', path:'notes/_PROPOSAL-apollo-story-2026-09-19-v1.html',
    pageHost:'footer .wrap',
    targets:[
      { sel:'section[id]', kind:'Section', fallbackNum:'.label', title:'h2, .line', host:'.wrap > div:last-child',
        skip:function(el){ return el.id==='tech'; } },
      { sel:'.beats > li', kind:'Beat', title:'b', host:'div', prefix:'beat', count:true }
    ]
  }'''
root = '/sessions/adoring-relaxed-allen/mnt/UX-design/'
if sys.argv[1:]==['prop2']:
    inject(root+'notes/_PROPOSAL-apollo-story-2026-09-20-v2.html', PROP.replace("proposal-story-v1","proposal-story-v2").replace("proposal v1","proposal v2").replace("2026-09-19-v1","2026-09-20-v2"))
elif sys.argv[1:]==['prop']:
    inject(root+'notes/_PROPOSAL-apollo-story-2026-09-19-v1.html', PROP)
else:
    inject(root+'notes/_STRAND-MAP-2026-09-19.html', STRAND)
    inject(root+'notes/_lanes/288/T/template-quality-review.html', REVIEW)
