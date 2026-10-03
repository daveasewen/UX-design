#!/usr/bin/env python3
"""Lane PR #316: s315-D7 (+ s315-D33) — the pending roundel: amber both modes, clock hands only, no ring; template drops the chip."""
import re, json, os
R = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../..'))
def sub1(path, old, new, count=1):
    p = os.path.join(R, path); s = open(p, encoding='utf-8').read()
    n = s.count(old)
    assert n == count, f"{path}: expected {count} match(es), found {n} for {old[:80]!r}"
    s = s.replace(old, new); open(p, 'w', encoding='utf-8').write(s)
HANDS = 'M9.6 3H8.4V9.6H13V8.4H9.6V3Z'   # media/time.svg, its third subpath only: the hands, byte-lifted
RING_PATH_RE = re.compile(r'<path style="fill:var\(--mark\)" fill-rule="evenodd" clip-rule="evenodd" d="M9 0C4\.03 0 0 4\.029[^"]*"/>')
NEWPATH = f'<path style="fill:var(--mark)" d="{HANDS}"/>'
for f in ('knowledge/snippets/Confirmation.reference.html', 'knowledge/snippets/Template-confirmation.reference.html'):
    p = os.path.join(R, f); s = open(p, encoding='utf-8').read()
    s2, n = RING_PATH_RE.subn(NEWPATH, s)
    assert n == 1, (f, n)
    assert 'H9.6V3Z' in s.split('class="pending is-warning"')[1][:900]
    open(p, 'w', encoding='utf-8').write(s2)

C = 'knowledge/snippets/Confirmation.reference.html'
sub1(C, '--success:#FFFFFF; --pending:#FFFFFF; --text:#E1E1E1;', '--success:#FFFFFF; --pending:#E0A61F; --text:#E1E1E1;')
sub1(C, '''  /* THE PENDING KIND (#314 TP2; Dave 14:55 2026-10-02 call 15, verbatim: "We should have an amber pending roundel"):
     the same 56px roundel, filled rag/warning, with the library's time glyph (media/time.svg) drawn as the MARK on top
     (--mark via the AUTO-TOKENS marks set: s122-D2 mono mark on #E0A61F, 7.99:1). Dark: the roundel goes WHITE with a
     black mark, the same policy as .success. The outcome is carried by the HEADING, the glyph is aria-hidden. */''',
'''  /* THE PENDING KIND (#314 TP2; Dave 14:55 2026-10-02 call 15, verbatim: "We should have an amber pending roundel"),
     REDRAWN #316 lane PR on s315-D7 (Dave 22:32 2026-10-02 call 7, verbatim: "the amber should be amber in both and it
     should be the same icon as we have for the amber notifications. I actually like the clock icon but it shouldn't have
     the circle. not for later, lets create a new roundel for pending with the clock hand only on the amber roundel.").
     Built the way the amber notification glyph is built (status-icons/warning.svg: an r=9 disc, the mark on top): the
     disc is rag/warning in BOTH modes (it no longer goes white in dark), and the mark is the CLOCK HANDS ONLY - the third
     subpath of media/time.svg, byte-lifted, with the ring dropped. --mark via the AUTO-TOKENS marks set (s122-D2 mono
     mark on #E0A61F, 7.99:1, both modes). The outcome is carried by the HEADING, the glyph is aria-hidden. */''')
sub1(C, '"time": "media/time.svg (the pending mark)"', '"time": "media/time.svg (the pending mark: its HANDS subpath only, the ring dropped - s315-D7)"')
sub1(C, '"driftAllow": { "--success": ["dark"], "--pending": ["dark"], "$reason": "RAG ROUNDEL POLICY', '"driftAllow": { "--success": ["dark"], "$pendingLeftThePolicy": "s315-D7 (#316 lane PR): --pending is rag/warning in BOTH modes now, so it is no longer a drift; Dave, call 7, verbatim: \'the amber should be amber in both\'.", "$reason": "RAG ROUNDEL POLICY')

T = 'knowledge/snippets/Template-confirmation.reference.html'
sub1(T, '<span class="cn-status-indicator"><span class="chip warn" role="status"><span class="dot" aria-hidden="true"></span>Awaiting a second approver</span></span>\n', '')
sub1(T, '    Status-indicator        .cn-status-indicator        the pending chip (variant B)\n', '')
sub1(T, '''  - Variant B's pending anchor is Confirmation's column without the success roundel: the state is
    carried by the Status-indicator chip and the words, not by a glyph the page lifted from
    Empty-state. (Confirmation draws one roundel, the success one; a pending roundel would be a''',
'''  - #316 lane PR (s315-D7 + s315-D33): variant B carries Confirmation's PENDING roundel - amber in
    both modes, the clock hands only, no ring - and the Status-indicator chip is DROPPED (Dave, call
    33, verbatim: "i've metioned this correction on a previous comment", pointing at call 7). The
    lines below are the #314 record, kept as history:
  - (#314) Variant B's pending anchor is Confirmation's column without the success roundel: the state is
    carried by the Status-indicator chip and the words, not by a glyph the page lifted from
    Empty-state. (Confirmation draws one roundel, the success one; a pending roundel would be a''')
sub1(T, '"success, pending (time)": "via Confirmation (its own roundel paths)"', '"success, pending (clock hands only, s315-D7)": "via Confirmation (its own roundel paths)"')
sub1(T, '    "Confirmation",\n    "Status-indicator",\n', '    "Confirmation",\n')

M = 'knowledge/components/confirmation.meta.json'
p = os.path.join(R, M); raw = open(p, encoding='utf-8').read(); m = json.loads(raw)
old_use = [v for v in m['variants'] if v.get('name') == 'pending'][0]['use']
new_use = ("Accepted, waiting on someone else: the amber roundel (rag/warning in BOTH modes) with the CLOCK HANDS ONLY as the mark "
           "(media/time.svg's hands subpath, the ring dropped), built like the amber notification glyph (status-icons/warning.svg: disc + mono mark). "
           "s315-D7, Dave 22:32 2026-10-02 call 7, verbatim: \"the amber should be amber in both and it should be the same icon as we have for the amber "
           "notifications. I actually like the clock icon but it shouldn't have the circle. not for later, lets create a new roundel for pending with the "
           "clock hand only on the amber roundel.\" Read with s315-D33 (call 33 points back at call 7): the roundel stays and the chip goes. "
           "History: #314 TP2 built it from call 15 (\"We should have an amber pending roundel\") with the full time glyph and a white dark-mode disc; #316 lane PR redrew it.")
sub1(M, json.dumps(old_use, ensure_ascii=False), json.dumps(new_use, ensure_ascii=False))
json.load(open(p, encoding='utf-8'))
print('ok')
