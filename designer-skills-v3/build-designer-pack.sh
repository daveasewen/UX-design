#!/usr/bin/env bash
# build-designer-pack.sh — the v3 release build. Run from the repo root:
#
#     bash designer-skills-v3/build-designer-pack.sh --manifest --commit <sha>
#     bash designer-skills-v3/build-designer-pack.sh --dry-run --out-dir /var/tmp/x --commit <sha>
#     bash designer-skills-v3/build-designer-pack.sh --release --commit <sha>
#     bash designer-skills-v3/build-designer-pack.sh --check <zip> --commit <sha>
#     bash designer-skills-v3/build-designer-pack.sh --selftest
#
# ⛔ RELEASE IS DAVE'S WORD (s219-D4(2)). `--release` refuses unless the manifest carries his
# ratification. Until then the only bake this script will perform is `--dry-run`, into a
# throwaway directory, which never touches designer-skills-v3/ or dist/.
#
# WHAT IS DIFFERENT FROM v2 (designer-skills-v2/build-designer-kb.sh), and why:
#
#   v2 carried a hand-written copy-list of `cp` lines. Its own receipt records the cost: "v1's
#   copy-list had gone stale — never shipped canon/type.css nor tokens/themes/". A copy-list is
#   a claim about the tree that nothing re-measures. v3 has NO copy-list: the ship set is a
#   GENERATED manifest (knowledge/_release/_v3_manifest.json), and this script reads it.
#
#   v2 baked into designer-skills-v2/knowledge/ inside the repo, then zipped that. v3 bakes into
#   a STAGE and zips the stage — designer-skills-v3/ holds this script and (from R3) the skills,
#   and never holds a baked copy of the engine. One less thing that can go stale.
#
#   v2 stamped `$(date)` into the README. v3 stamps the COMMIT's date, because a build-day stamp
#   makes two bakes of the same commit differ, and a pack whose bytes move on their own cannot be
#   delta-audited. Same commit + same manifest ⇒ byte-identical zip, proven by --dry-run twice.
#
# WHAT v2 GOT RIGHT AND v3 KEEPS: the bake comes from a NAMED COMMIT via `git archive`, never
# from the working tree. The v2 receipt: "baked from HEAD 7071538 (build green 38/38), NOT the
# dirty working tree — the conductor's mid-flight edits are untouched and deliberately not
# captured." That discipline is the reason a release can be reasoned about at all.
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
GEN="$ROOT/knowledge/_release/_gen_v3_manifest.py"
MANIFEST="$ROOT/knowledge/_release/_v3_manifest.json"
VERSION="v3.0.0"
PACKNAME="Apollo-designer-skills-${VERSION}"
DIST="$ROOT/designer-skills-v3/dist"

MODE=""
COMMIT=""
OUTDIR=""
CHECK_ZIP=""
FULL_STAGE=""

die() { echo "REFUSED: $*" >&2; exit 2; }

while [ $# -gt 0 ]; do
  case "$1" in
    --manifest) MODE=manifest ;;
    --release)  MODE=release ;;
    --dry-run)  MODE=dryrun ;;
    --selftest) MODE=selftest ;;
    --check)    MODE=check; CHECK_ZIP="${2:-}"; shift ;;
    --commit)   COMMIT="${2:-}"; shift ;;
    --out-dir)  OUTDIR="${2:-}"; shift ;;
    --full-stage) FULL_STAGE="${2:-}"; shift ;;
    -h|--help)  sed -n '2,30p' "${BASH_SOURCE[0]}"; exit 0 ;;
    *) die "unknown argument '$1' (--help for the contract)" ;;
  esac
  shift
done

[ -n "$MODE" ] || die "name a mode: --manifest | --dry-run | --release | --check <zip> | --selftest"

# ---- the two refusals that are the whole discipline ------------------------------------------

require_commit() {
  [ -n "$COMMIT" ] || die "no --commit. A build from 'the tree' is a build from nothing you can
         name later, and a release you cannot name is a release you cannot audit (v2 receipt:
         baked from HEAD 7071538, NOT the dirty working tree)."
  git -C "$ROOT" rev-parse --verify --quiet "${COMMIT}^{commit}" >/dev/null \
    || die "'$COMMIT' is not a commit in this repo."
  COMMIT="$(git -C "$ROOT" rev-parse "$COMMIT")"
}

require_clean() {
  if [ -n "$(git -C "$ROOT" status --porcelain)" ]; then
    die "the working tree is dirty. A RELEASE is cut from a clean tree so that what is on
         GitHub and what is in the zip are the same thing — commit or stash first. (A --dry-run
         is allowed on a dirty tree: it reads the COMMIT, not the tree, and writes nothing the
         repo keeps.)"
  fi
}

ratified() {
  python3 - "$MANIFEST" <<'PY'
import json, sys
m = json.load(open(sys.argv[1]))
sys.exit(0 if str(m.get("status", "")).upper().startswith("RATIFIED") else 1)
PY
}

# ---- modes -----------------------------------------------------------------------------------

case "$MODE" in

selftest)
  echo "=== generator selftest ==="
  python3 "$GEN" --selftest
  echo
  echo "=== refusal: no --commit ==="
  if bash "${BASH_SOURCE[0]}" --dry-run --out-dir /var/tmp/nope 2>/dev/null; then
    echo "RED — a bake with no named commit was ALLOWED"; exit 1
  else
    echo "green — refused, as it must"
  fi
  echo
  echo "=== refusal: --release on a dirty tree ==="
  if [ -z "$(git -C "$ROOT" status --porcelain)" ]; then
    echo "SKIPPED — tree is clean, the dirty-tree arm cannot be driven honestly right now"
  elif bash "${BASH_SOURCE[0]}" --release --commit HEAD 2>/dev/null; then
    echo "RED — a release was cut from a dirty tree"; exit 1
  else
    echo "green — refused, as it must"
  fi
  echo
  echo "=== refusal: --release without Dave's ratification ==="
  if ratified; then
    echo "SKIPPED — the manifest is already ratified"
  else
    echo "green — manifest status is PROPOSED, so --release cannot run"
  fi
  ;;

manifest)
  require_commit
  echo "probing the gates at ${COMMIT:0:12} (measured, not read by eye)…"
  python3 "$GEN" --probe --commit "$COMMIT" ${FULL_STAGE:+--full-stage "$FULL_STAGE"}
  python3 "$GEN" --manifest --commit "$COMMIT"
  # Dave's go/no-go page rides with the manifest — the page is GENERATED from it, so the two
  # cannot drift apart and be believed separately.
  PAGE="$ROOT/reviews/RELEASE-V3-MANIFEST-$(git -C "$ROOT" show -s --format=%cs "$COMMIT")-v1.html"
  [ -f "$PAGE" ] || PAGE="$(ls -1 "$ROOT"/reviews/RELEASE-V3-MANIFEST-*-v*.html 2>/dev/null | tail -1)"
  [ -n "$PAGE" ] && python3 "$GEN" --page "$PAGE"
  echo "page: $PAGE"
  ;;

dryrun|release)
  require_commit
  [ -f "$MANIFEST" ] || die "no manifest at $MANIFEST — run --manifest first."
  MAN_COMMIT="$(python3 -c 'import json,sys;print(json.load(open(sys.argv[1]))["commit"])' "$MANIFEST")"
  [ "$MAN_COMMIT" = "$COMMIT" ] \
    || die "the manifest was generated at ${MAN_COMMIT:0:12}, you asked to bake ${COMMIT:0:12}.
         Re-run --manifest. (The manifest IS the ship list; baking a different commit against it
         is exactly the stale-copy-list defect v3 exists to end.)"

  if [ "$MODE" = release ]; then
    require_clean
    ratified || die "the manifest's status is not RATIFIED. s219-D4(2): the exact cut is a
         proposed manifest for Dave's eye BEFORE the bake — release is his word, not the
         script's. Show him reviews/RELEASE-V3-MANIFEST-*.html, then set the status."
    OUTDIR="$(mktemp -d "${TMPDIR:-/var/tmp}/apollo-v3-XXXXXX")"
    ZIP="$DIST/${PACKNAME}.zip"
  else
    [ -n "$OUTDIR" ] || die "--dry-run needs --out-dir <throwaway dir>"
    case "$OUTDIR" in
      "$ROOT"|"$ROOT"/designer-skills-v3*|"$ROOT"/dist*)
        die "--dry-run must not write inside designer-skills-v3/ or dist/ — those are the
         RELEASE surfaces and s219-D4(5) freezes them. Pick a throwaway under /var/tmp." ;;
    esac
    mkdir -p "$OUTDIR"
    ZIP="$OUTDIR/${PACKNAME}.zip"
    echo "*** DRY RUN — nothing here is a release. Output: $OUTDIR ***"
  fi

  STAGE="$OUTDIR/$PACKNAME"
  rm -rf "$STAGE"
  mkdir -p "$STAGE"

  echo "staging from commit ${COMMIT:0:12} via git archive…"
  python3 "$GEN" --stage "$STAGE" --commit "$COMMIT"

  # ---- provenance, stamped from the COMMIT (never from today) --------------------------------
  MAN_SHA="$(python3 -c 'import hashlib,sys;print(hashlib.sha256(open(sys.argv[1],"rb").read()).hexdigest())' "$MANIFEST")"
  COMMIT_DATE="$(git -C "$ROOT" show -s --format=%cI "$COMMIT")"
  N_FILES="$(python3 -c 'import json,sys;print(json.load(open(sys.argv[1]))["totals"]["files"])' "$MANIFEST")"

  cp "$MANIFEST" "$STAGE/_MANIFEST.json"

  cat > "$STAGE/PROVENANCE.json" <<JSON
{
  "pack": "$PACKNAME",
  "version": "$VERSION",
  "commit": "$COMMIT",
  "commit_date": "$COMMIT_DATE",
  "manifest_sha256": "$MAN_SHA",
  "files": $N_FILES,
  "ruling": "s219-D4",
  "reproducible": "same commit + same manifest produces a byte-identical zip"
}
JSON

  cat > "$STAGE/README.md" <<MD
# Apollo — designer pack $VERSION

The working Apollo engine, plus a clean cut of Memento. Not a demo and not a summary: these are
the same tokens, component contracts, reference markup, canon CSS, gates, runbooks and library
the design system itself runs on. Build with it and see where you get to.

## Provenance — what this pack was baked from

| | |
|---|---|
| version | \`$VERSION\` |
| commit | \`$COMMIT\` |
| commit date | \`$COMMIT_DATE\` |
| manifest sha256 | \`$MAN_SHA\` |
| files | $N_FILES |
| ruling | \`s219-D4\` |

Every file above came out of that commit via \`git archive\` — not out of anyone's working
directory. The ship list is \`_MANIFEST.json\`, which is generated, not hand-kept. Two builds of
the same commit against the same manifest produce a **byte-identical zip**, so any difference
between two packs is a real difference and can be audited.

## What is in here

- \`knowledge/tokens/\` — every design token, plus the four theme override sets.
- \`knowledge/components/\` — one contract per component: props, variants, token bindings,
  states, anti-patterns, accessibility.
- \`knowledge/snippets/\` — the reviewed reference markup. This is what "correct" looks like.
- \`knowledge/canon/\` — canon.css and type.css, the composition layer, and the generators that
  mint them from tokens.
- \`knowledge/compliance/\` — which WCAG criteria apply to which component, and the rule set.
- \`knowledge/_validate_*.py\` — the gates. Each one in this pack was **run** outside the source
  repo before it was included; the verdicts are in \`_MANIFEST.json\`.
- \`knowledge/_RUNBOOK-*.md\` — the procedures: compose from canon, take a component through its
  gates, render and verify, write a criteria contract, onboard an existing code library.
- \`showroom/\` — the live library, including the foundations pages.
- \`memento-package/\` — Memento's machinery. Machinery only: no chain, no record. Your project
  grows its own.

## What is deliberately NOT in here

Review files, session notes, run logs, client project work, and the licensed material we cannot
redistribute. \`_MANIFEST.json\` lists every exclusion with its reason.

## Gates that need something installed

A few gates drive a real browser and need \`playwright\`. They are included and they name their
own dependency when you run them without it — see \`_MANIFEST.json\` for which ones.
MD

  echo "zipping (deterministic: fixed mtimes from the commit, sorted order)…"
  python3 "$GEN" --zip "$STAGE" --out "$ZIP" --commit "$COMMIT"
  echo
  ZSHA="$(python3 -c 'import hashlib,sys;print(hashlib.sha256(open(sys.argv[1],"rb").read()).hexdigest())' "$ZIP")"
  ZBYTES="$(wc -c < "$ZIP" | tr -d ' ')"
  echo "pack:  $ZIP"
  echo "sha256: $ZSHA"
  echo "size:  $(du -h "$ZIP" | cut -f1)"

  # Fold the measured download size and fingerprint back into Dave's page. The page must not
  # claim a zip size it never saw — the only honest source for it is a bake that actually ran.
  PAGE="$(ls -1 "$ROOT"/reviews/RELEASE-V3-MANIFEST-*-v*.html 2>/dev/null | tail -1)"
  if [ -n "$PAGE" ]; then
    python3 "$GEN" --page "$PAGE" --zip-bytes "$ZBYTES" --zip-sha "$ZSHA"
  fi
  ;;

check)
  require_commit
  [ -n "$CHECK_ZIP" ] || die "--check needs a zip path"
  python3 "$GEN" --check "$CHECK_ZIP" --commit "$COMMIT"
  ;;

esac
