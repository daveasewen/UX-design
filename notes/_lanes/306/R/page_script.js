(function(){
  var PAGE='decide-306-wrap-redesign-v1', PATH='notes/_DECIDE-306-wrap-redesign-2026-09-28-v1.html';
  var KEY='dave-decisions:'+PAGE, st={notes:{},dec:{}};
  try{ var s=JSON.parse(localStorage.getItem(KEY)||'null'); if(s&&s.dec) st=s; if(!st.notes) st.notes={}; }catch(e){}
  function save(){ try{ localStorage.setItem(KEY, JSON.stringify(st)); }catch(e){} refresh(); }
  function now(){ var d=new Date(),p=function(n){return (n<10?'0':'')+n;}; return d.getFullYear()+'-'+p(d.getMonth()+1)+'-'+p(d.getDate())+' '+p(d.getHours())+':'+p(d.getMinutes()); }
  var notes=document.querySelectorAll('textarea[data-g]'), chips=document.querySelectorAll('.chips');
  function paint(){
    notes.forEach(function(t){ t.value=st.notes[t.dataset.g]||''; });
    chips.forEach(function(c){ c.querySelectorAll('.chip').forEach(function(b){ b.classList.toggle('on', st.dec[c.dataset.d]===b.dataset.a); }); });
  }
  notes.forEach(function(t){ t.addEventListener('input',function(){ if(t.value.trim()) st.notes[t.dataset.g]=t.value; else delete st.notes[t.dataset.g]; st.at=now(); save(); }); });
  chips.forEach(function(c){ c.querySelectorAll('.chip').forEach(function(b){ b.addEventListener('click',function(){ var d=c.dataset.d; if(st.dec[d]===b.dataset.a) delete st.dec[d]; else st.dec[d]=b.dataset.a; st.at=now(); paint(); save(); }); }); });
  function qtext(c){ var li=c.closest('li'); var b=li.querySelector('b'); return b?b.textContent.trim():c.dataset.d; }
  function rtext(c){ var li=c.closest('li'); var r=li.querySelector('.rec'); return r?r.textContent.replace(/^Recommended:\s*/,'').trim():''; }
  function atext(c,a){ var b=c.querySelector('.chip[data-a="'+a+'"]'); return b?b.textContent.trim():a; }
  function markdown(){
    var L=['# DAVE-RULINGS — The wrap redesign, decision page v1','','source: `'+PATH+'`  ','exported: '+now()+'  ','status: his clicks and words, verbatim — quote, never paraphrase',''];
    L.push('## The six calls','');
    chips.forEach(function(c,i){ var a=st.dec[c.dataset.d]; L.push((i+1)+'. '+qtext(c)); L.push('   → **'+(a?atext(c,a):'not answered')+'** (recommended: '+rtext(c)+')'); });
    if(st.notes.page&&st.notes.page.trim()){ L.push('','## His words, verbatim','','> '+st.notes.page.trim().replace(/\n/g,'\n> ')); }
    L.push('','---','','<details><summary>machine copy</summary>','','```json',JSON.stringify({page:PAGE,path:PATH,exported:now(),answers:st},null,2),'```','','</details>','');
    return L.join('\n');
  }
  window.__ddMarkdown=markdown;
  function msg(s){ var m=document.getElementById('dd-msg'); if(m) m.textContent=s; }
  function copy(){ var t=markdown(); (navigator.clipboard?navigator.clipboard.writeText(t):Promise.reject()).then(function(){msg('Copied — paste it into the chat');},function(){ var ta=document.createElement('textarea');ta.value=t;document.body.appendChild(ta);ta.select();document.execCommand('copy');ta.remove();msg('Copied — paste it into the chat'); }); }
  function clear(){ st={notes:{},dec:{}}; paint(); save(); msg('Cleared'); }
  function refresh(){ var c=document.getElementById('dd-count'); if(c) c.textContent=Object.keys(st.dec).length+' of '+chips.length+' calls'; }
  var bar=document.createElement('div'); bar.className='dd-bar';
  bar.innerHTML='<div class="in"><b>Your decisions</b><span id="dd-count"></span><span class="msg" id="dd-msg">Saves in this browser as you go</span><button type="button" class="pri" id="dd-copy">Copy as text</button><button type="button" id="dd-clear">Clear</button></div>';
  document.body.appendChild(bar);
  document.getElementById('dd-copy').onclick=copy; document.getElementById('dd-clear').onclick=clear;
  paint(); refresh();
})();
