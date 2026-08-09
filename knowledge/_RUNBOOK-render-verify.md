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

✅ **RE-VERIFIED 2026-08-08 (#129) — THE #125 CONTRADICTION IS ADJUDICATED: THE DOWNLOAD WORKS.**
Two #125 subs recorded opposite first-hand readings (succeed-then-`EPERM` vs TLS-blocked-on-3-CDNs);
three sessions carried both without a winner. Run fresh today, first-hand, exit **0**:
`chromium_headless_shell-1234` (340M) + ffmpeg landed in full. **The TLS-blocked reading did NOT
reproduce** — `cdn.playwright.dev` connected and streamed bytes with the step-2 env set. The
succeed-then-noise reading is the right SPECIES (trailing host-requirements/`EPERM` errors arrive
AFTER a successful download — steps 3 and pothole 1 already say so). **Two NEW potholes, both
environmental, neither TLS:**
- **ENOSPC masquerades as "Download failure, code=1".** `$HOME` sits on a shared `/sessions` volume
  that was 98% full (237M free); the first attempt died mid-write with `ENOSPC: no space left on
  device` buried 15 lines up the log. **Check `df -h $HOME` before diagnosing the network**, and set
  `PLAYWRIGHT_BROWSERS_PATH=/var/tmp/pw-browsers-<session>` (root fs, ~2G free) — that is what made
  today's run land.
- **`/tmp` and `/sessions` are SHARED across sessions.** `/tmp/pwdl.log` already existed, owned by a
  foreign session — unwritable, but READABLE, so a `tail` after a failed redirect served another
  session's stale traceback as if it were this run's evidence (attribute-the-diff, environmental
  form). **Use a unique log path under `$HOME`, and treat any pre-existing `/tmp` artefact as
  foreign.**
*(Addition only; the #125 strata below and in the session record stand as history. 2026-08-08.)*

✅ **RE-VERIFIED 2026-08-08 (#136) — ENOSPC POTHOLE n=3, NEW WORKING RECIPE.** `$HOME` was 100% full
again (a fixed cutoff, not a slow leak — same class as #129's, third occurrence). The #129 fix
(`PLAYWRIGHT_BROWSERS_PATH` alone) was NOT sufficient this time; the full working env, all four
render-verified artefacts (1180+480, real HSBC face, drive-tested):
```bash
pip install --target /var/tmp/pylibs <pkg>          # pip itself ENOSPCs against $HOME otherwise
export PYTHONPATH=/var/tmp/pylibs:$PYTHONPATH
export PLAYWRIGHT_BROWSERS_PATH=/var/tmp/pw-browsers-<session>
export FONTCONFIG_FILE=/var/tmp/fonts-<session>.conf   # <dir> inside points at repo TTFs — no font copy
export TMPDIR=/var/tmp
export LD_LIBRARY_PATH=/var/tmp/chromelibs/root/usr/lib/aarch64-linux-gnu   # pre-existing, foreign-session libs
```
**`FONTCONFIG_FILE` pointed at the repo's own TTF paths is the new element** — no font copy needed,
where prior sessions copied fonts into the sandbox. **`LD_LIBRARY_PATH` libs pre-existed from a foreign
session** (the `/tmp`-is-shared fact from #129, used constructively this time rather than as a
contamination risk). *(Addition only; #129's recipe and history stand. 2026-08-08.)*
⛔ **THE `<dir>`→REPO ELEMENT ON THIS LINE AND LINE 42 IS SUPERSEDED — see § SYMLINK FARM (#138) below.**
It saved the disk and moved fontconfig's *writes* into the tree. Do not copy this block forward.

✅ **RE-VERIFIED AND SUPERSEDED 2026-08-09 (#138) — THE SYMLINK FARM. Fontconfig stops writing into the
repo it scans.** #136's `<dir>`→repo trick was DRIVEN again today and it reproduces exactly: `fc-cache`
against a conf whose `<dir>` is `knowledge/assets/fonts/_desktop/TTF/` writes **`.uuid`, `.uuid.LCK`,
`.uuid.TMP-XXXXXX`** into that directory (`.TMP` suffix is random — #136 got `NpSPVs`, #138 got
`SpeXCi`), and `git status --untracked-files=all` flags all three, which trips `s133-D2`'s clean-tree
push gate. **The permanent fix is a `/var/tmp` symlink farm: fontconfig scans the FARM, so its marker
lands in the farm.** ~5 KB of links, so it **preserves the ENOSPC constraint** that forced #136's
change rather than reopening it.

```bash
FARM=/var/tmp/fonts-<session>
mkdir -p $FARM
for f in <repo>/knowledge/assets/fonts/_desktop/TTF/*.ttf; do ln -s "$f" "$FARM/$(basename $f)"; done
export FONTCONFIG_FILE=/var/tmp/fonts-<session>.conf
```
```xml
<?xml version="1.0"?>
<!DOCTYPE fontconfig SYSTEM "fonts.dtd">
<fontconfig>
  <cachedir>/var/tmp/fccache-<session></cachedir>   <!-- cache OUTSIDE the repo, declared FIRST -->
  <dir>/var/tmp/fonts-<session></dir>               <!-- the FARM, never the repo dir -->
  <include ignore_missing="yes">/etc/fonts/fonts.conf</include>   <!-- ⚠ REQUIRED, see below -->
  <match target="pattern">
    <test name="family"><string>Univers Next for HSBC</string></test>
    <edit name="family" mode="prepend" binding="strong"><string>HSBC_MtUnivers_Latin</string></edit>
  </match>
  <match target="pattern">
    <test name="family"><string>Univers Next HSBC</string></test>
    <edit name="family" mode="prepend" binding="strong"><string>HSBC_MtUnivers_Latin</string></edit>
  </match>
</fontconfig>
```

⚠ **THE `<include>` IS NOT OPTIONAL, AND ITS ABSENCE IS INVISIBLE.** `FONTCONFIG_FILE` *replaces* the
system config; without the include the conf exposes **10 faces, all HSBC** (measured; the box has 394).
Every font request then falls back to the only faces present, so **a page renders entirely in the HSBC
cut and looks correct even when its fallback is broken** — and any width-probe returns the same number
for a real face and a nonexistent one, which is how #138's first probe produced a green that could not
fail. **The runbook never recorded the conf BODY, only the env var — that gap is what let #136's
`<dir>` choice travel unexamined. The body is now here.**

★ **ASSERT WITH A CONTROL, NOT A BOOLEAN.** `document.fonts.check(...)` returned `true` in BOTH the
broken and the working configuration — it does not discriminate. Measure a canvas string in the target
face **and in two controls** (a real different face, and a face that does not exist); the target must
differ from both:

| probe | broken conf | working conf | reading |
|---|---|---|---|
| `HSBC_MtUnivers_Latin` | 345 | **347** | the real cut |
| `"Univers Next HSBC"` (type.css `--uf`) | 345 | **347** | alias resolves |
| `"Univers Next for HSBC"` (snippet `--font`) | 345 | **347** | alias resolves |
| `DejaVu Sans` — control | 345 | 375 | genuinely different face |
| nonexistent face — control | 345 | 301 | default fallback |

*(40px `Handgloves 12345`, `showroom/chart-bar.html`, `goto file://`, identical at 1180 **and** 480.)*
**Both aliases must land on the target number and NOT on the nonexistent-face number** — that is the
assertion that catches a silent fallback.

**AND ASSERT THE TREE, every render run:** `ls -a <TTF dir> | grep -c '^\.uuid'` → **0**, and
`git status --short --untracked-files=all -- knowledge/` → **0 lines**. Driven three ways #138:
**(A)** farm conf from a clean dir → **0** · **(B)** mutation, only `<dir>` swapped back to the repo →
**3** (so the test CAN fail) · **(C)** after cleanup → **0**.

⚠ **CLEANUP MUST BE A SAME-MOUNT `mv`.** `mv` to `/var/tmp` **fails** — different filesystem, so it
becomes copy+unlink and the unlink is denied (`Operation not permitted`). #138 hit this and briefly
left its own strays in the tree. Move within the repo mount (`_to_delete/…`), which is a rename.

⚠ **ENOSPC POTHOLE n=4 (#138):** `/sessions` was **100% full, 18 M free** at session open — the same
fixed-cutoff shape as #129/#136. `/` had 1.7 G. This is why the fix must not reintroduce a font copy.
⚙ **Chromium did NOT need downloading:** `/var/tmp/pw-browsers-{129,s131,s136}`, `/var/tmp/pylibs` and
`/var/tmp/chromelibs` all survived from prior sessions — `/var/tmp` persists and is shared. *(Three
344 M browser copies now sit there against 1.7 G free; not this lane's to prune, noted.)*
⬛ **UNPROVEN BY SCOPE, DECLARED:** #138 did not test the farm in a sandbox with **no** pre-staged
`/var/tmp` — steps 1–4 (download + libs) were not re-run, only re-used. *(Addition only; #129's and
#136's recipes stand as history. 2026-08-09.)*

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
