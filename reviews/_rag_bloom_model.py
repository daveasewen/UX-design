#!/usr/bin/env python3
"""Apollo — first-cut BLOOM / DANCE model (v0 heuristic, calibrate to Dave's eye).

Extends the flat WCAG ratio with the two dimensions it ignores:
  · edge-extremity  — luminance step (bloom lever) + saturation (dance lever)
  · spatial frequency — stroke width -> degrees of visual angle (selects the mode)

Two failure modes, from canon (color/black $note two-lever + Dave's observation):
  BLOOM  = irradiation. Bright feature spills across its edge; light-on-dark looks HEAVIER.
           Grows with bright-side luminance x step, and is VISIBLE on thick fields.
  DANCE  = chromatic edge instability ("jazz"). Saturated colour at a high-spatial-frequency
           (thin) edge, worst when luminance contrast is low. The chromatic channel is
           low-pass (~4 c/deg); above that the edge won't resolve and shimmers.

Levers: bloom -> lower luminance step (the digital-black move). dance -> saturation ceiling.
Seed for Apollo Labs. NOT validated — numbers are relative, to be tuned against the most
sensitive observer (astigmatism = stricter test = better calibration)."""
import math

def hex2rgb(h):
    h=h.lstrip('#'); return tuple(int(h[i:i+2],16)/255 for i in (0,2,4))
def rgb2hex(rgb): return '#'+''.join(f'{max(0,min(255,round(c*255))):02X}' for c in rgb)
def _lin(c): return c/12.92 if c<=0.04045 else ((c+0.055)/1.055)**2.4
def _slin(c): return 12.92*c if c<=0.0031308 else 1.055*(c**(1/2.4))-0.055
def rellum(h):
    r,g,b=[_lin(x) for x in hex2rgb(h)]; return 0.2126*r+0.7152*g+0.0722*b
def wcag(a,b):
    x,y=rellum(a),rellum(b); hi,lo=max(x,y),min(x,y); return (hi+0.05)/(lo+0.05)
def oklab(h):
    r,g,b=[_lin(x) for x in hex2rgb(h)]
    l=0.4122214708*r+0.5363325363*g+0.0514459929*b
    m=0.2119034982*r+0.6806995451*g+0.1073969566*b
    s=0.0883024619*r+0.2817188376*g+0.6299787005*b
    l_,m_,s_=l**(1/3),m**(1/3),s**(1/3)
    return (0.2104542553*l_+0.7936177850*m_-0.0040720468*s_,
            1.9779984951*l_-2.4285922050*m_+0.4505937099*s_,
            0.0259040371*l_+0.7827717662*m_-0.8086757660*s_)
def oklab2hex(L,a,b):
    l_=L+0.3963377774*a+0.2158037573*b; m_=L-0.1055613458*a-0.0638541728*b; s_=L-0.0894841775*a-1.2914855480*b
    l,m,s=l_**3,m_**3,s_**3
    r=4.0767416621*l-3.3077115913*m+0.2309699292*s; g=-1.2684380046*l+2.6097574011*m-0.3413193965*s; bl=-0.0041960863*l-0.7034186147*m+1.7076147010*s
    return rgb2hex(tuple(_slin(x) for x in (r,g,bl)))

# --- model ---
F_CUT=4.0            # chromatic channel cutoff (c/deg)
K_CPD=16.5           # 1px stroke ~ 16.5 c/deg @ ~96dpi / 50cm
W_HALF=6.0           # px at which bloom-visibility is half

def cpd(w): return K_CPD/max(w,0.3)
def chroma_dist(f,b):
    _,af,bf=oklab(f); _,ab,bb=oklab(b); return math.hypot(af-ab,bf-bb)

def bloom(fg,bg,w):
    Yf,Yb=rellum(fg),rellum(bg); Ybr=max(Yf,Yb); S=abs(Yf-Yb)
    area=w/(w+W_HALF)                      # thick -> visible halo
    return Ybr*S*area
def dance(fg,bg,w):
    Lc=abs(rellum(fg)-rellum(bg))/(rellum(fg)+rellum(bg)+1e-6)  # Michelson
    Cc=chroma_dist(fg,bg)
    f=cpd(w); unresolved=(f/F_CUT)**2/(1+(f/F_CUT)**2)          # thin -> high
    return Cc*unresolved/(1+6*Lc)

# normalisation refs (=100)
BLOOM_REF=bloom('#FFFFFF','#1A1A1A',40)      # a white fill blooming on dark
DANCE_REF=dance('#2674DC','#1A1A1A',1)       # saturated blue 1px text on dark
def B(fg,bg,w): return round(100*bloom(fg,bg,w)/BLOOM_REF,1)
def D(fg,bg,w): return round(100*dance(fg,bg,w)/DANCE_REF,1)

DPG='#1A1A1A'
print('='*80); print('MODEL SANITY — known cases (Bloom / Dance, 0..100 rel)'); print('='*80)
for lab,fg,bg,w in [
    ('white text 2px on #1A1A1A (the halation classic)','#FFFFFF',DPG,2),
    ('white FILL 40px on #1A1A1A','#FFFFFF',DPG,40),
    ('sat blue 1px text on #1A1A1A (the "dance")','#2674DC',DPG,1),
    ('sat blue 40px fill on #1A1A1A','#2674DC',DPG,40),
    ('mid red 2px text on #1A1A1A','#CC4333',DPG,2)]:
    print(f'  {lab:52} bloom {B(fg,bg,w):5}  dance {D(fg,bg,w):5}')

print(); print('='*80)
print('§ SAT-CAPPED BAND B — cap OKLab chroma, hold L (0.64) + hue. Black text on fill.')
print('='*80)
bandB={'red':('#E35847',30.0),'green':('#3CA368',154.9),'blue':('#3E8AF4',257.4)}
CAP=0.72   # fraction of Band-B chroma retained (dance lever)
capped={}
for nm,(hx,H) in bandB.items():
    L,a,b=oklab(hx); C=math.hypot(a,b)
    Cc2=C*CAP; hxc=oklab2hex(L,Cc2*math.cos(math.atan2(b,a)),Cc2*math.sin(math.atan2(b,a)))
    capped[nm]=hxc
    print(f'  {nm:5} uncapped {hx}  C{C:.3f} | capped {hxc}  C{Cc2:.3f}')
    print(f'        black-on-fill  {wcag(hx,"#000000"):.2f} -> {wcag(hxc,"#000000"):.2f}   (luminance-driven, barely moves)')
    print(f'        mark/#1A1A1A   {wcag(hx,DPG):.2f} -> {wcag(hxc,DPG):.2f}')
    print(f'        DANCE 1px text {D(hx,DPG,1):5} -> {D(hxc,DPG,1):5}   BLOOM fill {B(hx,DPG,40):5} -> {B(hxc,DPG,40):5}')

print(); print('='*80)
print('§ STEP-DOWN-ON-COLOUR hypothesis — bloom of text vs its ground')
print('  (light-bleed compensation lightens weight only where bloom is high)')
print('='*80)
for lab,fg,bg in [
    ('white text on the dark PAGE #1A1A1A','#FFFFFF','#1A1A1A'),
    ('white text on RED fill #C33A2B (Band A)','#FFFFFF','#C33A2B'),
    ('white text on BLUE fill #1F6ED5 (Band A)','#FFFFFF','#1F6ED5'),
    ('black text on GREEN fill #3CA368 (Band B)','#000000','#3CA368'),
    ('black text on AMBER fill #F0B13A','#000000','#F0B13A')]:
    print(f'  {lab:44} bloom@2px {B(fg,bg,2):5}   (step {abs(rellum(fg)-rellum(bg)):.2f})')
print('  -> if bloom on colour << bloom on page, the dark-mode weight step-DOWN is unneeded on colour.')
