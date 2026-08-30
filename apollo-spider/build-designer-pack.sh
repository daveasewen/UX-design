#!/usr/bin/env bash
# build-designer-pack.sh — the Apollo — Spider release build. Run from the repo root:
#
#     bash apollo-spider/build-designer-pack.sh --manifest --commit <sha>
#     bash apollo-spider/build-designer-pack.sh --dry-run --out-dir /var/tmp/x --commit <sha>
#     bash apollo-spider/build-designer-pack.sh --release --commit <sha>
#     bash apollo-spider/build-designer-pack.sh --check <zip> --commit <sha>
#     bash apollo-spider/build-designer-pack.sh --selftest
#
# ⛔ RELEASE IS DAVE'S WORD (s219-D4(2)). `--release` refuses unless the manifest carries his
# ratification. Until then the only bake this script will perform is `--dry-run`, into a
# throwaway directory, which never touches apollo-spider/ or dist/.
#
# WHAT IS DIFFERENT FROM v2 (designer-skills-v2/build-designer-kb.sh), and why:
#
#   v2 carried a hand-written copy-list of `cp` lines. Its own receipt records the cost: "v1's
#   copy-list had gone stale — never shipped canon/type.css nor tokens/themes/". A copy-list is
#   a claim about the tree that nothing re-measures. Spider has NO copy-list: the ship set is a
#   GENERATED manifest (knowledge/_release/_pack_manifest.json), and this script reads it.
#
#   v2 baked into designer-skills-v2/knowledge/ inside the repo, then zipped that. Spider bakes into
#   a STAGE and zips the stage — apollo-spider/ holds this script and (from R3) the skills,
#   and never holds a baked copy of the engine. One less thing that can go stale.
#
#   v2 stamped `$(date)` into the README. Spider stamps the COMMIT's date, because a build-day stamp
#   makes two bakes of the same commit differ, and a pack whose bytes move on their own cannot be
#   delta-audited. Same commit + same manifest ⇒ byte-identical zip, proven by --dry-run twice.
#
# WHAT v2 GOT RIGHT AND SPIDER KEEPS: the bake comes from a NAMED COMMIT via `git archive`, never
# from the working tree. The v2 receipt: "baked from HEAD 7071538 (build green 38/38), NOT the
# dirty working tree — the conductor's mid-flight edits are untouched and deliberately not
# captured." That discipline is the reason a release can be reasoned about at all.
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
GEN="$ROOT/knowledge/_release/_gen_pack_manifest.py"
MANIFEST="$ROOT/knowledge/_release/_pack_manifest.json"
VERSION="v1.0.3"
PACKNAME="Apollo-Spider-${VERSION}"
DIST="$ROOT/apollo-spider/dist"

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
  PAGE="$ROOT/reviews/RELEASE-SPIDER-$(git -C "$ROOT" show -s --format=%cs "$COMMIT")-v1.html"
  [ -f "$PAGE" ] || PAGE="$(ls -1 "$ROOT"/reviews/RELEASE-SPIDER-*-v*.html 2>/dev/null | tail -1)"
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
         is exactly the stale-copy-list defect this release shape exists to end.)"

  if [ "$MODE" = release ]; then
    require_clean
    ratified || die "the manifest's status is not RATIFIED. s219-D4(2): the exact cut is a
         proposed manifest for Dave's eye BEFORE the bake — release is his word, not the
         script's. Show him reviews/RELEASE-SPIDER-*.html, then set the status."
    OUTDIR="$(mktemp -d "${TMPDIR:-/var/tmp}/apollo-spider-XXXXXX")"
    ZIP="$DIST/${PACKNAME}.zip"
  else
    [ -n "$OUTDIR" ] || die "--dry-run needs --out-dir <throwaway dir>"
    case "$OUTDIR" in
      "$ROOT"|"$ROOT"/apollo-spider*|"$ROOT"/dist*)
        die "--dry-run must not write inside apollo-spider/ or dist/ — those are the
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
  COMMIT_DATE="$(git -C "$ROOT" show -s --format=%cI "$COMMIT")"
  N_FILES="$(python3 -c 'import json,sys;print(json.load(open(sys.argv[1]))["totals"]["files"])' "$MANIFEST")"
  # ⛔ #220. The Gumdrop cut's version was TYPED here three times (PROVENANCE.json, the README
  # provenance table, the memento-package bullet) while its one home is the generator's
  # MEMENTO_CUT_VERSION. At the v1.0.1 bump all three would have shipped "v1.0.0" inside a pack
  # whose manifest said v1.0.1 — a pack that disagrees with itself about what it carries. It is
  # now READ from the manifest the generator wrote (ADR-0017, one home). A missing key dies loud
  # under `set -e` rather than defaulting to a version nobody chose.
  MEM_NAME="$(python3 -c 'import json,sys;print(json.load(open(sys.argv[1]))["carries"]["name"])' "$MANIFEST")"
  MEM_VERSION="$(python3 -c 'import json,sys;print(json.load(open(sys.argv[1]))["carries"]["version"])' "$MANIFEST")"
  MEM_WHAT_JSON="$(python3 -c 'import json,sys;print(json.dumps(json.load(open(sys.argv[1]))["carries"]["what"], ensure_ascii=False))' "$MANIFEST")"

  # ---- s225-D3 — THE CARRIED CUT'S VERSION IS STAMPED INTO THE STAGE, NEVER TYPED IN IT -------
  #
  # ⛔ WHAT #224 SHIPPED. Three `Memento — Gumdrop v1.0.0` literals rode inside the v1.0.2 pack
  # — two runbook headers and `memento-package/_state.json`'s `built_by` — beside a README that
  # said v1.0.2, because those three were hand-typed inside the cut while the README's copy was
  # already read from the manifest. Arm 5 of `_gate_pack_docs.py` caught it at #225; Dave ruled:
  # *"we are at 1.03"* — the Gumdrop cut versions WITH the pack, one version story, and EVERY
  # Gumdrop version literal derives from `carries.version`. This block is that derivation.
  #
  # WHY HERE AND IN THIS SHAPE. It is the same move the block above already makes for the README
  # and PROVENANCE — "It is now READ from the manifest the generator wrote (ADR-0017, one home).
  # A missing key dies loud under `set -e` rather than defaulting to a version nobody chose." The
  # only difference is that those two files are WRITTEN by this script, and these three come out
  # of the commit via `git archive`, so the derivation has to be a rewrite over the stage.
  #
  # ⛔ DETERMINISM IS INTACT, AND SO IS THE HEADER'S RULE. The replacement value comes from the
  # COMMITTED manifest, never from today — same commit + same manifest still produces a
  # byte-identical zip, and the stamp is IDEMPOTENT. It is also byte-NEUTRAL whenever the repo is
  # in sync, which is what keeps `--check`'s blob-fidelity arm green: that arm compares every
  # shipped path to the commit's blob, and only files the stamp actually MOVES can disagree with
  # it. So a moved byte is not silent — each one prints a DRIFT line naming the file, both
  # versions, and the consequence. Fix the drift at its source (the repo copy), do not tolerate
  # the line.
  #
  # SCOPE IS THE PRESENCE, NOT THE THREE KNOWN FILES [[gate-inside-the-growth-loop]]: the sweep
  # reads every staged text file, so a Gumdrop literal typed into a NEW document tomorrow is
  # derived too rather than becoming the fourth instance of #224. `_state.json` is JSON and
  # carries no comment marker of its own — the two runbook headers carry one, this block is the
  # address for all three, and the stamped JSON is re-parsed here so a broken stamp dies loud.
  python3 - "$STAGE" "$MEM_VERSION" <<'PY'
import json, os, re, sys
stage, want = sys.argv[1], sys.argv[2]
# The same spelling family arm 5 of _gate_pack_docs.py sweeps (GUMDROP_RE): em dash, en dash or
# hyphen, so a stamp can never be narrower than the gate that grades it.
RE = re.compile(r"(Memento\s*[—–\-]\s*Gumdrop\s+v)(\d+\.\d+\.\d+)")
carry, moved = 0, []
for root, dirs, files in os.walk(stage):
    dirs.sort()
    for name in sorted(files):
        p = os.path.join(root, name)
        try:
            src = open(p, encoding="utf-8").read()
        except (UnicodeDecodeError, OSError):
            continue                       # binary (the vendored encoder blob) — nothing to stamp
        if "Gumdrop" not in src:
            continue
        out, k = RE.subn(lambda m: m.group(1) + want.lstrip("v"), src)
        if not k:
            continue
        carry += 1
        rel = os.path.relpath(p, stage)
        if out != src:
            was = sorted({"v" + m.group(2) for m in RE.finditer(src)})
            open(p, "w", encoding="utf-8").write(out)
            moved.append((rel, ", ".join(was)))
        if p.endswith(".json"):
            with open(p, encoding="utf-8") as fh:
                json.load(fh)               # a stamp that breaks the JSON dies here, not later
print("carried-cut version stamped from the manifest: %s — %d staged file(s) carry the literal, "
      "%d rewritten" % (want, carry, len(moved)))
for rel, was in moved:
    print("  ⚠ DRIFT: %s typed %s and was stamped to %s. Its committed blob no longer matches "
          "what ships, so `--check` will name this path until the repo copy is synced."
          % (rel, was, want))
PY

  # ⛔ #223, s223-D8 — THE PACKED MANIFEST SHIPS STATUS-FREE, AND THE STAMP IS TAKEN OVER IT.
  # The manifest used to be `cp`'d in whole and its sha stamped below from the REPO-SIDE file.
  # Both of those made the zip a function of Dave's ratification word: flipping PROPOSED →
  # RATIFIED moved `_MANIFEST.json`, `PROVENANCE.json` and `README.md`, so a released pack could
  # never byte-match the dry-run twin he ruled on. The packed copy is now DERIVED by the
  # generator with the status key dropped, and MAN_SHA is the sha256 of THE BYTES THAT ACTUALLY
  # SHIP — which is also the only fingerprint a designer holding the zip can reproduce.
  # Repo-side, `knowledge/_release/_pack_manifest.json` keeps its status untouched: that is what
  # `--manifest-check`, `--drift` and Dave's go/no-go page read, and what `ratified` fences on.
  python3 "$GEN" --pack-copy "$STAGE/_MANIFEST.json"
  MAN_SHA="$(python3 -c 'import hashlib,sys;print(hashlib.sha256(open(sys.argv[1],"rb").read()).hexdigest())' "$STAGE/_MANIFEST.json")"

  # `carries.what` used to be TYPED here as a twin of the generator's sentence — the same defect
  # the version had, one register up. It is READ from the manifest now (ADR-0017, one home), and
  # emitted JSON-escaped so a sentence with a quote or a backslash in it cannot break the file.
  cat > "$STAGE/PROVENANCE.json" <<JSON
{
  "pack": "$PACKNAME",
  "name": "Apollo — Spider",
  "version": "$VERSION",
  "carries": {
    "name": "$MEM_NAME",
    "version": "$MEM_VERSION",
    "what": $MEM_WHAT_JSON
  },
  "commit": "$COMMIT",
  "commit_date": "$COMMIT_DATE",
  "manifest_sha256": "$MAN_SHA",
  "files": $N_FILES,
  "ruling": "s219-D8 (naming) · s219-D5 (the five cards) · s219-D4 (the cut)",
  "reproducible": "same commit + same manifest produces a byte-identical zip"
}
JSON

  cat > "$STAGE/README.md" <<MD
# Apollo — Spider ($VERSION), carrying Memento — Gumdrop

Apollo releases are named after the LUNAR MODULES, because they are the part that lands. Memento
is named after the COMMAND MODULES, because it is the part that navigates and remembers. This is
**Apollo — Spider**, and the clean cut of Memento inside it is **Memento — Gumdrop**. A release
takes one mission's whole pair: Spider and Gumdrop are both Apollo 9.

The working Apollo engine, plus a clean cut of Memento. Not a demo and not a summary: these are
the same tokens, component contracts, reference markup, canon CSS, gates, runbooks and library
the design system itself runs on. Build with it and see where you get to.

## Provenance — what this pack was baked from

| | |
|---|---|
| pack | \`Apollo — Spider\` |
| version | \`$VERSION\` |
| carries | \`$MEM_NAME $MEM_VERSION\` |
| commit | \`$COMMIT\` |
| commit date | \`$COMMIT_DATE\` |
| manifest sha256 | \`$MAN_SHA\` |
| files | $N_FILES |
| ruling | \`s219-D8\` (naming) · \`s219-D5\` (what ships) · \`s219-D4\` (the cut) |

Every file above came out of that commit via \`git archive\` — not out of anyone's working
directory. The ship list is \`_MANIFEST.json\`, which is generated, not hand-kept. Two builds of
the same commit against the same manifest produce a **byte-identical zip**, so any difference
between two packs is a real difference and can be audited.

## What is in here

- \`skills/\` — the five skills, at the root where you will find them. Four are written against
  this exact knowledge base; the fifth, \`check-with-gates\`, runs the packed gates on your work.
- \`ci-template/\` — a GitHub Actions workflow you copy into your own repo, the runner it calls,
  and a README saying what blocks and how to turn a check off honestly.
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
- \`FIRST-SESSION.md\` — **start here.** A guided first session with Memento: what it is in three
  sentences, then your first capture, your first ruling written through the machinery with every
  field explained, and your first wrap.
- \`.github/\` — the VS Code + Copilot bridge. \`copilot-instructions.md\` is loaded automatically
  and indexes the five skills with the phrases that should trigger each one; \`prompts/\` makes
  each skill a slash command. Without this the skills sit in the pack and never fire.
- \`.vscode/settings.json\` — the other half of that bridge: three Copilot settings that turn on
  the agent's debug-file log, which is where Copilot records **the server's own reported token
  usage for your session**. That is the session gauge, and until this cut the pack told you it
  did not exist. Reload the window once after unzipping.
  \`memento-package/runbooks/_RUNBOOK-context-gauge.md\` says how to read it, what the number
  means, and — just as important — what it must never be compared to.
- \`memento-package/\` — **$MEM_NAME $MEM_VERSION**: Memento's machinery, plus the cold start.
  The machinery is the engine this design system runs on. The record it ships is **empty on
  purpose**: an empty task store, an empty rulings store — both with the shapes already right and
  driven against those shapes before shipping — and a starter \`_CHAIN.md\` that explains the
  first move and is replaced the first time you wrap. Nothing in it is anyone else's history.
  Your project grows its own memory from nothing, which is the point: the shapes are machinery,
  the contents are your record. Its version moves WITH this pack (\`s225-D3\`): the cut in your
  hands is **$MEM_NAME $MEM_VERSION**, and every Gumdrop version line inside the pack is stamped
  from that one figure, so nothing in here can disagree with it about what you are holding.
- \`memento-package/_encoder-cache/\` — the \`cl100k_base\` encoder data, vendored so token
  measurement works with no download and no environment variable. Its README says what it is,
  what it mirrors, its sha256 and its licence.

## The canon generators, and one warning

The generators that mint canon from the tokens are in here, because this is the working engine
and not a baked copy of one. Changing a token and re-minting canon can produce canon that never
passed a gate. Each generator says so when you run it inside this pack and asks you to pass
\`--i-understand\` before it will proceed. Then run \`python3 ci-template/run-gates.py\` — that
is what tells you whether what you just minted still passes.

## What is deliberately NOT in here

Review files, session notes, run logs, client project work, and the licensed material we cannot
redistribute. \`_MANIFEST.json\` lists every exclusion with its reason.

## What you need installed

\`pip install tiktoken\` — the only one, and it is RECOMMENDED rather than required: the pack
carries its own exact encoder for machines that cannot install it. \`FIRST-SESSION.md\` § Before you
start says why: the chain generator counts tokens exactly and REFUSES to write the file at all on
an estimate — with \`tiktoken\` it does that faster, without it the pack's own engine does it.

**The pack also carries its own encoder.** \`memento-package/machinery/_encoder_home.py\` contains a
pure-Python \`cl100k_base\` implementation — the same pretokenizer, the same byte-pair merges, over
the same vendored data — which runs when \`tiktoken\` cannot be imported and NAMES ITSELF when it
does (\`purepy cl100k_base (exact, equality-gated)\`, never the real library's name). It is exact,
not an estimate, and the pack ships the gate that proves it:

    python3 memento-package/machinery/_encoder_home.py --equality-gate

which drives both encoders over this pack's own text and refuses on the first token they disagree
about. It is a few times slower, which is why \`tiktoken\` is still the recommended path.

**You do not need network access for the encoder itself.** \`tiktoken\` normally downloads its
\`cl100k_base\` encoding data from \`openaipublic.blob.core.windows.net\`, which is blocked on many
corporate laptops. That data ships inside this pack instead, at
\`memento-package/_encoder-cache/\` (see the README beside it), and
\`memento-package/machinery/_encoder_home.py\` — the one place that knows where it is — points
\`tiktoken\` at it automatically, by \`setdefault\`, so your own \`TIKTOKEN_CACHE_DIR\` still wins.
Only the \`tiktoken\` **wheel** still comes from PyPI. Check the whole path in one command:

    python3 memento-package/machinery/_encoder_home.py --check

If the vendored data is ever missing or damaged, that check and the chain generator both refuse
loudly and name the file — there is no estimate fallback and never a silently wrong number.

A few gates additionally drive a real browser and need \`playwright\`. They are included, they are
not in the default run, and they name their own dependency when you run them without it — a
\`COULD-NOT-ASK:\` line and exit 77, which does not fail the build. See \`_MANIFEST.json\` for
which ones.
MD

  # ---- ADVISORY: read the staged pack in the DESIGNER'S grammar (#221, from #220-L4) --------
  # This is the only moment the pack exists as a tree and can still be fixed without a re-cut.
  # Six of L4's nineteen findings were one defect — a shipped document naming a path or command
  # that is not in the pack it ships in — and no gate in the fleet reads a document the way the
  # person holding it will [[no-gate-parses-the-artefact]].
  # ⬛ ADVISORY, BY CONSTRUCTION: the gate returns 0 whatever it finds, and `|| true` is
  # deliberately NOT used, so a rc=2 REFUSAL (bad arguments, unreadable stage) still stops the
  # bake under `set -e`. Advisory means "its findings do not block"; it does not mean "ignore
  # the instrument when it cannot run". Promotion to blocking is Dave's word.
  echo "reading the staged pack as a designer would (ADVISORY)…"
  python3 "$ROOT/knowledge/_release/_gate_pack_docs.py" --stage "$STAGE"

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
  PAGE="$(ls -1 "$ROOT"/reviews/RELEASE-SPIDER-*-v*.html 2>/dev/null | tail -1)"
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
