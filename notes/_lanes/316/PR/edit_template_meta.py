#!/usr/bin/env python3
"""Lane PR #316: template-confirmation.meta.json follows s315-D7 + s315-D33 (pending roundel kept, chip dropped). String edits only."""
import json, os
R = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../..'))
P = os.path.join(R, 'knowledge/components/template-confirmation.meta.json')
s = open(P, encoding='utf-8').read()
def rep(old, new):
    global s
    assert s.count(old) == 1, (s.count(old), old[:90]); s = s.replace(old, new)
rep('"$note": "SUCCESS keeps Confirmation\'s rag/success roundel and its entrance animation. PENDING takes NO success device - see antiPatterns."',
    '"$note": "SUCCESS keeps Confirmation\'s rag/success roundel and its entrance animation. PENDING takes Confirmation\'s PENDING roundel (amber in both modes, the clock hands only, no ring; s315-D7) and NO entrance pop - see antiPatterns."')
rep('"use": "Accepted but NOT finished. No roundel, no green, no entrance pop: a decorative glyph at alpha/40 and a Status-indicator chip carrying the meaning in a word, plus the expiry stated plainly."',
    '"use": "Accepted but NOT finished. Confirmation\'s pending roundel (rag/warning in BOTH modes, the clock hands only, no ring), no green, no entrance pop; the HEADING carries the state in words and the message states the consequence plainly. The Status-indicator chip is DROPPED (#316 lane PR, s315-D7 read with s315-D33: Dave, call 7, verbatim: \\"lets create a new roundel for pending with the clock hand only on the amber roundel\\"; call 33, verbatim: \\"i\'ve metioned this correction on a previous comment\\")."')
rep('"component:confirmation", "component:status-indicator", "component:section-heading-lockup"', '"component:confirmation", "component:section-heading-lockup"')
rep('"announcements": "The pending chip is role=\\"status\\". The success page announces nothing beyond its heading - the person arrived here, so the state is the destination."',
    '"announcements": "Neither page announces beyond its heading - the person arrived here, so the state is the destination. (Until #316 the pending page carried a role=\\"status\\" chip; it was dropped with the chip, s315-D7/D33.)"')
rep('The pending chip carries its word and its dot is aria-hidden. The pending state also states its consequence in prose (\'Nothing has left the account yet\') rather than relying on the chip alone.',
    'The pending roundel is aria-hidden too and the HEADING carries the pending state (\'Payment waiting for approval\'); the message states its consequence in prose (\'Nothing has left the account yet\').')
rep('"Giving the PENDING variant a success device. Confirmation\'s roundel is built for a TICK: the mark is a page-cutout and the whole dark policy exists so that cutout stays legible. There is no ruled roundel for \'accepted but not finished\', and minting one would be a decision inside the RAG policy\'s own neighbourhood."',
    '"Giving the PENDING variant a SUCCESS device - the green roundel, the tick or the entrance pop. Pending has its own roundel since #316 (s315-D7: amber in both modes, the clock hands only); the success roundel stays for success alone."')
json.loads(s)
open(P, 'w', encoding='utf-8').write(s); print('ok')
