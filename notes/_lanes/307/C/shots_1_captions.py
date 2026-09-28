"""Item 1 — the dark caption ground in all four themes. Real artefact: the 'Capsule — Dark grey'
card on showroom/_foundations/bento-rails.html (canon.css + the page's generated CAPTION_GROUND_MINTS
block). Per theme: html[data-apollo-theme] set to the theme and body[data-theme] to the mode — the page's
own switch mechanism — and the card's own console scope attribute taken off so the card sits in the
page's theme. (Left on, a card-level theme attribute re-declares that theme's LIGHT page ground under a
dark body: supercharge measured #F7F6F4 behind a dark card. Recorded in the lane report.) Nothing redrawn."""
import sys; sys.path.insert(0, __file__.rsplit('/',1)[0])
from _lib import *

THEMES = ["mono", "legacy", "console", "supercharge"]
res = {}
with sync_playwright() as p:
    b = launch(p)
    pg = b.new_page(viewport={"width": 1440, "height": 1000}, device_scale_factor=2)
    pg.goto(url("showroom/_foundations/bento-rails.html"))
    wait_images(pg); fonts_ready(pg)
    card = pg.locator(".br-card", has=pg.locator("h4", has_text="Capsule — Dark grey")).first
    spec = card.locator(".br-spec").first
    for mode in ["dark", "light"]:
        for t in THEMES:
            pg.evaluate("""([t,m]) => { document.documentElement.setAttribute('data-apollo-theme', t);
                document.body.setAttribute('data-theme', m);
                document.querySelectorAll('.br-card').forEach(c => { const h=c.querySelector('h4');
                  if (h && h.textContent.trim()==='Capsule — Dark grey') c.querySelector('.br-spec').removeAttribute('data-apollo-theme'); }); }""", [t, mode])
            pg.wait_for_timeout(150)
            spec.scroll_into_view_if_needed()
            wait_images(pg)
            m = spec.evaluate("""(el) => { const cap=el.querySelector('.bm-cap'); const pgd=el.querySelector('.bm-page-ground');
                const cs=getComputedStyle(cap); let g=pgd; let bg=getComputedStyle(g).backgroundColor;
                while ((bg==='rgba(0, 0, 0, 0)' || bg==='transparent') && g.parentElement){ g=g.parentElement; bg=getComputedStyle(g).backgroundColor; }
                const desc=cap.querySelector('.bm-desc'); 
                return {cap_bg: cs.backgroundColor, ink: getComputedStyle(desc).color, page_bg: bg, page_from: g.className||g.tagName,
                        desc_h: desc.getBoundingClientRect().height, desc_sh: desc.scrollHeight, desc_ch: desc.clientHeight}; }""")
            cap = parse_rgb(m["cap_bg"]); pgc = parse_rgb(m["page_bg"]); ink = parse_rgb(m["ink"])
            m.update(cap_hex=hexof(cap), page_hex=hexof(pgc), ink_hex=hexof(ink),
                     ground_vs_page=round(contrast(cap, pgc), 2), dL=round(Lstar(cap) - Lstar(pgc), 2),
                     ink_on_cap=round(contrast(ink, cap), 2))
            res[f"{t}-{mode}"] = m
            spec.screenshot(path=str(OUT / f"1-caption-{t}-{mode}.png"))
    b.close()
save_json("1-caption-measures.json", res)
for k, v in res.items(): print(k, v["cap_hex"], "on", v["page_hex"], "ratio", v["ground_vs_page"], "dL*", v["dL"], "ink", v["ink_on_cap"], v["page_from"])
