from playwright.sync_api import sync_playwright
JS="""()=>{const s=document.querySelector('.seg .ind');const b=document.querySelector('.seg button[aria-pressed="true"]');
const cs=getComputedStyle(s), cb=getComputedStyle(b);
return {ind_bg:cs.backgroundColor, ind_w:cs.width, ind_h:cs.height, ind_rad:cs.borderRadius, ind_op:cs.opacity, btn_color:cb.color, seg_bg:getComputedStyle(document.querySelector('.seg')).backgroundColor};}"""
with sync_playwright() as p:
    b=p.chromium.launch()
    for name,url in [("MOCK","file:///sessions/serene-hopeful-pasteur/mnt/UX-design/reviews/assets/227-confirm/scratch/l3-concentric-ml-mock.html"),
                     ("REAL","file:///sessions/serene-hopeful-pasteur/mnt/UX-design/reviews/SEGMENTED-RULING-2026-08-30-v1.html")]:
        pg=b.new_page(viewport={'width':1300,'height':900}); pg.goto(url); pg.wait_for_timeout(500)
        print(name, pg.evaluate(JS)); pg.close()
    b.close()
