#!/usr/bin/env python3
"""RAG-colours review — candidate computation (OKLCh, matching R-D2/R-D3 method).
Computes dark-mode green re-cut + dark red/blue glyph-lift candidates, with measured
WCAG contrast against every ground that matters. Numbers feed gen_rag_colours.py.
Standalone: pure-python sRGB<->OKLab, no deps."""
import math

# ---------- colour maths ----------
def hex2rgb(h):
    h=h.lstrip('#'); return tuple(int(h[i:i+2],16)/255 for i in (0,2,4))
def rgb2hex(rgb):
    return '#'+''.join(f'{max(0,min(255,round(c*255))):02X}' for c in rgb)
def _lin(c): return c/12.92 if c<=0.04045 else ((c+0.055)/1.055)**2.4
def _slin(c): return 12.92*c if c<=0.0031308 else 1.055*(c**(1/2.4))-0.055
def rel_lum(h):
    r,g,b=[_lin(x) for x in hex2rgb(h)]
    return 0.2126*r+0.7152*g+0.0722*b
def contrast(a,b):
    la,lb=rel_lum(a),rel_lum(b)
    hi,lo=max(la,lb),min(la,lb)
    return (hi+0.05)/(lo+0.05)
# sRGB -> OKLab -> OKLCh
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
    l_=L+0.3963377774*a+0.2158037573*b
    m_=L-0.1055613458*a-0.0638541728*b
    s_=L-0.0894841775*a-1.2914855480*b
    l,m,s=l_**3,m_**3,s_**3
    r= 4.0767416621*l-3.3077115913*m+0.2309699292*s
    g=-1.2684380046*l+2.6097574011*m-0.3413193965*s
    bl=-0.0041960863*l-0.7034186147*m+1.7076147010*s
    return tuple(_slin(x) for x in (r,g,bl))
def srgb2oklch(h):
    L,a,b=srgb2oklab(h)
    C=math.hypot(a,b); H=math.degrees(math.atan2(b,a))%360
    return L,C,H
def oklch2hex(L,C,H):
    a=C*math.cos(math.radians(H)); b=C*math.sin(math.radians(H))
    return rgb2hex(oklab2srgb(L,a,b))

# ---------- grounds ----------
WHITE='#FFFFFF'; BLACK='#000000'
DARK_PAGE='#1A1A1A'   # the digital black (R-D1 §5)
DARK_PAGE2='#111111'  # the #111 the ledger quotes for glyph-on-text tests

def report(label,hexv,grounds):
    L,C,H=srgb2oklch(hexv)
    parts=' · '.join(f'{g[1]} {contrast(hexv,g[0]):.2f}' for g in grounds)
    print(f'  {label:26} {hexv}  L{L:.3f} C{C:.3f} H{H:.1f}   {parts}')

print('='*78)
print('CURRENT CANON (from token store)')
print('='*78)
print('LIGHT — single value each hue, white text on fill = green-vs-white on white page')
for lab,hx in [('red  #B92F1E','#B92F1E'),('amber-bg #F0B13A','#F0B13A'),
               ('amber-glyph #C58900','#C58900'),('green #2B7E4F','#2B7E4F'),
               ('blue #306EC6','#306EC6')]:
    report(lab,hx,[(WHITE,'wht'),(BLACK,'blk')])
print()
print('DARK — the three OPEN items, measured on the dark page/#111')
for lab,hx in [('red  #CC4333','#CC4333'),('blue #2674DC','#2674DC'),
               ('green(incumbent) #1AA05C','#1AA05C')]:
    report(lab,hx,[(WHITE,'wht'),(BLACK,'blk'),(DARK_PAGE,'pg1A'),(DARK_PAGE2,'pg11')])

print()
print('='*78)
print('§2 DARK-MODE GREEN — candidate ladder (hue held ~154.9°, R-D4 green hue)')
print('='*78)
Lg,Cg,Hg=srgb2oklch('#2B7E4F')
print(f'  ref light green #2B7E4F = L{Lg:.3f} C{Cg:.3f} H{Hg:.1f}')
print('  GOAL: works as glyph on dark page (>=4.5 text / >=3 icon) AND readable text on fill.')
print('  Path A — LIGHT green + BLACK text on fill (mirrors amber "always black text"):')
for L in (0.72,0.76,0.80,0.84):
    hx=oklch2hex(L,Cg,Hg)
    report(f'  A L={L:.2f}',hx,[(BLACK,'blk-txt'),(DARK_PAGE,'pg1A'),(WHITE,'wht')])
print('  Path B — DARK green + WHITE text on fill (mirrors light mode). Note glyph-on-dark suffers:')
for L in (0.50,0.54,0.58):
    hx=oklch2hex(L,Cg,Hg)
    report(f'  B L={L:.2f}',hx,[(WHITE,'wht-txt'),(DARK_PAGE,'pg1A'),(BLACK,'blk')])

print()
print('='*78)
print('§3 DARK RED & BLUE as GLYPH-ON-TEXT (marks/text on dark page)')
print('='*78)
print('  Current: red #CC4333 pg1A / blue #2674DC pg1A — pass 3:1 icon, FAIL 4.5 text.')
print('  Lift candidates (hold hue, raise L until >=4.5 on #1A1A1A):')
for base,name in [('#CC4333','red'),('#2674DC','blue')]:
    L0,C0,H0=srgb2oklch(base)
    print(f'  --- {name} base L{L0:.3f} C{C0:.3f} H{H0:.1f} ---')
    for L in (L0+0.06,L0+0.10,L0+0.14):
        hx=oklch2hex(L,C0,H0)
        report(f'  L={L:.2f}',hx,[(DARK_PAGE,'pg1A'),(DARK_PAGE2,'pg11'),(WHITE,'wht')])
