#!/usr/bin/env python3
"""Lane PR #316: s315-D40 — the footer stays dark in dark mode, one ladder step above the black page. String edits only."""
import json, os
R = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../..'))
CALL40 = ("\"if the footer is dark in light mode it should stay dark in dark mode, if the page is black it should be a "
          "different dark grey to differentiate them\"")
def edit(path, pairs, is_json=False):
    p = os.path.join(R, path); s = open(p, encoding='utf-8').read()
    for old, new in pairs:
        assert s.count(old) == 1, (path, s.count(old), old[:100]); s = s.replace(old, new)
    if is_json: json.loads(s)
    open(p, 'w', encoding='utf-8').write(s)
F = 'knowledge/snippets/Footer.reference.html'
edit(F, [
 ('''  TWO-RED LAW ON AN INVERSE SURFACE (s151-D1):''',
  '''  ★★★ #316 lane PR — s315-D40, DAVE, call 40 (review page export 2026-10-02 22:32 BST), verbatim:
      ''' + CALL40 + '''
      What it changed: the band is DARK IN BOTH MODES. It no longer takes surface/action-primary (the
      ground that INVERTS, which drew a #FAFAFA band under the dark page); it takes surface/dark-band,
      minted from the neutral ladder for this word — #1A1A1A in light (color/neutral/4, as before) and
      #313131 in dark (color/neutral/5, ONE STEP ABOVE the #1A1A1A page, so the two never merge). The
      ink is text/reverse, flat white in both modes (17.4:1 light, 13.0:1 dark). The pips keep
      border/strong (#808080): 4.41:1 light, 3.29:1 dark. Note (b) below is the #261 record, kept as
      history; its "light band in dark" consequence is what call 40 refused. The token NAME
      surface/dark-band is proposed (token names are Dave's, s145-D1).

  TWO-RED LAW ON AN INVERSE SURFACE (s151-D1) — since #316 the plate is DARK IN BOTH MODES, so a red
  here would be #F6604C in both. The #261 text follows, kept as history:'''),
 ('''    --ft-band:#1A1A1A;        /* surface/action-primary — dark plate under a light page */
    --ft-ink:#FFFFFF;         /* text/on-inverse — 17.4:1 on the plate */''',
  '''    /* s315-D40 (#316 lane PR), Dave, call 40: the band stays DARK in dark mode, a different dark grey
       from the black page. surface/dark-band (minted from the ladder) + text/reverse (flat white). */
    --ft-band:#1A1A1A;        /* surface/dark-band — dark plate under a light page (color/neutral/4) */
    --ft-ink:#FFFFFF;         /* text/reverse — 17.4:1 on the plate */'''),
 ('''    --ft-band:#FAFAFA;        /* surface/action-primary — the plate INVERTS: light band on a dark page */
    --ft-ink:#333333;         /* text/on-inverse — 12.0:1 on the plate */''',
  '''    --ft-band:#313131;        /* surface/dark-band — STAYS DARK, one ladder step above the #1A1A1A page (color/neutral/5) */
    --ft-ink:#FFFFFF;         /* text/reverse — 13.0:1 on the plate */'''),
 ('"--ft-band": "surface/action-primary", "--ft-ink": "text/on-inverse",',
  '"--ft-band": "surface/dark-band", "--ft-ink": "text/reverse",'),
 ('{ "fg": "text/on-inverse", "bg": "surface/action-primary", "context": "text" },',
  '{ "fg": "text/reverse", "bg": "surface/dark-band", "context": "text" },'),
 ('{ "fg": "border/strong", "bg": "surface/action-primary", "context": "ui" },',
  '{ "fg": "border/strong", "bg": "surface/dark-band", "context": "ui" },'),
])
M = 'knowledge/components/footer.meta.json'
p = os.path.join(R, M); s = open(p, encoding='utf-8').read(); t = json.loads(s)['tokens']
old_band = '"ft-band": ' + json.dumps(t['ft-band'], ensure_ascii=False)
old_ink = '"ft-ink": ' + json.dumps(t['ft-ink'], ensure_ascii=False)
new_band = '"ft-band": ' + json.dumps("surface/dark-band — THE DARK PLATE, DARK IN BOTH MODES (s315-D40, #316 lane PR). #1A1A1A light (color/neutral/4) / #313131 dark (color/neutral/5, one ladder step above the #1A1A1A dark page). Dave, call 40, verbatim: " + CALL40 + ". Until #316 this was surface/action-primary (#1A1A1A / #FAFAFA), the ground that inverts, which drew a light band under the dark page. The name surface/dark-band is PROPOSED (token names are Dave's, s145-D1).", ensure_ascii=False)
new_ink = '"ft-ink": ' + json.dumps("text/reverse — the plate's ink, flat white in both modes: 17.4:1 on #1A1A1A, 13.0:1 on #313131 (s315-D40). Until #316 it was text/on-inverse (#FFFFFF / #333333), the label of the inverting ground.", ensure_ascii=False)
edit(M, [(old_band, new_band), (old_ink, new_ink),
 ('"$reversedOutBand": "#261 Ft3.', '"$reversedOutBand": "⛔ SUPERSEDED IN ITS DARK HALF BY s315-D40 (#316): the band stays DARK in dark mode on surface/dark-band; see ft-band. The #261 record follows, kept as history. #261 Ft3.'),
 ('"$dotRing": "#261 Ft3:', '"$dotRing": "(#316: the dark-mode plate is now #313131, a DARK ground, so the ring is no longer what keeps the green dot visible there; it stays, harmless, on both plates.) #261 Ft3:'),
 ('"$twoRedLawOnAnInverseSurface": "s151-D1 on this component:', '"$twoRedLawOnAnInverseSurface": "(#316, s315-D40: the plate is DARK in both modes now, so a red here would be #F6604C in both; the inversion below is #261 history.) s151-D1 on this component:'),
], is_json=True)
print('ok')
