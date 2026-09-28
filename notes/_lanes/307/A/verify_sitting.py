#!/usr/bin/env python3
"""Drive the #307 sitting page: counts, take-all, export, console, clipping, screenshots."""
import os, json, re
from playwright.sync_api import sync_playwright
ROOT=os.getcwd(); A=os.path.join(ROOT,'notes/_lanes/307/A'); PAGE=os.path.join(ROOT,'notes/_SITTING-307-reopened-78-2026-09-28-v1.html')
R={}
with sync_playwright() as pw:
    b=pw.chromium.launch(executable_path=os.environ['RENDER_SHELL'])
    ctx=b.new_context(viewport={'width':1440,'height':900}, accept_downloads=True)
    pg=ctx.new_page(); errs=[]
    pg.on('console', lambda m: errs.append(m.text) if m.type=='error' else None)
    pg.on('pageerror', lambda e: errs.append(str(e)))
    pg.goto('file://'+PAGE); pg.wait_for_timeout(400)
    R['cards']=pg.locator('li.pr').count()
    R['by_verdict']=pg.evaluate("['partly','unsure','live'].map(v=>[v,document.querySelectorAll('li.pr.v-'+v).length])")
    R['themes']=pg.evaluate("[...document.querySelectorAll('section[id^=t-]')].map(s=>[s.querySelector('h2').textContent,s.querySelectorAll('li.pr').length])")
    R['theme_sum']=sum(n for _,n in R['themes'])
    R['ids_unique']=pg.evaluate("new Set([...document.querySelectorAll('li.pr')].map(l=>l.dataset.id)).size")
    R['count_before']=pg.inner_text('#dd-count')
    pg.screenshot(path=A+'/01-top.png')
    # clipping check: text boxes whose content overflows their box
    clip_js="""()=>{const out=[];document.querySelectorAll('.label,.kind,.kind span,.opt,.qq,.k,.tcount,.qt,.qs,.rec,.rid,h1,h2,.sub,.tally b,.tally span,.chip,.dd-bar b,.dd-bar span').forEach(e=>{const cs=getComputedStyle(e);if(cs.display==='none')return;if(e.scrollHeight>e.clientHeight+1&&cs.overflowY!=='visible')out.push(e.className+':'+e.textContent.slice(0,40));if(e.scrollWidth>e.clientWidth+1&&cs.overflowX!=='visible')out.push('x '+e.className+':'+e.textContent.slice(0,40));});return out;}"""
    R['clipped_1440']=pg.evaluate(clip_js)
    R['hscroll_1440']=pg.evaluate("document.documentElement.scrollWidth>innerWidth")
    # line-box vs glyph: any single-line label whose line-height is under 1.2x its font size (descender risk)
    R['tight_lines']=pg.evaluate("""()=>{const o=[];document.querySelectorAll('.label,.kind,.opt,.k,.tcount,.chip,.rt,.qs,.rid').forEach(e=>{const cs=getComputedStyle(e);const lh=parseFloat(cs.lineHeight),fs=parseFloat(cs.fontSize);if(lh&&lh<1.2*fs)o.push(e.className+' '+lh+'/'+fs)});return [...new Set(o)];}""")
    t=pg.locator('#t-colour'); t.scroll_into_view_if_needed(); t.screenshot(path=A+'/02-theme-colour.png')
    c=pg.locator('#c-W-72'); c.scroll_into_view_if_needed(); pg.wait_for_timeout(100)
    pg2=ctx.new_page(); pg2.set_viewport_size({'width':1100,'height':900})
    # close-up at 2x
    ctx2=b.new_context(viewport={'width':1100,'height':900}, device_scale_factor=2); p3=ctx2.new_page(); p3.goto('file://'+PAGE); p3.wait_for_timeout(300)
    p3.locator('#c-W-72').screenshot(path=A+'/03-partly-card-W-72-2x.png')
    p3.locator('#c-W-229').screenshot(path=A+'/04-unsure-card-W-229-2x.png')
    p3.locator('#c-W-391').screenshot(path=A+'/05-newly-settled-W-391-2x.png')
    ctx2.close(); pg2.close()
    # take all in one theme first, then the page
    pg.locator('.take[data-t="old"]').click(); pg.wait_for_timeout(100)
    R['after_theme_take']=pg.inner_text('#dd-count'); R['old_tcount']=pg.inner_text('.tcount[data-t="old"]')
    # change one by hand to prove it stays editable and take-all does not overwrite it
    pg.locator('#c-W-99zr .opt[data-a="c"]').click()
    pg.locator('#c-W-99zr textarea').fill('test note from the verifier')
    pg.locator('#take-page').click(); pg.wait_for_timeout(150)
    R['after_page_take']=pg.inner_text('#dd-count')
    R['on_buttons']=pg.locator('.opt.on').count(); R['done_cards']=pg.locator('li.pr.done').count()
    R['W-99zr_kept_hand_pick']=pg.evaluate("document.querySelector('#c-W-99zr .opt.on').dataset.a")
    R['recommended_on']=pg.evaluate("[...document.querySelectorAll('li.pr')].filter(l=>l.querySelector('.opt.on')&&l.querySelector('.opt.on').dataset.a===l.dataset.rec).length")
    pg.locator('#t-parts').scroll_into_view_if_needed(); pg.wait_for_timeout(100)
    pg.screenshot(path=A+'/06-after-take-all.png')
    with pg.expect_download() as dl: pg.click('#dd-save')
    d=dl.value; R['download_name']=d.suggested_filename
    out=A+'/TEST-EXPORT-by-verifier-'+d.suggested_filename; d.save_as(out)
    md=open(out,encoding='utf-8').read()
    R['export_entries']=len(re.findall(r'^- \*\*',md,re.M))
    R['export_answered_lines']=len(re.findall(r'^  → \*\*',md,re.M))
    R['export_note_present']='his note, verbatim: "test note from the verifier"' in md
    mj=json.loads(re.search(r'```json\n(.*?)```',md,re.S).group(1)); R['export_json_answers']=len(mj['answers']['ans'])
    R['export_path']=out
    # reload persists
    pg.reload(); pg.wait_for_timeout(300); R['after_reload']=pg.inner_text('#dd-count')
    # mobile + dark
    ctx3=b.new_context(viewport={'width':390,'height':844}, color_scheme='dark'); p4=ctx3.new_page(); p4.goto('file://'+PAGE); p4.wait_for_timeout(300)
    R['hscroll_390']=p4.evaluate("document.documentElement.scrollWidth>innerWidth")
    R['clipped_390']=p4.evaluate(clip_js)
    p4.screenshot(path=A+'/07-mobile-dark-top.png')
    p4.locator('#c-W-63').scroll_into_view_if_needed(); p4.screenshot(path=A+'/08-mobile-dark-card.png')
    ctx3.close()
    R['console_errors']=errs
    b.close()
json.dump(R,open(A+'/verify-receipt.json','w'),indent=1,ensure_ascii=False)
print(json.dumps(R,indent=1,ensure_ascii=False))
