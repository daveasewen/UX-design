#!/usr/bin/env python3
"""291 / P3 - slide 10's three anatomy drawings get markedly bigger.

Provenance. Dave, looking at slide 10 (the P2 three-up) with a crop of the
three cells, said verbatim:

    lets make better use of the space here, the images could be bigger

Edits v12 IN PLACE. Idempotent only from a fresh copy of
notes/_lanes/291/P3/v12-before-p3.html; every cut asserts on its anchor.

What changes: ONE number, the .pic box height on slide 10, plus a print guard
so the printed deck keeps the height it had. Type, spacing, copy, columns and
the rule box are untouched; the room comes out of the slide's top/bottom slack
(159/160px before, ~112px after).
"""
import pathlib

P = pathlib.Path('/sessions/fervent-affectionate-carson/mnt/UX-design'
                 '/notes/_DEMO-SLIDES-apollo-2026-09-20-v12.html')
s = P.read_text(encoding='utf-8')
n0 = len(s.splitlines())


def sub(old, new, why):
    global s
    assert s.count(old) == 1, 'anchor %r x%d - %s' % (old[:70], s.count(old), why)
    s = s.replace(old, new, 1)
    print('ok  ', why)


# 1 ---- the image box grows; width:100% and object-fit:contain are kept, so
#        the drawings keep their aspect ratio and nothing is cropped. At
#        1440x900 the box goes 340x135 -> 340x229.5, and the widest-aspect
#        drawings (gearbox / books, 900x630 and 1200x840 = 1.4286) draw
#        328x229.5 - 88% of the 373px cell, up from 51.7%.
sub(".grid5 .pic{display:block;width:100%;height:clamp(96px,15vh,150px);object-fit:contain;\n"
    "  margin:0 0 var(--s3);mix-blend-mode:multiply}",
    "/* v12/P3: the drawings were ~52% of the cell's width in a 135px box, with the\n"
    "   cell empty around them. The box is now 25.5vh (229.5px at 900), so the\n"
    "   gearbox and the books draw ~88% of the cell width. Aspect ratio is still\n"
    "   object-fit:contain - no crop, no distortion - and the number, title and\n"
    "   copy below keep their type and their var(--s3) gap. */\n"
    ".grid5 .pic{display:block;width:100%;height:clamp(150px,25.5vh,240px);object-fit:contain;\n"
    "  margin:0 0 var(--s3);mix-blend-mode:multiply}",
    '.grid5 .pic box height 135 -> 229.5 at 1440x900')

# 2 ---- print keeps the height it had (the printed slide is a fixed 1280x720
#        box; growing the picture there is a separate, unasked question).
sub("  #bkHost{display:none!important}\n"
    "  #gbHost{display:none!important}\n",
    "  #bkHost{display:none!important}\n"
    "  #gbHost{display:none!important}\n"
    "  /* v12/P3: on screen the anatomy pictures grew; print keeps its old box. */\n"
    "  .grid5 .pic{height:clamp(96px,15vh,150px)}\n",
    'print guard: .grid5 .pic keeps the pre-P3 height')

P.write_text(s, encoding='utf-8')
print('\nlines: %d -> %d' % (n0, len(s.splitlines())))
