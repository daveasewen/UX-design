---
name: sandbox-html-rendering
description: "Working recipe to render a snippet's HTML (container queries + JS) to PNG in the Linux sandbox for visual verification"
metadata: 
  node_type: memory
  type: reference
  originSessionId: 452a0a17-6e63-4feb-ad8c-b23dfebbbd1b
---

We CAN render reference snippets / fitness-tests to real screenshots in the sandbox (headless Chromium via Playwright) — useful for verifying card-collapse, container queries, JS state, dark mode before Dave reviews. Non-obvious setup gotchas (all without root):

1. `pip install playwright --break-system-packages`
2. Browser download fails TLS (`UNABLE_TO_GET_ISSUER_CERT_LOCALLY`) — the egress proxy's CA isn't in Node's bundle. Fix: `export NODE_EXTRA_CA_CERTS=/etc/ssl/certs/ca-certificates.crt` then `python3 -m playwright install chromium`.
3. Chromium misses one system lib `libXdamage.so.1` and there's no sudo. Fix: `apt-get download libxdamage1` (works without root) → `dpkg-deb -x` → add the extracted dir to `LD_LIBRARY_PATH`.
4. Playwright's preflight still hard-fails on the lib check → `export PLAYWRIGHT_SKIP_VALIDATE_HOST_REQUIREMENTS=1`, and launch with `args=["--no-sandbox","--disable-dev-shm-usage","--disable-gpu"]`.
5. To trigger a `@container` collapse, set the page `viewport` narrow (the `.wrap` is capped at 100%); no need to drive the demo slider.

CAVEAT: the sandbox has NO Univers Next for HSBC font (renders fall back to Liberation/DejaVu), so screenshots verify LAYOUT/structure, not the real HSBC type. The font lives on HSBC's "Create" brand portal (create.hsbc) which is SSO login-gated — NOT fetchable from the sandbox; don't retry. For real-font renders, Dave must drop the licensed font files into the project (e.g. knowledge/assets/fonts/). See [[component-review-program]].

UPDATE 2026-06-29 — render may be BLOCKED in a fresh sandbox (it was this session): (a) Playwright now ships chromium as a separate `chromium_headless_shell`; the default `p.chromium.launch()` looks for headless_shell which `install chromium` does NOT place → pass `executable_path=<~/.cache/ms-playwright/chromium-*/chrome-linux/chrome>`. (b) The CA fix alone was insufficient for the download; also needed `export NODE_TLS_REJECT_UNAUTHORIZED=0`. (c) The full chrome (v149, arm64) SEGFAULTS on launch (even `--version`) — it needs more system libs than libXdamage, and `playwright install-deps` requires root (no sudo → "no new privileges"), so the libs can't be installed. Net: a one-off visual self-render was NOT possible; fell back to Dave reviewing the HTML in his own browser (his preferred surface anyway). If this recurs, do NOT repeat the full yak-shave — get the libs baked into the image or render on the agency machine. The recipe below still holds wherever chrome CAN actually run.

**UPDATE 2026-07-01 — WORKING RENDER LOOP (use this; stop fighting the sandbox).** Sandbox chromium STILL segfaults (even `--version`, exit 139) — confirmed again, don't retry. The path that WORKS is rendering in **Dave's own Chrome via the Claude-in-Chrome MCP** + a tiny local server:
1. Dave runs, on his Mac, from the project root: `python3 -m http.server 8000` (leave running).
2. Load the chrome tools (ToolSearch `select:mcp__claude-in-chrome__list_connected_browsers,...navigate,...computer`). `list_connected_browsers` shows his Mac (isLocal).
3. `navigate` to **`http://localhost:8000/<relative/path.html>`** then `computer{action:screenshot}` → I SEE it (real fonts, real render) and can critique + tidy.
GOTCHAS: (a) **`file://` is blocked** — the navigate tool prepends `https://` to it → error page. MUST use `http://localhost`. (b) **Chrome caches** — after an Edit, a plain re-navigate serves the OLD file; **cache-bust with `?v=N`** in the URL. (d) **`python3 -m http.server` is SINGLE-THREADED and DEADLOCKS** (browser keep-alive on the HTML holds the one thread while it needs a 2nd connection for canon.css → page never reaches document_idle → screenshot/scroll error "Page still loading"). Use a THREADING server instead: `python3 -c "import http.server,socketserver; socketserver.ThreadingTCPServer.allow_reuse_address=True; socketserver.ThreadingTCPServer(('',8000),http.server.SimpleHTTPRequestHandler).serve_forever()"`. (c) closes the render→critique→fix→re-render loop end-to-end (proved on sme-payments-final.html: tightened `--s7`→`--s6` spacing + bumped stat weight 200→300, confirmed against the render). Every session: ask Dave to start the server, then self-check before presenting.

**UPDATE 2026-07-03 — IN-SANDBOX RENDER WORKS AGAIN (headless SHELL, not full chrome).** The
07-01 "stop fighting the sandbox" verdict applied to FULL chrome (still assume segfault). The
**headless shell** runs fine: `NODE_EXTRA_CA_CERTS=/etc/ssl/certs/ca-certificates.crt python3 -m
playwright install chromium-headless-shell` (this exact target! `install chromium --only-shell`
also pulls ffmpeg, whose TLS failure makes the installer DELETE the whole ms-playwright cache —
including the shell that already worked) + libXdamage to `~/.local/chromelibs` + both env vars +
default `launch()` (pw 1.61 picks the shell). Full 38-snippet state-contrast sweep + review-page
renders all ran in-sandbox. NEW gotcha: **background processes now DIE when the bash call ends**
(bwrap --die-with-parent) — nohup is silent death; CHUNK long jobs into ≤45 s calls. Claude-in-
Chrome loop (above) still the route for REAL-FONT renders.

**UPDATE 2026-07-16 — FULL CHROME RENDERS IN-SANDBOX (supersedes the "segfault, give up" verdict) — CONFIRMED WORKING, no root.** Fresh cloud sandbox (arm64, uid≠0, sudo blocked by "no new privileges"). Full v149 chrome rendered a Swiss dossier to PNG fine once ENOUGH libs were present (not just libXdamage). The confirmed recipe:
1. `pip3 install playwright --break-system-packages`
2. **TLS trick (the important one):** `export NODE_TLS_REJECT_UNAUTHORIZED=0` THEN `python3 -m playwright install chromium`. Today `NODE_EXTRA_CA_CERTS=/etc/ssl/certs/ca-certificates.crt` was NOT enough — the reject-unauthorized flag was what let the download succeed (falls back to the `playwright.download.prss.microsoft.com` mirror; the `cdn.playwright.dev` host may DNS-fail with EAI_AGAIN, that's fine).
3. **Libs without root** — chrome needs ~18 shared libs. In a scratch dir: `apt-get download libxdamage1 libxcomposite1 libxrandr2 libgbm1 libxkbcommon0 libasound2 libnss3 libnspr4 libatk1.0-0 libatk-bridge2.0-0 libcups2 libdrm2 libxfixes3 libxrender1 libxext6 libxcb1 libxi6` (works non-root, no `apt-get update` needed) → `for d in *.deb; do dpkg -x "$d" root/; done` → `export LD_LIBRARY_PATH=$PWD/root/usr/lib/aarch64-linux-gnu:$LD_LIBRARY_PATH`.
4. Launch with `executable_path=~/.cache/ms-playwright/chromium-1228/chrome-linux/chrome`, `headless=True`, `args=["--no-sandbox","--disable-dev-shm-usage","--disable-gpu"]`. (Default `launch()` wants `chromium_headless_shell` which may still be downloading — pass the full-chrome path explicitly.)
5. Background downloads DIE when the bash call ends AND each call caps at 45 s — run `nohup … &` then poll with a follow-up `sleep 40; tail` call.
6. To view a PNG: file tools can't reach `/tmp` — `cp` it into the outputs mount (`/sessions/<s>/mnt/outputs/`) then Read that path.
This is Dave's explicitly-requested "TLS CA trick" home. Still no Univers font (layout-only). Claude-in-Chrome loop = the route for REAL-FONT renders.

**UPDATE 2026-07-17 — the full-chrome recipe worked AGAIN, first try.** Confirmed the 07-16 recipe end-to-end: `pip install playwright --break-system-packages`; `NODE_TLS_REJECT_UNAUTHORIZED=0 python3 -m playwright install chromium` (download ~187MB — run it in a FOREGROUND bash call with the default 45s not enough? it finished ~2 min so it ran across one long call; background `nohup` DIES with the parent, don't bother); `apt-get download` the ~17 libs → `dpkg -x` → `LD_LIBRARY_PATH=…/root/usr/lib/aarch64-linux-gnu`; then `PLAYWRIGHT_SKIP_VALIDATE_HOST_REQUIREMENTS=1` + launch with `executable_path=~/.cache/ms-playwright/chromium-1228/chrome-linux/chrome, headless=True, args=["--no-sandbox","--disable-dev-shm-usage","--disable-gpu"]`. Rendered the grid-retrofit review sheet + Tranche-2 + Account-card to PNG, `cp` into outputs mount, Read = saw them. Layout-only (still no Univers). Used it to visually verify the retrofit didn't distort icons. NOTE: `render.py` glob must cover `~/.cache/ms-playwright/` (not `.local/share`).

GIT COMMITS FROM SANDBOX (2026-06-22): commits CAN work IF you pass an inline identity (`git -c user.name=.. -c user.email=..`, reuse the repo's existing author via `git log -1 --format='%an'/'%ae'`) — the bare commit fails with "unable to auto-detect email". BUT every `git add`/commit leaves a 0-byte `.git/index.lock` the sandbox CANNOT delete (`rm` → "Operation not permitted"; the `.git` mount blocks unlink). A commit succeeds only when NO lock pre-exists; the leftover then BLOCKS the next commit ("Another git process is running"). Only Dave can clear it (`rm -f .git/index.lock` on his Mac). Net: UNRELIABLE even after Dave clears the lock — the commit's OWN index.lock cleanup hits the unlink block intermittently (a few landed this session, others bounced even commit-only with the lock pre-cleared). DEFAULT to handing Dave ONE paste-ready commit to run on his Mac; do NOT keep bouncing "clear the lock → go" at him (it's his workflow anyway — see [[workflow-commit-summaries]]).
