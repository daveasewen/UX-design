from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page()
    pg.goto('file:///sessions/serene-hopeful-pasteur/mnt/UX-design/showroom/chart-bar.html')
    pg.wait_for_timeout(400)
    for fam in ['HSBC_MtUnivers_Latin','"Univers Next HSBC"','"Univers Next for HSBC"','DejaVu Sans','NoSuchFaceXYZ']:
        w=pg.evaluate("""(f)=>{const c=document.createElement('canvas').getContext('2d');c.font='40px '+f;return c.measureText('Handgloves 12345').width;}""",fam)
        print(f"{fam:28s} {w}")
    b.close()
