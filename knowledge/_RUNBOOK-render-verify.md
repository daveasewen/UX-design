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
</fontconfig>
EOF
fc-cache -f
```
The alias means repo CSS declaring `"Univers Next for HSBC"` renders in the licensed cut with **no
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

## Failure modes (dated, observed)

| Symptom | Reading | Move |
|---|---|---|
| Installer exits non-zero after download | Host-validation, EXPECTED (step 3) | Check the cache, proceed |
| `UNABLE_TO_GET_ISSUER_CERT_LOCALLY` | Proxy CA missing from Node | Step 2, both vars |
| Cache empty though install "ran" | ffmpeg TLS wipe (07-03) or inter-call wipe (07-18) | Re-run step 3; don't re-diagnose |
| Chrome vanishes mid-session | Cache wiped between calls (07-18) | Re-run step 3 |
| Full chrome SIGSEGV on launch | Lib set incomplete (06-29 arc) | Shell first; else the ~17-lib set (07-16) |
| `nohup` job dead next call | `--die-with-parent` | Chunk ≤45 s; poll within the call |
| Render fine but wrong font | Alias file missing / fc-cache stale | Step 5; assert `document.fonts.check` |

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
