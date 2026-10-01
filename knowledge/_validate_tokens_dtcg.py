#!/usr/bin/env python3
"""_validate_tokens_dtcg.py — the FIVE PROOFS of the s311-D8 move (tokens to DTCG 2025.10).

s311-D8 (Dave, #311, 2026-10-01): "Tokens to DTCG — now, one generator, extras under
$extensions." The generator is knowledge/tokens/gen_dtcg.py; this gate is what says the move
lost nothing and moved no pixel. It is BLOCKING (wired in _build_all.STEPS and test_gates) and
every proof it cannot make it names UNMEASURED with the reason — never a quiet PASS.

  proof 1  SPINE BYTE-EQUAL  — canon.css's AUTO-GENERATED TOKENS span, re-rendered from the
           DTCG files through the read-site seam (_dtcg_load), equals the committed span byte
           for byte (gen_canon_tokens --check, in-process, plus a sha of the span).
  proof 2  SNIPPET THEME BLOCKS BYTE-EQUAL — every [data-theme] block of all 137 snippets (+ 9
           tranches, + the canon.css literals) re-projects from the DTCG files with zero
           changes (gen_snippet_tokens --check --quiet, as a subprocess: ~11 s). The snippets
           are not edited by the move; this is what says so.
  proof 3  EVERY MOVED KEY RECOVERABLE — for each base file (+ its modes/dark context):
           to_legacy() then to_dtcg() equals the file on disk (nothing in $extensions.apollo
           is orphaned, nothing standard is lost), the count of `$` keys restored equals the
           count moved, and no non-standard `$` key survives at the top level. With
           --receipt DIR the same inverse is compared, by parse, against a directory of
           pre-s311 files (the landing receipt; V can rebuild one with `git show 97c7793:…`).
  proof 4  THEME OVERRIDES THROUGH THE RESOLVER — UNMEASURED until themes/*.overrides.json are
           a `theme` modifier of apollo.resolver.json (owed, named in the J report). The gate
           checks the resolver document itself: version 2025.10, every $ref a real file, the
           dark context listing exactly the files under modes/dark/.
  proof 5  STYLE DICTIONARY v4 PARSES — when `node` and a resolvable `style-dictionary`
           (node_modules at the repo root, or --sd-dir DIR / $APOLLO_SD_DIR) are present, both
           contexts are built and the warning blocks counted and named; otherwise UNMEASURED
           with the reason. Measured at #312 J: SD 4.4.0, 591 tokens per context, 2 warning
           classes — 11 root-$description merge collisions (file metadata, not tokens) and 5
           prose notes containing `{…}` (pre-existing in `$note`; SD resolves braces outside
           $value, the spec does not).

    python3 knowledge/_validate_tokens_dtcg.py                 # the five proofs
    python3 knowledge/_validate_tokens_dtcg.py --quick         # proofs 1, 3, 4 only (no 11 s)
    python3 knowledge/_validate_tokens_dtcg.py --receipt DIR   # + the pre-s311 fixture compare
    python3 knowledge/_validate_tokens_dtcg.py --sd-dir DIR    # DIR holds node_modules/style-dictionary
    python3 knowledge/_validate_tokens_dtcg.py --selftest      # the bites
    python3 knowledge/_validate_tokens_dtcg.py --json

Exit non-zero on any FAIL. UNMEASURED is printed, named, and does not fail the gate.
"""
import os as _hg_os, sys as _hg_sys  # noqa: E402 - help gate (#158 write-by-default class)
_hg_d = _hg_os.path.dirname(_hg_os.path.abspath(__file__))
while _hg_d != "/" and not _hg_os.path.exists(_hg_os.path.join(_hg_d, "_helpgate.py")):
    _hg_d = _hg_os.path.dirname(_hg_d)
_hg_sys.path.insert(0, _hg_d)
from _helpgate import help_gate as _help_gate; _help_gate(__doc__, __name__, __file__)
import copy
import hashlib
import importlib.util
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
TOK = os.path.join(HERE, "tokens")
CANON = os.path.join(HERE, "canon", "canon.css")
SPAN_RE = re.compile(r"/\* ===== AUTO-GENERATED TOKENS START =====.*?AUTO-GENERATED TOKENS END ===== \*/", re.S)
STANDARD_KEYS = {"$value", "$type", "$description", "$extensions", "$deprecated"}


class GateError(Exception):
    """A named failure of the gate's own machinery (a crash is not a fail)."""


def _gen(tokdir=TOK):
    spec = importlib.util.spec_from_file_location("gen_dtcg", os.path.join(tokdir, "gen_dtcg.py"))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def _load(p):
    with open(p, encoding="utf-8") as fh:
        return json.load(fh)


# ---------------------------------------------------------------- proof 1
def proof_spine(knowledge=HERE):
    canon_dir = os.path.join(knowledge, "canon")
    sys.path.insert(0, canon_dir)
    sys.path.insert(0, knowledge)
    import gen_canon_tokens as gct  # noqa: E402
    importlib.reload(gct)
    canon = os.path.join(canon_dir, "canon.css")
    if not os.path.exists(canon):
        return {"status": "UNMEASURED", "why": "canon.css absent at %s" % canon}
    before = open(canon, "rb").read()
    import io, contextlib
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        rc = gct.main(check=True)
    after = open(canon, "rb").read()
    if after != before:
        return {"status": "FAIL", "why": "gen_canon_tokens --check WROTE canon.css"}
    m = SPAN_RE.search(before.decode("utf-8"))
    sha = hashlib.sha256(m.group(0).encode("utf-8")).hexdigest()[:16] if m else None
    if rc != 0:
        return {"status": "FAIL", "why": "canon.css token spine differs from what the DTCG files "
                                         "render to (gen_canon_tokens --check rc=%d)" % rc,
                "spanSha": sha}
    return {"status": "PASS", "why": "AUTO-GENERATED TOKENS span byte-equal (sha256 %s…)" % sha,
            "spanSha": sha}


# ---------------------------------------------------------------- proof 2
def proof_snippets(knowledge=HERE):
    script = os.path.join(knowledge, "gen_snippet_tokens.py")
    r = subprocess.run([sys.executable, script, "--check", "--quiet"],
                       capture_output=True, text=True, timeout=600)
    out = (r.stdout + r.stderr).strip()
    m = re.search(r"(\d+) manifest bindings across (\d+) snippets \+ (\d+) tranches; (\d+) value\(s\) would change; (\d+) canon\.css literal", out)
    detail = out.splitlines()[-1] if out else ""
    if r.returncode != 0:
        return {"status": "FAIL", "why": "gen_snippet_tokens --check rc=%d :: %s" % (r.returncode, detail)}
    if m:
        return {"status": "PASS", "why": "%s bindings across %s snippets + %s tranches, %s value(s) "
                                         "would change, %s canon literal(s) would change"
                                         % m.groups(), "snippets": int(m.group(2)),
                "changes": int(m.group(4)) + int(m.group(5))}
    return {"status": "PASS", "why": detail}


# ---------------------------------------------------------------- proof 3
def _dollar_keys(node, acc, under_ext=False):
    if isinstance(node, dict):
        for k, v in node.items():
            if k.startswith("$") and not under_ext:
                acc.append(k)
            _dollar_keys(v, acc, under_ext or k == "$extensions")
    elif isinstance(node, list):
        for v in node:
            _dollar_keys(v, acc, under_ext)


def _moved_keys(node, acc):
    """count of $extensions.apollo.<k> entries that are moved keys (not KEEP_IN_APOLLO)."""
    g = _GEN
    if isinstance(node, dict):
        ext = node.get("$extensions")
        if isinstance(ext, dict) and isinstance(ext.get("apollo"), dict):
            acc.extend(k for k in ext["apollo"] if k not in g.KEEP_IN_APOLLO)
        for k, v in node.items():
            if k != "$extensions":
                _moved_keys(v, acc)


def proof_roundtrip(tokdir=TOK, receipt_dir=None):
    g = _GEN
    bases, darks = {}, {}
    for n in g.BASE_FILES:
        p = os.path.join(tokdir, n)
        if not os.path.exists(p):
            raise GateError("base token file missing: %s" % p)
        bases[n] = _load(p)
        dp = os.path.join(tokdir, "modes", "dark", n)
        darks[n] = _load(dp) if os.path.exists(dp) else None
    res = g.DtcgResolver(bases, darks)
    fails, notes = [], []
    moved_total = restored_total = 0
    legacy = {}
    for n in g.BASE_FILES:
        try:
            legacy[n] = g.to_legacy(bases[n], darks[n], res)
        except g.DtcgMoveError as e:
            fails.append("%s: inverse refused :: %s" % (n, e))
            continue
        stray = [k for k in set(_dollar_keys_top(bases[n]) + (_dollar_keys_top(darks[n]) if darks[n] else []))
                 if k not in STANDARD_KEYS]
        if stray:
            fails.append("%s: non-standard `$` key(s) at the top level: %s" % (n, ", ".join(sorted(stray))))
        moved = []
        _moved_keys(bases[n], moved)
        if darks[n]:
            _moved_keys(darks[n], moved)
        restored = []
        _dollar_keys(legacy[n], restored)
        restored_nonstd = [k for k in restored if k not in STANDARD_KEYS]
        # every moved key must come back as a `$` key (alias may fold into two refs: counted by name)
        moved_names = sorted("$" + k for k in moved)
        missing = [k for k in moved_names if k not in restored_nonstd]
        if missing:
            fails.append("%s: moved key(s) not restored by the inverse: %s" % (n, ", ".join(missing[:8])))
        moved_total += len(moved)
        restored_total += len(restored_nonstd)
    spine = g.Spine(legacy)
    for n in g.BASE_FILES:
        if n not in legacy:
            continue
        base2, dark2 = g.to_dtcg(copy.deepcopy(legacy[n]), spine, n)
        if base2 != bases[n]:
            fails.append("%s: to_dtcg(to_legacy(file)) != file (base)" % n)
        if (dark2 or None) != (darks[n] or None):
            fails.append("%s: to_dtcg(to_legacy(file)) != file (modes/dark)" % n)
    notes.append("%d files, %d moved keys under $extensions.apollo, %d `$` keys restored by the inverse"
                 % (len(legacy), moved_total, restored_total))
    if receipt_dir:
        ok = 0
        for n in g.BASE_FILES:
            fp = os.path.join(receipt_dir, n)
            if not os.path.exists(fp):
                fails.append("receipt: no fixture for %s in %s" % (n, receipt_dir))
                continue
            if _load(fp) == legacy.get(n):
                ok += 1
            else:
                fails.append("receipt: to_legacy(%s) != pre-s311 fixture" % n)
        notes.append("receipt: %d/%d files equal their pre-s311 fixture by parse" % (ok, len(g.BASE_FILES)))
    return {"status": "FAIL" if fails else "PASS", "why": "; ".join(notes), "fails": fails}


def _dollar_keys_top(node):
    acc = []
    _dollar_keys(node, acc)
    return acc


# ---------------------------------------------------------------- proof 4
def proof_resolver(tokdir=TOK):
    rp = os.path.join(tokdir, "apollo.resolver.json")
    if not os.path.exists(rp):
        return {"status": "FAIL", "why": "apollo.resolver.json missing"}
    r = _load(rp)
    fails = []
    if r.get("version") != "2025.10":
        fails.append("resolver version is %r, not 2025.10" % (r.get("version"),))
    refs = []
    for s in r.get("sets", {}).values():
        refs += [x.get("$ref") for x in s.get("sources", [])]
    for m in r.get("modifiers", {}).values():
        for ctx in m.get("contexts", {}).values():
            refs += [x.get("$ref") for x in ctx]
    for ref in refs:
        if not ref or not os.path.exists(os.path.join(tokdir, ref)):
            fails.append("$ref %r does not resolve to a file under tokens/" % (ref,))
    for ro in r.get("resolutionOrder", []):
        ref = ro.get("$ref", "")
        kind, _, name = ref.lstrip("#/").partition("/")
        if name not in r.get(kind, {}):
            fails.append("resolutionOrder %r names nothing" % ref)
    dark_listed = sorted(os.path.basename(x["$ref"]) for x in
                         r.get("modifiers", {}).get("color-scheme", {}).get("contexts", {}).get("dark", []))
    dark_on_disk = sorted(f for f in os.listdir(os.path.join(tokdir, "modes", "dark"))
                          if f.endswith(".json")) if os.path.isdir(os.path.join(tokdir, "modes", "dark")) else []
    if dark_listed != dark_on_disk:
        fails.append("dark context lists %s but modes/dark/ holds %s" % (dark_listed, dark_on_disk))
    if fails:
        return {"status": "FAIL", "why": "; ".join(fails), "fails": fails}
    if "theme" not in r.get("modifiers", {}):
        return {"status": "UNMEASURED",
                "why": "resolver document OK (version 2025.10, %d $refs resolve, dark context = modes/dark/); "
                       "the theme override sets are not yet a `theme` modifier, so their resolution "
                       "cannot be compared with gen_theme_cascade — owed (s311-D8 remainder, J report)"
                       % len(refs)}
    return {"status": "UNMEASURED", "why": "a `theme` modifier exists but this gate has no comparer for it yet"}


# ---------------------------------------------------------------- proof 5
SD_SCRIPT = r"""
import StyleDictionary from 'style-dictionary';
import fs from 'node:fs';
const tok = process.argv[2];
const r = JSON.parse(fs.readFileSync(tok + '/apollo.resolver.json','utf8'));
const base = r.sets.base.sources.map(s => tok + '/' + s.$ref);
const dark = r.modifiers['color-scheme'].contexts.dark.map(s => tok + '/' + s.$ref);
const warns = [];
const origLog = console.log;
console.warn = (...a) => { warns.push(a.join(' ')); };
console.error = (...a) => { warns.push(a.join(' ')); };
console.log = (...a) => { const s=a.join(' '); if (/warn|collision|reference/i.test(s)) warns.push(s); };
async function run(cfg) {
  const sd = new StyleDictionary({ ...cfg, log: { verbosity: 'verbose', warnings: 'warn', errors: { brokenReferences: 'console' } } });
  await sd.hasInitialized;
  const tokens = await sd.exportPlatform('css');
  let n = 0; (function count(o){ for (const k in o){ if (o[k] && typeof o[k]==='object'){ if ('$value' in o[k] || 'value' in o[k]) n++; else count(o[k]); } } })(tokens);
  return n;
}
const cfg = (src, inc) => ({ usesDtcg: true, include: inc, source: src,
  platforms: { css: { transformGroup: 'css', files: [{ destination: 'apollo.css', format: 'css/variables' }] } } });
const nLight = await run(cfg(base, []));
const nDark = await run(cfg(dark, base));
console.log = origLog;
const classes = {};
for (const w of warns) { const h = (w.match(/^\s*([^\n:]+)/) || [,'other'])[1].trim(); classes[h] = (classes[h]||0) + 1; }
console.log(JSON.stringify({ lightTokens: nLight, darkTokens: nDark, warningBlocks: warns.length, classes,
  references: new Set(warns.join('\n').split('\n').filter(l => /tries to reference/.test(l))).size,
  collisions: new Set(warns.join('\n').split('\n').filter(l => /Collision detected at/.test(l))).size }));
"""


def proof_style_dictionary(tokdir=TOK, sd_dir=None):
    node = shutil.which("node")
    if not node:
        return {"status": "UNMEASURED", "why": "no `node` on PATH"}
    cands = [sd_dir, os.environ.get("APOLLO_SD_DIR"), os.path.dirname(HERE)]
    sd_root = next((c for c in cands if c and os.path.isdir(os.path.join(c, "node_modules", "style-dictionary"))), None)
    if not sd_root:
        return {"status": "UNMEASURED",
                "why": "style-dictionary not installed (looked for node_modules/style-dictionary under "
                       "--sd-dir, $APOLLO_SD_DIR and the repo root); `npm i style-dictionary@4` there to measure"}
    script = os.path.join(sd_root, ".apollo_sd_check.mjs")
    with open(script, "w", encoding="utf-8") as fh:
        fh.write(SD_SCRIPT)
    try:
        r = subprocess.run([node, script, tokdir], capture_output=True, text=True, timeout=300)
    finally:
        try:
            os.remove(script)
        except OSError:
            pass
    if r.returncode != 0:
        return {"status": "FAIL", "why": "style-dictionary did not parse the spine :: %s" % (r.stderr.strip()[-400:],)}
    try:
        data = json.loads(r.stdout.strip().splitlines()[-1])
    except (ValueError, IndexError):
        return {"status": "FAIL", "why": "style-dictionary probe printed no verdict :: %s" % r.stdout[-300:]}
    try:
        ver = json.load(open(os.path.join(sd_root, "node_modules", "style-dictionary", "package.json")))["version"]
    except Exception:
        ver = "?"
    why = ("style-dictionary %s parsed %d light / %d dark tokens; %d warning block(s): %d root-$description "
           "merge collision(s) (file metadata, not tokens), %d prose `{…}` reference(s) inside "
           "$extensions.apollo notes" % (ver, data["lightTokens"], data["darkTokens"], data["warningBlocks"],
                                          data["collisions"], data["references"]))
    status = "PASS" if data["warningBlocks"] == 0 else "PASS WITH WARNINGS"
    return {"status": status, "why": why, "data": data, "version": ver}


# ---------------------------------------------------------------- runner
def run(quick=False, receipt=None, sd_dir=None, tokdir=TOK, knowledge=HERE):
    global _GEN
    _GEN = _gen(tokdir)
    proofs = {}
    proofs["1-spine"] = proof_spine(knowledge)
    proofs["2-snippets"] = ({"status": "SKIPPED", "why": "--quick"} if quick else proof_snippets(knowledge))
    proofs["3-roundtrip"] = proof_roundtrip(tokdir, receipt)
    proofs["4-themes"] = proof_resolver(tokdir)
    proofs["5-style-dictionary"] = ({"status": "SKIPPED", "why": "--quick"} if quick
                                    else proof_style_dictionary(tokdir, sd_dir))
    nfail = sum(1 for p in proofs.values() if p["status"] == "FAIL")
    return proofs, nfail


_GEN = None


def selftest():
    """Bites, each on a temp copy of tokens/: a moved key deleted · a stray $note re-minted ·
    a reference broken · the resolver's dark list drifted · a dark value edited through the
    legacy view is seen (the seam is live, not cached stale)."""
    global _GEN
    _GEN = _gen(TOK)
    tmp = tempfile.mkdtemp(prefix="tokens-dtcg-")
    try:
        def fresh():
            d = os.path.join(tmp, "tokens")
            if os.path.exists(d):
                shutil.rmtree(d)
            shutil.copytree(TOK, d, ignore=shutil.ignore_patterns("_*", "*.md", "palettes", "_proposals", "_manifests"))
            return d
        # bite 1: delete a moved key -> proof 3 FAIL (unrecoverable)
        d = fresh()
        p = os.path.join(d, "semantic-colour.json")
        doc = _load(p)
        node = doc["border"]["action-strong"]
        assert "note" in node["$extensions"]["apollo"], "fixture: border/action-strong has no moved note"
        del node["$extensions"]["apollo"]["note"]
        # a deleted note is not a round-trip failure by itself (nothing orphaned) — the RECEIPT catches it
        json.dump(doc, open(p, "w"), indent=2, ensure_ascii=False)
        r = proof_roundtrip(d, receipt_dir=None)
        assert r["status"] == "PASS", "bite 1a: shape round-trip must still pass when a note is simply gone"
        fixture = os.path.join(tmp, "fixture")
        os.makedirs(fixture, exist_ok=True)
        for n in _GEN.BASE_FILES:
            json.dump(_GEN.to_legacy(_load(os.path.join(TOK, n)),
                                     _load(os.path.join(TOK, "modes", "dark", n)) if os.path.exists(os.path.join(TOK, "modes", "dark", n)) else None,
                                     _GEN.DtcgResolver({m: _load(os.path.join(TOK, m)) for m in _GEN.BASE_FILES},
                                                       {m: (_load(os.path.join(TOK, "modes", "dark", m)) if os.path.exists(os.path.join(TOK, "modes", "dark", m)) else None) for m in _GEN.BASE_FILES})),
                      open(os.path.join(fixture, n), "w"), indent=2, ensure_ascii=False)
        r = proof_roundtrip(d, receipt_dir=fixture)
        assert r["status"] == "FAIL" and any("fixture" in f for f in r["fails"]), "bite 1b: receipt did not catch the deleted note"
        # bite 2: a stray $note re-minted at the top level -> proof 3 FAIL
        d = fresh()
        p = os.path.join(d, "layout.json")
        doc = _load(p)
        doc["border-radius"]["default"]["$note"] = "re-minted the old way"
        json.dump(doc, open(p, "w"), indent=2, ensure_ascii=False)
        r = proof_roundtrip(d)
        assert r["status"] == "FAIL" and any("non-standard" in f for f in r["fails"]), r
        # bite 3: a reference broken -> inverse refuses -> FAIL
        d = fresh()
        p = os.path.join(d, "semantic-colour.json")
        doc = _load(p)
        doc["background"]["default"]["$value"] = "{color.neutral.999}"
        json.dump(doc, open(p, "w"), indent=2, ensure_ascii=False)
        r = proof_roundtrip(d)
        assert r["status"] == "FAIL" and any("refused" in f for f in r["fails"]), r
        # bite 4: resolver dark list drifted -> proof 4 FAIL
        d = fresh()
        p = os.path.join(d, "apollo.resolver.json")
        doc = _load(p)
        doc["modifiers"]["color-scheme"]["contexts"]["dark"].append({"$ref": "modes/dark/ghost.json"})
        json.dump(doc, open(p, "w"), indent=2)
        r = proof_resolver(d)
        assert r["status"] == "FAIL", r
        # bite 5: the seam is live — edit a dark value on disk, the legacy view shows it
        d = fresh()
        sys.path.insert(0, HERE)
        import _dtcg_load as L
        importlib.reload(L)
        before = L.load_legacy(os.path.join(d, "semantic-colour.json"))["background"]["default"]["dark"]["$value"]
        dp = os.path.join(d, "modes", "dark", "semantic-colour.json")
        doc = _load(dp)
        doc["background"]["default"]["$value"] = "#123456"
        json.dump(doc, open(dp, "w"), indent=2)
        os.utime(dp, None)
        after = L.load_legacy(os.path.join(d, "semantic-colour.json"))["background"]["default"]["dark"]["$value"]
        assert before != "#123456" and after == "#123456", (before, after)
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
    print("_validate_tokens_dtcg selftest OK (5 bites: deleted note caught by the receipt · stray $note "
          "FAILS · broken reference FAILS · resolver drift FAILS · the seam reads live)")


def main():
    args = sys.argv[1:]
    if "--selftest" in args:
        selftest()
        return 0
    receipt = sd_dir = None
    if "--receipt" in args:
        receipt = args[args.index("--receipt") + 1]
    if "--sd-dir" in args:
        sd_dir = args[args.index("--sd-dir") + 1]
    try:
        proofs, nfail = run(quick="--quick" in args, receipt=receipt, sd_dir=sd_dir)
    except GateError as e:
        print("GATE ERROR (a crash is not a fail) :: %s" % e, file=sys.stderr)
        return 2
    if "--json" in args:
        print(json.dumps(proofs, indent=2))
    else:
        print("TOKENS→DTCG 2025.10 GATE — s311-D8, the five proofs")
        for k, p in proofs.items():
            print("  %-20s %-19s %s" % (k, p["status"], p["why"]))
            for f in p.get("fails", []):
                print("      FAIL " + f)
        print("%s — %d failure(s)" % ("FAIL" if nfail else "PASS", nfail))
    return 1 if nfail else 0


if __name__ == "__main__":
    sys.exit(main())
