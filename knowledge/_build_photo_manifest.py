#!/usr/bin/env python3
"""_build_photo_manifest.py — the committed surface for the NON-REPO photography originals (W-93, s217-D1).

THE SHAPE (s217-D1, Dave, #217): originals stay NON-REPO — the #211 `.gitignore` fence at
`knowledge/assets/photography/` STANDS. What is committed is (a) a MANIFEST covering every
original — filename · pixel dimensions · EXIF description · licence source — and (b) web-sized
DERIVATIVES for the photos actually consumed by the library, each derivative carrying a manifest
row. A hosted cloud image store is NOTED FOR THE FUTURE by that ruling and is NOT designed for here.

OUTPUTS (all outside the ignored folder — verified with `git check-ignore`):
  knowledge/_PHOTOGRAPHY-MANIFEST.json   machine surface, one row per original (the KG's pointer target)
  knowledge/_PHOTOGRAPHY-MANIFEST.md     human surface, generated from the same rows
  knowledge/assets/photography-web/       committed derivatives (sRGB JPEG, max edge 1600, <=300 KB)

UNKNOWN IS NEVER DEFAULTED. An absent EXIF field is written as `null` in JSON and the literal
string `UNKNOWN` in the Markdown, with `*_basis` naming WHERE the value came from. A licence
source that cannot be derived says `UNKNOWN (no XMP credit, filename carries no provenance)` —
it never silently becomes "Getty".

FAILS LOUD AND NAMED. Unreadable files are collected, printed by name with their exception, and
the run exits 1 after declaring the residual count. A crash is not a fail: the residual is a
stated number, not a traceback.

NO TAGGING TAXONOMY. EXIF description text is copied VERBATIM (after a mechanical mojibake
repair that is recorded alongside the raw bytes). Deriving tags/keywords/categories from it is
UNRULED work and is deliberately absent.

USAGE
  python3 knowledge/_build_photo_manifest.py --manifest
      Scan the originals folder, write the JSON + MD manifest. Requires the originals to be
      present in the working tree (they are NON-REPO — a clone without them cannot regenerate).

  python3 knowledge/_build_photo_manifest.py --derivatives a.jpg b.jpg ...
  python3 knowledge/_build_photo_manifest.py --derivatives-from knowledge/_PHOTOGRAPHY-USED.txt
      Mint web derivatives for the named originals only (s217-D1: USED photos only).

  python3 knowledge/_build_photo_manifest.py --check
      GATE (no writes, no originals needed): every file in the derivatives dir must carry a row
      in the committed manifest, and no original JPEG may be git-trackable. Exit 1 on either.
      ⬛ DECLARED AT BIRTH: not yet routed into `_build_all.py` or the commit seam — an instrument
      without a consumer cannot fail. Wiring it is the conductor's call and is priced, not done.

  python3 knowledge/_build_photo_manifest.py --selftest
      Drives --check both directions on real fixtures (fail-arm, pass-arm, mutation-arm).
"""
import os as _hg_os, sys as _hg_sys  # noqa: E402 - help gate (#158 write-by-default class)
_hg_d = _hg_os.path.dirname(_hg_os.path.abspath(__file__))
while _hg_d != "/" and not _hg_os.path.exists(_hg_os.path.join(_hg_d, "_helpgate.py")):
    _hg_d = _hg_os.path.dirname(_hg_d)
_hg_sys.path.insert(0, _hg_d)
from _helpgate import help_gate as _help_gate, write_gate as _write_gate  # noqa: E402
_help_gate(__doc__, __name__, __file__)
_write_gate(__file__, writes="knowledge/_PHOTOGRAPHY-MANIFEST.{json,md}")

import argparse, io, json, os, re, subprocess, sys, warnings

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ORIGINALS = os.path.join(ROOT, "knowledge", "assets", "photography")
DERIV_DIR = os.path.join(ROOT, "knowledge", "assets", "photography-web")
JSON_OUT = os.path.join(ROOT, "knowledge", "_PHOTOGRAPHY-MANIFEST.json")
MD_OUT = os.path.join(ROOT, "knowledge", "_PHOTOGRAPHY-MANIFEST.md")

MAX_EDGE = 1600          # px, longest side
TARGET_KB = 300          # measured ceiling per derivative, not an intention
QUALITY_LADDER = [82, 78, 74, 70, 66, 62, 58]


class ManifestError(Exception):
    """Loud, named refusal — never a silent skip."""


# ---------------------------------------------------------------- text repair
def _demojibake(s):
    """UTF-8 bytes read as latin-1 come back as 'Â©'. Repair, at most twice, only when it helps.

    Returns (repaired, n_passes). Never lossy: a pass that cannot round-trip is refused, so a
    genuinely latin-1 string is returned untouched.
    """
    if not isinstance(s, str):
        return s, 0
    out, n = s, 0
    for _ in range(2):
        if not re.search(r"[ÂÃ]", out):
            break
        try:
            cand = out.encode("latin-1").decode("utf-8")
        except (UnicodeEncodeError, UnicodeDecodeError):
            break
        if cand == out:
            break
        out, n = cand, n + 1
    return out, n


def _clean(v):
    """EXIF values arrive as str|bytes|None. Return a stripped str, or None for absent/empty."""
    if v is None:
        return None
    if isinstance(v, bytes):
        v = v.decode("utf-8", "replace")
    v = str(v).replace("\x00", "").strip()
    return v or None


# ---------------------------------------------------------------- XMP scrape
_XMP_ATTR = {
    "credit": r'photoshop:Credit="([^"]*)"',
    "source": r'photoshop:Source="([^"]*)"',
    "web_statement": r'xmpRights:WebStatement="([^"]*)"',
    "licensor_url": r'plus:LicensorURL="([^"]*)"',
}
_XMP_ELEM = {
    "credit": r"<photoshop:Credit>(.*?)</photoshop:Credit>",
    "source": r"<photoshop:Source>(.*?)</photoshop:Source>",
    "web_statement": r"<xmpRights:WebStatement>(.*?)</xmpRights:WebStatement>",
    "licensor_url": r'plus:LicensorURL="([^"]*)"',
}


def _xmp_fields(xmp_bytes):
    if not xmp_bytes:
        return {}
    txt = xmp_bytes.decode("utf-8", "replace") if isinstance(xmp_bytes, bytes) else str(xmp_bytes)
    out = {}
    for key in _XMP_ATTR:
        m = re.search(_XMP_ATTR[key], txt) or re.search(_XMP_ELEM[key], txt, re.S)
        if m:
            val = re.sub(r"\s+", " ", m.group(1)).strip()
            val = val.replace("&amp;", "&")
            if val:
                out[key] = val
    return out


# ---------------------------------------------------------------- provenance
def _filename_provenance(name):
    """What the FILENAME alone says. UNKNOWN is a real answer."""
    if name.startswith("GettyImages-"):
        return "Getty Images"
    if name.startswith("EyeEm_"):
        return "EyeEm"
    if re.fullmatch(r"\d+\.jpe?g", name, re.I):
        return None      # bare number — the filename carries no provenance
    return None


def _licence_source(name, xmp, exif_copyright):
    """(value, basis). Never defaults; UNKNOWN is stated with the reason."""
    fn = _filename_provenance(name)
    if xmp.get("credit"):
        val = xmp["credit"]
        basis = "xmp:photoshop:Credit"
        if fn and fn.lower() not in val.lower():
            basis += " (filename says %s)" % fn
        return val, basis
    if fn:
        return fn, "filename prefix"
    if exif_copyright:
        return exif_copyright, "exif:Copyright (no XMP credit, filename carries no provenance)"
    return None, "UNKNOWN — no XMP credit, no filename provenance, no EXIF copyright"


# ---------------------------------------------------------------- scan
def scan(originals=ORIGINALS):
    """-> (rows, failures). Reads EXIF + XMP only; never decodes full pixel data."""
    try:
        from PIL import Image, ExifTags
    except ImportError as exc:                                   # loud, named
        raise ManifestError("Pillow is not importable (%s) — the manifest cannot be measured, "
                            "and a guessed dimension is not a measurement." % exc)
    if not os.path.isdir(originals):
        raise ManifestError(
            "originals folder absent: %s\n"
            "  Originals are NON-REPO by s217-D1 — a clone without them cannot regenerate the "
            "manifest. Use the COMMITTED manifest, or restore the folder." % originals)

    names = sorted(n for n in os.listdir(originals)
                   if n.lower().endswith((".jpg", ".jpeg")) and not n.startswith("."))
    rows, failures = [], []
    for name in names:
        path = os.path.join(originals, name)
        try:
            with warnings.catch_warnings():
                warnings.simplefilter("ignore")   # PIL grumbles about oversized MakerNote IFDs
                im = Image.open(path)
                width, height = im.size
                exif = im.getexif()
                tags = {ExifTags.TAGS.get(k, k): v for k, v in exif.items()}
                xmp = _xmp_fields(im.info.get("xmp"))
        except Exception as exc:                                 # noqa: BLE001 — declared residual
            failures.append((name, repr(exc)))
            continue

        desc_raw = _clean(tags.get("ImageDescription"))
        desc, desc_fixes = _demojibake(desc_raw) if desc_raw else (None, 0)
        cop_raw = _clean(tags.get("Copyright"))
        cop, cop_fixes = _demojibake(cop_raw) if cop_raw else (None, 0)
        artist_raw = _clean(tags.get("Artist"))
        artist, _ = _demojibake(artist_raw) if artist_raw else (None, 0)
        lic, lic_basis = _licence_source(name, xmp, cop)

        row = {
            "filename": name,
            "width": width,
            "height": height,
            "orientation": ("landscape" if width > height
                            else "portrait" if height > width else "square"),
            "bytes": os.path.getsize(path),
            "exif_description": desc,
            "exif_description_basis": ("exif:ImageDescription" if desc else
                                       "UNKNOWN — no EXIF ImageDescription on this file"),
            "exif_copyright": cop,
            "exif_artist": artist,
            "licence_source": lic,
            "licence_source_basis": lic_basis,
            "licence_web_statement": xmp.get("web_statement"),
            "licensor_url": xmp.get("licensor_url"),
            "xmp_source": xmp.get("source"),
            "derivative": None,      # filled by --derivatives; null = no committed derivative
        }
        if desc_fixes or cop_fixes:
            row["mojibake_repaired"] = {"description_passes": desc_fixes,
                                        "copyright_passes": cop_fixes,
                                        "description_raw": desc_raw if desc_fixes else None,
                                        "copyright_raw": cop_raw if cop_fixes else None}
        rows.append(row)
    return rows, failures


# ---------------------------------------------------------------- derivatives
def derivative_name(original):
    """Deterministic: lowercase stem, non-alnum -> '-', collapsed, '-w1600.jpg'."""
    stem = os.path.splitext(original)[0].lower()
    stem = re.sub(r"[^a-z0-9]+", "-", stem).strip("-")
    return "%s-w%d.jpg" % (stem, MAX_EDGE)


def mint(names, originals=ORIGINALS, out_dir=DERIV_DIR):
    """-> (minted, failures). sRGB JPEG, max edge MAX_EDGE, quality stepped down until <= TARGET_KB."""
    from PIL import Image, ImageCms
    os.makedirs(out_dir, exist_ok=True)
    minted, failures = [], []
    for name in names:
        src = os.path.join(originals, name)
        if not os.path.isfile(src):
            failures.append((name, "original absent (NON-REPO fence: is the folder present?)"))
            continue
        try:
            with warnings.catch_warnings():
                warnings.simplefilter("ignore")
                im = Image.open(src)
                icc = im.info.get("icc_profile")
                im = im.convert("RGB")
                if icc:                      # convert TO sRGB rather than dropping the profile
                    try:
                        src_p = ImageCms.ImageCmsProfile(io.BytesIO(icc))
                        im = ImageCms.profileToProfile(im, src_p, ImageCms.createProfile("sRGB"),
                                                       outputMode="RGB")
                    except Exception as exc:                     # noqa: BLE001
                        failures.append((name, "ICC->sRGB conversion failed: %r "
                                               "(NOT silently shipped)" % exc))
                        continue
                w, h = im.size
                scale = MAX_EDGE / float(max(w, h))
                if scale < 1:
                    im = im.resize((max(1, round(w * scale)), max(1, round(h * scale))),
                                   Image.LANCZOS)
                out = os.path.join(out_dir, derivative_name(name))
                for q in QUALITY_LADDER:
                    im.save(out, "JPEG", quality=q, optimize=True, progressive=True)
                    if os.path.getsize(out) <= TARGET_KB * 1024:
                        break
                size = os.path.getsize(out)
                minted.append({"original": name, "derivative": os.path.basename(out),
                               "width": im.size[0], "height": im.size[1],
                               "bytes": size, "kb": round(size / 1024.0, 1), "quality": q,
                               "over_target": size > TARGET_KB * 1024})
        except Exception as exc:                                 # noqa: BLE001
            failures.append((name, repr(exc)))
    return minted, failures


# ---------------------------------------------------------------- emit
def write_md(rows, failures, path=MD_OUT):
    have_desc = sum(1 for r in rows if r["exif_description"])
    have_lic = sum(1 for r in rows if r["licence_source"])
    have_deriv = sum(1 for r in rows if r["derivative"])
    L = []
    A = L.append
    A("# Photography manifest — the committed surface for NON-REPO originals")
    A("")
    A("**Generated** by `knowledge/_build_photo_manifest.py --manifest`. Do not hand-edit: "
      "regenerate. **Ruling in force `s217-D1`** — originals stay NON-REPO behind the #211 "
      "`.gitignore` fence at `knowledge/assets/photography/`; this manifest plus the web-sized "
      "derivatives in `knowledge/assets/photography-web/` are the committed surface. A hosted "
      "cloud image store is NOTED FOR THE FUTURE by that ruling, not designed for here.")
    A("")
    A("## Measured coverage (a count is not a measurement — these are counted rows over the real population)")
    A("")
    A("| measure | value |")
    A("|---|---|")
    A("| originals scanned | %d |" % len(rows))
    A("| unreadable (declared residual) | %d |" % len(failures))
    A("| EXIF description present | %d / %d (%.1f%%) |"
      % (have_desc, len(rows), 100.0 * have_desc / max(1, len(rows))))
    A("| licence source derived | %d / %d (%.1f%%) |"
      % (have_lic, len(rows), 100.0 * have_lic / max(1, len(rows))))
    A("| committed web derivative | %d / %d |" % (have_deriv, len(rows)))
    A("")
    if failures:
        A("### Unreadable files (LOUD AND NAMED)")
        A("")
        for n, e in failures:
            A("- `%s` — %s" % (n, e))
        A("")
    A("## What is NOT here (declared, not omitted)")
    A("")
    A("- **No tags, keywords or categories.** The tagging approach is UNRULED (#211 owed item 3); "
      "EXIF description text is copied verbatim and nothing is inferred from it.")
    A("- **No KG nodes or edges.** What a KG mapping would need is priced in "
      "`knowledge/_PHOTOGRAPHY-KG-NOTE.md`, not built.")
    A("- **No preference ordering.** The photos carrying derivatives are SPECIMEN PICKS for the "
      "Image-block and Carousel pages; picking a specimen is not a ruling and Dave swaps by eye.")
    A("")
    A("## Rows")
    A("")
    A("`UNKNOWN` means the field is absent on the file — it is never defaulted. `derivative` names "
      "the committed web-sized file in `knowledge/assets/photography-web/`, or `—` where the "
      "original has no derivative (s217-D1: USED photos only).")
    A("")
    A("| # | filename | px | orient | EXIF description (verbatim) | licence source | basis | derivative |")
    A("|---:|---|---|---|---|---|---|---|")
    for i, r in enumerate(rows, 1):
        d = (r["exif_description"] or "UNKNOWN").replace("|", "\\|")
        A("| %d | `%s` | %d×%d | %s | %s | %s | %s | %s |"
          % (i, r["filename"], r["width"], r["height"], r["orientation"], d,
             (r["licence_source"] or "UNKNOWN").replace("|", "\\|"),
             r["licence_source_basis"].replace("|", "\\|"),
             ("`%s`" % r["derivative"]) if r["derivative"] else "—"))
    A("")
    with open(path, "w", encoding="utf-8") as fh:
        fh.write("\n".join(L))
    return path


def load_manifest():
    if not os.path.isfile(JSON_OUT):
        raise ManifestError("no committed manifest at %s — run --manifest first." % JSON_OUT)
    with open(JSON_OUT, encoding="utf-8") as fh:
        return json.load(fh)


# ---------------------------------------------------------------- gate
def check(deriv_dir=DERIV_DIR, manifest=None, root=ROOT):
    """-> (orphans, tracked_originals). Both empty == clean."""
    man = manifest if manifest is not None else load_manifest()
    known = {r.get("derivative") for r in man["rows"] if r.get("derivative")}
    present = sorted(n for n in os.listdir(deriv_dir)
                     if not n.startswith(".") and n.lower().endswith((".jpg", ".jpeg"))) \
        if os.path.isdir(deriv_dir) else []
    orphans = [n for n in present if n not in known]
    missing = [n for n in sorted(known) if n not in present]
    try:
        tracked = subprocess.run(["git", "ls-files", "knowledge/assets/photography"],
                                 cwd=root, capture_output=True, text=True, check=True).stdout
    except Exception as exc:                                     # noqa: BLE001
        raise ManifestError("git ls-files could not run (%r) — the fence claim is UNCHECKED, "
                            "and an unchecked fence is not a fence." % exc)
    tracked_originals = [l for l in tracked.splitlines() if l.strip()]
    return orphans, missing, tracked_originals


def _selftest():
    import shutil, tempfile
    ok = True
    tmp = tempfile.mkdtemp(prefix="photoman-", dir=os.environ.get("TMPDIR", "/var/tmp"))
    try:
        man = load_manifest()
        d = os.path.join(tmp, "deriv")
        os.makedirs(d)
        # pass-arm — the live pair
        o, m, t = check(DERIV_DIR, man)
        print("  [1] live pair -> orphans=%d missing=%d tracked-originals=%d : %s"
              % (len(o), len(m), len(t), "PASS" if not (o or m or t) else "FAIL"))
        ok &= not (o or m or t)
        # fail-arm — an orphan derivative MUST be flagged
        open(os.path.join(d, "not-in-the-manifest-w1600.jpg"), "w").close()
        o2, _, _ = check(d, man)
        print("  [2] orphan derivative -> flagged=%s : %s"
              % (bool(o2), "PASS" if o2 else "FAIL"))
        ok &= bool(o2)
        # mutation-arm — strip one derivative from the manifest copy; its file MUST orphan
        mut = json.loads(json.dumps(man))
        hit = next((r for r in mut["rows"] if r.get("derivative")), None)
        if hit is None:
            print("  [3] mutation arm -> NO derivative rows exist : FAIL (gate cannot be tested)")
            ok = False
        else:
            hit["derivative"] = None
            o3, _, _ = check(DERIV_DIR, mut)
            print("  [3] manifest row removed -> its file orphans=%s : %s"
                  % (bool(o3), "PASS" if o3 else "FAIL"))
            ok &= bool(o3)
        # missing-arm — a manifest row with no file MUST be flagged
        _, m4, _ = check(d, man)
        print("  [4] empty deriv dir -> missing flagged=%s : %s"
              % (bool(m4), "PASS" if m4 else "FAIL"))
        ok &= bool(m4)
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
    print("\n%s" % ("✅ selftest PASS — the gate can fail, and fails on the right shapes"
                    if ok else "❌ selftest FAIL"))
    return 0 if ok else 1


# ---------------------------------------------------------------- main
def main(argv=None):
    ap = argparse.ArgumentParser(add_help=False)
    ap.add_argument("--manifest", action="store_true")
    ap.add_argument("--derivatives", nargs="*", default=None)
    ap.add_argument("--derivatives-from", default=None)
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--selftest", action="store_true")
    args = ap.parse_args(argv)

    if args.selftest:
        return _selftest()

    if args.check:
        orphans, missing, tracked = check()
        for n in orphans:
            print("✖ ORPHAN derivative (no manifest row): %s" % n)
        for n in missing:
            print("✖ MISSING derivative (manifest row names a file that is not there): %s" % n)
        for n in tracked:
            print("✖ ORIGINAL IS GIT-TRACKED — the s217-D1/#211 fence is BREACHED: %s" % n)
        if orphans or missing or tracked:
            print("❌ photo-manifest gate: %d orphan(s), %d missing, %d tracked original(s)"
                  % (len(orphans), len(missing), len(tracked)))
            return 1
        print("✅ photo-manifest gate: every derivative carries a row, every row has its file, "
              "no original is git-tracked.")
        return 0

    wanted = None
    if args.derivatives_from:
        with open(args.derivatives_from, encoding="utf-8") as fh:
            wanted = [l.strip() for l in fh if l.strip() and not l.startswith("#")]
    elif args.derivatives is not None:
        wanted = list(args.derivatives)

    if not args.manifest and wanted is None:
        print("nothing asked for — pass --manifest, --derivatives, --check or --selftest "
              "(--help for the contract).", file=sys.stderr)
        return 2

    rows, failures = scan()
    by_name = {r["filename"]: r for r in rows}

    # A re-scan must never DROP a derivative row already recorded — carry them forward first,
    # then let this run's mints overwrite their own rows only.
    if os.path.isfile(JSON_OUT):
        try:
            prev = {r["filename"]: r for r in load_manifest()["rows"]}
        except Exception:                                        # noqa: BLE001
            prev = {}
        for n, r in by_name.items():
            p = prev.get(n) or {}
            for k in ("derivative", "derivative_px", "derivative_bytes"):
                if p.get(k):
                    r[k] = p[k]

    minted = []
    if wanted is not None:
        unknown = [n for n in wanted if n not in by_name]
        if unknown:
            raise ManifestError("named originals are not in the folder: %s" % ", ".join(unknown))
        minted, mint_fail = mint(wanted)
        for m in minted:
            by_name[m["original"]]["derivative"] = m["derivative"]
            by_name[m["original"]]["derivative_px"] = "%dx%d" % (m["width"], m["height"])
            by_name[m["original"]]["derivative_bytes"] = m["bytes"]
        for n, e in mint_fail:
            print("✖ derivative NOT minted: %s — %s" % (n, e), file=sys.stderr)
            failures.append((n, "derivative: " + e))

    payload = {
        "_README": ("Committed manifest for the NON-REPO photography originals (W-93, s217-D1). "
                    "Generated by knowledge/_build_photo_manifest.py — do not hand-edit. "
                    "null means the field is ABSENT on the file: unknown is never defaulted."),
        "ruling": "s217-D1",
        "originals_path": "knowledge/assets/photography (NON-REPO — .gitignore, #211)",
        "derivatives_path": "knowledge/assets/photography-web (COMMITTED)",
        "derivative_spec": {"max_edge_px": MAX_EDGE, "target_kb": TARGET_KB,
                            "colour": "sRGB", "format": "progressive JPEG"},
        "counts": {
            "originals": len(rows),
            "unreadable": len(failures),
            "exif_description_present": sum(1 for r in rows if r["exif_description"]),
            "exif_copyright_present": sum(1 for r in rows if r["exif_copyright"]),
            "licence_source_derived": sum(1 for r in rows if r["licence_source"]),
            "derivatives": sum(1 for r in rows if r.get("derivative")),
        },
        "unreadable": [{"filename": n, "error": e} for n, e in failures],
        "rows": rows,
    }
    with open(JSON_OUT, "w", encoding="utf-8") as fh:
        json.dump(payload, fh, indent=1, ensure_ascii=False)
        fh.write("\n")
    write_md(rows, failures, MD_OUT)

    print("manifest: %d rows -> %s" % (len(rows), os.path.relpath(JSON_OUT, ROOT)))
    print("          %s" % os.path.relpath(MD_OUT, ROOT))
    print("EXIF description present: %d/%d" % (payload["counts"]["exif_description_present"], len(rows)))
    print("licence source derived  : %d/%d" % (payload["counts"]["licence_source_derived"], len(rows)))
    for m in minted:
        print("derivative: %-46s %5d x %-5d %6.1f KB q%d%s"
              % (m["derivative"], m["width"], m["height"], m["kb"], m["quality"],
                 "  ⚠ OVER TARGET" if m["over_target"] else ""))
    if failures:
        print("❌ %d file(s) could not be read/minted — DECLARED RESIDUAL:" % len(failures))
        for n, e in failures:
            print("   %s — %s" % (n, e))
        return 1
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except ManifestError as exc:
        print("❌ photo manifest could not run: %s" % exc, file=sys.stderr)
        sys.exit(2)
