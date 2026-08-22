#!/usr/bin/env python3
"""_validate_descender_computed.py — G2, the RENDER leg of the descender-clip gate (ds-005).

WHY A SECOND LEG EXISTS
-----------------------
`_validate_descender_clip.py` has two legs and both of them are ARITHMETIC:

  leg 1  the override STRING is present somewhere in the file
  leg 2  the override's specificity BEATS the leading-trim rule, per a resolver written here

Leg 2's resolver is a model of the cascade, not the cascade. It can be right about the clause and
wrong about the feature — [[mutation-tests-the-clause-not-the-feature]]. G2 closes that by DRIVING
the thing: it loads real pages in headless Chromium and reads `getComputedStyle`, which is Chromium's
own cascade resolution, on the actual label elements the overrides name.

WHAT IT COMPARES
----------------
The reference snippet (`knowledge/snippets/<Name>.reference.html`) is the REVIEWED artefact: the
cascade Dave signed off. canon.css is a projection of it through the absorb prefixer. So the
assertion is a comparison, not a constant:

    for every label an ds-005 override names, canon must compute the SAME
    `text-box-trim` / `text-box-edge` as the snippet does.

A canon label computing `cap alphabetic` where the snippet computes `text` is a descender clip that
leg 1 reports green (string present) and that leg 2 can only INFER. Here it is observed.

Two pages per component, both `goto file://…`:
  SNIPPET  the reference file itself, untouched
  CANON    a harness staged in TMPDIR: type.css + canon.css, then the snippet's own <body> markup
           VERBATIM inside `<div class="canon"><div class="cn-<slug>">` — i.e. exactly how canon
           projects that component. The markup is COPIED, never re-drawn
           [[specimen-starts-from-reference]].

SANDBOX RULES OBEYED HERE (each one has burned a prior session — knowledge/_RUNBOOK-render-verify.md)
  · `page.set_content()` is BANNED — it drops the linked stylesheets silently. Always `goto file://`.
  · `document.fonts.check()` LIES — it returned true in both a working and a broken font config.
    The precondition here is the CANVAS PROBE with two controls (a real different face, and a face
    that does not exist); the target must differ from BOTH.
  · Transitions must be SETTLED before any computed read — `*{transition:none;animation:none}` is
    injected into the page BEFORE the first read, never a same-task read after a class change.
  · Nothing survives a tool-call boundary and long runs get killed — `--range A:B` + `--resume`
    chunk the work and bank partial results in a JSON file under TMPDIR.
  · Scratch goes to TMPDIR (default /var/tmp); `/tmp` and `$HOME` ENOSPC and flap between calls.

Usage:
  python3 knowledge/_validate_descender_computed.py                 # all components
  python3 knowledge/_validate_descender_computed.py --range 0:8     # chunk (half-open, by index)
  python3 knowledge/_validate_descender_computed.py --resume        # merge banked chunks + verdict
  python3 knowledge/_validate_descender_computed.py --list          # the work list, no browser
  python3 knowledge/_validate_descender_computed.py --bite <slug>   # MUTATION ARM: plant a losing
                                                                    # override in a TEMP canon copy
                                                                    # for <slug> and require a RED
Exit 0 = every driven label matches its snippet. Non-zero = mismatch, or the run could not be
driven (an UNDRIVEABLE environment is a LOUD refusal, never a silent pass).

Environment (all overridable; the defaults are the runbook's):
  PLAYWRIGHT_BROWSERS_PATH, PYTHONPATH, LD_LIBRARY_PATH, TMPDIR, FONTCONFIG_FILE
"""
import os as _hg_os, sys as _hg_sys  # noqa: E402 - help gate (#158 write-by-default class)
_hg_d = _hg_os.path.dirname(_hg_os.path.abspath(__file__))
while _hg_d != "/" and not _hg_os.path.exists(_hg_os.path.join(_hg_d, "_helpgate.py")):
    _hg_d = _hg_os.path.dirname(_hg_d)
_hg_sys.path.insert(0, _hg_d)
from _helpgate import help_gate as _help_gate; _help_gate(__doc__, __name__, __file__)

import os, re, sys, json, glob, tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
CANON_CSS = os.path.join(HERE, "canon", "canon.css")
TYPE_CSS = os.path.join(HERE, "canon", "type.css")
SNIPPETS = os.path.join(HERE, "snippets")
SCRATCH = os.environ.get("TMPDIR", "/var/tmp")
BANK = os.path.join(SCRATCH, "descender-computed-bank.json")

# Reuse the arithmetic leg's parser so the two legs cannot drift apart on what a "rule" is.
sys.path.insert(0, HERE)
import _validate_descender_clip as A  # noqa: E402

# The one property pair that decides a descender clip. `text-box-trim` says whether the box is
# trimmed at all; `text-box-edge` says to WHICH edge. Chromium serialises `text text` as `text`.
PROPS = ("text-box-trim", "text-box-edge")

# The canvas probe string + size from the runbook's table (40px "Handgloves 12345").
PROBE_TEXT, PROBE_PX = "Handgloves 12345", 40

# ≥2 widths, per the runbook: "one width proves one layout, nothing else". Several ds-005 overrides
# live inside an @media/@container arm (App-shell-nav-rail's `.sh-rail .sn-label` is the case that
# forced this), so a single-viewport run leaves them UNDRIVEN and calls it green.
VIEWPORTS = ((1180, 1400), (480, 1400))


# ---------------------------------------------------------------------------- the work list
def work_list(canon_css_text=None):
    """[(slug, [local selector, ...]), ...] — every ds-005 override in the AUTO-COMPONENTS block,
    with the generated scope stripped back to the selector the SNIPPET authored.

    Derived from canon.css itself, not from a hand list: a component that gains an override
    tomorrow joins this run without anyone remembering to add it [[gate-inside-the-growth-loop]].
    """
    raw = canon_css_text if canon_css_text is not None else open(CANON_CSS, encoding="utf-8").read()
    si = raw.find("AUTO-COMPONENTS START")
    if si < 0:
        raise SystemExit("descender --computed: no AUTO-COMPONENTS block in canon.css")
    body = re.sub(r"/\*.*?\*/", "", raw[si:], flags=re.S)
    out = {}
    for m in A.RULE.finditer(body):
        if not A.OVR_TEXTBOX.search(m.group(2)):
            continue
        for s in A._split_top(A._norm(m.group(1))):
            # both prefixer shapes, so this leg still works if someone reverts the :where() fix
            mm = re.match(r"(?::where\()?\.cn-([a-z0-9-]+)\)?\s+(.+)$", s)
            if not mm:
                continue
            slug, local = mm.group(1), mm.group(2).strip()
            if local.startswith(">"):          # a child combinator left dangling by the strip
                continue
            out.setdefault(slug, [])
            if local not in out[slug]:
                out[slug].append(local)
    return sorted((k, v) for k, v in out.items() if snippet_for(k))


def snippet_for(slug):
    """The reference snippet whose generated scope is `.cn-<slug>`, or None."""
    for p in sorted(glob.glob(os.path.join(SNIPPETS, "*.reference.html"))):
        name = os.path.basename(p).replace(".reference.html", "")
        if re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-") == slug:
            return p
    return None


# ---------------------------------------------------------------------------- page staging
SETTLE = ("<style id='g2-settle'>*,*::before,*::after{transition:none !important;"
          "animation:none !important;}</style>")


def canon_page(slug, snippet_path, canon_css_path, out_path):
    """Stage the CANON harness: the snippet's own <body> markup, verbatim, under the canon scope.

    Scripts are stripped: this leg reads the STATIC cascade, and a demo harness that flips classes
    on load would make the read non-deterministic (and a same-task read after a class change is the
    #ds-019 misread the runbook records). `<base>` keeps any relative asset in the markup resolving
    against the snippet's own directory.
    """
    html = open(snippet_path, encoding="utf-8").read()
    m = re.search(r"<body[^>]*>(.*)</body>", html, re.S)
    if not m:
        raise SystemExit(f"descender --computed: {os.path.basename(snippet_path)} has no <body>")
    markup = re.sub(r"<script\b.*?</script>", "", m.group(1), flags=re.S | re.I)
    base = "file://" + os.path.dirname(os.path.abspath(snippet_path)) + "/"
    doc = (f"<!doctype html><html><head><meta charset='utf-8'>"
           f"<base href='{base}'>"
           f"<link rel='stylesheet' href='file://{os.path.abspath(TYPE_CSS)}'>"
           f"<link rel='stylesheet' href='file://{os.path.abspath(canon_css_path)}'>"
           f"{SETTLE}</head><body data-theme='light'>"
           f"<div class='canon'><div class='cn-{slug}'>{markup}</div></div></body></html>")
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(doc)
    return out_path


def snippet_page(snippet_path, out_path):
    """Stage the SNIPPET side: the reviewed file, byte-for-byte, plus the settle style and minus
    its scripts. The <style> block — the reviewed cascade — is untouched, which is the point."""
    html = open(snippet_path, encoding="utf-8").read()
    html = re.sub(r"<script\b.*?</script>", "", html, flags=re.S | re.I)
    base = "file://" + os.path.dirname(os.path.abspath(snippet_path)) + "/"
    html = html.replace("<head>", f"<head><base href='{base}'>", 1)
    html = html.replace("</head>", SETTLE + "</head>", 1)
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(html)
    return out_path


# ---------------------------------------------------------------------------- the browser
READ_JS = """
(sels) => {
  const out = {};
  for (const s of sels) {
    const rows = [];
    let nodes = [];
    try { nodes = Array.from(document.querySelectorAll(s)); } catch (e) { out[s] = {error: String(e)}; continue; }
    nodes.forEach((el, i) => {
      const cs = getComputedStyle(el);
      const r = el.getBoundingClientRect();
      rows.push({i: i,
                 trim: cs.getPropertyValue('text-box-trim').trim(),
                 edge: cs.getPropertyValue('text-box-edge').trim(),
                 h: Math.round(r.height * 100) / 100,
                 txt: (el.textContent || '').trim().slice(0, 24)});
    });
    out[s] = {n: nodes.length, rows: rows};
  }
  return out;
}
"""

FONT_PROBE_JS = """
() => {
  const c = document.createElement('canvas').getContext('2d');
  const w = (fam) => { c.font = '%dpx ' + fam; return Math.round(c.measureText(%s).width * 100) / 100; };
  return {target: w('HSBC_MtUnivers_Latin'),
          alias1: w('"Univers Next HSBC"'),
          alias2: w('"Univers Next for HSBC"'),
          control: w('"DejaVu Sans"'),
          missing: w('"NoSuchFace-ZZQQ"')};
}
""" % (PROBE_PX, json.dumps(PROBE_TEXT))


def launch(p):
    shell = (glob.glob(os.path.join(os.environ.get("PLAYWRIGHT_BROWSERS_PATH", ""),
                                    "chromium_headless_shell-*/chrome-linux/headless_shell"))
             or glob.glob(os.path.expanduser(
                 "~/.cache/ms-playwright/chromium_headless_shell-*/chrome-linux/headless_shell")))
    return p.chromium.launch(executable_path=shell[0] if shell else None, headless=True,
                             args=["--no-sandbox", "--disable-dev-shm-usage", "--disable-gpu"])


def font_precondition(page):
    """The runbook's canvas probe WITH CONTROLS. `document.fonts.check()` is deliberately not used:
    it returned true in both the working and the broken configuration, so it cannot discriminate.
    Reported, not fatal — text-box-edge is a keyword and resolves identically in any face; the
    HEIGHT column is the part that needs the real cut, so a miss downgrades that column's weight."""
    r = page.evaluate(FONT_PROBE_JS)
    r["ok"] = bool(r["target"] != r["missing"] and r["control"] != r["target"])
    return r


def drive(items, canon_css_path=None):
    """Render each (slug, selectors) both ways. Returns {slug: {...}}; raises on an undriveable env."""
    try:
        from playwright.sync_api import sync_playwright
    except Exception as e:                                    # a crash is not a fail — name it
        raise SystemExit(f"descender --computed: UNDRIVEABLE — playwright not importable ({e}). "
                         f"Stage it per knowledge/_RUNBOOK-render-verify.md and set PYTHONPATH / "
                         f"PLAYWRIGHT_BROWSERS_PATH. This is a REFUSAL, not a pass.")
    canon_css_path = canon_css_path or CANON_CSS
    stage = tempfile.mkdtemp(prefix="g2-", dir=SCRATCH)
    results = {}
    with sync_playwright() as p:
        b = launch(p)
        pg = b.new_page(viewport={"width": VIEWPORTS[0][0], "height": VIEWPORTS[0][1]})
        first_font = None
        for slug, sels in items:
            snip = snippet_for(slug)
            cp = canon_page(slug, snip, canon_css_path, os.path.join(stage, f"{slug}.canon.html"))
            sp = snippet_page(snip, os.path.join(stage, f"{slug}.snip.html"))
            row = {"selectors": sels, "widths": {}}
            for w, h in VIEWPORTS:
                pg.set_viewport_size({"width": w, "height": h})
                side_rows = {}
                for side, path in (("snippet", sp), ("canon", cp)):
                    pg.goto("file://" + os.path.abspath(path))
                    pg.wait_for_timeout(250)      # settle style is already in the document
                    if first_font is None:
                        first_font = font_precondition(pg)
                    side_rows[side] = pg.evaluate(READ_JS, sels)
                row["widths"][str(w)] = side_rows
            results[slug] = row
        b.close()
    results["_font"] = first_font
    results["_stage"] = stage
    return results


# ---------------------------------------------------------------------------- the verdict
def verdict(results):
    """(fails, driven, skipped, notes) — the rendered ds-005 assertion, per element, per viewport.

    THE FAILING ASSERTION IS THE COMPARISON: canon must compute the same `text-box-edge` as the
    REVIEWED snippet, on the same element, at the same width. That is exactly what the absorb
    prefixer is supposed to preserve and exactly what it was breaking. Two things driving the real
    files taught this leg, both recorded so nobody re-derives them:

    · `text-box-trim` legitimately DIFFERS between the two sides. A standalone snippet carrying no
      leading-trim rule of its own (File-upload) computes `none`, while canon's global
      `.canon :is(…)` trims the same label. Edge is `text` on both sides — descender-safe, no
      defect. Failing that would be a gate reporting a difference it has no rule against.

    · "canon is trimmed AND computes `cap alphabetic`" is NOT a sound failure either. Several
      ds-005 overrides live inside an `@media`/`@container` arm (App-shell-nav-rail's
      `.sh-rail .sn-label`), so at a width where that arm is not in force the label computes
      `cap alphabetic` on BOTH sides, by design — and several of those labels are the sr-only
      clip-path form with nothing visible to clip. An absolute rule here fires on correct CSS.
      It is kept as a NOTE, and answered instead by driving more than one viewport.

      FAIL  canon's computed `text-box-edge` differs from the snippet's, at any driven width
      NOTE  both sides trimmed at `cap alphabetic` (override out of force at this width)
      NOTE  the two sides differ only on `text-box-trim`, edge equal and descender-safe
    """
    fails, driven, skipped, notes = [], 0, [], []
    for slug, row in sorted(results.items()):
        if slug.startswith("_"):
            continue
        for w, sides in sorted(row["widths"].items(), key=lambda kv: -int(kv[0])):
            for sel in row["selectors"]:
                s_side, c_side = sides["snippet"].get(sel, {}), sides["canon"].get(sel, {})
                at = f"{slug} @{w}px · `{sel}`"
                if s_side.get("error") or c_side.get("error"):
                    fails.append(f"{at} — selector error: "
                                 f"{s_side.get('error') or c_side.get('error')}")
                    continue
                sn, cn = s_side.get("n", 0), c_side.get("n", 0)
                if sn == 0 and cn == 0:
                    # the override names a state-only element the static markup never instantiates
                    skipped.append(f"{at} (0 nodes either side)")
                    continue
                if sn != cn:
                    fails.append(f"{at} — node count differs: snippet {sn}, canon {cn}. "
                                 f"The canon harness is not rendering the same markup.")
                    continue
                for a_row, b_row in zip(s_side["rows"], c_side["rows"]):
                    driven += 1
                    if a_row["edge"] != b_row["edge"]:
                        fails.append(
                            f"{at} [{a_row['i']}] 'text-box-edge': snippet computes "
                            f"{a_row['edge']!r} but canon computes {b_row['edge']!r} "
                            f"(label {a_row['txt']!r}, heights {a_row['h']} vs {b_row['h']}px). "
                            f"The ds-005 override is CASCADE-DEAD in the rendered canon — the "
                            f"descenders clip. Fix the SCOPE's specificity, not the override.")
                    elif b_row["trim"] != "none" and b_row["edge"] == "cap alphabetic":
                        notes.append(
                            f"{at} [{b_row['i']}] both sides trimmed at 'cap alphabetic' "
                            f"({b_row['txt']!r}, {b_row['h']}px) — the override for this label is "
                            f"not in force at this width (an @media/@container arm, or the sr-only "
                            f"clip-path form). Canon matches the snippet; nothing regressed here.")
                    elif a_row["trim"] != b_row["trim"]:
                        notes.append(
                            f"{at} [{a_row['i']}] 'text-box-trim' snippet {a_row['trim']!r} vs "
                            f"canon {b_row['trim']!r}, edge {b_row['edge']!r} both sides — canon's "
                            f"global `.canon :is(…)` trim reaching a label the standalone snippet "
                            f"does not trim. Descender-safe; not a ds-005 defect.")
    return fails, driven, skipped, notes


def report(results, fails, driven, skipped, notes=(), label="G2"):
    f = results.get("_font") or {}
    if f:
        print(f"  font probe (canvas, {PROBE_PX}px {PROBE_TEXT!r}): target={f.get('target')} "
              f"alias1={f.get('alias1')} alias2={f.get('alias2')} control={f.get('control')} "
              f"missing={f.get('missing')} -> {'DISCRIMINATES' if f.get('ok') else 'NOT DISCRIMINATING'}")
        if not f.get("ok"):
            print("  ⚠ the font config does not discriminate — the HEIGHT column below is not "
                  "evidence. text-box-edge/-trim are keywords and are unaffected.")
    for s in skipped:
        print(f"  · not instantiated in static markup, not driven: {s}")
    for s in notes:
        print(f"  ⓘ {s}")
    for x in fails:
        print(f"  ✗ {x}")
    n_comp = len([k for k in results if not k.startswith('_')])
    widths = sorted({w for k, v in results.items() if not k.startswith('_')
                     for w in v.get("widths", {})}, key=lambda x: -int(x))
    if fails:
        print(f"\n{label} FAIL — {len(fails)} rendered mismatch(es) across {n_comp} component(s), "
              f"{driven} label-read(s) driven at {', '.join(w + 'px' for w in widths)}.")
        return 1
    print(f"\n{label} PASS — {driven} label-read(s) driven in Chromium across {n_comp} "
          f"component(s) at {', '.join(w + 'px' for w in widths)}; every ds-005 override computes "
          f"in canon exactly what it computes in its reviewed snippet.")
    return 0


# ---------------------------------------------------------------------------- the mutation arm
def bite(slug):
    """Drive G2 RED on purpose. Stages a TEMP copy of canon.css in which <slug>'s ds-005 overrides
    are demoted to a genuinely losing form, and requires the run to catch it.

    A green that cannot go red is not evidence [[mutation-tests-the-clause-not-the-feature]].
    The repo copy of canon.css is never touched.
    """
    raw = open(CANON_CSS, encoding="utf-8").read()
    # Demote: strip the :where() from THIS slug's trim rule so the scope inflates it again, exactly
    # the #214 defect. Nothing authored is edited — the scaffolding is put back the way it was.
    pat = re.compile(r":where\((\.cn-%s)\)" % re.escape(slug))
    mutated, n = pat.subn(r"\1", raw)
    mutated = mutated.replace(":where(.canon) :is(button,", ".canon :is(button,")
    if n == 0:
        raise SystemExit(f"--bite {slug}: nothing to mutate (no :where(.cn-{slug}) in canon.css)")
    tmp = os.path.join(SCRATCH, f"canon-bite-{slug}.css")
    with open(tmp, "w", encoding="utf-8") as f:
        f.write(mutated)
    items = [(s, sels) for s, sels in work_list(mutated) if s == slug]
    if not items:
        raise SystemExit(f"--bite {slug}: no ds-005 override for that slug")
    print(f"--bite {slug}: {n} scope wrapper(s) reverted in a TEMP canon copy ({tmp}); "
          f"driving {len(items[0][1])} selector(s) — a RED here is the PASS.")
    res = drive(items, canon_css_path=tmp)
    fails, driven, skipped, notes = verdict(res)
    report(res, fails, driven, skipped, notes, label="G2 --bite")
    if fails:
        print(f"\n✓ MUTATION ARM PASS — the reverted scope was CAUGHT in the rendered cascade "
              f"({len(fails)} mismatch(es)). G2 can fail, so its green means something.")
        return 0
    print(f"\n✗ MUTATION ARM FAIL — the planted regression rendered CLEAN. G2 cannot fail on this "
          f"input and its green proves nothing. Do not trust it.")
    return 1


# ---------------------------------------------------------------------------- entry
def main(argv):
    items = work_list()
    if "--list" in argv:
        for i, (slug, sels) in enumerate(items):
            print(f"{i:3d}  {slug:<32} {len(sels)} selector(s)")
        print(f"{len(items)} component(s), {sum(len(s) for _, s in items)} selector(s)")
        return 0
    if "--bite" in argv:
        return bite(argv[argv.index("--bite") + 1])

    banked = {}
    if "--resume" in argv and os.path.exists(BANK):
        banked = json.load(open(BANK))

    lo, hi = 0, len(items)
    if "--range" in argv:
        a, _, b = argv[argv.index("--range") + 1].partition(":")
        lo, hi = int(a or 0), int(b or len(items))
    chunk = items[lo:hi]
    if chunk:
        res = drive(chunk)
        banked.update({k: v for k, v in res.items() if not k.startswith("_")})
        banked["_font"] = res.get("_font")
        with open(BANK, "w") as f:
            json.dump(banked, f)
        print(f"driven [{lo}:{hi}] — {len(chunk)} component(s) banked to {BANK}")

    done = [k for k in banked if not k.startswith("_")]
    if len(done) < len(items) and "--resume" not in argv and (lo, hi) != (0, len(items)):
        print(f"partial: {len(done)}/{len(items)} component(s) banked. Run the next --range, "
              f"then --resume for the verdict.")
        return 0
    fails, driven, skipped, notes = verdict(banked)
    return report(banked, fails, driven, skipped, notes)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
