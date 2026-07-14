#!/usr/bin/env python3
"""
_LIVE-STATE staleness gate (ADR-0007, lightweight-first slice) — the drift-killer.

WHY: context staleness = an unrecorded supersession edge (ADR-0007). A cold session once burned a
whole sitting reasoning from a retired artifact as if it were live; this session the ledger's own
"Last refreshed" stamp had silently drifted 5 days. The manual ledger retains state well but its
metadata rots quietly. This gate makes the hand-maintained `_LIVE-STATE.md` *trustworthy* by
checking it against reality — without the risky full-generation migration.

SCOPE (this slice = validate, not generate). Full generation of the LIVE/DEAD blocks from
front-matter edges is deferred; the value now is catching drift. Architected so the same parse can
later drive generation.

CHECKS (advisory — earns blocking by bite-test, ADR-0005 §5):
  1. Freshness drift   — `Last refreshed:` stamp vs the newest decision-bearing doc change
                         (git commit date, falling back to mtime). The exact bug we hit.
  2. Dead-node resurrection — a node listed in SUPERSEDED/DEAD that is still cited in the LIVE
                         section, or a tombstoned artifact still referenced (un-tombstoned) elsewhere.
  3. Tombstone consistency — each DEAD file entry actually exists AND carries a tombstone banner.
  4. Lifecycle contradiction — an ADR marked DEFERRED/superseded in its own audit banner but still
                         cited as current truth in the LIVE section.
  5. Orphan supersession edge — a DEAD "superseded-by X" whose X can't be found (ADR/§/file).

Writes `_LIVE-STATE-CHECK.md` + prints a summary. Non-zero exit = warning count (advisory in
_build_all.py; flip to blocking once it's been quiet for a few sessions).

Run:  python3 knowledge/_build_live_state.py
"""
import os, re, sys, subprocess, datetime

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
LIVE = os.path.join(ROOT, "_LIVE-STATE.md")
DECISIONS = os.path.join(ROOT, "docs", "decisions")
OUT = os.path.join(HERE, "_LIVE-STATE-CHECK.md")

TOMB_RE = re.compile(r"superseded|tombstone|retired|DEAD|do not build|do-not-build", re.I)
ADR_RE = re.compile(r"ADR-(\d{4})")
DATE_RE = re.compile(r"(\d{4})-(\d{2})-(\d{2})")
# file-ish tokens inside a bullet (paths + bare filenames)
FILE_RE = re.compile(r"`?([\w./-]+\.(?:md|html|json|py|css))`?")


def read(p):
    try:
        return open(p, encoding="utf-8").read()
    except Exception:
        return ""


def split_sections(md):
    """Return {section_title: body} keyed by '## ' headers."""
    secs, cur, buf = {}, "_preamble", []
    for line in md.splitlines():
        m = re.match(r"^##\s+(.*)", line)
        if m:
            secs[cur] = "\n".join(buf)
            cur, buf = m.group(1).strip(), []
        else:
            buf.append(line)
    secs[cur] = "\n".join(buf)
    return secs


def section(secs, *keywords):
    for k, v in secs.items():
        if all(kw.lower() in k.lower() for kw in keywords):
            return v
    return ""


def git_date(path):
    try:
        r = subprocess.run(["git", "-C", ROOT, "log", "-1", "--format=%cs", "--", path],
                           capture_output=True, text=True, timeout=8)
        s = r.stdout.strip()
        if s:
            return s
    except Exception:
        pass
    try:
        return datetime.date.fromtimestamp(os.path.getmtime(path)).isoformat()
    except Exception:
        return None


def bullets(body):
    out, cur = [], None
    for line in body.splitlines():
        if re.match(r"^\s*[-*]\s+", line):
            if cur is not None:
                out.append(cur)
            cur = line
        elif cur is not None and line.strip() and not line.startswith("#"):
            cur += " " + line.strip()
        elif cur is not None:
            out.append(cur)
            cur = None
    if cur is not None:
        out.append(cur)
    return out


def main():
    md = read(LIVE)
    if not md:
        print("no _LIVE-STATE.md found");  return 0
    secs = split_sections(md)
    live_body = section(secs, "LIVE")
    dead_body = section(secs, "SUPERSEDED") or section(secs, "DEAD")
    findings = []  # (severity, check, msg)

    # ---- 1. freshness drift ----
    m = re.search(r"Last refreshed:\s*(\d{4}-\d{2}-\d{2})", md)
    stamp = m.group(1) if m else None
    tracked = []
    if os.path.isdir(DECISIONS):
        tracked += [os.path.join(DECISIONS, f) for f in os.listdir(DECISIONS) if f.endswith(".md")]
    for f in os.listdir(HERE):
        if f.startswith("_") and (f.endswith(".md")) and "FINDINGS" in f.upper():
            tracked.append(os.path.join(HERE, f))
    tracked.append(os.path.join(HERE, "_FIXED-FLEX-CHARTER.md"))
    newest, newest_f = None, None
    for f in tracked:
        d = git_date(f)
        if d and (newest is None or d > newest):
            newest, newest_f = d, os.path.relpath(f, ROOT)
    if stamp and newest and newest > stamp:
        findings.append(("⚠", "freshness",
            f"`Last refreshed: {stamp}` is older than the newest decision-doc change "
            f"({newest}, `{newest_f}`). Refresh the stamp + reconcile the ledger."))
    elif not stamp:
        findings.append(("⚠", "freshness", "No `Last refreshed:` stamp found in the header."))

    # ---- parse DEAD entries ----
    dead_entries = []
    for b in bullets(dead_body):
        # The dead node is only what's LEFT of the supersession arrow; files to the RIGHT are the
        # LIVE replacement (superseder) and must NOT be treated as dead.
        left = re.split(r"→|superseded[ -]?by|superseded by|\bretired\b", b, maxsplit=1, flags=re.I)[0]
        right = b[len(left):]
        files = [x for x in FILE_RE.findall(left) if not x.endswith("_LIVE-STATE.md")]
        node = files[0] if files else left.strip("-* ").split("—")[0].strip()[:70]
        sup = None
        sm = re.search(r"(?:superseded[ -]?by|→\s*superseded by|by)\s+([^\(.]+)", right, re.I)
        if sm:
            sup = sm.group(1).strip()
        dead_entries.append({"raw": b, "node": node, "files": files, "sup": sup,
                             "tombstoned": bool(re.search(r"tombstone", b, re.I))})

    # ---- 2. dead-node resurrection (LIVE cites a dead node) ----
    for d in dead_entries:
        for f in d["files"]:
            base = os.path.basename(f)
            if base in live_body:
                findings.append(("⚠", "resurrection",
                    f"DEAD node `{base}` is cited in the LIVE section — live truth points at a "
                    f"superseded artifact."))

    # dead artifacts still referenced (un-tombstoned) elsewhere in the corpus
    dead_files = [os.path.basename(f) for d in dead_entries for f in d["files"] if f.endswith((".html", ".md"))]
    if dead_files:
        scan_dirs = [HERE, os.path.join(HERE, "_fitness-test")]
        for base in set(dead_files):
            hits = []
            for sd in scan_dirs:
                if not os.path.isdir(sd):
                    continue
                for fn in os.listdir(sd):
                    p = os.path.join(sd, fn)
                    if not os.path.isfile(p) or fn == "_LIVE-STATE-CHECK.md":
                        continue
                    if fn.endswith((".md", ".html")) and base in read(p) and fn != base:
                        body = read(p)
                        # only flag if the reference isn't itself marked dead near the mention
                        if not TOMB_RE.search(body[max(0, body.find(base) - 120): body.find(base) + 120]):
                            hits.append(os.path.relpath(p, ROOT))
            if hits:
                findings.append(("i", "reference",
                    f"DEAD artifact `{base}` is mentioned (no nearby tombstone) in: "
                    + ", ".join(f"`{h}`" for h in hits[:4]) + ("…" if len(hits) > 4 else "")))

    # ---- 3. tombstone consistency ----
    for d in dead_entries:
        for f in d["files"]:
            ap = os.path.join(ROOT, f) if not os.path.isabs(f) else f
            if not os.path.exists(ap):
                # try under knowledge/
                alt = os.path.join(HERE, f)
                ap = alt if os.path.exists(alt) else ap
            if not os.path.exists(ap):
                findings.append(("⚠", "tombstone", f"DEAD entry `{f}` — file not found (moved/renamed? edge is orphaned)."))
            elif not TOMB_RE.search(read(ap)[:1500]):
                findings.append(("⚠", "tombstone", f"DEAD file `{f}` exists but has NO tombstone banner in its first lines."))

    # ---- 4. lifecycle contradiction (ADR deferred/superseded but LIVE cites it) ----
    adr_state = {}
    if os.path.isdir(DECISIONS):
        for fn in sorted(os.listdir(DECISIONS)):
            if not fn.endswith(".md"):
                continue
            mnum = ADR_RE.search(fn)
            if not mnum:
                continue
            head = read(os.path.join(DECISIONS, fn))[:1600]
            aid = "ADR-" + mnum.group(1)
            state = "accepted"
            # lifecycle comes from the Status line, not stray 'superseded' mentions in prose
            sl = re.search(r"\*\*Status:\*\*\s*([^\n·|]+)", head)
            status_txt = (sl.group(1) if sl else "").lower()
            if "supersed" in status_txt or "retired" in status_txt:
                state = "superseded"
            # explicit audit-banner deferral (validation state), or a banner retiring THIS adr
            if re.search(r"\bDEFERRED\b|validation state\s*=\s*`?defer", head):
                state = "deferred"
            if re.search(aid + r"[^\n]{0,40}(superseded|retired)\b", head, re.I):
                state = "superseded"
            adr_state[aid] = state
    for adr in set(ADR_RE.findall(live_body)):
        aid = "ADR-" + adr
        st = adr_state.get(aid)
        if st in ("deferred", "superseded"):
            findings.append(("⚠", "lifecycle",
                f"LIVE section cites `{aid}` as current truth, but its own banner marks it **{st}**."))

    # ---- 5. orphan supersession edges ----
    known_files = set()
    for base_dir in (HERE, DECISIONS, os.path.join(HERE, "_fitness-test")):
        if os.path.isdir(base_dir):
            known_files.update(os.listdir(base_dir))
    for d in dead_entries:
        if d["sup"]:
            tgt = d["sup"]
            ok = ("§" in tgt or "ADR" in tgt or "git split" in tgt.lower()
                  or any(os.path.basename(x) in known_files for x in FILE_RE.findall(tgt))
                  or "GOOD-MORNING" in tgt or "charter" in tgt.lower())
            if not ok:
                findings.append(("i", "orphan-edge",
                    f"DEAD `{d['node']}` → superseded-by \"{tgt[:40]}\" — target not resolvable to a known ADR/§/file."))

    # ---- report ----
    warns = [f for f in findings if f[0] == "⚠"]
    infos = [f for f in findings if f[0] == "i"]
    L = ["# _LIVE-STATE staleness check", "",
         "*Generated by `_build_live_state.py` (ADR-0007 gate, advisory). Consistency only — "
         "**never implies validity** (a clean ledger is not a vouched one; see the audit banner in "
         "`_LIVE-STATE.md`).*", "",
         f"**{len(warns)} warning(s) · {len(infos)} note(s).** "
         + ("✅ ledger is internally consistent." if not warns else "⚠ drift detected — see below."),
         ""]
    by = {}
    for sev, chk, msg in findings:
        by.setdefault(chk, []).append((sev, msg))
    order = ["freshness", "resurrection", "lifecycle", "tombstone", "orphan-edge", "reference"]
    labels = {"freshness": "1 · Freshness drift", "resurrection": "2 · Dead-node resurrection",
              "tombstone": "3 · Tombstone consistency", "lifecycle": "4 · Lifecycle contradiction",
              "orphan-edge": "5 · Orphan supersession edge", "reference": "· Dead-artifact references (info)"}
    for chk in order:
        if chk in by:
            L.append(f"## {labels.get(chk, chk)}")
            for sev, msg in by[chk]:
                L.append(f"- {sev} {msg}")
            L.append("")
    if not findings:
        L.append("_Nothing flagged._")
    L += ["---",
          f"*Checked: {len(dead_entries)} DEAD entries · {len(adr_state)} ADRs · "
          f"LIVE section {len(bullets(live_body))} bullets.*"]
    open(OUT, "w", encoding="utf-8").write("\n".join(L) + "\n")

    print(f"_LIVE-STATE check: {len(warns)} warning(s), {len(infos)} note(s) -> "
          + os.path.relpath(OUT, ROOT))
    for sev, chk, msg in findings:
        print(f"  {sev} [{chk}] {re.sub(chr(96),'',msg)[:110]}")
    return len(warns)


if __name__ == "__main__":
    warns = main()
    # Advisory by default (ADR-0005 §5: earns blocking by bite-test). `--strict` exits with the
    # warning count so it can gate once it's proven quiet. _build_all.py runs it without --strict.
    sys.exit(warns if "--strict" in sys.argv else 0)
