---
name: chromium-in-sandbox-recipe
description: "How to get a real Chromium running in the Cowork Linux sandbox (arm64, no root) so _drive_chart_engine.py and other browser-driven gates can run — playwright + one extracted lib"
metadata: 
  node_type: memory
  type: reference
  originSessionId: b85cd634-cc72-496f-ab06-959bc56ae8e4
  modified: 2026-09-09T17:58:13.473Z
sources: [cowork-import]
imported_at: 2026-09-16T03:14:10Z
---

Proven at #263 (2026-09-09). The sandbox is aarch64, no sudo, `playwright install-deps` fails. Only ONE library is missing:

```
pip install playwright --break-system-packages
python3 -m playwright install chromium
apt-get download libxdamage1 && dpkg-deb -x libxdamage1_*.deb ~/.local/xd
cp ~/.local/xd/usr/lib/aarch64-linux-gnu/libXdamage.so.1* ~/.local/lib/
export LD_LIBRARY_PATH=$HOME/.local/lib
python3 knowledge/_drive_chart_engine.py      # Chromium 151, 27 pages × 8 combos, ~2 min
```

`ldd ~/.cache/ms-playwright/chromium_headless_shell-*/chrome-linux/headless_shell | grep "not found"` is the check.

#289 (2026-09-20) amendment, measured: `playwright install chromium` failed with `UNABLE_TO_GET_ISSUER_CERT_LOCALLY`; `export NODE_EXTRA_CA_CERTS=/etc/ssl/certs/ca-certificates.crt` first, and install `chromium-headless-shell` (the binary now lives at `chromium_headless_shell-*/chrome-headless-shell-linux-arm64/chrome-headless-shell`, so the ldd glob above needs that path). `LD_LIBRARY_PATH` must be exported in EVERY bash call — each call is a fresh shell. The sandbox is rebuilt between sessions, so this is re-done each time it is needed (cheap: <2 min). `_probe_fail_open.py --expect red` (lane D3's driven aria probe) also becomes runnable.

**Why it matters:** "no browser here" was the standing reason driven receipts went stale and gates were argued from CSS instead of driven ([[mutation-tests-the-clause-not-the-feature]]). It is no longer a valid refusal. See [[eleven-defaults-ruled-tenth-release-gate-263]].


