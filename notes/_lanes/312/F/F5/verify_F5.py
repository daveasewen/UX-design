#!/usr/bin/env python3
"""#312 lane F5 - verify the review page at 1440 and 390 and prove Copy as text returns every call.
Run at the seat, in ONE bash call:
  export TMPDIR=/dev/shm; bash knowledge/_render/ensure_env.sh; source knowledge/_render/seat_env.sh
  python3 notes/_lanes/312/F/F5/verify_F5.py
Writes notes/_lanes/312/F/F5/img/*.png, F5-verify.json and F5-copy-text-proof.txt. Reads nothing but the page.
"""
import os, json
from playwright.sync_api import sync_playwright

REPO = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..', '..', '..'))
PAGE = os.path.join(REPO, 'notes', '_REVIEW-312-F-the-pictures-you-are-owed-2026-10-01-v1.html')
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'img')
os.makedirs(OUT, exist_ok=True)
URL = 'file://' + PAGE
facts = {'page': os.path.relpath(PAGE, REPO), 'widths': {}}

PROBE = r"""() => {
  const imgs=[...document.images];
  const broken=imgs.filter(i=>!i.complete||i.naturalWidth===0).map(i=>i.getAttribute('src'));
  const vw=document.documentElement.clientWidth;
  const over=[];
  document.querySelectorAll('body *').forEach(el=>{
    if(el.closest('.scroll')||el.closest('nav.toc')||el.closest('.bar')) return;
    const r=el.getBoundingClientRect();
    if(r.width>0 && r.right>vw+1) over.push((el.tagName+'.'+(el.className||'')).slice(0,60)+' right='+Math.round(r.right));
  });
  return {imgs:imgs.length, broken, scrollW:document.documentElement.scrollWidth, clientW:vw,
          bodyScrollW:document.body.scrollWidth, overflowing:over.slice(0,12), overflowCount:over.length,
          calls:document.querySelectorAll('.call').length, glanceRows:document.querySelectorAll('#glance-table tbody tr').length,
          height:document.documentElement.scrollHeight};
}"""

with sync_playwright() as p:
    b = p.chromium.launch(executable_path=os.environ.get('RENDER_SHELL'))
    for w, h in ((1440, 900), (390, 844)):
        ctx = b.new_context(viewport={'width': w, 'height': h}, device_scale_factor=1)
        pg = ctx.new_page()
        pg.goto(URL, wait_until='load')
        pg.wait_for_timeout(600)
        pg.evaluate("()=>{try{localStorage.clear()}catch(e){}}")
        pg.reload(wait_until='load'); pg.wait_for_timeout(600)
        pg.add_style_tag(content='html{scroll-behavior:auto !important}')
        r = pg.evaluate(PROBE)
        shots = []
        for anchor in ('top', 'glance', 'containers', 'topnav', 'ring', 'forks', 'house'):
            pg.evaluate("(a)=>{const e=document.getElementById(a); window.scrollTo(0, e? e.getBoundingClientRect().top+window.scrollY-52 : 0)}", anchor)
            pg.wait_for_timeout(250)
            f = f'F5-{w}-{anchor}.png'
            pg.screenshot(path=os.path.join(OUT, f))
            shots.append(f)
        r['shots'] = shots
        if w == 1440:
            # Copy as text, before any answer
            t0 = pg.evaluate('()=>window.__reviewText()')
            qs = pg.evaluate("()=>[...document.querySelectorAll('.call')].map(e=>({id:e.dataset.id,q:e.dataset.q,rec:e.dataset.rec}))")
            r['before'] = {'every_q_present': all(q['q'] in t0 for q in qs), 'not_answered': t0.count('Chose: not answered'),
                           'recommended_lines': t0.count('   Recommended: ')}
            # click every recommended chip, and write a page note
            for q in qs:
                if q['rec']:
                    pg.locator(f'.call[data-id="{q["id"]}"] .chip[data-v="{q["rec"]}"]').click()
            pg.locator('.call[data-id="page"] textarea').fill('F5 verify note')
            pg.locator('.call[data-id="containers"] textarea').fill('F5 verify comment on call 1')
            t1 = pg.evaluate('()=>window.__reviewText()')
            r['after'] = {'every_q_present': all(q['q'] in t1 for q in qs), 'the_recommendation': t1.count('(the recommendation)'),
                          'not_answered': t1.count('Chose: not answered'), 'page_note': 'F5 verify note' in t1,
                          'comment_1': 'F5 verify comment on call 1' in t1,
                          'count': pg.inner_text('#count'),
                          'glance_recommended': pg.evaluate("()=>[...document.querySelectorAll('#glance-table tbody td.st')].filter(t=>t.textContent==='Recommended').length")}
            # Copy button: does it report success
            try:
                ctx.grant_permissions(['clipboard-read', 'clipboard-write'])
            except Exception as e:
                r['after']['grant'] = str(e)[:120]
            pg.click('#copy'); pg.wait_for_timeout(400)
            r['after']['copy_msg'] = pg.inner_text('#msg')
            try:
                clip = pg.evaluate('()=>navigator.clipboard.readText()')
                r['after']['clipboard_equals_text'] = (clip == pg.evaluate('()=>window.__reviewText()'))
            except Exception as e:
                r['after']['clipboard_read'] = 'unavailable: ' + str(e)[:100]
            # Export button produces a download
            try:
                with pg.expect_download(timeout=5000) as dl:
                    pg.click('#export')
                d = dl.value
                path = os.path.join('/dev/shm', 'f5-export.txt'); d.save_as(path)
                r['after']['export_file'] = d.suggested_filename
                r['after']['export_equals_text'] = (open(path).read() == pg.evaluate('()=>window.__reviewText()'))
            except Exception as e:
                r['after']['export'] = 'failed: ' + str(e)[:120]
            # persistence across a reload
            pg.reload(wait_until='load'); pg.wait_for_timeout(500)
            pg.add_style_tag(content='html{scroll-behavior:auto !important}')
            r['after']['count_after_reload'] = pg.inner_text('#count')
            with open(os.path.join(os.path.dirname(OUT), 'F5-copy-text-proof.txt'), 'w') as fh:
                fh.write(pg.evaluate('()=>window.__reviewText()'))
            pg.evaluate("()=>{const e=document.getElementById('glance-table'); window.scrollTo(0, e.getBoundingClientRect().top+window.scrollY-60)}"); pg.wait_for_timeout(300)
            pg.screenshot(path=os.path.join(OUT, 'F5-1440-answered-glance.png'))
            pg.evaluate("()=>{try{localStorage.clear()}catch(e){}}")
        if w == 390:
            for cid in ('containers','navfamily','topnav-rule'):
                pg.locator(f'.call[data-id="{cid}"] .chip em').first.click()
            pg.evaluate("()=>{const e=document.getElementById('glance-table'); window.scrollTo(0, e.getBoundingClientRect().top+window.scrollY-60)}"); pg.wait_for_timeout(300)
            pg.screenshot(path=os.path.join(OUT, 'F5-390-answered-glance.png'))
            r['answered_390'] = pg.inner_text('#count')
            pg.evaluate("()=>{try{localStorage.clear()}catch(e){}}")
        facts['widths'][w] = r
        ctx.close()
    b.close()

with open(os.path.join(os.path.dirname(OUT), 'F5-verify.json'), 'w') as fh:
    json.dump(facts, fh, indent=1)
print(json.dumps(facts, indent=1))
