#!/usr/bin/env python3
"""Build film B (313-sq) cuts A and B from button-film.src.html, embedding the house Univers (Light, Regular)."""
import base64, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, '..', '..', '..', '..'))
TTF = os.path.join(REPO, 'knowledge', 'assets', 'fonts', '_desktop', 'TTF')

src = open(os.path.join(HERE, 'button-film.src.html'), encoding='utf-8').read()
lt = base64.b64encode(open(os.path.join(TTF, 'HSBC_MtUnivers_Latin-Lt.ttf'), 'rb').read()).decode()
rg = base64.b64encode(open(os.path.join(TTF, 'HSBC_MtUnivers_Latin-Rg.ttf'), 'rb').read()).decode()

for cut in ('a', 'b'):
    out = (src.replace('__FONT_LT__', lt).replace('__FONT_RG__', rg)
              .replace('__CUTNAME__', cut.upper()).replace('__CUT__', cut))
    p = os.path.join(HERE, f'button-film-{cut}.html')
    open(p, 'w', encoding='utf-8').write(out)
    print(p, len(out.encode()), 'bytes')
