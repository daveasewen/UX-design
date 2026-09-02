#!/usr/bin/env bash
# knowledge/_render/seat_env.sh — the PER-SEAT render environment, GENERATED at run time, never stored.
#
# WHY (#238 lane M, `_RUNBOOK-render-verify.md` EIGHTH STRATUM): three strata in a row died of one
# class — a STORED artefact whose absolute path resolves to nothing at the seat that reads it:
#   1. #219 fifth stratum: a lib dir that still EXISTS but is HOLLOW (`ls -A` empty) → "recipe broken".
#   2. #237 lane T finding 11: `outputs/_render-env-229/fonts.conf` hardcodes ANOTHER seat's mount
#      (`/sessions/determined-affectionate-euler/...`) in <cachedir> and <dir> → resolves to nothing here.
#   3. #238 lane M: the same env's font FARM is symlinks with ABSOLUTE foreign-seat targets — at this seat
#      `ls` shows 10 links and `-e` resolves 0 of them → fontconfig sees 0 HSBC faces → SILENT fallback.
# The seat name is in the path (`/sessions/<seat>/mnt/...`) and it changes every session, so anything
# that bakes it in is dead on arrival at the next seat. The fix is the CLASS fix: derive every path from
# THIS seat, write the seat-bound half (fonts.conf, farm, fccache) to $TMPDIR, and ASSERT each path
# RESOLVES before any launch. Only the seat-free half (pylibs, pw-browsers, chromelibs) is reused from
# the mount, and each of those is asserted too.
#
# USAGE — in the SAME bash call as the render (nothing survives a call boundary; /dev/shm is per-call):
#   source knowledge/_render/seat_env.sh [<durable env dir>]      # default: <repo>/outputs/_render-env-229
#   python3 <driver.py> ...                                        # same call
# Prints `SEAT_ENV: OK seat=<seat> ...` and exports PYTHONPATH PLAYWRIGHT_BROWSERS_PATH LD_LIBRARY_PATH
# FONTCONFIG_FILE TMPDIR RENDER_SHELL RENDER_SEAT. On any failed assertion prints `SEAT_ENV: FAIL <which>`
# and returns 1 — the FIRST probe is never a launch attempt (fifth stratum: ls, then ldd, never launch).
#
# Must be SOURCED (it exports); running it as a child would export into a process that then exits.

_se_fail() { echo "SEAT_ENV: FAIL $*" >&2; return 1; }

_se_main() {
  local here repo seat envdir libdir shell ttf farm conf n ok faces total
  here="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd -P)"
  repo="$(cd "$here/../.." && pwd -P)"
  # seat = the third path segment of the repo mount (/sessions/<seat>/mnt/UX-design); HOME as fallback.
  seat="$(printf '%s' "$repo" | awk -F/ '$2=="sessions"{print $3}')"
  [ -n "$seat" ] || seat="$(basename "${HOME:-unknown}")"

  envdir="${1:-$repo/outputs/_render-env-229}"
  [ -d "$envdir" ] || { _se_fail "envdir absent: $envdir"; return 1; }

  # --- seat-free half, reused from the mount, each ASSERTED (never trusted by name) ---------------
  libdir="$envdir/chromelibs/usr/lib/aarch64-linux-gnu"
  [ -d "$libdir" ] && [ -n "$(ls -A "$libdir" 2>/dev/null)" ] \
    || { _se_fail "lib dir hollow or absent: $libdir (fifth-stratum shape)"; return 1; }

  shell="$(ls -d "$envdir"/pw-browsers/chromium_headless_shell-*/chrome-linux/headless_shell 2>/dev/null | head -1)"
  [ -x "$shell" ] || { _se_fail "headless_shell not found under $envdir/pw-browsers"; return 1; }

  n="$(LD_LIBRARY_PATH="$libdir" ldd "$shell" 2>/dev/null | grep -c 'not found')"
  [ "$n" = "0" ] || { LD_LIBRARY_PATH="$libdir" ldd "$shell" | grep 'not found' >&2; _se_fail "ldd: $n lib(s) not found"; return 1; }

  PYTHONPATH="$envdir/pylibs${PYTHONPATH:+:$PYTHONPATH}" python3 -c 'import playwright, greenlet, pyee' 2>/dev/null \
    || { _se_fail "playwright does not import from $envdir/pylibs"; return 1; }

  # --- seat-bound half, GENERATED here, never read from the mount -----------------------------------
  export TMPDIR="${TMPDIR:-/dev/shm}"
  [ -d "$TMPDIR" ] && [ -w "$TMPDIR" ] || { _se_fail "TMPDIR not writable: $TMPDIR"; return 1; }
  local seatdir="$TMPDIR/render-$seat"
  farm="$seatdir/fonts"; conf="$seatdir/fonts.conf"
  mkdir -p "$farm" "$seatdir/fccache" || { _se_fail "mkdir under $TMPDIR"; return 1; }

  ttf="$repo/knowledge/assets/fonts/_desktop/TTF"
  [ -d "$ttf" ] || { _se_fail "TTF dir absent: $ttf"; return 1; }
  ok=0; n=0
  for f in "$ttf"/*.ttf; do
    n=$((n+1)); ln -sfn "$f" "$farm/$(basename "$f")"; [ -e "$farm/$(basename "$f")" ] && ok=$((ok+1))
  done
  [ "$n" -gt 0 ] && [ "$ok" = "$n" ] || { _se_fail "farm links resolve $ok/$n (a dangling farm is the #238 third cause)"; return 1; }

  # #138 body: cachedir FIRST (outside the repo), the FARM (never the repo dir), the include (never optional).
  cat > "$conf" <<EOF
<?xml version="1.0"?>
<!DOCTYPE fontconfig SYSTEM "fonts.dtd">
<fontconfig>
  <cachedir>$seatdir/fccache</cachedir>
  <dir>$farm</dir>
  <include ignore_missing="yes">/etc/fonts/fonts.conf</include>
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

  export FONTCONFIG_FILE="$conf"
  fc-cache -f "$farm" >/dev/null 2>&1 || true
  # count FULL patterns (one per file): `fc-list : family` DEDUPES identical family strings (10 files → 6 lines).
  faces="$(fc-list | grep -c 'HSBC_MtUnivers_Latin')"
  total="$(fc-list | wc -l | tr -d ' ')"
  [ "$faces" -ge 10 ] || { _se_fail "fontconfig sees $faces HSBC faces (want >=10): conf=$conf"; return 1; }
  [ "$total" -gt "$faces" ] || { _se_fail "fontconfig sees ONLY the farm ($total faces) — the <include> is not resolving (#138 shape)"; return 1; }

  # --- the exports (all ride in this call; launch() must NOT pass env=) ---------------------------
  export PYTHONPATH="$envdir/pylibs${PYTHONPATH:+:$PYTHONPATH}"
  export PLAYWRIGHT_BROWSERS_PATH="$envdir/pw-browsers"
  export LD_LIBRARY_PATH="$libdir${LD_LIBRARY_PATH:+:$LD_LIBRARY_PATH}"
  export PLAYWRIGHT_SKIP_VALIDATE_HOST_REQUIREMENTS=1
  export RENDER_SHELL="$shell" RENDER_SEAT="$seat" RENDER_REPO="$repo"
  echo "SEAT_ENV: OK seat=$seat shell=$shell faces=$faces/$total farm=$ok/$n libs=$(ls -A "$libdir" | wc -l | tr -d ' ') conf=$conf"
}

_se_main "$@"
