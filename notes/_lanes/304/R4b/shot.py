import os, sys
from playwright.sync_api import sync_playwright
f,w,out=sys.argv[1],int(sys.argv[2]),sys.argv[3]
clip=None
if len(sys.argv)>4: x,y,cw,ch=map(float,sys.argv[4].split(',')); clip={"x":x,"y":y,"width":cw,"height":ch}
dpr=float(sys.argv[5]) if len(sys.argv)>5 else 1
with sync_playwright() as p:
    b=p.chromium.launch(executable_path=os.environ["RENDER_SHELL"],headless=True,args=["--no-sandbox"])
    pg=b.new_page(viewport={"width":w,"height":900},device_scale_factor=dpr)
    pg.emulate_media(reduced_motion="reduce")
    pg.goto("file://"+os.path.abspath(f)); pg.wait_for_timeout(600)
    pg.screenshot(path=out, full_page=True, clip=clip) if clip else pg.screenshot(path=out, full_page=True)
    b.close()
print(out)
