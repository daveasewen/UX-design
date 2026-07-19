#!/usr/bin/env python3
"""RAG LIGHT-mode fill derivation (R-D11).

The dark set (R-D10) was tuned entirely on the dark page (#1A1A1A). Dave's white-page
screenshot exposed R-D11: salience is contrast-WITH-GROUND, so the ramp INVERTS light<->dark.
On white the light fills (amber/green/blue) wash out (fill-vs-white < 3) and the deep-red
breach becomes the QUIETEST cell. => status FILLS are PER-MODE, not mode-stable.

This reconstructs the salience metric used inline for v7-v10 (never saved to a script):
    salience = mean OKLab distance of (fill, text) from the PAGE.
and derives a ground-aware LIGHT-mode fill set on the WHITE page.

Standalone, pure-python. Same OKLab/contrast maths as _rag_colours_calc.py + the bloom model."""
import math

# ---------- colour maths (identical to _rag_colours_calc.py) ----------
def hex2rgb(h):
    h=h.lstrip('#'); return tuple(int(h[i:i+2],16)/255 for i in (0,2,4))
def rgb2hex(rgb):
    return '#'+''.join(f'{max(0,min(255,round(c*255))):02X}' for c in rgb)
def _lin(c): return c/12.92 if c<=0.04045 else ((c+0.055)/1.055)**2.4
def _slin(c): return 12.92*c if c<=0.0031308 else 1.055*(c**(1/2.4))-0.055
def rel_lum(h):
    r,g,b=[_lin(x) for x in hex2rgb(h)]; return 0.2126*r+0.7152*g+0.0722*b
def contrast(a,b):
    la,lb=rel_lum(a),rel_lum(b); hi,lo=max(la,lb),min(la,lb); return (hi+0.05)/(lo+0.05)
def srgb2oklab(h):
    r,g,b=[_lin(x) for x in hex2rgb(h)]
    l=0.4122214708*r+0.5363325363*g+0.0514459929*b
    m=0.2119034982*r+0.6806995451*g+0.1073969566*b
    s=0.0883024619*r+0.2817188376*g+0.6299787005*b
    l_,m_,s_=l**(1/3),m**(1/3),s**(1/3)
    return (0.2104542553*l_+0.7936177850*m_-0.0040720468*s_,
            1.9779984951*l_-2.4285922050*m_+0.4505937099*s_,
            0.0259040371*l_+0.7827717662*m_-0.8086757660*s_)
def oklab2srgb(L,a,b):
    l_=L+0.3963377774*a+0.2158037573*b; m_=L-0.1055613458*a-0.0638541728*b; s_=L-0.0894841775*a-1.2914855480*b
    l,m,s=l_**3,m_**3,s_**3
    r= 4.0767416621*l-3.3077115913*m+0.2309699292*s
    g=-1.2684380046*l+2.6097574011*m-0.3413193965*s
    bl=-0.0041960863*l-0.7034186147*m+1.7076147010*s
    return tuple(_slin(x) for x in (r,g,bl))
def srgb2oklch(h):
    L,a,b=srgb2oklab(h); C=math.hypot(a,b); H=math.degrees(math.atan2(b,a))%360; return L,C,H
def oklch2hex(L,C,H):
    a=C*math.cos(math.radians(H)); b=C*math.sin(math.radians(H)); return rgb2hex(oklab2srgb(L,a,b))
def okdist(a,b):
    la,aa,ba=srgb2oklab(a); lb,ab,bb=srgb2oklab(b); return math.hypot(la-lb,aa-ab,ba-bb)

# ---------- the salience metric (reconstructed, R-D9) ----------
def salience(fill,text,page):
    """mean OKLab distance of (fill, text) from the page. x100 to match the ledger scale."""
    return 100*(okdist(fill,page)+okdist(text,page))/2

WHITE='#FFFFFF'; DARK='#1A1A1A'

def line(sev,fill,text,page):
    L,C,H=srgb2oklch(fill)
    fvp=contrast(fill,page); tvf=contrast(text,fill)
    sal=salience(fill,text,page)
    tag='' if fvp>=3 else '  <-- WASHES OUT (<3 vs page)'
    aa='' if tvf>=4.5 else '  <-- TEXT < AA'
    print(f'  {sev:8} {fill} {("wht" if text==WHITE else "blk")}  '
          f'L{L:.3f} C{C:.3f} H{H:.0f}   fill/pg {fvp:4.2f}  txt/fill {tvf:5.2f}  '
          f'sal {sal:5.1f}{tag}{aa}')

def ramp_ok(rows,page):
    sals=[salience(f,t,page) for _,f,t in rows]
    order=all(sals[i]>sals[i+1] for i in range(len(sals)-1))
    return order,sals

# ============================================================================
print('='*94)
print('CONTROL — R-D10 DARK set, measured on the DARK page (the locked, correct ramp)')
print('='*94)
DARKSET=[('breach','#B92F1E',WHITE),('watch','#F0B13A','#000000'),
         ('healthy','#43AD6F','#000000'),('info','#5F92B9','#000000')]
for s,f,t in DARKSET: line(s,f,t,DARK)
ok,sals=ramp_ok(DARKSET,DARK); print(f'  ramp monotonic on dark: {ok}   salience {[round(x,1) for x in sals]}')

print()
print('='*94)
print('THE PROBLEM — the SAME R-D10 set measured on the WHITE page (R-D11: inverts)')
print('='*94)
for s,f,t in DARKSET: line(s,f,t,WHITE)
ok,sals=ramp_ok(DARKSET,WHITE); print(f'  ramp monotonic on white: {ok}   salience {[round(x,1) for x in sals]}  <-- BACKWARDS')

# ---------- white-appropriate loudness (the salience metric mis-ranks on white) ----------
def loud_white(fill,border=None):
    """On white the eye reads the darkest EDGE (fill or its border) vs the page, weighted by
    chroma. This is the white-ground analogue of dark-page salience; use it to order severity."""
    _,C,_=srgb2oklch(fill)
    edge=max(contrast(fill,WHITE), contrast(border,WHITE) if border else 0)
    return edge*(1+C)   # boundary strength lifted by how saturated the hue is

# ============================================================================
# Strategy 0 — RESTORE the R-D4 light values (built + ruled for the WHITE page before the
#   dark-ramp work re-seated green/blue lighter). Dark-ramp values (#43AD6F/#5F92B9, black text)
#   are DARK-ONLY. Amber keeps R-D3 (#F0B13A) + its ruled glyph #C58900 as a border on white.
# ============================================================================
print()
print('='*94)
print('STRATEGY 0 (LEAD) — restore R-D4 light values (white text) + amber border; measured on WHITE')
print('  green/blue return to the values already ruled for white; dark-ramp values stay dark-only')
print('='*94)
S0=[('breach','#B92F1E',WHITE,None),('watch','#F0B13A','#000000','#C58900'),
    ('healthy','#2B7E4F',WHITE,None),('info','#306EC6',WHITE,None)]
for s,f,t,bd in S0:
    L,C,H=srgb2oklch(f)
    bstr=f'  border {bd} ({contrast(bd,WHITE):.2f}/pg)' if bd else ''
    print(f'  {s:8} {f} {("wht" if t==WHITE else "blk")}  L{L:.3f} C{C:.3f}  '
          f'fill/pg {contrast(f,WHITE):4.2f}  txt/fill {contrast(t,f):5.2f}  '
          f'loud {loud_white(f,bd):4.2f}{bstr}')
lo=[loud_white(f,bd) for _,f,_,bd in S0]
print(f'  severity by white-loudness: {[round(x,2) for x in lo]}   monotonic: {all(lo[i]>lo[i+1] for i in range(len(lo)-1))}')

# ============================================================================
# Strategy A — DARKEN green/blue to hold their boundary on white; red + amber unchanged.
#   red already deep (6.02 vs white). amber is the lightness carve-out (border, see below).
#   green/blue re-seated darker + white text so they hold >=3 vs white AND order under amber.
# ============================================================================
print()
print('='*94)
print('STRATEGY A — darken green/blue for white (white text); red/amber held')
print('  goal: fill/pg >= 3, txt AA, ramp breach>watch>healthy>info on WHITE')
print('='*94)
# hold the R-D10 hues, drop L until fill-vs-white ~>=3.3 with white text
gL,gC,gH=srgb2oklch('#43AD6F'); bL,bC,bH=srgb2oklch('#5F92B9')
A_green=oklch2hex(0.520,gC,gH)          # darker green, white text
A_blue =oklch2hex(0.500,bC*1.15,bH)     # darker blue, restore a little chroma
A=[('breach','#B92F1E',WHITE),('watch','#F0B13A','#000000'),
   ('healthy',A_green,WHITE),('info',A_blue,WHITE)]
for s,f,t in A: line(s,f,t,WHITE)
ok,sals=ramp_ok(A,WHITE); print(f'  ramp monotonic on white: {ok}   salience {[round(x,1) for x in sals]}')

# ============================================================================
# Strategy B — MATTING/BORDER: keep the ruled dark HUES as fills, give every light fill a
#   hairline border in its own darker "glyph" value so the cell reads on white. Amber stays
#   exactly R-D3 (#F0B13A/#C58900). This preserves identity + the amber ruling; the boundary
#   is a manifestation treatment, not a hue change. (matting concept already in R-D2/R-D4.)
# ============================================================================
print()
print('='*94)
print('STRATEGY B — keep R-D10 hues as fills + a darker BORDER per hue (boundary on white)')
print('  border value = each hue dropped to ~L0.50 (its "glyph"); amber border = #C58900 (ruled)')
print('='*94)
def border_for(fill,amber_glyph=None):
    if amber_glyph: return amber_glyph
    L,C,H=srgb2oklch(fill); return oklch2hex(min(L,0.50),C,H)
B=[('breach','#B92F1E',WHITE,None),('watch','#F0B13A','#000000','#C58900'),
   ('healthy','#43AD6F','#000000',None),('info','#5F92B9','#000000',None)]
for s,f,t,ag in B:
    bd=border_for(f,ag)
    L,C,H=srgb2oklch(f)
    print(f'  {s:8} fill {f} {("wht" if t==WHITE else "blk")}  border {bd}  '
          f'fill/pg {contrast(f,WHITE):4.2f}  border/pg {contrast(bd,WHITE):4.2f}  '
          f'txt/fill {contrast(t,f):5.2f}  sal {salience(f,t,WHITE):5.1f}')
print('  (border/pg is the boundary the eye reads; fill keeps the ruled hue + text)')

# ============================================================================
# Strategy C — ground-inverted RE-CUT: purpose-built white-page fills, ramp by depth+chroma.
#   all white text except amber; severity tracks darkness+saturation (the white-page analogue
#   of the dark-page brightness ramp).
# ============================================================================
print()
print('='*94)
print('STRATEGY C — per-mode re-cut for white; ramp carried by depth + chroma')
print('='*94)
C_set=[('breach',oklch2hex(0.505,0.170,29),WHITE),      # deep saturated red
       ('watch','#F0B13A','#000000'),                    # amber held (carve-out)
       ('healthy',oklch2hex(0.560,0.130,155),WHITE),     # green, mid-deep
       ('info',oklch2hex(0.530,0.115,250),WHITE)]        # blue, calm low-chroma cyan-lean
for s,f,t in C_set: line(s,f,t,WHITE)
ok,sals=ramp_ok(C_set,WHITE); print(f'  ramp monotonic on white: {ok}   salience {[round(x,1) for x in sals]}')

# ============================================================================
# V2 (R-D12) — no lines; BLACK text on green+blue; blue tweak ladder. Amber ruled fine
# (R-D6: label carries meaning). fill-vs-white here is a SALIENCE lever, not an AA floor;
# the floor is the LABEL contrast (black/white text on fill).
# ============================================================================
print()
print('='*94)
print('V2 (R-D12) — black-text states, no lines. floor = LABEL contrast; fill/white = salience')
print('='*94)
V2=[('breach','#B92F1E',WHITE),('watch','#F0B13A','#000000'),
    ('healthy','#429363','#000000'),('info','#5F94B1','#000000')]
for s,f,t in V2:
    print(f'  {s:8} {f} {("wht" if t==WHITE else "blk")}  '
          f'label/fill {contrast(t,f):5.2f} (floor, >=4.5)  fill/white {contrast(f,WHITE):4.2f} (salience)')
print('  R-D4 green/blue are too DARK for black text (below AA) -> re-seat lighter:')
for lab,hx in [('green #2B7E4F',"#2B7E4F"),('blue #306EC6',"#306EC6")]:
    print(f'    {lab}: black-on-fill {contrast(hx,"#000000"):.2f}  <-- < 4.5')
print('  blue tweak ladder (all black text, all label-contrast >= AA):')
for lab,hx in [('green-lean  #5F94B1',"#5F94B1"),('grn-lean+lt #649ABA',"#649ABA"),('purple-lean #7483BA',"#7483BA")]:
    print(f'    {lab}: label {contrast(hx,"#000000"):5.2f}  fill/white {contrast(hx,WHITE):4.2f}')

# ============================================================================
# FINAL LOCKED SET (R-D14) — light Option C + dark R-D10. green/blue per-mode.
# ============================================================================
print()
print('='*94)
print('FINAL LOCKED (R-D14) — verify light on white + dark on #1A1A1A')
print('='*94)
DARKP='#1A1A1A'
FINAL=[('breach','#B92F1E','#B92F1E',WHITE),('watch','#F0B13A','#F0B13A','#000000'),
       ('healthy','#5DAC7B','#43AD6F','#000000'),('info','#7DABCD','#5F92B9','#000000')]
for lbl,page,idx in [('LIGHT/white',WHITE,1),('DARK/#1A1A1A',DARKP,2)]:
    print(f'  {lbl}:')
    for sev,lf,df,txt in FINAL:
        fill=lf if idx==1 else df
        print(f'    {sev:8} {fill} {"wht" if txt==WHITE else "blk"}  label {contrast(txt,fill):5.2f}  fill/pg {contrast(fill,page):4.2f}')
print('  ramp (green>blue): light', round(contrast("#5DAC7B",WHITE),2),'>',round(contrast("#7DABCD",WHITE),2),
      '| dark', round(contrast("#43AD6F",DARKP),2),'>',round(contrast("#5F92B9",DARKP),2))

print()
print('='*94)
print('NOTE: salience halves white-text fills on white (text term -> 0 vs white page).')
print('That is a metric artifact of the WHITE ground, not the eye — so BOTH numbers matter:')
print('  salience (severity ordering)  AND  fill-vs-page (boundary / washout).')
print('Dave rules from the specimen; these are candidates, not a promotion.')
print('='*94)
