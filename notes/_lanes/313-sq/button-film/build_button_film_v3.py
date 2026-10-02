#!/usr/bin/env python3
"""Build film B v3 (Dave's script edit, 313-sq): embeds Univers and the Supercharge colour palette
(the 2026 supporting palette, color/supporting/* in knowledge/tokens/colour.json) into button-film-a-v3.html."""
import base64, json, os

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, '..', '..', '..', '..'))
TTF = os.path.join(REPO, 'knowledge', 'assets', 'fonts', '_desktop', 'TTF')
colour = json.load(open(os.path.join(REPO, 'knowledge', 'tokens', 'colour.json')))
sup = colour['color']['supporting']
ORDER = ['burnt-orange', 'apricot-orange', 'sun-yellow', 'olive-green', 'mint-green',
         'forest-green', 'sky-blue', 'midnight-blue', 'dusk-purple', 'rose-pink']   # round the wheel, by hue
assert sorted(ORDER) == sorted(k for k in sup if not k.startswith('$')), sorted(sup)
pal = [[f, [sup[f][str(s)]['$value'] for s in range(1, 6)]] for f in ORDER]
src = open(os.path.join(HERE, 'button-film-v3.src.html'), encoding='utf-8').read()
b64 = lambda n: base64.b64encode(open(os.path.join(TTF, n), 'rb').read()).decode()
out = (src.replace('__FONT_LT__', b64('HSBC_MtUnivers_Latin-Lt.ttf')).replace('__FONT_RG__', b64('HSBC_MtUnivers_Latin-Rg.ttf'))
          .replace('__SUPPORT__', json.dumps(pal)))
p = os.path.join(HERE, 'button-film-a-v3.html'); open(p, 'w', encoding='utf-8').write(out)
print(os.path.basename(p), len(out.encode()), 'bytes · palette', len(pal), 'families x 5')
