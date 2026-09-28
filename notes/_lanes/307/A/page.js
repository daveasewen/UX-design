(function(){
  var PAGE='sitting-307-reopened-78-v1', PATH='notes/_SITTING-307-reopened-78-2026-09-28-v1.html';
  var ROWS=__ROWS__, THEMES=__THEMES__, N=Object.keys(ROWS).length;
  var KEY='dave-decisions:'+PAGE, st={ans:{},when:{},how:{},notes:{}};
  try{ var s=JSON.parse(localStorage.getItem(KEY)||'null'); if(s&&s.ans){ st=s; ['when','how','notes'].forEach(function(k){ if(!st[k]) st[k]={}; }); } }catch(e){}
  function save(){ try{ localStorage.setItem(KEY, JSON.stringify(st)); }catch(e){} refresh(); }
  function p(n){return (n<10?'0':'')+n;}
  function now(){ var d=new Date(); return d.getFullYear()+'-'+p(d.getMonth()+1)+'-'+p(d.getDate())+' '+p(d.getHours())+':'+p(d.getMinutes()); }
  function today(){ var d=new Date(); return d.getFullYear()+'-'+p(d.getMonth()+1)+'-'+p(d.getDate()); }
  function fname(){ return 'DAVE-RULINGS-'+today()+'-reopened-78.md'; }
  var groups=document.querySelectorAll('.opts'), notes=document.querySelectorAll('textarea[data-g]');
  function paint(){
    groups.forEach(function(g){ var id=g.dataset.q, a=st.ans[id];
      g.querySelectorAll('.opt').forEach(function(b){ b.classList.toggle('on', a===b.dataset.a); b.setAttribute('aria-pressed', a===b.dataset.a?'true':'false'); });
      g.closest('.pr').classList.toggle('done', !!a); });
    notes.forEach(function(t){ t.value=st.notes[t.dataset.g]||''; });
  }
  function set(id,a,how){ st.ans[id]=a; st.when[id]=now(); st.how[id]=how; }
  groups.forEach(function(g){ g.querySelectorAll('.opt').forEach(function(b){ b.addEventListener('click',function(){ var id=g.dataset.q;
    if(st.ans[id]===b.dataset.a){ delete st.ans[id]; delete st.when[id]; delete st.how[id]; } else set(id,b.dataset.a,'click');
    st.at=now(); paint(); save(); }); }); });
  notes.forEach(function(t){ t.addEventListener('input',function(){ if(t.value.trim()) st.notes[t.dataset.g]=t.value; else delete st.notes[t.dataset.g]; st.at=now(); save(); }); });
  function takeAll(ids,how){ var k=0; ids.forEach(function(id){ if(!st.ans[id]){ set(id,ROWS[id].rec,how); k++; } }); st.at=now(); paint(); save(); msg(k?('Filled '+k+' with the recommendation. Change any you like.'):'Every card here is already answered'); }
  document.querySelectorAll('.take').forEach(function(b){ b.addEventListener('click',function(){ var t=THEMES.filter(function(x){return x.k===b.dataset.t;})[0]; takeAll(t.ids,'take-all: '+t.n); }); });
  var tp=document.getElementById('take-page'); if(tp) tp.addEventListener('click',function(){ takeAll(Object.keys(ROWS),'take-all: whole page'); });
  var VN={PARTLY:'partly settled',UNSURE:'likely settled',LIVE:'still open'};
  function markdown(){
    var done=Object.keys(st.ans).filter(function(i){return ROWS[i];}), byTake=done.filter(function(i){return (st.how[i]||'').indexOf('take-all')===0;}).length;
    var L=['# DAVE-RULINGS — The 78 reopened questions, sitting page v1','','file: '+fname()+'  ','source: `'+PATH+'`  ','exported: '+now()+'  ','answered: '+done.length+' of '+N+' ('+byTake+' by a take-all, '+(done.length-byTake)+' by hand)  ','status: his clicks and words, verbatim — quote, never paraphrase',''];
    THEMES.forEach(function(t,ti){
      var a=t.ids.filter(function(i){return st.ans[i];}).length;
      L.push('## '+(ti+1)+'. '+t.n+' ('+a+' of '+t.ids.length+' answered)','');
      t.ids.forEach(function(i){ var r=ROWS[i], k=st.ans[i];
        L.push('- **'+r.q+'**  ');
        if(k) L.push('  → **'+r.o[k]+'** · '+(k===r.rec?'the recommendation':'not the recommendation')+' · '+(st.how[i]||'')+' · '+(st.when[i]||'')+'  ');
        else L.push('  → _not answered_  ');
        if(st.notes[i]&&st.notes[i].trim()) L.push('  his note, verbatim: "'+st.notes[i].trim().replace(/\n/g,' / ')+'"  ');
        L.push('  `'+i+' · '+VN[r.v]+' · #'+r.s+'`');
      });
      L.push('');
    });
    if(st.notes.page&&st.notes.page.trim()){ L.push('## His words, verbatim','','> '+st.notes.page.trim().replace(/\n/g,'\n> '),''); }
    L.push('---','','<details><summary>machine copy</summary>','','```json',JSON.stringify({page:PAGE,path:PATH,file:fname(),exported:now(),answered:done.length,of:N,answers:st},null,2),'```','','</details>','');
    return L.join('\n');
  }
  function msg(s){ var m=document.getElementById('dd-msg'); if(m) m.textContent=s; }
  function copy(){ var t=markdown(); (navigator.clipboard?navigator.clipboard.writeText(t):Promise.reject()).then(function(){msg('Copied — paste it into the chat');},function(){ var ta=document.createElement('textarea');ta.value=t;document.body.appendChild(ta);ta.select();document.execCommand('copy');ta.remove();msg('Copied — paste it into the chat'); }); }
  function saveFile(){ var b=new Blob([markdown()],{type:'text/markdown'}), a=document.createElement('a'); a.href=URL.createObjectURL(b); a.download=fname(); document.body.appendChild(a); a.click(); setTimeout(function(){ URL.revokeObjectURL(a.href); a.remove(); },0); msg('Saved as '+fname()); }
  function clear(){ st={ans:{},when:{},how:{},notes:{}}; paint(); save(); msg('Cleared'); }
  function refresh(){ var d=Object.keys(st.ans).filter(function(i){return ROWS[i];}).length;
    var c=document.getElementById('dd-count'); if(c) c.textContent=d+' of '+N+' answered';
    var tl=document.getElementById('tl-done'); if(tl) tl.textContent=d;
    document.querySelectorAll('.tcount[data-t]').forEach(function(s){ var t=THEMES.filter(function(x){return x.k===s.dataset.t;})[0]; s.textContent=t.ids.filter(function(i){return st.ans[i];}).length+' of '+t.ids.length+' answered'; }); }
  var bar=document.createElement('div'); bar.className='dd-bar';
  bar.innerHTML='<div class="in"><b>Your decisions</b><span id="dd-count"></span><span class="msg" id="dd-msg">Saves in this browser as you go</span><button type="button" class="pri" id="dd-copy">Copy as text</button><button type="button" id="dd-save">Save as file</button><button type="button" id="dd-clear">Clear</button></div>';
  document.body.appendChild(bar);
  document.getElementById('dd-copy').onclick=copy; document.getElementById('dd-save').onclick=saveFile; document.getElementById('dd-clear').onclick=clear;
  window.__sitting={markdown:markdown,fname:fname};
  paint(); refresh();
})();
