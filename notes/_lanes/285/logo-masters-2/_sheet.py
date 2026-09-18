#!/usr/bin/env python3
"""Build the #285 contact sheet from the masters on disk (no help gate: lane scratch).

    python3 _sheet.py        # writes MASTERS-2026-09-18.html next to this file
"""
import os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", "..", ".."))
MAST = os.path.join(ROOT, "knowledge", "assets", "logos", "masters")
BEFORE = os.path.join(HERE, "before")
STEPS = [24, 28, 32, 36, 40]
NAMES = [f"{lock}-{theme}-{mode}"
         for lock in ("hexagon", "masterbrand")
         for theme in ("light", "dark")
         for mode in ("colour", "mono")]
SHORT = {"hexagon": "hex", "masterbrand": "mb"}
MAXH = max(STEPS)

CSS = open(os.path.join(HERE, "_sheet.css")).read()


def svg(path):
    s = open(path).read().strip()
    return re.sub(r"\n+", "", s)


def dims(s):
    return int(re.search(r'width="(\d+)"', s).group(1)), int(re.search(r'height="(\d+)"', s).group(1))


def one_x(name, dark):
    cells = []
    for h in STEPS:
        s = svg(os.path.join(MAST, "%s-%d.svg" % (name, h)))
        w, hh = dims(s)
        cells.append('<div class="sz"><div class="art">%s</div>'
                     '<span>%d px &middot; %d&times;%d</span></div>' % (s, h, w, hh))
    return '<div class="rack%s">%s</div>' % (" on-dark" if dark else "", "".join(cells))


def four_x(name, dark):
    cells = []
    for h in STEPS:
        s = svg(os.path.join(MAST, "%s-%d.svg" % (name, h)))
        w, hh = dims(s)
        cells.append('<div class="zc"><div class="zbox" style="width:%dpx;height:%dpx">'
                     '<div class="zin">%s</div></div><span>%d px &middot; %d&times;%d</span></div>'
                     % (w * 4, hh * 4, s, h, w, hh))
    return '<div class="rack zrack%s">%s</div>' % (" on-dark" if dark else "", "".join(cells))


def ba_cell(path, tag, cls):
    s = svg(path)
    w, hh = dims(s)
    return ('<div class="zc ba3"><span class="ba %s">%s</span>'
            '<div class="zbox" style="width:%dpx;height:%dpx"><div class="zin">%s</div></div>'
            '<span>%s</span></div>' % (cls, tag, w * 4, hh * 4, s, os.path.basename(path)))


def build():
    out = []
    out.append('<!DOCTYPE html>\n<html lang="en"><head>\n<meta charset="utf-8">'
               '<title>The forty masters, re-cut &mdash; #285</title>\n<style>\n%s</style>'
               '</head><body>' % CSS)
    jump = ''.join('<a href="#%s">%s-%s-%s</a>' % (n, SHORT[n.split("-")[0]], n.split("-")[1], n.split("-")[2])
                   for n in NAMES)
    out.append('<nav><div class="wrapper"><span class="now">#285 &mdash; the masters, re-cut</span>'
               '<div class="jump"><a href="#ba">before/after</a>%s</div></div></nav>' % jump)

    out.append('<section><div class="wrapper">'
               '<p class="label">Contact sheet &middot; 2026-09-18 &middot; lane LM2</p>'
               '<h1>The wordmark moves rigidly now.</h1>'
               '<p class="lede">Dave, on the #284 masters: <em>&ldquo;the word mark is distorted, look at '
               'the B&rdquo;</em>. Two causes, both in <code>snap_wordmark()</code>. It snapped on-path '
               'nodes inside S, B and C to whole pixels while leaving their cubic control points where '
               'they were &mdash; so the bowls kinked. And it scaled x and y by different factors: at the '
               '32&nbsp;px step the wordmark was drawn <b>4.4&nbsp;% wider than tall</b>.</p>'
               '<p class="lede">Both are gone. The wordmark is now placed by one uniform scale &mdash; '
               '<code>h/85</code>, the same factor the hexagon is drawn at &mdash; plus one translation '
               'shared by every coordinate of every glyph, control points included. Nothing inside a glyph '
               'is snapped to anything. The hexagon is unchanged: exact on the <code>h/4</code> grid.</p>'
               '<div class="stats">'
               '<div><b>40</b><span>masters on disk</span></div>'
               '<div><b>0</b><span>nodes snapped in a glyph</span></div>'
               '<div><b>1.0000</b><span>x-scale &divide; y-scale, every file</span></div>'
               '<div><b>0</b><span>files with a viewBox</span></div>'
               '</div></div></section>')

    # ---- before / after
    ba = []
    for h in (24, 40):
        ba.append('<div class="bapair"><p class="cap2">masterbrand-light-colour-%d &mdash; 4&times;</p>'
                  '<div class="rack zrack">%s%s</div></div>'
                  % (h,
                     ba_cell(os.path.join(BEFORE, "masterbrand-light-colour-%d.svg" % h), "BEFORE", "bad"),
                     ba_cell(os.path.join(MAST, "masterbrand-light-colour-%d.svg" % h), "AFTER", "good")))
    out.append('<section class="grey" id="ba"><div class="wrapper">'
               '<p class="label">Rule by eye</p><h2>Before / after, at 4&times;.</h2>'
               '<p class="sub">Left: the file committed at #284 (recovered with <code>git show HEAD:</code>). '
               'Right: the file on disk now. Look at the B &mdash; the join where each bowl leaves the stem, '
               'and whether the two bowls are the same shape. Then the C\'s terminals.</p>'
               '%s</div></section>' % "".join(ba))

    # ---- the eight lockups
    for n in NAMES:
        dark = "-dark-" in n
        out.append('<section id="%s"><div class="wrapper"><div class="lock">'
                   '<h3>%s</h3>'
                   '<p class="sub">Ground: %s &middot; five raw-height steps, inline at 1:1, no CSS scaling.</p>'
                   '%s'
                   '<p class="cap2">4&times; &mdash; <code>transform:scale(4)</code>, '
                   '<code>transform-origin:top left</code>, in a wrapper box sized 4&times; the file</p>'
                   '%s</div></div></section>'
                   % (n, n, "black" if dark else "white", one_x(n, dark), four_x(n, dark)))

    out.append('<footer><div class="wrapper">Generated by '
               '<code>notes/_lanes/285/logo-masters-2/_sheet.py</code> from '
               '<code>knowledge/assets/logos/masters/</code> &middot; brief '
               '<code>notes/_lanes/285/logo-masters-2/BRIEF.md</code></div></footer></body></html>')
    return "\n".join(out)


if __name__ == "__main__":
    p = os.path.join(HERE, "MASTERS-2026-09-18.html")
    open(p, "w").write(build())
    print("wrote", p, os.path.getsize(p), "bytes")
