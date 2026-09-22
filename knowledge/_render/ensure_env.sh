#!/usr/bin/env bash
# knowledge/_render/ensure_env.sh — BUILD (or repair) the DURABLE, seat-free half of the render env
# on the mount, so `seat_env.sh` finds it at every seat. #296 (2026-09-22), on Dave's "can we
# permanently fix this?" after a session rendered in the cloud because `outputs/_render-env-229`
# had vanished from the mount.
#
# WHAT LIVES WHERE
#   <repo>/outputs/_render-env/            ← durable, gitignored, on Dave's disk, survives the VM
#     pw-browsers/chromium_headless_shell-*/  the aarch64 headless shell (Playwright CDN, ~340 MB)
#     pylibs/                                playwright + greenlet + pyee (pip --target, ~40 MB)
#     chromelibs/usr/lib/aarch64-linux-gnu/  system libs the shell needs that the VM lacks (dpkg -x)
#   $TMPDIR/render-<seat>/                 ← seat-bound half (fonts.conf, farm, fccache): seat_env.sh
#                                            GENERATES it every call. Never stored. (#238 class fix.)
#
# IDEMPOTENT: every step is skipped when its assertion already passes. Safe to run at every boot.
# USAGE (one bash call; network needed only on first build):
#   bash knowledge/_render/ensure_env.sh [<envdir>]     # default <repo>/outputs/_render-env
#   source knowledge/_render/seat_env.sh                 # then, in the render call
# Prints `ENSURE_ENV: OK ...` or `ENSURE_ENV: FAIL <which>` (exit 1). Never a launch attempt.
set -u
here="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd -P)"
repo="$(cd "$here/../.." && pwd -P)"
envdir="${1:-$repo/outputs/_render-env}"
fail() { echo "ENSURE_ENV: FAIL $*" >&2; exit 1; }
mkdir -p "$envdir" || fail "cannot mkdir $envdir"

export TMPDIR="${TMPDIR:-/dev/shm}"
export NODE_EXTRA_CA_CERTS=/etc/ssl/certs/ca-certificates.crt   # #228: the CDN needs the system CA
export PLAYWRIGHT_BROWSERS_PATH="$envdir/pw-browsers"
export PLAYWRIGHT_SKIP_VALIDATE_HOST_REQUIREMENTS=1

# 1 · pylibs — playwright importable from the mount, no per-session pip.
if ! PYTHONPATH="$envdir/pylibs" python3 -S -c 'import playwright, greenlet, pyee' 2>/dev/null; then
  echo "ENSURE_ENV: installing playwright into $envdir/pylibs"
  pip install --no-cache-dir --quiet --target "$envdir/pylibs" playwright || fail "pip playwright"
  PYTHONPATH="$envdir/pylibs" python3 -S -c 'import playwright, greenlet, pyee' || fail "playwright still does not import"
fi
export PYTHONPATH="$envdir/pylibs${PYTHONPATH:+:$PYTHONPATH}"

# 2 · the headless shell — downloaded ONCE to the mount.
shell="$(ls -d "$envdir"/pw-browsers/chromium_headless_shell-*/chrome-linux/headless_shell "$envdir"/pw-browsers/chromium_headless_shell-*/chrome-headless-shell-linux-*/chrome-headless-shell 2>/dev/null | head -1)"
if [ ! -x "${shell:-/nonexistent}" ]; then
  echo "ENSURE_ENV: downloading chromium-headless-shell to $envdir/pw-browsers"
  python3 -m playwright install chromium-headless-shell >/dev/null 2>&1 || true   # host-req exit is EXPECTED
  shell="$(ls -d "$envdir"/pw-browsers/chromium_headless_shell-*/chrome-linux/headless_shell "$envdir"/pw-browsers/chromium_headless_shell-*/chrome-headless-shell-linux-*/chrome-headless-shell 2>/dev/null | head -1)"
  [ -x "${shell:-/nonexistent}" ] || fail "headless_shell absent after install (CDN/TLS? see runbook)"
fi

# 3 · chromelibs — every lib `ldd` cannot find, fetched by apt-get download + dpkg -x (no root needed).
libdir="$envdir/chromelibs/usr/lib/aarch64-linux-gnu"; mkdir -p "$libdir"
missing() { LD_LIBRARY_PATH="$libdir" ldd "$shell" 2>/dev/null | awk '/not found/{print $1}'; }
if [ -n "$(missing)" ]; then
  echo "ENSURE_ENV: fetching missing libs: $(missing | tr '\n' ' ')"
  ( cd "$TMPDIR" && for so in $(missing); do
      pkg="$(printf '%s' "$so" | sed -E 's/\.so\.([0-9]+).*$/\1/; s/^lib//' | tr 'A-Z' 'a-z')"
      pkg="lib$pkg"
      apt-get download "$pkg" >/dev/null 2>&1 || echo "ENSURE_ENV: could not download $pkg for $so" >&2
    done
    for deb in ./*.deb; do [ -f "$deb" ] && dpkg -x "$deb" "$envdir/chromelibs"; done; rm -f ./*.deb ) 
fi
n="$(missing | wc -l | tr -d ' ')"
[ "$n" = "0" ] || { missing >&2; fail "ldd: $n lib(s) still not found — add them to chromelibs by hand (runbook)"; }

# 4 · the durable half must not have a seat baked into it (the #237/#238 class): assert no /sessions/ path.
if grep -rIl --exclude-dir=pw-browsers --exclude-dir=pylibs --exclude-dir=chromelibs '/sessions/' "$envdir" 2>/dev/null | grep -q .; then
  fail "a file under $envdir bakes a /sessions/<seat> path — the seat-bound half must live in \$TMPDIR"
fi

echo "ENSURE_ENV: OK envdir=$envdir shell=$shell pylibs=$(ls "$envdir/pylibs" | wc -l | tr -d ' ') libs=$(ls -A "$libdir" | wc -l | tr -d ' ') size=$(du -sh "$envdir" | cut -f1)"
