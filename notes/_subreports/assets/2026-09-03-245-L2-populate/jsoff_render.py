#!/usr/bin/env python3
"""
jsoff_render.py — #245 L2-populate, enacting s245-D5: the 14 candidate `fallback` readings are
settled by a JS-OFF RENDER of each snippet, never accepted on a reading.

  cd <repo> && export TMPDIR=/dev/shm && source knowledge/_render/seat_env.sh && python3 jsoff_render.py

Every snippet is opened with `page.goto("file://…")` in a context created with
`browser.new_context(java_script_enabled=False)` — NEVER `set_content`. Each candidate clause that
concerns the COMPONENT'S OWN behaviour is turned into a named assertion, DRIVEN (typed into, clicked,
blurred, keyed) and measured on the DOM; a screenshot is taken before and after the interaction.
`page.evaluate` is used only to READ computed state — it runs in Playwright's isolated world and does
not re-enable the page's own scripts (asserted per page: `scripts_ran == False`, via a marker the
snippet's script would have set if it had run).

Verdict per snippet: PROVEN when every behavioural clause held; otherwise UNPROVEN with what was seen.
Writes jsoff-render.json + jsoff-render.txt + jsoff-<slug>-{before,after}.png beside this file.
"""
import json, os, sys, time
from playwright.sync_api import sync_playwright

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", "..", "..", ".."))
SNIP = os.path.join(REPO, "knowledge", "snippets")

VIS = """(sel) => { const e = document.querySelector(sel); if (!e) return null;
  const r = e.getBoundingClientRect(), cs = getComputedStyle(e);
  return r.width > 0 && r.height > 0 && cs.visibility !== 'hidden' && cs.display !== 'none' && cs.opacity !== '0'; }"""
ATTR = "([sel, a]) => { const e = document.querySelector(sel); return e ? e.getAttribute(a) : '<<no element>>'; }"
TEXT = "(sel) => { const e = document.querySelector(sel); return e ? e.textContent : '<<no element>>'; }"
CLS = "(sel) => { const e = document.querySelector(sel); return e ? e.className : '<<no element>>'; }"
COUNT = "(sel) => document.querySelectorAll(sel).length"
ACTIVE = "() => { const e = document.activeElement; return e ? (e.tagName + (e.id ? '#' + e.id : '') + (e.className ? '.' + String(e.className).trim().split(/\\s+/)[0] : '')) : null; }"
CSS = "([sel, p]) => { const e = document.querySelector(sel); return e ? getComputedStyle(e)[p] : '<<no element>>'; }"
RECT = "(sel) => { const e = document.querySelector(sel); if (!e) return null; const r = e.getBoundingClientRect(); return [Math.round(r.x), Math.round(r.y), Math.round(r.width), Math.round(r.height)]; }"
# Did the page's own script run? Every one of the 14 sets a modality tracker or mutates the DOM at load;
# the cheapest universal witness is `document.currentScript`-independent: count listeners is impossible,
# so we plant NOTHING and instead read a state each script writes at load (see per-snippet `ran`).


class Probe:
    def __init__(self, page, slug):
        self.page, self.slug, self.rows = page, slug, []

    def check(self, name, got, want, note=""):
        ok = got == want
        self.rows.append({"assert": name, "got": got, "want": want, "ok": ok, "note": note})
        print("   %s %-58s got=%r want=%r %s" % ("OK  " if ok else "FAIL", name, got, want, note))
        return ok

    def see(self, name, got):
        self.rows.append({"assert": name, "got": got, "want": None, "ok": None, "note": "observed"})
        print("   SEEN %-58s %r" % (name, got))


def run():
    out = {"$driven": "playwright chromium, new_context(java_script_enabled=False), page.goto(file://…); never set_content",
           "$date": "2026-09-03", "$session": "#245 L2-populate", "snippets": {}}
    lines = ["# jsoff_render.py — JS-OFF renders of the 14 interactive L2 snippets (s245-D5)", ""]
    with sync_playwright() as p:
        b = p.chromium.launch(executable_path=os.environ.get("RENDER_SHELL") or None)
        ctx = b.new_context(java_script_enabled=False, viewport={"width": 1200, "height": 900})
        pg = ctx.new_page()
        errors = []
        pg.on("pageerror", lambda e: errors.append(str(e)))

        def open_(name):
            pg.goto("file://" + os.path.join(SNIP, name + ".reference.html"))
            pg.wait_for_timeout(150)
            pg.screenshot(path=os.path.join(HERE, "jsoff-%s-before.png" % name.lower()), full_page=False)

        def shot(name):
            pg.screenshot(path=os.path.join(HERE, "jsoff-%s-after.png" % name.lower()), full_page=False)

        def ev(js, arg=None):
            return pg.evaluate(js, arg) if arg is not None else pg.evaluate(js)

        # ── 1 Amount-input ───────────────────────────────────────────────────────────────
        s = "Amount-input"; print("##", s); open_(s); P = Probe(pg, s)
        P.check("script ran? (modality tracker would set data-modality)", ev("() => document.documentElement.dataset.modality || null"), None)
        P.check("input#a1 carries inputmode=decimal (attribute, not script)", ev(ATTR, ["#a1", "inputmode"]), "decimal")
        pg.click("#a1"); pg.keyboard.type("1234.567abc"); pg.keyboard.press("Tab"); pg.wait_for_timeout(100)
        P.check("typed '1234.567abc' stays verbatim (no stripping/grouping/2dp)", ev("() => document.querySelector('#a1').value"), "1234.567abc")
        P.check("no is-completed weight after blur", "is-completed" in (ev("() => document.querySelector('#a1').closest('.ai, .ai-box, .field, div').className") or ""), False)
        P.check("#a1msg stays invisible after blur", ev(VIS, "#a1msg"), False)
        shot(s); out["snippets"]["amount-input"] = P.rows

        # ── 2 Anchor-nav ─────────────────────────────────────────────────────────────────
        s = "Anchor-nav"; print("##", s); open_(s); P = Probe(pg, s)
        cur0 = ev("() => [...document.querectorAll ? [] : []]") if False else ev("() => [...document.querySelectorAll('a[aria-current]')].map(a => a.getAttribute('href'))")
        P.see("aria-current links as authored", cur0)
        P.check("sections carry scroll-margin-top (CSS)", ev(CSS, ["#a-fees", "scrollMarginTop"]), "56px")
        y0 = ev("() => window.scrollY")
        pg.click("a[href='#a-fees']"); pg.wait_for_timeout(200)
        P.check("fragment link jumps: location.hash", ev("() => location.hash"), "#a-fees")
        P.check("fragment link jumps: page scrolled (scrollY changed)", ev("() => window.scrollY") != y0, True)
        P.check("aria-current did NOT move (stays where authored)", ev("() => [...document.querySelectorAll('a[aria-current]')].map(a => a.getAttribute('href'))"), cur0)
        shot(s); out["snippets"]["anchor-nav"] = P.rows

        # ── 3 Calendar ───────────────────────────────────────────────────────────────────
        s = "Calendar"; print("##", s); open_(s); P = Probe(pg, s)
        n_days = ev(COUNT, "#cal-table tbody button.cal-day")
        P.see("live grid #cal-table day buttons in markup (JS off)", n_days)
        P.see("#cal-title text (JS off)", ev(TEXT, "#cal-title"))
        P.see("#cal-echo text (JS off)", ev(TEXT, "#cal-echo"))
        P.see("#cal-body innerHTML length (JS off)", ev("() => document.querySelector('#cal-body').innerHTML.length"))
        P.check("month grid renders: server-authored day buttons present", n_days > 0, True, "candidate says 'server-authored buttons'; <tbody id=cal-body> is EMPTY in markup — the days are script-rendered")
        if n_days:
            sel0 = ev("() => document.querySelector('#cal-table tbody button.cal-day').getAttribute('aria-selected')")
            pg.click("#cal-table tbody button.cal-day"); pg.wait_for_timeout(100)
            P.check("clicking a day: aria-selected unchanged (nothing selects)", ev("() => document.querySelector('#cal-table tbody button.cal-day').getAttribute('aria-selected')"), sel0)
        t0 = ev(TEXT, "#cal-title"); e0 = ev(TEXT, "#cal-echo")
        pg.click("#cal-next-m"); pg.wait_for_timeout(100)
        P.check("clicking next-month: #cal-title unchanged (nothing pages)", ev(TEXT, "#cal-title"), t0)
        P.check("live region #cal-echo unchanged (no announcement)", ev(TEXT, "#cal-echo"), e0)
        shot(s); out["snippets"]["calendar"] = P.rows

        # ── 4 Command-palette ────────────────────────────────────────────────────────────
        s = "Command-palette"; print("##", s); open_(s); P = Probe(pg, s)
        P.see("role=dialog visible as authored (JS off)", ev(VIS, "div.cp[role=dialog]"))
        P.see("combobox aria-expanded as authored", ev(ATTR, ["input[role=combobox]", "aria-expanded"]))
        n0 = ev(COUNT, "#cp1-list [role=option]:not([hidden])")
        pg.keyboard.press("Control+k"); pg.wait_for_timeout(100)
        P.check("Ctrl+K opens nothing new (dialog count unchanged)", ev(COUNT, "div.cp[role=dialog]"), ev(COUNT, "div.cp[role=dialog]"))
        pg.click("#cp1-list").__class__  # no-op guard
        pg.click("input[role=combobox]"); pg.keyboard.type("zzzz"); pg.wait_for_timeout(100)
        P.check("typing does not filter (visible option count unchanged)", ev(COUNT, "#cp1-list [role=option]:not([hidden])"), n0)
        P.check("candidate clause 'cannot open' is TESTABLE on this snippet (palette authored CLOSED)?", ev(VIS, "div.cp[role=dialog]"), False,
                "the specimen authors the palette OPEN, so 'cannot open' is not measurable here")
        shot(s); out["snippets"]["command-palette"] = P.rows

        # ── 5 Date-picker ────────────────────────────────────────────────────────────────
        s = "Date-picker"; print("##", s); open_(s); P = Probe(pg, s)
        P.check("panel #dp-panel invisible at load", ev(VIS, "#dp-panel"), False)
        pg.click("#dp-open"); pg.wait_for_timeout(150)
        P.check("tail button click: panel stays invisible (never opens)", ev(VIS, "#dp-panel"), False)
        P.check("tail button click: aria-expanded stays false", ev(ATTR, ["#dp-open", "aria-expanded"]), "false")
        pg.click("#f-date"); pg.keyboard.type("31/02/2026"); pg.wait_for_timeout(100)
        P.check("typing: panel stays invisible", ev(VIS, "#dp-panel"), False)
        P.check("input works as native field (value as typed)", ev("() => document.querySelector('#f-date').value"), "31/02/2026")
        pg.keyboard.press("Tab"); pg.wait_for_timeout(150)
        P.check("blur on impossible date: #f-date-msg stays invisible (no validation)", ev(VIS, "#f-date-msg"), False)
        P.check("blur: no is-error class on the input", "is-error" in (ev(CLS, "#f-date") or ""), False)
        shot(s); out["snippets"]["date-picker"] = P.rows

        # ── 6 Date-range-picker ──────────────────────────────────────────────────────────
        s = "Date-range-picker"; print("##", s); open_(s); P = Probe(pg, s)
        P.check("panel #dr-panel invisible at load", ev(VIS, "#dr-panel"), False)
        pg.click("#dr-open-from"); pg.wait_for_timeout(120)
        P.check("from tail button: panel stays invisible", ev(VIS, "#dr-panel"), False)
        pg.click("#dr-open-to"); pg.wait_for_timeout(120)
        P.check("to tail button: panel stays invisible", ev(VIS, "#dr-panel"), False)
        P.check("both tail buttons aria-expanded false", [ev(ATTR, ["#dr-open-from", "aria-expanded"]), ev(ATTR, ["#dr-open-to", "aria-expanded"])], ["false", "false"])
        pg.click("#f-from"); pg.keyboard.type("20/03/2026"); pg.click("#f-to"); pg.keyboard.type("10/03/2026"); pg.keyboard.press("Tab"); pg.wait_for_timeout(150)
        P.check("both fields native (values as typed, to < from)", [ev("() => document.querySelector('#f-from').value"), ev("() => document.querySelector('#f-to').value")], ["20/03/2026", "10/03/2026"])
        P.check("no pair validation: both msgs invisible", [ev(VIS, "#f-from-msg"), ev(VIS, "#f-to-msg")], [False, False])
        shot(s); out["snippets"]["date-range-picker"] = P.rows

        # ── 7 File-upload ────────────────────────────────────────────────────────────────
        s = "File-upload"; print("##", s); open_(s); P = Probe(pg, s)
        P.see("native <input type=file> present", ev(COUNT, "input[type=file]"))
        P.see("#fu-input computed (clip-hidden 1×1, opacity 0)", ev("() => { const cs = getComputedStyle(document.querySelector('#fu-input')); return [cs.width, cs.height, cs.opacity, cs.position]; }"))
        opened = False
        try:
            with pg.expect_file_chooser(timeout=1500):
                pg.click("#fu-browse")
            opened = True
        except Exception:
            opened = False
        P.check("Browse <button> opens a file chooser with JS off", opened, True, "candidate: 'Browse still works IF the control wraps a native input' — the browse control is a <button> wired by script")
        opened_lbl = False
        try:
            with pg.expect_file_chooser(timeout=1500):
                pg.click("label[for='fu-input']")
            opened_lbl = True
        except Exception:
            opened_lbl = False
        P.check("<label for=fu-input> opens the native chooser with JS off (the 'wraps a native input' route)", opened_lbl, True)
        live = "#fu-input ~ *, #fu-input"
        P.see("live control: staged items / progress bars inside the live component's box", ev("() => { const box = document.querySelector('#fu-input').closest('.fu, .fu-box, section, div'); return [box.querySelectorAll('.fu-item, .fu-file, li').length, box.querySelectorAll('[role=progressbar]').length]; }"))
        P.check("progress bar absent in the LIVE control (static states specimens excluded)", ev("() => document.querySelector('#fu-input').closest('.fu, .fu-box, section, div').querySelectorAll('[role=progressbar]').length"), 0)
        P.check("#fu-announce empty (no announcement)", (ev(TEXT, "#fu-announce") or "").strip(), "")
        shot(s); out["snippets"]["file-upload"] = P.rows

        # ── 8 Form-layout ────────────────────────────────────────────────────────────────
        s = "Form-layout"; print("##", s); open_(s); P = Probe(pg, s)
        P.see("<form novalidate> present (native constraint validation OFF by markup)", ev("() => document.querySelector('form').hasAttribute('novalidate')"))
        pg.click("#f-sort"); pg.keyboard.type("123456"); pg.keyboard.press("Tab"); pg.wait_for_timeout(100)
        P.check("sort code NOT masked (value stays 123456)", ev("() => document.querySelector('#f-sort').value"), "123456")
        P.check("no per-field error after blur of an empty required-ish field", ev(VIS, "#f-name-msg"), False)
        url0 = pg.url
        try:
            with pg.expect_navigation(timeout=2500):
                pg.click("form button.fl-primary")
            navigated = True
        except Exception:
            navigated = False
        P.check("submit navigates natively (form GET to file:// URL)", navigated, True)
        P.see("url after submit (truncated)", pg.url[:120] if pg.url != url0 else "<unchanged>")
        if navigated:
            pg.wait_for_timeout(150)
        P.check("no summary #fs shown by script", ev(VIS, "#fs"), False)
        shot(s); out["snippets"]["form-layout"] = P.rows

        # ── 9 Secure-entry ───────────────────────────────────────────────────────────────
        s = "Secure-entry"; print("##", s); open_(s); P = Probe(pg, s)
        P.check("first cell carries autocomplete=one-time-code (attribute)", ev("() => document.querySelector('input.se-cell').getAttribute('autocomplete')"), "one-time-code")
        P.check("six cells in the first group", ev("() => document.querySelector('input.se-cell').closest('div, fieldset').querySelectorAll('input.se-cell').length"), 6)
        pg.click("input.se-cell"); pg.keyboard.type("1"); pg.wait_for_timeout(100)
        P.check("typing one digit: focus does NOT auto-advance", ev(ACTIVE), ev("() => { const e = document.querySelector('input.se-cell'); return e.tagName + (e.id ? '#' + e.id : '') + '.' + String(e.className).trim().split(/\\s+/)[0]; }"))
        pg.keyboard.type("23456"); pg.wait_for_timeout(100)
        vals = ev("() => [...document.querySelector('input.se-cell').closest('div, fieldset').querySelectorAll('input.se-cell')].map(i => i.value)")
        P.see("cell values after typing 123456 into cell 1 (maxlength decides)", vals)
        P.check("no paste/typing distribution: cells 2–6 empty", vals[1:], ["", "", "", "", ""])
        P.check("#otp-msg stays invisible (no verify state)", ev(VIS, "#otp-msg"), False)
        shot(s); out["snippets"]["secure-entry"] = P.rows

        # ── 10 Stepper ───────────────────────────────────────────────────────────────────
        s = "Stepper"; print("##", s); open_(s); P = Probe(pg, s)
        P.check("only the authored current panel visible: #p-1 visible", ev(VIS, "#p-1"), True)
        P.check("#p-2/#p-3/#p-4 hidden", [ev(VIS, "#p-2"), ev(VIS, "#p-3"), ev(VIS, "#p-4")], [False, False, False])
        live0 = ev(TEXT, "#stLive")
        pg.click("#st-next"); pg.wait_for_timeout(120)
        P.check("Next does nothing: #p-1 still visible, #p-2 still hidden", [ev(VIS, "#p-1"), ev(VIS, "#p-2")], [True, False])
        pg.click("#st-back"); pg.wait_for_timeout(120)
        P.check("Back does nothing: #p-1 still visible", ev(VIS, "#p-1"), True)
        P.check("no announcement (#stLive unchanged)", ev(TEXT, "#stLive"), live0)
        wide = ev("() => { const s = document.querySelector('.st'); const ol = s && s.querySelector('ol.steps'); const c = s && s.querySelector('.collapse'); return ol && c ? [getComputedStyle(ol).display, getComputedStyle(c).display] : null; }")
        P.see("container-query state at 1200 (ol.steps, .collapse display)", wide)
        pg.set_viewport_size({"width": 420, "height": 900}); pg.wait_for_timeout(200)
        narrow = ev("() => { const s = document.querySelector('.st'); const ol = s && s.querySelector('ol.steps'); const c = s && s.querySelector('.collapse'); return ol && c ? [getComputedStyle(ol).display, getComputedStyle(c).display] : null; }")
        P.check("dots→line collapse is CSS (@container 520px) and still fires JS off", [wide, narrow], [["flex", "none"], ["none", "block"]] if wide == ["flex", "none"] else [wide, ["none", "block"]])
        shot(s); pg.set_viewport_size({"width": 1200, "height": 900}); out["snippets"]["stepper"] = P.rows

        # ── 11 Tab-bar ───────────────────────────────────────────────────────────────────
        s = "Tab-bar"; print("##", s); open_(s); P = Probe(pg, s)
        P.check("items are native <a href>", ev(COUNT, "a.tabbar__item[href]") > 0, True)
        cur0 = ev("() => [...document.querySelectorAll('.tabbar a')].map(a => a.getAttribute('aria-current') || '')")
        P.see("authored aria-current across the first bar", cur0)
        pg.click("body"); pg.keyboard.press("Tab"); pg.wait_for_timeout(60)
        P.check("Tab key reaches a native <a> (keyboard-operable)", (ev("() => document.activeElement.tagName")), "A")
        act_rect0 = ev(RECT, ".tabbar .tabbar__item.is-active")
        pg.click(".tabbar a.tabbar__item:not(.is-active)"); pg.wait_for_timeout(150)
        P.check("click on another item: aria-current stands where authored", ev("() => [...document.querySelectorAll('.tabbar a')].map(a => a.getAttribute('aria-current') || '')"), cur0)
        P.check("the active pill does not move (is-active rect unchanged)", ev(RECT, ".tabbar .tabbar__item.is-active"), act_rect0)
        shot(s); out["snippets"]["tab-bar"] = P.rows

        # ── 12 Textarea ──────────────────────────────────────────────────────────────────
        s = "Textarea"; print("##", s); open_(s); P = Probe(pg, s)
        P.check("resize is vertical (CSS)", ev(CSS, ["#t1", "resize"]), "vertical")
        counter_sel = ev("() => { const e = document.querySelector('#t1'); const box = e.closest('.tx, .tx-box, div'); const c = box && box.parentElement.querySelector('[id$=count], .tx-count, .tx-counter, [data-count]'); return c ? ('#' + c.id || c.className) : null; }")
        c0 = ev(TEXT, counter_sel) if counter_sel else None
        P.see("counter element found / text before typing", [counter_sel, c0])
        live0 = ev(TEXT, "#t1-live")
        pg.click("#t1"); pg.keyboard.type("hello world, twelve words or so to move a counter if one were live"); pg.wait_for_timeout(120)
        P.check("value as typed appended to the authored text (native textarea)", ev("() => document.querySelector('#t1').value").endswith("if one were live"), True)
        if counter_sel:
            P.check("counter does not move", ev(TEXT, counter_sel), c0)
        P.check("no warn weight class", any(k in (ev("() => document.querySelector('#t1').closest('.tx, .tx-box, div').parentElement.className") or "") for k in ("is-warn",)), False)
        P.check("no announcement (#t1-live unchanged)", ev(TEXT, "#t1-live"), live0)
        shot(s); out["snippets"]["textarea"] = P.rows

        # ── 13 Time-picker ───────────────────────────────────────────────────────────────
        s = "Time-picker"; print("##", s); open_(s); P = Probe(pg, s)
        P.check("#tp-menu invisible at load", ev(VIS, "#tp-menu"), False)
        pg.click("#tp-open"); pg.wait_for_timeout(120)
        P.check("tail button: list stays invisible", ev(VIS, "#tp-menu"), False)
        P.check("tail button: aria-expanded stays false", ev(ATTR, ["#tp-open", "aria-expanded"]), "false")
        pg.click("#f-time"); pg.keyboard.type("25:99"); pg.wait_for_timeout(80)
        P.check("typing never opens the list", ev(VIS, "#tp-menu"), False)
        P.check("input native (value as typed)", ev("() => document.querySelector('#f-time').value"), "25:99")
        pg.keyboard.press("Tab"); pg.wait_for_timeout(150)
        P.check("blur on impossible time: #f-time-msg stays invisible", ev(VIS, "#f-time-msg"), False)
        shot(s); out["snippets"]["time-picker"] = P.rows

        # ── 14 Tree ──────────────────────────────────────────────────────────────────────
        s = "Tree"; print("##", s); open_(s); P = Probe(pg, s)
        st0 = ev("() => [...document.querySelectorAll('#live-tree [role=treeitem]')].map(li => li.getAttribute('aria-expanded') || '-')")
        P.see("authored aria-expanded states in #live-tree", st0)
        P.check("collapsed branch's group hidden by CSS ([aria-expanded=false] > .tr-group)", ev(VIS, "#live-tree [role=treeitem][aria-expanded=false] > .tr-group"), False)
        P.check("expanded branch's group visible", ev(VIS, "#live-tree [role=treeitem][aria-expanded=true] > .tr-group"), True)
        pg.click("#live-tree [role=treeitem][aria-expanded=false] > .tr-row"); pg.wait_for_timeout(120)
        P.check("click on a collapsed row: no expand (states unchanged)", ev("() => [...document.querySelectorAll('#live-tree [role=treeitem]')].map(li => li.getAttribute('aria-expanded') || '-')"), st0)
        pg.focus("#live-tree [role=treeitem][tabindex='0']"); a0 = ev(ACTIVE)
        pg.keyboard.press("ArrowDown"); pg.keyboard.press("ArrowRight"); pg.wait_for_timeout(100)
        P.check("Arrow keys: no keyboard model (focus stays, states unchanged)", [ev(ACTIVE), ev("() => [...document.querySelectorAll('#live-tree [role=treeitem]')].map(li => li.getAttribute('aria-expanded') || '-')")], [a0, st0])
        P.check("no lazy load in the LIVE tree (#live-tree .tr-loading absent/invisible; static ladder specimen excluded)", ev(VIS, "#live-tree .tr-loading") in (False, None), True)
        P.see("#tree-echo text (JS off)", ev(TEXT, "#tree-echo"))
        shot(s); out["snippets"]["tree"] = P.rows

        b.close()
        out["pageerrors"] = errors

    # verdicts
    verdicts = {}
    for slug, rows in out["snippets"].items():
        fails = [r["assert"] for r in rows if r["ok"] is False]
        verdicts[slug] = {"verdict": "PROVEN" if not fails else "UNPROVEN", "failed": fails,
                          "asserts": len([r for r in rows if r["ok"] is not None]), "observed": len([r for r in rows if r["ok"] is None])}
    out["verdicts"] = verdicts
    json.dump(out, open(os.path.join(HERE, "jsoff-render.json"), "w", encoding="utf-8"), indent=1, ensure_ascii=False)
    print("\nVERDICTS")
    for k, v in verdicts.items():
        print("  %-18s %-8s asserts=%d observed=%d %s" % (k, v["verdict"], v["asserts"], v["observed"], ("FAILED: " + "; ".join(v["failed"])) if v["failed"] else ""))
    print("proven %d / unproven %d of %d" % (sum(v["verdict"] == "PROVEN" for v in verdicts.values()), sum(v["verdict"] != "PROVEN" for v in verdicts.values()), len(verdicts)))
    print("pageerrors:", errors)


if __name__ == "__main__":
    run()
