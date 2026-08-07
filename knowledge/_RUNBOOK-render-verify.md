# Runbook — render-verify (Chromium + Playwright in the sandbox)

The repeatable procedure for rendering repo HTML to PNG **inside the Linux sandbox**, with the real
HSBC face, so the agent can SEE its own work before handing it over. Stood up 2026-07-23 at Dave's
ask ("there should be a runbook for chromium and playwright") — the recipe had lived only in agent
memory (`sandbox-html-rendering`, arc 2026-06-22 → 07-18), which is exactly the durable-rule-on-a-
Polaroid failure. **Every step below was run and OBSERVED working 2026-07-23** in a fresh sandbox
(arm64, no root, 45 s bash cap) unless marked HISTORY.

**What renders are FOR:** PNG = the agent's own verification — the 4th check after mechanical proofs
(contrast maths, `node --check`, gates). **HTML is what Dave reviews, never PNGs.** A standing
"render-verify OWED" note clears only when a render has been *seen*, not when the pipeline exists.

⛔ **THIS RUNBOOK WAS DECLARED DEAD BY A SESSION THAT NEVER OPENED IT — RE-VERIFIED WORKING #124.**
#123 declared a render gap on the grounds that *"chromium is TLS-blocked in-sandbox"*; #124 carried that
claim forward as fact and Dave caught it (*"and there is a runbook for chromium and playwright"*). The
recipe below was then run **end to end and it WORKS** — headless-shell download, no-root libs, render
**and drive** at 1180/480, PNGs seen. ⇒ ★★ **A FENCE INHERITED AS A FACT IS A PREMISE, AND PREMISES AGE
FASTER THAN RULES.** Before declaring a render gap, **run the recipe** — an environmental fence is
verified like repo state, against the thing itself, never quoted from a prior session's banner.
⚠ Scope, stated honestly: this says the RECIPE works. It says nothing about
`_validate_state_contrast.py`'s exemption, which is a separate record and is **not touched here.**
⚠ **Price the read, not just the render (#124):** two FULL-PAGE PNG reads were the swallow that crossed
that session's stop line. Assert numerically first, then read **the smallest crop that carries the
verdict** — `_RUNBOOK-context-gauge.md` § PRICE THE INSTRUMENT.

---

## The recipe (headless shell — the default)

Every bash call is independent: **re-export the env vars in every call.** Hard 45 s cap per call —
chunk long steps.

**1 · Playwright**
```bash
pip install playwright --break-system-packages
```

**2 · TLS env (the egress proxy's CA isn't in Node's bundle)**
```bash
export NODE_TLS_REJECT_UNAUTHORIZED=0 NODE_EXTRA_CA_CERTS=/etc/ssl/certs/ca-certificates.crt
```
Historically `NODE_EXTRA_CA_CERTS` alone was not always enough (2026-07-16); set both. If
`cdn.playwright.dev` DNS-fails (`EAI_AGAIN`), the `playwright.download.prss.microsoft.com` mirror
usually succeeds — that fallback is automatic, let it run.

**3 · Download the browser — EXACT target, and read the "failure" correctly**
```bash
setsid nohup python3 -m playwright install chromium-headless-shell > /tmp/pwdl.log 2>&1 &
sleep 38; tail -5 /tmp/pwdl.log; ls ~/.cache/ms-playwright/
```
- Target is `chromium-headless-shell` verbatim. HISTORY (2026-07-03): `install chromium --only-shell`
  pulled ffmpeg whose TLS failure made the installer **delete the entire ms-playwright cache**,
  including a shell that already worked. 2026-07-23 ffmpeg rode along fine *with the TLS env set*.
- Launch-and-poll **within one call** works; a background process does NOT survive the call ending
  (`bwrap --die-with-parent`) — never `nohup` across calls, chunk instead.
- ⚠ **EXPECTED non-zero exit:** after the download lands, the installer fails its *host-requirements
  validation* (missing system libs). **That is not a download refusal** — check
  `ls ~/.cache/ms-playwright/`: if `chromium_headless_shell-*` is there, proceed. (2026-07-22's
  "sandbox refused the headless-shell download" is consistent with this misread; both states are
  recorded, today's observation is: download works.)

**4 · System libs, without root**
```bash
mkdir -p ~/.local/chromelibs && cd ~/.local/chromelibs
apt-get download libxdamage1 libasound2 libnss3 libnspr4 libatk1.0-0 libatk-bridge2.0-0 \
  libcups2 libxcomposite1 libxrandr2 libgbm1 libxkbcommon0
for d in *.deb; do dpkg -x "$d" root/; done
export LD_LIBRARY_PATH=$HOME/.local/chromelibs/root/usr/lib/aarch64-linux-gnu:$LD_LIBRARY_PATH
```
(`apt-get download` needs no root and no `apt-get update`.) Full chrome needs ~6 more:
`libdrm2 libxfixes3 libxrender1 libxext6 libxcb1 libxi6`.

**5 · Fonts — the real HSBC face (DAVE'S RULE: always the HSBC cut, never stock Univers Next Pro)**
```bash
mkdir -p ~/.fonts ~/.config/fontconfig
cp knowledge/assets/fonts/_desktop/TTF/*.ttf ~/.fonts/
cat > ~/.config/fontconfig/fonts.conf << 'EOF'
<?xml version="1.0"?>
<!DOCTYPE fontconfig SYSTEM "fonts.dtd">
<fontconfig>
  <match target="pattern">
    <test name="family"><string>Univers Next for HSBC</string></test>
    <edit name="family" mode="prepend" binding="strong"><string>HSBC_MtUnivers_Latin</string></edit>
  </match>
  <match target="pattern">
    <test name="family"><string>Univers Next HSBC</string></test>
    <edit name="family" mode="prepend" binding="strong"><string>HSBC_MtUnivers_Latin</string></edit>
  </match>
</fontconfig>
EOF
fc-cache -f
```
⚠ **The alias must cover BOTH font strings** (folded 2026-07-26, observed 2026-07-24): snippets
declare `"Univers Next for HSBC"` (`--font`) but **type.css `--uf` declares `"Univers Next HSBC"`** —
with only the first match, chart composite text silently falls back to a stock face while everything
else renders correctly. Both `<match>` blocks above are required.
The alias means repo CSS declaring either string renders in the licensed cut with **no
file edits**. Assert in-page: `document.fonts.check('16px HSBC_MtUnivers_Latin')` must be `true`.
**Licence: DESKTOP** — rendering for our own verification is fine; embedding/serving/committing the
font into anything shared is NOT covered (the Latin *webfont* blocker `ASSERT-001` is untouched by
this runbook). Terms: `knowledge/assets/WebfontUserGuide-2024.pdf`.

**6 · Launch + shoot**
```bash
export LD_LIBRARY_PATH=$HOME/.local/chromelibs/root/usr/lib/aarch64-linux-gnu:$LD_LIBRARY_PATH \
       PLAYWRIGHT_SKIP_VALIDATE_HOST_REQUIREMENTS=1
python3 /tmp/render.py
```
```python
# /tmp/render.py — the proven shape (2026-07-23)
from playwright.sync_api import sync_playwright
import glob, os
shell = glob.glob(os.path.expanduser(
    '~/.cache/ms-playwright/chromium_headless_shell-*/chrome-linux/headless_shell'))
with sync_playwright() as p:
    b = p.chromium.launch(executable_path=shell[0] if shell else None, headless=True,
        args=["--no-sandbox","--disable-dev-shm-usage","--disable-gpu"])
    pg = b.new_page(viewport={"width":1180,"height":1400})
    pg.goto('file:///sessions/<session>/mnt/UX-design/<path>.html')   # file:// works in-sandbox
    pg.wait_for_timeout(1200)                                         # let CSS entry motion settle
    assert pg.evaluate("document.fonts.check('16px HSBC_MtUnivers_Latin')")
    pg.screenshot(path='/sessions/<session>/mnt/outputs/out.png', full_page=True)
    b.close()
```
Pass `executable_path` explicitly — default `launch()` resolution has broken before (2026-06-29).
Narrow the `viewport` to trigger `@container` collapses; no need to drive demo sliders.

**7 · See it**
Screenshot to the **outputs mount** (`/sessions/<session>/mnt/outputs/`) — file tools cannot reach
`/tmp` — then `Read` the PNG. A render that is produced but not read verifies nothing.

---

## Sandbox environment — stage on the SHARED MOUNT, not `$HOME` (folded 2026-07-26; observed working 2026-07-25)

Two sandbox facts break the naive recipe: **(a) `$HOME` rotates between bash calls** (cache + pip
installs don't survive), and **(b) calls load-balance across sandbox *instances* with unshared
`~/.cache`** — so even within one session, step 3's download can land on an instance a later call
never sees ("instance-flapping": the browser is there, then it isn't).

The fix that beat it (2026-07-25 session, render-verified output): **stage Playwright + the browser
+ chromelibs + fonts on the shared mount** (`/sessions/<session>/mnt/outputs/` or the repo mount —
shared across instances and calls), and point every env var there in EVERY call:

```bash
M=/sessions/<session>/mnt/outputs/_render-env       # any shared-mount dir
export PLAYWRIGHT_BROWSERS_PATH=$M/pw-browsers      # browser download target + lookup
pip install playwright --break-system-packages --target=$M/pylibs   # if pip state also flaps
export PYTHONPATH=$M/pylibs:$PYTHONPATH
export LD_LIBRARY_PATH=$M/chromelibs/root/usr/lib/aarch64-linux-gnu:$LD_LIBRARY_PATH
# fonts: keep ~/.fonts + fonts.conf per call (cheap to re-copy from the repo mount), or point
# FONTCONFIG_FILE at a conf staged on the mount.
```

Alternative when the env fights back: **do everything in ONE bash call** (download+libs+fonts+render
fit in ~40s warm, observed 2026-07-24) — one call = one instance, no flapping window.

| Symptom | Reading | Move |
|---|---|---|
| Installer exits non-zero after download | Host-validation, EXPECTED (step 3) | Check the cache, proceed |
| `UNABLE_TO_GET_ISSUER_CERT_LOCALLY` | Proxy CA missing from Node | Step 2, both vars |
| Cache empty though install "ran" | ffmpeg TLS wipe (07-03) or inter-call wipe (07-18) | Re-run step 3; don't re-diagnose |
| Chrome vanishes mid-session | Cache wiped between calls (07-18) | Re-run step 3 |
| Full chrome SIGSEGV on launch | Lib set incomplete (06-29 arc) | Shell first; else the ~17-lib set (07-16) |
| `nohup` job dead next call | `--die-with-parent` | Chunk ≤45 s; poll within the call |
| Render fine but wrong font | Alias file missing / fc-cache stale | Step 5; assert `document.fonts.check` |

## Two potholes banked 2026-07-26 (legend-wave lane ① — the recipe otherwise held first-try, from scratch)

**The runbook worked verbatim in a fresh sandbox** (arm64, no root): pip → TLS env → download →
expected host-validation failure with the shell present → 11 libs → fonts + the two-alias fontconfig →
render. No new steps needed. Two things cost time anyway:

**1 · `/tmp` was NOT writable.** `nohup … > /tmp/pwdl.log` failed with *Permission denied*, and the
background job died silently with it. `~/.cache`, `~/.fonts`, `~/.local` were all fine — it is `/tmp`
specifically. **Put logs and scratch on the outputs mount** (`/sessions/<s>/mnt/outputs/`), which is
writable and readable by the file tools. ⚠ This also affects the verify scripts: they default to
`JSDOM=/tmp/node_modules/jsdom`. That path happened to survive here, but do not assume it — the env
var exists for exactly this.

**2 · Render the SNIPPET, not the showroom page.** `showroom/<Component>.html` is a HARNESS: it loads
the component in an **iframe**. A `page.evaluate` that queries `document.querySelectorAll` from the top
frame therefore finds nothing and returns cleanly — no error, just empty results, which reads as
"the selector is wrong" and sends you looking in the wrong place. Cost one wasted shot on Chart-bar.
Point `goto` at `knowledge/snippets/<Component>.reference.html` — the canon artefact anyway — or drive
`page.frames()` deliberately.

## ★★ Pothole banked 2026-07-27 — SETTLE THE TRANSITION BEFORE YOU READ (it cost a whole false defect)

**A computed value read in the SAME TASK as a class change is the PRE-transition value.** This is not
subtle and it is not rare — it produced **ds-019**, a defect entry asserting that `.dv-legrow.is-solo`
"matches, its variables resolve, and it still does not paint", which was **wrong**, and which then
blocked DV-D17's render-proof and set the next window hunting a CSS rule that does not exist.

`.dv-legrow` carries `transition: border-color var(--ease), background var(--ease)` = **0.16s**.
Measured time series on the canon snippet, `.is-solo` applied directly:

| when | `border-top-color` | `background-color` |
|---|---|---|
| before add | `rgb(225,225,225)` (`--line`) | `rgba(0, 0, 0, 0)` |
| **t=0, same task** | **`rgb(225,225,225)`** | **`oklab(0 0 0 / 0)`** ← *what ds-019 recorded as proof* |
| t≈50ms | `rgb(145,145,145)` | `oklab(0.217785 … / 0.0241082)` |
| **t≈150ms +** | **`rgb(26,26,26)` = `--ink`** ✓ | **6% ink** ✓ |

⚠ **`oklab(…)` serialisation is the SIGNATURE OF AN IN-FLIGHT INTERPOLATION, not of a failed
declaration.** Chromium interpolates toward a `color-mix()` result in oklab. Reading `oklab(0 0 0 / 0)`
as *"fully transparent, so the declaration lost"* is exactly the misread. **The predecessor probe's
positive control actually DID detect this** — it saw `oklab(0 0 0 / 0)` differ from `rgba(0, 0, 0, 0)`
and passed — and the session dismissed its own control as a string-comparison artefact. **The control
was right for a reason nobody looked for.**

⇒ **RULE: any proof touching a transitioned property must settle first.** Either inject
`*{transition:none !important;animation:none !important}` **before** the class change (deterministic —
this is what `knowledge/_render/cdp_matched_styles.py --settle off` does by default), or wait past the
longest declared duration. **Never read in the same task.** ⚠ And when a measurement contradicts a
screenshot Dave has actually seen, **suspect the measurement first** — here the screenshot was right
and the probe was wrong for two sessions.

**Assert numerically, not visually, wherever the finding allows it.** ds-010's closure is a table of
`getComputedStyle(rect).fill` per figure, and ds-012 is a table of per-label `getBBox()` — both far
more durable in the record than "I looked and it seemed right", and both re-runnable. Take the PNG too
(a render still catches what you did not think to assert), but lead with the numbers.

## ★ Three potholes banked 2026-07-27 — two carried debts and one new (sessions #8–#11)

**1 · `__dirlock` EPERM is a failure message AFTER a success.** With `PLAYWRIGHT_BROWSERS_PATH` on the
outputs mount, the install ends with `EPERM: operation not permitted, rmdir '__dirlock'`. **Same species
as the host-requirements exit at step 3: the download landed.** `ls ~/.cache/ms-playwright/` — if
`chromium_headless_shell-*` is there, **proceed.** *(Carried in `GOOD-MORNING` §C·4 for four sessions
under "fold into the runbook next time that file is touched"; folded here 2026-07-27 #11.)*

**2 · The sandbox cannot `os.remove` under the repo mount — and a cleanup error can EAT YOUR VERDICT.**
`unlink` returns `EPERM` on the repo mount, so a probe's `--bite` teardown raises **after** the checks
have run. First observation (#11): the bite had correctly gone red, and the traceback replaced the
verdict line, so the run *looked* like a crash rather than a pass. **Two rules, both structural:**
**print the verdict BEFORE cleanup**, and **`shutil.move` the artefact to `outputs/` (same mount,
`.gitignore` line 45) — never `os.remove`, never a cross-mount move** (cross-mount degrades to
copy+unlink and hits the same `EPERM`).

**3 · Read CELLS, never flattened `textContent`.** A probe scraping ratios with `(\d+\.\d+):1` over a
table's `textContent` reported `11.31:1` where the page displayed `1.31:1` — adjacent `<td>`s
concatenate without a separator, so `#E1E1E1` + `1.31:1` becomes `…E1E1E11.31:1` and `\d+` greedily
eats the hex digit. **The document was right; the instrument was wrong** — the week's signature failure,
one more time. Query `r.cells[n].textContent`, and prefer `re.fullmatch` over `findall` so a malformed
scrape fails loud instead of returning a plausible number.

## Fallback — real-browser loop (Claude-in-Chrome on Dave's Mac)

If in-sandbox rendering is down, or a true-browser check is wanted: Dave starts a **THREADING**
server from the repo root (plain `python3 -m http.server` **deadlocks** — single thread + keep-alive):
```bash
python3 -c "import http.server,socketserver; socketserver.ThreadingTCPServer.allow_reuse_address=True; socketserver.ThreadingTCPServer(('',8000),http.server.SimpleHTTPRequestHandler).serve_forever()"
```
Then navigate the extension to `http://localhost:8000/<path>` (**`file://` is blocked**) and
screenshot. **Chrome caches** — cache-bust `?v=N` after every edit.

## When to run

Before handing Dave anything that claims visual correctness — review sheets, snippets, showroom
panes. The 2026-07-23 stand-up itself is the case study: the first render of the Q6 sheet caught
dark-on-dark dial text that every mechanical check had passed.

**Render responsive surfaces at ≥2 viewport widths.** Same day, same sheet: a single-viewport pass
missed a viewBox stretch (specimen text + strokes scaling with pane width — banned physics) that
Dave caught in his browser at a narrower window. One width proves one layout, nothing else.
