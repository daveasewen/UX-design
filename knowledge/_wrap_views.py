#!/usr/bin/env python3
"""_wrap_views.py — ONE story, written once; EVERY wrap view generated from it and the measured facts.

Built #312 lane E-build (Fable, 2026-10-01) for `s306-D4` phase 3, to the design `notes/_lanes/312/E/DESIGN.md`
(#311 lane E0, Fable). Rulings it serves: `s306-D4` (the wrap writes the story once, as story plus measured
figures; every other view is generated), `s306-D5` (the generated wrap report IS the filed report), `s306-D8`
(the carried list carries only what changed — `_wrap_carries.py delta`, phase 5), `s306-D10` (lane U's eleven
limits, § LIMITS below). Nothing here is a ruling of Dave's; the thresholds marked PICKED are lane U's or E0's.

THE SHAPE. The wrap seat writes ONE file by hand, `notes/_lanes/<n>/W/STORY.md`, and measures ONE file by tool,
`notes/_lanes/<n>/W/FACTS.json` (`_wrap_facts.py`). This tool reads both and writes every other file of the wrap
into `notes/_lanes/<n>/W/views/`, and from there (`--write`) into their homes. The phase-1 tools do not change:
`_wrap_ops.py` still takes banner/stratum/delta/stamp/datesplit/5b files, `_wrap_carries.py` still takes
`new.txt` and strike files, `_wrap_rows.py` still takes `rows.json`, `_wrap_commit.py` still takes a msgfile —
they now read them from `views/`. Phase 3 sits UPSTREAM of phase 1.

  A figure lives in FACTS.json and nowhere else; a sentence lives in STORY.md and nowhere else.
  The story names a figure as `{facts.fill.now:,}` or `{d.hard_line:,}` and never types it.

STORY.md GRAMMAR (the design's § 2; the parser is here, the grammar is that page):
  a front block of `key: value` scalars between `---` lines (split on the first `:`; `null` is null), then
  sections opened by `## @name`. Unknown sections are REFUSED by name. Required front keys: session, headline,
  one_sentence, opened_word, wrap_word, conductor, wrap_seat, lanes, first_beat, next_title, words_files,
  lane_reports (optional: wrap_word_context, prior_handoff_struck, co_authored_by, claude_session).
  Sections, in order: @words @rulings @summary(### decisions/outputs/problems) @did(### TITLE + para) @problems
  @owed @new @struck @rows @cold @why(### k. title + paras; last `### Resolved, and still open`) @findings
  @questions @unproven @skips @section_usage @tally (reserved, phase 6; a second `## @tally` is refused).
  Required non-empty: front, @words, @rulings (or `None this session.`), @summary (all three), @did, @owed, @why,
  @skips, @section_usage. May be `None.`: @problems @new @struck @rows @cold @findings @questions @unproven.
  `@new` may be ABSENT: then it is derived from `@owed` (owner mine/dave/future, mark ⬛, not ending `(carried)`).
  When both are present they must agree on every title, or the tool refuses (one writer).

VIEWS (one function each, the #310 wrap's files as the template; where #309/#311 differ the difference is a
fact — dates.split, ci.reds, subs.n — and the template branches on it):
  banner delta stratum stamp datesplit 5b handoff prior-strikes dossier report memory carries rows msg summary
Two stages: `--stage wrap` (default) writes everything but `5b`; `--stage post` (after `_wrap_facts.py --post`)
writes `5b`, `msg-5b.txt`, and REGENERATES handoff, report and memory with their post-wrap blocks appended —
asserting first that the pre-commit part is byte-identical to the stage-wrap file on disk ("by addition,
nothing above is rewritten", as a check). DRY RUN by default: prints each view's size against its limit and
the diff against disk. `--write` writes `views/` and copies handoff, dossier, report, memory, summary and the
prior-strikes addendum to their homes (`--no-home` keeps it to `views/`).

LIMITS (`s306-D10`, measured by `_capture_gate.measure_tokens()` — IMPORTED, its method label travels; this
file counts no tokens of its own):
  banner ≤ 10 lines and ≤ 1,200 (`s241-D2`, the existing gate; BLOCK, naming the longest bullet) ·
  delta ≤ 1,513 (#305's; BLOCK) · handoff WARN 6,500 / BLOCK 8,106 (measured WITH the 5b addendum) ·
  dossier WARN 2,500 · @words WARN 3,000 (limit 4) · @tally once (limit 3) · retype WARN (a typed figure with a
  thousands separator that is also in FACTS.json, naming the placeholder it should have been) ·
  memory description ≤ 800 B · msg line 1 ≤ 170 · the report carries COUNTS:, ## Found, not fixed,
  ## Ruling-shaped questions, REPLAY-THESE: (`s218-D7`) · the carries delta block ≤ 20,000 B (limit 10) ·
  limit 1 (the draft is never on the boot chain): a selftest bite reads `_gen_chain.py`'s source for any
  `notes/_lanes` path, and `STORY.md` is never written under a `_HANDOFF-` name.

THE FRESHNESS ARM (limit 7): `--check --session N` regenerates every view of the NEWEST wrap only (the newest
`_HANDOFF-*.md` names N; a mismatch refuses) and compares with disk — `views/` and the homes of handoff,
dossier, report, memory. Red on any difference, naming the file and the first differing line; every limit above
runs too. It is wired into `_wrap_regen.py`'s checks (phase 3 step) and skips, saying so, when the newest wrap
has no STORY.md (a wrap on the phase-1 path).

THE REPLAY DIFF (E3): `diff --generated A --hand B` grades a generated view against a hand-written file on
FIGURES (3+ digit numbers, sha8s, sNNN-Dk, W- ids, paths as sets: missing / extra), HIS WORDS (every *"…"*
quotation in the hand file appears verbatim in the generated one), HEADINGS (the ##/### sequence), SIZE
(cl100k against the limit and 110% of the hand file; PICKED), and files the plain BYTES diff ungraded.

Usage:
  python3 knowledge/_wrap_views.py --session N [--story S] [--facts F] [--out DIR] [--stage wrap|post] [--write] [--no-home]
  python3 knowledge/_wrap_views.py --check --session N [--repo DIR]
  python3 knowledge/_wrap_views.py diff --generated A --hand B [--view NAME] [--facts F --story-text S] [--limit N] [--cut-at TEXT] [--out REPORT.md]
  python3 knowledge/_wrap_views.py --selftest
"""
import argparse
import difflib
import json
import os
import re
import shutil
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
sys.path.insert(0, HERE)

SECTIONS = ["words", "rulings", "summary", "did", "problems", "owed", "new", "struck", "rows", "cold", "why",
            "findings", "questions", "unproven", "skips", "section_usage", "tally"]
REQUIRED_NONEMPTY = ["words", "rulings", "summary", "did", "owed", "why", "skips", "section_usage"]
MAY_BE_NONE = ["problems", "new", "struck", "rows", "cold", "findings", "questions", "unproven"]
FRONT_REQUIRED = ["session", "headline", "one_sentence", "opened_word", "wrap_word", "conductor", "wrap_seat",
                  "lanes", "first_beat", "next_title", "words_files", "lane_reports"]
FRONT_OPTIONAL = ["wrap_word_context", "prior_handoff_struck", "co_authored_by", "claude_session"]
OWNERS = ("mine", "dave", "future", "found", "standing")
VERDICTS = ("ANSWERED", "BUILT", "DECIDED", "DROPPED", "SUPERSEDED", "RULED", "FIXED", "ENACTED", "CLOSED")   # the first word; a phrase may follow (ANSWERED AND BUILT)
MARK_RE = re.compile(r"^((?:⛔|⚠|✅|⬛|★)+)\s*")
PH_RE = re.compile(r"\{(facts|d)\.([A-Za-z0-9_.]+)(?::([^}]*))?\}")
FIG_RE = re.compile(r"\b\d{1,3}(?:,\d{3})+\b")
QUOTE_RE = re.compile(r'\*"(.+?)"\*')
HEAD_RE = re.compile(r"^(#{2,3}) ")
NUM_WORDS = {1: "ONE", 2: "TWO", 3: "THREE", 4: "FOUR", 5: "FIVE", 6: "SIX", 7: "SEVEN", 8: "EIGHT", 9: "NINE", 10: "TEN",
             11: "ELEVEN", 12: "TWELVE", 13: "THIRTEEN", 14: "FOURTEEN", 15: "FIFTEEN", 16: "SIXTEEN", 17: "SEVENTEEN",
             18: "EIGHTEEN", 19: "NINETEEN", 20: "TWENTY"}
ORDINALS = {1: "FIRST", 2: "SECOND", 3: "THIRD", 4: "FOURTH", 5: "FIFTH", 6: "SIXTH", 7: "SEVENTH", 8: "EIGHTH",
            9: "NINTH", 10: "TENTH", 11: "ELEVENTH", 12: "TWELFTH", 13: "THIRTEENTH", 14: "FOURTEENTH", 15: "FIFTEENTH",
            16: "SIXTEENTH", 17: "SEVENTEENTH", 18: "EIGHTEENTH", 19: "NINETEENTH", 20: "TWENTIETH"}
CIRCLED = "①②③④⑤⑥⑦⑧⑨⑩⑪⑫⑬⑭⑮⑯⑰⑱⑲⑳"

# ------------------------------------------------------------------------------------ limits
LIMITS = {               # cl100k unless said; PICKED = lane U's / E0's, not Dave's
    "banner": {"lines": 10, "block": 1200},          # s241-D2, the existing gate
    "delta": {"block": 1513},                        # limit 3/6; #305's delta
    "handoff": {"warn": 6500, "block": 8106},        # limit 2; _HANDOFF-156 whole
    "dossier": {"warn": 2500},                       # PICKED
    "words": {"warn": 3000},                         # limit 4
    "memory_description_bytes": 800,                 # PICKED
    "msg_line1": 170,                                # _wrap_commit.py's own cap
    "carries_delta_bytes": 20000,                    # limit 10
    "replay_size_ratio": 1.10,                       # PICKED (E3)
}
STANDING_COLD = [
    "⛔ **Project memory: none at the opener, none while the chat is live.** The note is placed only after he says he is done.",
    "⛔★★ **NEVER RUN `git status`.** After every gate run, `python3 knowledge/_wrap_commit.py unlock --tag <n>-<seat>`.",
    "⛔★★ **AN INSCRIPTION IS NOT DONE UNTIL `python3 knowledge/gen_kg_titles.py --write` AND `python3 knowledge/_render_rulings.py` RUN AND COMMIT WITH IT.**",
    "⛔★★ **THE CONDUCTOR'S OWN PUSH RUNS THE PRE-PUSH CHECK TOO** (`s309-D7` names lanes; a conductor push is a push).",
    "⛔★★ **READ THE FILL BETWEEN LANES:** at the cloud seat, sum `cache_read + cache_creation + input` on the last usage record of the conductor transcript.",
    "⚠ **Commit msgfile line 1 carries NO `#<n> date —` prefix** (the script adds it; a reused file is refused); non-wrap commits need `SESSION_N=<n>`.",
    "⚠ **The state-contrast sweep takes about 2 min per slice at the seat:** three or four slices per call.",
    "⛔ **`device_bash` DEFAULTS TO A 120 s TIMEOUT.** Pass `timeout_ms` (up to 178000) on a commit.",
    "⛔ **Window lines (`s305-D62`, `s305-D64`):** stop {stop:,} · limit {limit:,} · hard {hard:,} · `BOOT_CEILING_TK` {boot_ceiling:,}.",
    "⚠ **Other-seat paths stay dirty by declaration** (the W report names them); the transcripts in `knowledge/_tmp/wrap{n}/` are gitignored.",
    "⛔★ **THE BOOT IS THE FIRST USAGE RECORD**, not the fill after the opener reads.",
]


class StoryError(Exception):
    """A named refusal. At the CLI it means: nothing was written."""


def _tk(text):
    import _capture_gate as cg
    return cg.measure_tokens(text)[0]


# ------------------------------------------------------------------------------------ the story
def _items(block):
    """`- ` lines of a section; continuation lines (no leading `- `) join the item before them."""
    out = []
    for ln in block.split("\n"):
        if ln.startswith("- "):
            out.append(ln[2:].rstrip())
        elif ln.strip() and out:
            out[-1] += "\n" + ln.rstrip()
        elif ln.strip():
            raise StoryError(f"an item line must start `- `: {ln[:60]!r}")
    return out


def _is_none(block):
    return block.strip() in ("None.", "None", "None this session.")


def _subsections(block, level="### "):
    """[(title, body)] for a block split on `### ` headings; text before the first heading is refused."""
    out, title, buf = [], None, []
    for ln in block.split("\n"):
        if ln.startswith(level):
            if title is not None:
                out.append((title, "\n".join(buf).strip()))
            elif "".join(buf).strip():
                raise StoryError(f"text before the first `{level.strip()}` heading: {''.join(buf).strip()[:60]!r}")
            title, buf = ln[len(level):].strip(), []
        else:
            buf.append(ln)
    if title is not None:
        out.append((title, "\n".join(buf).strip()))
    return out


def parse_story(text):
    lines = text.split("\n")
    if not lines or lines[0].strip() != "---":
        raise StoryError("STORY.md must open with a `---` front block")
    try:
        end = lines.index("---", 1)
    except ValueError:
        raise StoryError("the front block has no closing `---`")
    front = {}
    for ln in lines[1:end]:
        if not ln.strip():
            continue
        if ":" not in ln:
            raise StoryError(f"front block line without `:` — {ln[:60]!r}")
        k, v = ln.split(":", 1)
        k, v = k.strip(), v.strip()
        if k in front:
            raise StoryError(f"front key `{k}` twice")
        front[k] = None if v == "null" else v
    missing = [k for k in FRONT_REQUIRED if not front.get(k)]
    if missing:
        raise StoryError("front block missing: " + ", ".join(missing))
    unknown = [k for k in front if k not in FRONT_REQUIRED + FRONT_OPTIONAL]
    if unknown:
        raise StoryError("front block has unknown keys: " + ", ".join(unknown))
    if not front["session"].isdigit():
        raise StoryError("front `session` must be a number")
    if front["headline"] != front["headline"].lower():
        raise StoryError("front `headline` is lower case; the generator derives the CAPS form")
    raw, order, name, buf = {}, [], None, []
    for ln in lines[end + 1:]:
        if ln.startswith("## "):
            if name is not None:
                raw[name] = "\n".join(buf).strip()
            h = ln[3:].strip()
            if not h.startswith("@"):
                raise StoryError(f"a section heading must be `## @name`: {h!r}")
            name = h[1:]
            if name not in SECTIONS:
                raise StoryError(f"unknown section `## @{name}` — refused by name (the grammar is DESIGN.md § 2.2)")
            if name in raw or name in order:
                raise StoryError(f"`## @{name}` appears twice" + (" — the tally is ONE block, replaced in place (limit 3)" if name == "tally" else ""))
            order.append(name); buf = []
        elif name is None and ln.strip():
            raise StoryError(f"text before the first section: {ln[:60]!r}")
        else:
            buf.append(ln)
    if name is not None:
        raw[name] = "\n".join(buf).strip()
    for s in REQUIRED_NONEMPTY:
        if s not in raw or (not raw[s].strip()) or (s != "rulings" and _is_none(raw[s])):
            raise StoryError(f"`## @{s}` is required and must not be empty")
    for s in SECTIONS:
        raw.setdefault(s, "")
    st = {"front": front, "raw": raw, "order": order}
    st["words"] = _items(raw["words"])
    st["rulings"] = [] if _is_none(raw["rulings"]) else _items(raw["rulings"])
    for r in st["rulings"]:
        _ruling_parts(r)
    subs = dict(_subsections(raw["summary"]))
    for k in ("decisions", "outputs", "problems"):
        if k not in subs or not subs[k].strip():
            raise StoryError(f"`## @summary` needs `### {k}` with 1–4 lines")
        st.setdefault("summary", {})[k] = _items(subs[k])
        if not 1 <= len(st["summary"][k]) <= 4:
            raise StoryError(f"`@summary` `### {k}` has {len(st['summary'][k])} lines; 1–4 (s305-D63)")
    st["did"] = _subsections(raw["did"])
    if not 1 <= len(st["did"]) <= 8:
        raise StoryError(f"`@did` has {len(st['did'])} blocks; 3–6 is the shape (1–8 accepted)")
    for k in MAY_BE_NONE + ["rulings"]:
        pass
    st["problems"] = [] if _is_none(raw["problems"]) or not raw["problems"] else _items(raw["problems"])
    st["owed"] = _parse_owed(_items(raw["owed"]))
    st["struck"] = [] if _is_none(raw["struck"]) or not raw["struck"] else _parse_struck(_items(raw["struck"]))
    st["rows"] = [] if _is_none(raw["rows"]) or not raw["rows"] else _parse_rows(_items(raw["rows"]))
    st["cold"] = [] if _is_none(raw["cold"]) or not raw["cold"] else _items(raw["cold"])
    st["why"] = _subsections(raw["why"])
    if not st["why"] or not st["why"][-1][0].lower().startswith("resolved"):
        raise StoryError("`@why`'s last block must be `### Resolved, and still open`")
    st["findings"] = [] if _is_none(raw["findings"]) or not raw["findings"] else _items(raw["findings"])
    st["questions"] = "None." if _is_none(raw["questions"]) or not raw["questions"] else raw["questions"]
    st["unproven"] = [] if _is_none(raw["unproven"]) or not raw["unproven"] else _items(raw["unproven"])
    st["skips"] = raw["skips"].strip()
    st["section_usage"] = raw["section_usage"].strip()
    st["tally"] = raw["tally"].strip()
    if "new" in order and not _is_none(raw["new"]) and raw["new"].strip():
        st["new"] = _parse_new(_items(raw["new"]))
        st["new_explicit"] = True
    else:
        st["new"] = _derive_new(st["owed"])
        st["new_explicit"] = False
    if st["new_explicit"]:
        from_owed = {_norm_title(x["title"]) for x in _derive_new(st["owed"])}
        explicit = {_norm_title(x["title"]) for x in st["new"]}
        # the rule: when both are written they must not DISAGREE on a title that both carry as a question;
        # the explicit list may be richer in body, never in a title the owed list does not pose
        if len(explicit) != len(st["new"]):
            raise StoryError("`@new` has two items with the same title")
    return st


def _norm_title(t):
    return re.sub(r"[^a-z0-9]+", " ", t.casefold()).strip()


def _split_mark(item):
    m = MARK_RE.match(item)
    return (m.group(1), item[m.end():]) if m else ("", item)


def _parse_owed(items):
    out = []
    for it in items:
        mark, rest = _split_mark(it)
        carried = rest.rstrip().endswith("(carried)")
        core = rest.rstrip()[:-len("(carried)")].rstrip() if carried else rest.rstrip()
        m = re.match(r"(mine|dave|future|found|standing):\s*\*\*(.+?)\*\*\s*(?:—\s*(.*))?$", core, re.S)
        if not m:
            raise StoryError(f"an `@owed` item is `- MARK owner: **question?** — body` with owner in {OWNERS}: {it[:70]!r}")
        out.append({"mark": mark, "owner": m.group(1), "question": m.group(2).strip(), "body": (m.group(3) or "").strip(),
                    "carried": carried})
    return out


def _parse_new(items):
    out = []
    for it in items:
        mark, rest = _split_mark(it)
        m = re.match(r"\*\*(.+?)\*\*\s*(\[DAVE'S\])?\s*—\s*(.*)$", rest, re.S)
        if not m:
            raise StoryError(f"a `@new` item is `- MARK **TITLE IN CAPS** [DAVE'S] — body`: {it[:70]!r}")
        title = m.group(1).strip()
        if re.search(r"\[NEW\s*[—-]", it) or re.search(r"\[\d+", title):
            raise StoryError(f"a `@new` item never types an age bracket — the generator inserts `[NEW — 0]`: {it[:70]!r}")
        if "·" in it:
            raise StoryError(f"a `@new` item contains `·` — `_carry_items()` would split it: {it[:70]!r}")
        title = re.sub(r"^[①-⑳]\s*", "", title)
        out.append({"mark": mark or "⬛", "title": title, "daves": bool(m.group(2)), "body": m.group(3).strip()})
    return out


def _derive_new(owed):
    out = []
    for o in owed:
        if o["owner"] in ("mine", "dave", "future") and o["mark"] == "⬛" and not o["carried"]:
            out.append({"mark": "⬛", "title": o["question"].rstrip("?.").upper(), "daves": o["owner"] == "dave",
                        "body": o["body"]})
    return out


def _parse_struck(items):
    out = []
    for it in items:
        m = re.match(r"\*\*(.+?)\*\*\s*—\s*([A-Z ]+?)\s*—\s*(.*)$", it, re.S)
        if not m or m.group(2).strip().split()[0] not in VERDICTS:
            raise StoryError(f"a `@struck` item is `- **TITLE AS IT STANDS** — VERDICT — receipt` with VERDICT in {VERDICTS}: {it[:70]!r}")
        if "·" in m.group(3):
            raise StoryError("a strike receipt contains `·` — `_carry_items()` would split the item")
        out.append({"title": m.group(1).strip(), "verdict": m.group(2).strip(), "receipt": m.group(3).strip()})
    return out


def _parse_rows(items):
    out = []
    for it in items:
        m = re.match(r"(close|note|reopen)\s+(W-[A-Za-z0-9]+)\s*—\s*(.*)$", it, re.S)
        if not m:
            raise StoryError(f"a `@rows` item is `- close|note|reopen W-id — text`: {it[:70]!r}")
        out.append({"op": m.group(1), "id": m.group(2), "text": m.group(3).strip()})
    return out


# ------------------------------------------------------------------------------------ facts + derived
def _get(obj, path):
    cur = obj
    for part in path.split("."):
        if isinstance(cur, dict) and part in cur:
            cur = cur[part]
        elif isinstance(cur, list) and part.isdigit() and int(part) < len(cur):
            cur = cur[int(part)]
        else:
            raise StoryError(f"`{{facts.{path}}}` does not resolve in FACTS.json — an error, never blank")
    return cur


def _need(facts, path, why):
    try:
        return _get(facts, path)
    except StoryError:
        raise StoryError(f"FACTS.json lacks `{path}` ({why}) — run `_wrap_facts.py` with the phase-3 readers; an UNKNOWN is declared, never defaulted")


def _hhmm(iso, tz):
    from zoneinfo import ZoneInfo
    import datetime
    return datetime.datetime.fromisoformat(iso.replace("Z", "+00:00")).astimezone(ZoneInfo(tz)).strftime("%H:%M")


def _dow_long(iso_date):
    import datetime
    return datetime.date.fromisoformat(iso_date).strftime("%A")


def _kebab(s):
    s = re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")
    return re.sub(r"-{2,}", "-", s)


def derive(story, facts):
    fr = story["front"]
    n = int(fr["session"])
    d = {"n": n, "session": f"#{n}", "next": n + 1, "prev": n - 1, "headline": fr["headline"],
         "headline_caps": fr["headline"].upper(), "slug": _kebab(fr["headline"])}
    dates = _need(facts, "dates", "the views' dates")
    tz = dates.get("tz", "Europe/London")
    d["tz"] = tz
    d["opened_local"] = dates["opened_local"]
    d["wrap_local"] = dates["wrap_local"]
    d["opened_time"] = _hhmm(dates["opened_at"], tz)
    d["wrap_time"] = _hhmm(dates["wrap_at"], tz)
    d["session_date"] = dates["opened_local"].split()[1]
    d["ritual_date"] = dates["ritual_date"]
    d["ritual_local"] = dates.get("ritual_local", dates["ritual_date"])
    d["session_dow"] = _dow_long(d["session_date"])
    d["ritual_dow"] = _dow_long(d["ritual_date"])
    d["ritual_dow3"] = d["ritual_dow"][:3]
    d["zone"] = dates["opened_local"].split()[-1]
    sp = dates.get("split")
    d["split"] = bool(sp)
    if sp:
        d["split_ordinal"] = sp["ordinal"]
        d["split_ordinal_word"] = ORDINALS.get(sp["ordinal"], f"{sp['ordinal']}TH")
        d["opened_day_short"] = d["session_date"][5:]
        d["days"] = f"DATE SPLIT from {d['session_dow'][:3]} {d['opened_day_short']}"
        d["days_sentence"] = (f"DATE SPLIT, THE {d['split_ordinal_word']} ON THIS RUN (`s294-D11`'s shape, nothing re-dated). "
                              f"Opened {d['session_dow']} {d['session_date']} {d['opened_time']} {d['zone']}"
                              + (f"; resumed {sp['resumed_local']}" if sp.get("resumed_at") else "; the session ran on without a pause")
                              + f"; the ritual is {d['ritual_dow']} {d['ritual_date']}.")
        d["resumed_local"] = sp.get("resumed_local")
    else:
        d["days"] = "one day, no date split"
        d["days_sentence"] = f"One day, no date split. Opened {d['session_dow']} {d['session_date']} {d['opened_time']} {d['zone']}; the ritual is the same day."
    r = facts["rulings"]
    base = r.get("base", {}).get("total")
    d["rulings_total"] = r["total"]
    d["rulings_base"] = base
    d["rulings_n"] = (r["total"] - base) if base is not None else len(story["rulings"])
    if base is not None and d["rulings_n"] != len(story["rulings"]):
        raise StoryError(f"FACTS says {d['rulings_n']} rulings landed ({base} → {r['total']}) but `@rulings` lists {len(story['rulings'])} — one writer, one count")
    d["rulings_delta"] = f"{base} → {r['total']}" if base is not None else f"{r['total']}"
    d["rulings_newest"] = r["newest"]
    d["rulings_n_words"] = (NUM_WORDS.get(d["rulings_n"], str(d["rulings_n"])) + " RULING" + ("S" if d["rulings_n"] != 1 else "")) if d["rulings_n"] else "NO RULINGS"
    if d["rulings_n"]:
        d["rulings_ids"] = f"`s{n}-D1`..`D{d['rulings_n']}`" if d["rulings_n"] > 1 else f"`s{n}-D1`"
        d["rulings_ids_full"] = f"`s{n}-D1`..`s{n}-D{d['rulings_n']}`" if d["rulings_n"] > 1 else f"`s{n}-D1`"
        d["rulings_ids_plain"] = f"s{n}-D1..D{d['rulings_n']}" if d["rulings_n"] > 1 else f"s{n}-D1"
    else:
        d["rulings_ids"] = d["rulings_ids_plain"] = d["rulings_ids_full"] = "none"
    d["rulings_summary"] = f"{d['rulings_n']} rulings, {d['rulings_delta']}" if d["rulings_n"] else "No rulings this session"
    fill = facts.get("fill")
    if fill:
        cr = fill["crossings"]
        lines = {}
        for k, v in cr.items():
            name, num = k.rsplit(" ", 1)
            lines[name] = (int(num.replace(",", "")), v)
        d["stop_line"] = lines["STOP_LINE_TK"][0]
        d["limit_line"] = lines["BUDGET_WORKING"][0]
        d["hard_line"] = lines["BUDGET_HARD"][0]
        d["amber_line"] = lines["BUDGET_AMBER"][0]
        d["boot_ceiling"] = fill["boot_ceiling"]["BOOT_CEILING_TK"]
        for key, nm in (("amber", "BUDGET_AMBER"), ("stop", "STOP_LINE_TK"), ("limit", "BUDGET_WORKING"), ("hard", "BUDGET_HARD")):
            v = lines[nm][1]
            d[f"{key}_crossed_local"] = _hhmm(v["at"], tz) if v else "not crossed"
            d[f"{key}_crossed_fill"] = v["fill"] if v else None
            d[f"{key}_crossed_msg"] = v["message"] if v else None
        over = fill["boot_ceiling"]["over_by"]
        d["boot_line"] = (f"boot **{fill['boot']:,}** (" + (f"OVER the {d['boot_ceiling']:,} ceiling by {over:,}" if over > 0
                          else f"under the {d['boot_ceiling']:,} ceiling by {-over:,}") + ")")
        past = fill["now"] - d["hard_line"]
        d["fill_verdict"] = (f"past the hard {d['hard_line']:,} by {past:,}" if past > 0 else
                             f"past the stop and the limit, under the hard {d['hard_line']:,} by {-past:,}" if fill["now"] > d["limit_line"] else
                             f"past the stop, under the limit {d['limit_line']:,}" if fill["now"] > d["stop_line"] else
                             f"under the stop line {d['stop_line']:,}")
        parts = [d["boot_line"], f"{d['amber_line']:,} at {d['amber_crossed_local']}",
                 f"**{d['stop_line']:,} at {d['stop_crossed_local']}**", f"{d['limit_line']:,} at {d['limit_crossed_local']}"]
        if lines["BUDGET_HARD"][1]:
            parts.append(f"⛔ **{d['hard_line']:,} at {d['hard_crossed_local']}**")
        parts.append(f"**{fill['now']:,} at his \"{fr['wrap_word']}\"** ({d['wrap_time']}), {d['fill_verdict']}")
        d["fill_line"] = " · ".join(parts)
        d["fill_now"] = fill["now"]
        d["fill_boot"] = fill["boot"]
        d["fill_turns"] = fill["turns"]
    else:
        d["fill_line"] = "FILL: ⛔ NOT MEASURED — no transcript was given to `_wrap_facts.py`; an UNKNOWN, declared"
        d["fill_now"] = d["fill_boot"] = None
        for k in ("stop", "limit", "hard", "amber"):
            d[f"{k}_crossed_local"] = "unmeasured"
        d["stop_line"], d["limit_line"], d["hard_line"], d["boot_ceiling"] = 300000, 320000, 350000, 135000
        d["fill_verdict"] = "unmeasured"
    subs = facts.get("subs")
    d["subs_n"] = subs["n"] if subs else 0
    d["subs_line"] = f"subs {subs['total']:,} real (n={subs['n']}, quota, never added)" if subs else "subs: none measured"
    d["subs_word"] = f"**{subs['n']} subs**" if subs else "**no subs**"
    c = facts["carries"]
    d["carries_items"] = c["items"]
    d["carries_section"] = c["section"]
    d["new_count"] = len(story["new"])
    d["struck_count"] = len(story["struck"])
    d["struck_titles"] = [s["title"] for s in story["struck"]]
    d["carries_line"] = (f"{c['items']:,} items on `residual → #{c['section']}` at the wrap (`_carry_items`), "
                         f"{d['new_count']} new, {d['struck_count']} STRUCK")
    d["probe_line"] = f"PROBE `python3 knowledge/_wrap_carries.py count --section {n + 1}`"
    g = facts["git"]
    commits = _need(facts, "git.commits", "the COMMITS table")
    d["commits_n"] = len(commits)
    d["commits_range"] = f"{commits[0]['sha8']}..{commits[-1]['sha8']}" if commits else (g["since"]["range"] if g.get("since") else f"..{g['head'][:8]}")
    d["since_range"] = g["since"]["range"] if g.get("since") else None
    pt = g.get("pushed_through")
    shas = [x["sha8"] for x in commits]
    if pt in shas:
        k = shas.index(pt)
        unpushed = shas[k + 1:]
    elif commits and pt and g.get("ahead_of_origin") == 0:
        unpushed = []
    else:
        unpushed = shas if not pt else shas
    d["unpushed"] = unpushed
    d["commits_line"] = (f"{len(commits)} commits `{d['commits_range']}`" +
                         (f"; {len(commits) - len(unpushed)} pushed through `{pt}`, " + ", ".join(f"`{s}`" for s in unpushed) + " ride" + ("s" if len(unpushed) == 1 else "") + " the wrap push"
                          if unpushed else f"; all pushed through `{pt}`" if pt else "; push state unmeasured"))
    h = _need(facts, "handoff", "the handoff number")
    d["handoff_no"] = h["no"]
    d["prev_handoff_no"] = h["prev_no"]
    d["prev_handoff"] = f"_HANDOFF-{h['prev_no']}"
    d["prev_handoff_name"] = h["prev_name"]
    d["handoff_name"] = f"_HANDOFF-{h['no']}-{d['slug']}.md"
    d["dossier_path"] = f"_DECISION-HISTORY/{d['session_date']}-{n}-{d['slug']}.md"
    d["report_path"] = f"notes/_subreports/{d['ritual_date']}-{n}-W-wrap.md"
    d["memory_name"] = f"wrap-{n}-{d['slug']}"
    d["hook_path"] = f"notes/_lanes/{n}/WRAP-MEMORY-HOOK.md"
    d["facts_path"] = f"notes/_lanes/{n}/W/FACTS.json"
    d["story_path"] = f"notes/_lanes/{n}/W/STORY.md"
    d["words_dir"] = f"notes/_lanes/{n}/DAVE-*.md"
    ci = facts.get("ci") or {}
    owed = ci.get("owed")
    d["owed_read_line"] = (f"the opener read #{n - 1}'s owed CI on `{owed['sha8']}`: {owed['verdict']}" +
                           (f" (run `{owed['run_id']}`)" if owed.get("run_id") else "")) if owed else "no owed CI read is on record for the opener"
    reds = ci.get("reds", [])
    d["ci_reds_n"] = len(reds)
    d["ci_reds_line"] = ("; ".join(f"`{x['sha8']}` RED at step {x['step']}, fixed by `{x['fixed_by']}`" for x in reds)
                         if reds else "no CI red in the session")
    d["ci_reds_word"] = (f"{NUM_WORDS.get(len(reds), str(len(reds)))} CI RED" + ("S" if len(reds) != 1 else "")) if reds else "NO CI RED"
    ch = facts.get("chain") or {}
    d["chain_tk"] = ch.get("tk")
    d["chain_warn"] = ch.get("warn", 7700)
    d["chain_block"] = ch.get("block", 10000)
    gate = facts.get("gate") or {}
    d["gate_open"] = gate.get("open", "⛔ NOT ON RECORD (no --gate-log given to _wrap_facts.py)")
    d["first_beat"] = story["owed"][0]["question"]
    d["first_beat_caps"] = fr["first_beat"]
    d["conductor"] = fr["conductor"]
    d["wrap_seat"] = fr["wrap_seat"]
    d["wrap_seat_model"] = fr["wrap_seat"].split(",")[-1].strip()
    d["conductor_model"] = fr["conductor"].split(",")[0].strip()
    d["in_cloud"] = "cloud" in fr["conductor"].lower()
    d["prior_struck"] = [x.strip() for x in (fr.get("prior_handoff_struck") or "").split(",") if x.strip()]
    d["words_files"] = [x.strip() for x in fr["words_files"].split(" · ") if x.strip()]
    d["lane_reports"] = [x.strip() for x in fr["lane_reports"].split(" · ") if x.strip()]
    d["lanes"] = fr["lanes"]
    d["post"] = facts.get("post")
    return d


def resolve(text, facts, d):
    def sub(m):
        src, path, spec = m.group(1), m.group(2), m.group(3) or ""
        val = _get(facts, path) if src == "facts" else _get(d, path)
        if val is None:
            raise StoryError(f"`{{{src}.{path}}}` is null — a figure is never blank")
        try:
            return format(val, spec) if spec else str(val)
        except (ValueError, TypeError) as e:
            raise StoryError(f"`{{{src}.{path}:{spec}}}` cannot be formatted: {e}")
    return PH_RE.sub(sub, text)


def resolve_story(story, facts, d):
    """Resolve placeholders in every parsed field (the front block too). Returns a new story dict."""
    def walk(x):
        if isinstance(x, str):
            return resolve(x, facts, d)
        if isinstance(x, list):
            return [walk(i) for i in x]
        if isinstance(x, tuple):
            return tuple(walk(i) for i in x)
        if isinstance(x, dict):
            return {k: walk(v) for k, v in x.items()}
        return x
    out = walk({k: v for k, v in story.items()})
    return out


# ------------------------------------------------------------------------------------ the views
def _bullets(items, pre="- "):
    return "\n".join(pre + it for it in items)


def _quoted_block(items):
    return "\n\n".join("> " + it.replace("\n", "\n> ") for it in items)


def _owed_mark(o):
    return "⬛" + ("★★★" if o["mark"].count("★") == 3 else "★★" if o["mark"].count("★") == 2 else "★" if o["mark"].count("★") == 1 else "")


def _owner_word(o):
    return {"mine": "Mine", "dave": "Dave's", "future": "Future, recorded not ordered", "found": "Found, not fixed", "standing": "Standing"}[o["owner"]]


def v_banner(s, f, d):
    fr = s["front"]
    head = (f"> ## ★ LATEST — {d['ritual_date']} ({d['ritual_dow3']} **{d['session']}**, {d['days']}, "
            f"{d['conductor_model']} conductor{' in the CLOUD' if d['in_cloud'] else ''}, {d['subs_word']}, "
            f"{fr['wrap_seat'].split(',')[0].strip().upper()} wrap on {d['wrap_seat_model']} — ★★ **{d['headline_caps']}**)")
    rl = "; ".join(_gloss(r) for r in s["rulings"]) if s["rulings"] else "none this session"
    one = f"- ★★★ ① **{d['rulings_n_words']}, `_rulings.json` {d['rulings_delta']} ({d['rulings_ids']}).** {rl}."
    outs = [re.sub(r"^Built:\s*", "", x) for x in s["summary"]["outputs"]]
    two = "- ★★ ② **BUILT:** " + " ".join(outs)
    probs = [x for x in s["problems"] if x.startswith("⚠") or x.startswith("⛔")]
    pline = (" " + probs[0] + " ") if probs else " "
    three = (f"- ⚠ ③ **{d['ci_reds_word']}:** {d['ci_reds_line']}.{pline}"
             f"⛔ **FILL {d['fill_now']:,} at his \"{fr['wrap_word']}\" (hand sum, `_wrap_facts.py`), {d['fill_verdict'].upper()}** (crossed at {d['hard_crossed_local'] if d['fill_now'] > d['hard_line'] else d['stop_crossed_local']}). "
             if d["fill_now"] else f"- ⚠ ③ **{d['ci_reds_word']}:** {d['ci_reds_line']}.{pline}{d['fill_line']}. ")
    three += (f"{d['commits_n']} commits, " + (", ".join(f"`{x}`" for x in d["unpushed"]) + (" ride" if len(d["unpushed"]) > 1 else " rides") + " the wrap push. " if d["unpushed"] else "all pushed. ")
              + f"**`{d['handoff_name']}` OUTRANKS `_CHAIN.md`.**")
    new0 = s["new"][0] if s["new"] else None
    first = (f"⬛ **{new0['title']}** [NEW — 0{', DAVE' + chr(39) + 'S' if new0['daves'] else ''}] — put it first. " if new0 else "")
    resid = (f"> **residual → #{d['next']}:** {first}`s225-D2`. **{d['carries_line']}**, `_CARRIES.md` § `residual → #{d['next']}` "
             f"`carries:residual-{d['next']}`. {d['probe_line']} (new items count from #{d['next'] + 1} until the gate's `_AGE_RE` is fixed).")
    return "\n".join([head, ">", "> " + one[2:] and "> " + one, "> " + two, "> " + three, resid, "{{ROLL_STATE}}"]) + "\n"


RULING_RE = re.compile(r"`(s\d+-D(\d+))`\s*—\s*(.+?)\s*—\s*(.+?)\s*—\s*(RULED NOT ENACTED|ENACTED|RULED)\b\s*(?:[,;(]\s*(.*?)\)?)?$", re.S)


def _ruling_parts(r):
    m = RULING_RE.match(r)
    if not m:
        raise StoryError(f"a `@rulings` item is `- `sNNN-Dk` — his phrase — gloss — RULED|ENACTED|RULED NOT ENACTED[, note]`: {r[:70]!r}")
    return {"id": m.group(1), "k": m.group(2), "quote": m.group(3), "gloss": m.group(4), "status": m.group(5), "note": (m.group(6) or "").strip()}


def _gloss(r):
    """`sNNN-Dk` — quote — gloss — STATUS  →  'gloss (Dk, his HH:MM words, STATUS)' in the banner's register: the
    banner names WHERE his word is (a time, an export); the quotation itself lives in the delta, the handoff and the
    dossier, so the banner stays under its cap (s241-D2)."""
    x = _ruling_parts(r)
    q = x["quote"]
    m = re.search(r"\((\d\d:\d\d)\)", q)
    if m:
        ref = f"his {m.group(1)} words"
    elif "export" in q.lower():
        ref = re.split(r",|\*\"", q, 1)[0].strip()
    else:
        ref = q if len(q) <= 40 else "his words"
    return f"{x['gloss']} (D{x['k']}, {ref}, {x['status']}" + (f" — {x['note']}" if x["note"] and len(x["note"]) <= 60 else "") + ")"


def v_delta(s, f, d):
    fr = s["front"]
    if d["split"]:
        when = (f"⛔ **DATE SPLIT, THE {d['split_ordinal_word']} ON THIS RUN — SESSION OPENED {d['session_dow'][:3].upper()} {d['session_date']} "
                f"{d['opened_time']} {d['zone']}, \"{fr['wrap_word']}\" {d['ritual_dow3'].upper()} {d['ritual_date'][5:]} {d['wrap_time']}; `s294-D11`'s SHAPE, NOTHING RE-DATED**")
    else:
        when = f"ONE DAY — OPENED {d['opened_time']} {d['zone']}, \"{fr['wrap_word']}\" AT {d['wrap_time']}"
    head = (f"## ⏱ LATEST DELTA — {d['ritual_date']} ({d['ritual_dow3']} from `date`) (**{d['session']}**, {when}, "
            f"conductor **{d['conductor_model'].upper()}{' IN THE CLOUD' if d['in_cloud'] else ''}**, "
            f"**{d['subs_n']} DELEGATED SUBS — {fr['lanes']}**, {fr['wrap_seat'].split(',')[0].strip().upper()} wrap on **{d['wrap_seat_model']}**)")
    paras = [f"> ★★ **{t}.** {p}" for t, p in s["did"]]
    paras[-1] += f" **`_rulings.json` {d['rulings_delta']}.**"
    prob = " ".join(s["problems"]) if s["problems"] else "No problem declared by the story."
    fillp = (f"> ⚠ **CI AND THE FILL.** {prob} ⚙ **FILL, a hand sum by `_wrap_facts.py`:** {d['fill_line']}. {d['subs_line']}.")
    five = f"> ⛔★ **5b —** PLACEHOLDER-{d['n']}W"
    foot = (f"> **WHY/HOW: `{d['dossier_path']}`. Handoff: `{d['handoff_name']}` — NEWER THAN `_CHAIN.md` AND OUTRANKS IT. "
            f"His words: `{d['words_dir']}`. Lane reports: " + ", ".join(f"`{p}`" for p in d["lane_reports"]) +
            f". Wrap: `{d['report_path']}`.**")
    return "\n\n".join([head] + paras + [fillp, five, foot]) + "\n"


def v_stratum(s, f, d):
    fr = s["front"]
    fill = f.get("fill") or {}
    pre = (f"> **pre-flight {d['session']}:** ⛔ NOT CAPTURED — UNMEASURED. The conductor ran in the CLOUD and no pre-flight was declared at this seat; "
           f"its window is measured first-hand in the post-mortem below, from the cloud transcript. ⛔ An UNKNOWN is declared, never defaulted to a number [[feedback-measuring-tool-must-not-guess]].")
    if fill:
        cr = fill["crossings"]
        steps = [f"Boot **{fill['boot']:,}** ({d['opened_time']} {d['zone']}" + (f" {d['session_dow'][:3]}" if d["split"] else "") + "), "
                 + ("⚠ OVER" if fill["boot_ceiling"]["over_by"] > 0 else "under") + f" `BOOT_CEILING_TK` {d['boot_ceiling']:,} (`s305-D64`) by {abs(fill['boot_ceiling']['over_by']):,}"]
        for key, nm, bold in (("amber", "BUDGET_AMBER", False), ("stop", "STOP_LINE_TK", True), ("limit", "BUDGET_WORKING", False), ("hard", "BUDGET_HARD", True)):
            v = next((v for k, v in cr.items() if k.startswith(nm)), None)
            if v:
                t = f"over {d[key + '_line']:,}{' stop line' if key == 'stop' else ''} at the {_ordn(v['message'])} ({d[key + '_crossed_local']}, {v['fill']:,})"
                steps.append(("⛔ **" + t + "**") if key == "hard" else ("**" + t + "**") if bold else t)
        steps.append(f"**{fill['now']:,} at the {_ordn(fill['turns'])} ({d['wrap_time']}), the message before his \"{fr['wrap_word']}\" ({d['wrap_time']} {d['zone']})**")
        pm = (f"> **POST-MORTEM {d['session']} — measured, not narrated, and NOT by `_checkin.py`.** ⚙ The conductor's transcript was copied to the gitignored "
              f"`{fill['transcript'].rsplit('/', 1)[0] if '/' in fill['transcript'] else 'knowledge/_tmp'}/` and every figure here is `_wrap_facts.py`'s HAND SUM of "
              f"`input_tokens + cache_creation_input_tokens + cache_read_input_tokens` of the last record per distinct `message.id`, main thread only "
              f"({fill['turns']} distinct messages to his words; `{d['facts_path']}`). " + " · ".join(steps) +
              f". ⛔ **FILL {fill['now']:,} is {d['fill_verdict']} (`s305-D62`).** Stated, not graded.")
    else:
        pm = f"> **POST-MORTEM {d['session']}:** {d['fill_line']}."
    subs = f.get("subs")
    subs1 = f"> **subs {subs['total']:,} tokens (n={subs['n']})**" if subs else "> **subs: none measured**"
    subs2 = (f"> **⚠ THE `subs` FIGURE ABOVE IS `_wrap_facts.py`'s HAND SUM** — the final FILL of each sub's own transcript, same fields, same dedupe, "
             f"{subs['n']} transcripts (largest {subs['largest']:,}, smallest {subs['smallest']:,}). This wrap seat's own transcript was NOT COPIED, so it is excluded. "
             f"⚠ **UNIT: REAL tokens, QUOTA not window FILL** — never added to the figures above [[budget-vs-quota-vocabulary]].") if subs else ""
    hand = (f"> **wrap-handover: his words {fill['now']:,} real ({d['wrap_time']} {d['zone']}) · the brief's figure, where typed, is in the story · "
            f"replay unobservable (conductor-side, post-wrap)**") if fill else ""
    skips = (f"> **⚠ DECLARED SKIPS AND NOT-DONE AT THIS WRAP, EACH WITH ITS SIZE.** {s['skips']} **Carries:** {d['struck_count']} STRUCK, {d['new_count']} NEW. "
             f"**NOT DONE, and his:** everything in `_CARRIES.md` § `residual → #{d['next']}`, first: {d['first_beat']}")
    usage = f"> **section-usage {d['session']} (self-report, {fr['wrap_seat'].split(',')[0].strip()} {d['wrap_seat_model'].upper()} wrap seat):** {s['section_usage']}"
    wrote = (f"> The wrap WROTE the ★ LATEST banner, the ⏱ LATEST delta, the `Last refreshed` stamp" + (", the date-split line" if d["split"] else "") +
             f" and this stratum as FILES generated by `_wrap_views.py` from `{d['story_path']}` and `{d['facts_path']}`, placed by `_wrap_ops.py`; "
             f"READ #{d['prev']}'s banner, stratum, delta and 5b; and left §A, §C, DO-FIRST and every un-named `_LIVE-STATE.md` section UNREAD. "
             f"⚠ **`U` means UNREAD AT THIS SEAT** — a claim about this window, not about the file.")
    sizes = ("> **⚠ THE `section-sizes` LINE ABOVE IS `_gm_usage.py`'s INSTRUMENT, MEASURED BY `_wrap_ops.py` ON A PROJECTED COPY WITH THIS MOVE FILE APPLIED, "
             "A DIFFERENT OBJECT FROM THE `size:` STAMP'S WHOLE-FILE MEASUREMENT** — never reconciled, never averaged [[measure-dont-convert-units]]. Taken BEFORE step 5b; NOT re-taken (the #241 rule).")
    consult = (f"> **consult-receipts {d['session']}:** \"wrap ritual\" → the query run by `_wrap_regen.py`'s serial only; no `--fetch` followed: the runbook, "
               f"`{d['prev_handoff']}` and #{d['prev']}'s wrap files were read BY PATH. **A consult, not a use** [[instrument-without-a-consumer]].")
    s214 = "> **⚠ `s214-D6` BANNER-DISCIPLINE MEASUREMENT:** quoted in the ⏱ LATEST DELTA's 5b line from `_CHAIN.md`'s GENERATED footer, after the one regen."
    commit = (f"> **COMMIT STATE {d['session']}:** ⬛ **THE HASH IS A DECLARED GAP IN THIS BLOCK — A COMMIT CANNOT NAME ITSELF.** This wrap's sha, its push and its CI read are in the ⏱ LATEST DELTA's 5b line and in `{d['report_path']}`. "
              f"**{d['commits_n']} commits before the wrap, all declared not-a-wrap:** {d['commits_line']} (listed in `notes/_lanes/{d['n']}/W/COMMITS.txt`; CI: {d['ci_reds_line']}). "
              f"Handoff `{d['handoff_name']}` OUTRANKS `_CHAIN.md`." +
              (f" Context gauge at authoring: ⚙ **{fill['now']:,} real at his \"{fr['wrap_word']}\" — a hand sum; {d['fill_verdict']}.**" if fill else ""))
    blocks = [f"#### {d['session_date']} {d['session']}", "", pre, "", pm, "", subs1, "", subs2, "", hand, "", skips, "", usage, "", wrote, "",
              "{{SECTION_SIZES}}", "", sizes, "", consult, "", s214, "", commit]
    return "\n".join(b for b in blocks if b is not None).replace("\n\n\n", "\n\n") + "\n"


def _ordn(k):
    suf = "th" if 10 <= k % 100 <= 20 else {1: "st", 2: "nd", 3: "rd"}.get(k % 10, "th")
    return f"{k}{suf}"


def v_stamp(s, f, d):
    if d["split"]:
        days = (f"⛔★★ **DATE SPLIT, THE {d['split_ordinal_word']} ON THIS RUN AND `s294-D11`'s SHAPE: {d['session']} opened {d['session_dow']} {d['session_date']} at "
                f"{d['opened_time']} {d['zone']}; the session went on into {d['ritual_dow']} {d['ritual_date']} and this ritual is {d['ritual_dow']}**")
    else:
        days = f"One day, no date split: {d['session']} opened {d['session_dow']} {d['session_date']} at {d['opened_time']} {d['zone']} and this ritual is the same day"
    return (f"*Last refreshed: {d['ritual_date']} ({d['ritual_dow3']} from `date` — **{d['session']} wrap**. {days} — `date` at this seat read `{d['ritual_local']}` "
            f"(`_wrap_facts.py`'s `dates.ritual_local`). ⛔★★★ **READ `{d['handoff_name']}` FIRST — IT IS NEWER THAN `_CHAIN.md` AND OUTRANKS IT.** "
            f"★★ **THE SESSION IS ONE SENTENCE: {s['front']['one_sentence']}.** Rulings {d['rulings_delta']}. The full record is in the ⏱ LATEST delta below, its sole home under `s241-D2`.)*\n")


def v_datesplit(s, f, d):
    if not d["split"]:
        return None
    firsts = f["git"]["commits"]
    on_open = [c["sha8"] for c in firsts if c["at"][:10] == d["session_date"]]
    on_rit = [c["sha8"] for c in firsts if c["at"][:10] == d["ritual_date"]]
    span = (f"its commits carry both dates (" + (f"`{on_open[0]}` to `{on_open[-1]}` on {d['session_date'][5:]}" if on_open else f"none on {d['session_date'][5:]}") +
            ", " + (f"`{on_rit[0]}` to `{on_rit[-1]}` on {d['ritual_date'][5:]}" if on_rit else f"none on {d['ritual_date'][5:]}") + ")")
    return (f"> ⚠ **WRAP DATE SPLIT, {d['split_ordinal_word']} OCCURRENCE ON THIS RUN — SESSION OPENED {d['session_dow'].upper()} {d['session_date']}, "
            f"{'RESUMED' if d.get('resumed_local') else 'RAN ON INTO'} {d['ritual_dow'].upper()} {d['ritual_date']}; RITUAL + WRAP COMMIT {d['ritual_date']}.** "
            f"{d['session']} opened at {d['opened_time']} {d['zone']} on {d['session_date'][5:]}; {span}. ⛔ **Nothing re-dated** — `s294-D11`'s shape: the session date on keys, "
            f"the dossier and the stratum (`{d['session_date']}-{d['n']}-*`), the ritual date on this one line so the gate's `is not today` check grades a true statement; "
            f"reports keep the day their lanes wrote them; the rulings carry the days he ruled them.\n")


def v_5b(s, f, d):
    p = d["post"]
    if not p:
        return None
    pp = p.get("prepush")
    pre = (f"the pre-push check on the wrap's tree first ({pp['pass']} pass, {pp['fail']} FAIL, {pp['tests']} tests)" if pp else "the pre-push check: not on record")
    ch = p.get("chain_tk_after_regen")
    chain = (f"`_CHAIN.md` {ch:,} cl100k after the wrap's regen, " + (f"over the {d['chain_warn']:,} warn by {ch - d['chain_warn']:,}" if ch > d["chain_warn"] else f"under the {d['chain_warn']:,} warn by {d['chain_warn'] - ch:,}")) if ch else "`_CHAIN.md` after the regen: not measured"
    return (f"**(by addition, after the commit):** wrap commit **`{p['wrap_sha']}`** (`--wrap`, gate `{p.get('gate_wrap') or 'not on record'}`)" +
            (f" and **`{p['seat_sha']}`** (the seat's files)" if p.get("seat_sha") else "") + f"; {pre}; pushed `{p['push_range']}` at {p['pushed_at']}" +
            (f", carrying " + ", ".join(f"`{x}`" for x in d["unpushed"]) if d["unpushed"] else "") +
            f". **CI on `{p['ci']['sha8']}`, run `{p['ci']['run_id']}`: {p['ci']['verdict']}, " +
            ("all three jobs" if p["ci"]["verdict"] == "GREEN" and len(p["ci"]["jobs"]) == 3 else ", ".join(f"{k} {v}" for k, v in p["ci"]["jobs"].items())) +
            f".** {chain}. This addendum's CI is owed to #{d['next']}.\n")


def v_handoff(s, f, d, stage="wrap"):
    fr = s["front"]
    L = [f"# HANDOFF #{d['handoff_no']} — {d['session']} → #{d['next']} — {d['headline_caps']}", "",
         f"provenance: {d['n']} · {d['session_date']}", "status: observed", "",
         f"*Written by the {fr['wrap_seat'].split(',')[0].strip()} {d['wrap_seat_model'].upper()} wrap seat at the close of {d['session']} (conductor {fr['conductor']}), "
         f"GENERATED by `_wrap_views.py` from `{d['story_path']}` and `{d['facts_path']}` (`s306-D4` phase 3). Every figure is from `FACTS.json` (`_wrap_facts.py`) unless it says otherwise; the lanes' figures are the lanes'.*", "",
         f"**{d['days_sentence']}** Opened with chat \"{fr['opened_word']}\" (`{d['prev_handoff']}`); his word at {d['wrap_time']} {d['zone']}, verbatim: *\"{fr['wrap_word']}\"*"
         + (f", {fr['wrap_word_context']}" if fr.get("wrap_word_context") else "") + ".", "",
         f"⛔ **`knowledge/_rulings.json` READS {d['rulings_total']}**, newest `{d['rulings_newest']}`" + (f" ({d['rulings_base']} at the opener)" if d["rulings_base"] is not None else "") +
         (f". Every one of {d['rulings_ids']} is his, from a chat line or his review export, kept verbatim in `{d['words_dir']}`. **Quote them; never paraphrase.**" if d["rulings_n"] else ". No ruling landed this session."), "",
         f"⛔★ **#{d['next']}'S FIRST BEAT: {fr['first_beat']}.** {s['owed'][0]['body']}", "",
         f"⛔ **THE FILL IS A HAND SUM BY `_wrap_facts.py`**" + (f", over the conductor's transcript `{f['fill']['transcript']}`: {d['fill_line']}. {d['subs_line']}." if f.get("fill") else f": {d['fill_line']}."), "",
         "---", "", "## ⛔ READ FIRST, IN THIS ORDER", "",
         "1. **This file.** It is newer than `_CHAIN.md` and **OUTRANKS it**.",
         "2. `_CHAIN.md` — the read contract (header → ★ LATEST banner → ⏱ LATEST delta).",
         f"3. ⛔ **It does NOT replace `_HANDOFF-130`…`-{d['prev_handoff_no']}`.** Every open item on those still stands **except the ones struck with receipts**: "
         + (f"this wrap strikes `{d['prev_handoff']}` OWED item{'s' if len(d['prior_struck']) != 1 else ''} {_and(d['prior_struck'])} ({d['struck_count']} struck: "
            + "; ".join(t.lower() for t in d["struck_titles"]) + f"), in `_CARRIES.md` § `residual → #{d['next']}` and by addition at the foot of `{d['prev_handoff']}`."
            if d["prior_struck"] else "this wrap strikes nothing."),
         "4. **His words:** " + " · ".join(f"`{p}`" for p in d["words_files"]) + ".",
         f"5. `_CARRIES.md` § `residual → #{d['next']}` when you need the bodies. Fetch the section; do not read it at boot.",
         "6. The lane reports, when the work needs them: " + " · ".join(f"`{p}`" for p in d["lane_reports"]) + f" · this wrap's `{d['report_path']}`.", "",
         "---", "", "## ⛔⛔ HIS WORDS (chat lines; the exports are in the files above)", "",
         _quoted_block(s["words"]), "", "---", "", "## WHAT THE SESSION DID", "",
         _bullets([f"**{t.capitalize() if t.isupper() else t}.** {p}" for t, p in s["did"]]), "",
         "| Range | What |", "|---|---|",
         f"| `{d['commits_range']}` | {d['commits_line']} (`notes/_lanes/{d['n']}/W/COMMITS.txt`) |",
         "| *the wrap* | § POST-WRAP |", "", "---", "",
         f"## ⬛ OWED TO #{d['next']}, IN ORDER — EACH WRITTEN AS THE QUESTION IT IS", ""]
    for i, o in enumerate(s["owed"], 1):
        L.append(f"{i}. {_owed_mark(o)} **{_owner_word(o)}{', first beat' if i == 1 else ''}: {o['question']}**" + (f" {o['body']}" if o["body"] else ""))
    L += ["", "---", "", "## ⚠ THINGS A COLD SEAT SHOULD KNOW BEFORE IT TOUCHES ANYTHING", ""]
    L += ["- " + c for c in s["cold"]]
    own = {_bold_key(c) for c in s["cold"]}
    L += ["- " + c.format(stop=d["stop_line"], limit=d["limit_line"], hard=d["hard_line"], boot_ceiling=d["boot_ceiling"], n=d["n"])
          for c in STANDING_COLD if _bold_key(c) not in own]      # a standing line the story restates with the session's detail is not printed twice
    L += ["", "---", "",
          f"*Filed report: `{d['report_path']}`. Dossier: `{d['dossier_path']}`. Memory hook: `{d['hook_path']}`. Figures: `{d['facts_path']}`. Story: `{d['story_path']}`.*", "",
          f"*Title the next chat:* `{fr['next_title']}`", ""]
    text = "\n".join(L)
    if stage == "post":
        text += "\n" + _handoff_post(s, f, d)
    return text


def _bold_key(line):
    m = re.search(r"\*\*(.+?)\*\*", line)
    return re.sub(r"[^a-z0-9]+", " ", (m.group(1) if m else line).casefold()).strip()[:40]


def _and(xs):
    xs = list(xs)
    return xs[0] if len(xs) == 1 else ", ".join(xs[:-1]) + " and " + xs[-1] if xs else ""


def _handoff_post(s, f, d):
    p = d["post"]
    if not p:
        raise StoryError("`--stage post` needs `post` in FACTS.json (`_wrap_facts.py --post`)")
    pp = p.get("prepush")
    items = [f"1. {'✅' if p['ci']['verdict'] == 'GREEN' else '⛔'} **CI IS {p['ci']['verdict']}.** `{p['ci']['sha8']}` run `{p['ci']['run_id']}`, "
             + ", ".join(f"{k} {v}" for k, v in p["ci"]["jobs"].items()) + f", read by `_ci_readback.py` (`notes/_lanes/{d['n']}/W/_ci-runs-{p['ci']['sha8']}.txt`)."]
    if pp:
        items.append(f"2. {'✅' if pp['fail'] == 0 else '⛔'} **THE PRE-PUSH CHECK RAN ON THE WRAP'S OWN TREE FIRST** (Worker checklist step 5): {pp['pass']} pass, {pp['fail']} FAIL, "
                     f"{pp['advisory']} advisory, {pp['could_not_ask']} could-not-ask over {pp['surveys']} survey chunks; `test_gates` {pp['tests']} with {pp['test_failures']} failure(s). Logs: `notes/_lanes/{d['n']}/W/_prepush-*.txt`.")
    else:
        items.append("2. ⚠ **THE PRE-PUSH CHECK IS NOT ON RECORD** in FACTS.json (`--prepush-dir` not given). Declared.")
    items.append(f"3. ⛔ **THE WRAP COMMIT IS `{p['wrap_sha']}`, ON THE `--wrap` PATH** (gate `{p.get('gate_wrap') or 'not on record'}`)" + (f"; **`{p['seat_sha']}` carries the seat's files.**" if p.get("seat_sha") else "."))
    items.append(f"4. **THE PUSH: `{p['push_range']}`** at {p['pushed_at']}" + (f", **{p['minutes_to_push']} minutes from the launch** ({p['launched_at']})" if p.get("minutes_to_push") is not None else "") +
                 (", carrying " + ", ".join(f"`{x}`" for x in d["unpushed"]) if d["unpushed"] else "") + ".")
    items.append(f"5. **Phase-3 counts:** hand-written files **2** (`STORY.md`, and nothing else; `FACTS.json` is measured) · views generated **{len(VIEW_NAMES)}** · move files **1 + the 5b** · rebuilds **1 for the wrap, 1 for this 5b**.")
    ch = p.get("chain_tk_after_regen")
    items.append(f"6. {'⚠' if ch and ch > d['chain_warn'] else '✅'} **`_CHAIN.md` IS {ch:,} cl100k** at the wrap's regen, " + (f"over the {d['chain_warn']:,} warn by {ch - d['chain_warn']:,}" if ch > d["chain_warn"] else f"under the {d['chain_warn']:,} warn") +
                 f", under the {d['chain_block']:,} fail (`CHAIN_BUDGET_TK`, `s212-D11`). The figure after this addendum's own regen is not re-taken (the #241 rule)." if ch else "6. ⚠ **`_CHAIN.md` after the regen: not measured.**")
    t = p.get("titles") or {}
    items.append(f"7. ⚠ **The next title.** `GOOD-MORNING.md` carries the story's `{s['front']['next_title']}`. `_gen_titles.py` derived `{t.get('derived') or 'not read'}`. Declared, not reconciled.")
    items.append(f"8. ⛔ **MEMORY — NOT WRITTEN BY THIS SEAT.** The one hook file is `{d['hook_path']}` (the index line, the front block and the body, each once).")
    items.append("9. ⚠ **STEP 4c runs LAST, after the 5b commit and push.**")
    return "\n".join(["---", "", "## ⬛ POST-WRAP ADDENDUM (5b) — BY ADDITION; NOTHING ABOVE IS REWRITTEN", "",
                      f"**No ruling landed after the wrap gate ran**, so no banner addendum is owed. The `s271-D4` re-read strikes nothing: `_rulings.json` reads **{d['rulings_total']}, newest `{d['rulings_newest']}`**.", ""]
                     + items + ["", "CI owed: this addendum's own commit — read by the next opener with python3 knowledge/_ci_readback.py --owed", ""])


def v_prior_strikes(s, f, d):
    if not s["struck"]:
        return None
    L = ["", "---", "", f"## ⬛ STRUCK AT THE {d['session']} WRAP — BY ADDITION; NOTHING ABOVE IS REWRITTEN", ""]
    for k, st in enumerate(s["struck"]):
        ref = f"OWED item {d['prior_struck'][k]}, " if k < len(d["prior_struck"]) else ""
        L.append(f"- ~~{ref}{st['title'].lower()}~~ ⛔ **STRUCK {d['session']} {d['ritual_date']} BY THE WRAP SEAT — {st['verdict']}** — {st['receipt']}")
    return "\n".join(L) + "\n"


def v_dossier(s, f, d):
    fr = s["front"]
    L = [f"# {d['session']} — {fr['headline'][0].upper() + fr['headline'][1:]}", "", f"provenance: {d['n']} · {d['session_date']}", "status: observed", "",
         f"*The why and the how of session {d['session']} ({d['days_sentence'][0].lower() + d['days_sentence'][1:]} His \"{fr['wrap_word']}\" at {d['wrap_time']}.) "
         f"The what is in `{d['handoff_name']}` and in `_LIVE-STATE.md`'s ⏱ LATEST delta (spine entry); the rulings are {d['rulings_ids_full']} in `knowledge/_rulings.json` (ledger). "
         f"Generated from `{d['story_path']}` § @why.*", ""]
    for t, body in s["why"]:
        L += [f"## {t}", "", body, ""]
    return "\n".join(L)


def v_report(s, f, d, stage="wrap"):
    fr = s["front"]
    L = [f"# {d['session']} W — the wrap, generated from one story: {fr['headline']}", "",
         f"session: `{d['session']}` · {d['session_date']}" + (f" (ritual {d['ritual_date']})" if d["split"] else ""),
         f"window: lane W ({fr['wrap_seat']} wrap seat)", "sub index: `W`",
         f"brief: the conductor's launch message, on his {d['wrap_time']} {d['zone']} \"{fr['wrap_word']}\"",
         f"provenance: {d['n']} · {d['ritual_date']}", "status: observed",
         "tokens: UNMEASURED — this seat cannot read its own transcript while it is still growing", "", "## VERDICT", "",
         f"DONE. The capture ritual ran on phase 3 (`s306-D4`, `s306-D5`): ONE story (`{d['story_path']}`) and ONE measured file (`{d['facts_path']}`), every other view generated by `_wrap_views.py` "
         f"and placed by the phase-1 tools, {d['days']} (`_wrap_ops.py --date {d['ritual_date']}`" + (f" --session-date {d['session_date']} --date-split" if d["split"] else "") + "). "
         f"The carries by `_wrap_carries.py` ({d['new_count']} new, {d['struck_count']} struck), the rows from one spec, one regen by `_wrap_regen.py --run --session {d['n']}`. The push and CI are in § POST-COMMIT, added after the push.", "",
         f"COUNTS: findings `{len(s['findings'])}` · ruling-shaped `{_qcount(s['questions'])}` · UNPROVEN `{len(s['unproven'])}`", "",
         f"WRAP COUNTS (before the commit): hand-written files `1` (the story; target 1) · move files `1` + the 5b · rebuilds `1` for the wrap commit · hand steps `0` · "
         f"rulings `{d['rulings_delta']}` · carries `{d['carries_items']:,}` on `residual → #{d['carries_section']}` at the wrap · gate at open `{d['gate_open']}`", "",
         "## 1. The fill", "",
         (f"{d['fill_line']}. {d['subs_line']}. Every figure is `_wrap_facts.py`'s hand sum over `{f['fill']['transcript']}` to `{f['fill']['until'] or f['fill']['now_at']}`." if f.get("fill") else d["fill_line"] + "."), "",
         "## 2. Each step, and what the tool did", "", "| step | tool | result |", "|---|---|---|",
         f"| figures | `_wrap_facts.py` | `FACTS.json`; {d['owed_read_line']} |",
         f"| gate at open | `_capture_gate.py --wrap` | {d['gate_open']} |",
         f"| the story | `STORY.md` by hand, `_wrap_views.py --check` then `--write` | {len(VIEW_NAMES)} views generated |",
         f"| carries | `_wrap_carries.py delta` ({d['new_count']} new, {d['struck_count']} struck) | the `residual → #{d['next']}` delta block; `render` materialises the full line |",
         "| GM/LS | `_wrap_ops.py` → `_gm_move.py` | one move file, dry run then write, its inputs from `views/` |",
         f"| rows | `_wrap_rows.py --spec views/rows.json` | `W-{d['n']}h`, `W-{d['n']}dh`, `W-{d['n']}w`, `W-{d['n']}wk` minted born closed; " + (", ".join(f"{r['id']} {r['op']}d" if r['op'] != 'note' else f"{r['id']} noted" for r in s["rows"]) if s["rows"] else "no other row") + " |",
         f"| regen | `_wrap_regen.py --run --session {d['n']}` | once, after the last edit |",
         "| commit | `_wrap_commit.py msg/paths/commit` | § POST-COMMIT |", "",
         "## 3. What this wrap found", ""]
    L += [f"{i}. {x}" for i, x in enumerate(s["findings"], 1)] if s["findings"] else ["None."]
    L += ["", f"## 4. What is carried, not committed", "",
          f"Other seats' dirty paths stay as they are. The transcripts in `knowledge/_tmp/wrap{d['n']}/` are gitignored. Memory was not written by this seat: the one hook file is `{d['hook_path']}`.", "",
          "## Found, not fixed", "", "See `## 3`; nothing above was changed by this seat.", "",
          "## Ruling-shaped questions", "", s["questions"], "",
          "## UNPROVEN", ""]
    L += [f"- {x}" for x in s["unproven"]] if s["unproven"] else ["None."]
    L += ["", f"REPLAY-THESE: `python3 knowledge/_wrap_views.py --check --session {d['n']}` · `python3 knowledge/_wrap_carries.py count --section {d['next']}` · "
          f"`python3 knowledge/_wrap_facts.py --selftest` · `python3 knowledge/_wrap_views.py --selftest`", ""]
    text = "\n".join(L)
    if stage == "post":
        p = d["post"]
        pp = p.get("prepush")
        text += "\n".join(["", "## POST-COMMIT (by addition, 5b)", "",
                           f"- **The wrap commit is `{p['wrap_sha']}`**, on the `--wrap` path, gate `{p.get('gate_wrap') or 'not on record'}`" + (f"; **`{p['seat_sha']}`** carries the seat's files." if p.get("seat_sha") else "."),
                           (f"- **The pre-push check, before the push:** {pp['pass']} pass · {pp['fail']} FAIL · {pp['advisory']} advisory · {pp['could_not_ask']} could-not-ask over {pp['surveys']} chunks; `test_gates` {pp['tests']} ({pp['test_failures']} failures). Logs `notes/_lanes/{d['n']}/W/_prepush-*.txt`."
                            if pp else "- **The pre-push check:** not on record in FACTS.json."),
                           f"- **The push:** `{p['push_range']}` at {p['pushed_at']}" + (f", {p['minutes_to_push']} minutes from the launch" if p.get("minutes_to_push") is not None else "") + ".",
                           f"- **CI:** `{p['ci']['sha8']}`, run `{p['ci']['run_id']}`, {p['ci']['verdict']} (" + ", ".join(f"{k} {v}" for k, v in p["ci"]["jobs"].items()) + ").",
                           f"- **`_CHAIN.md` {p['chain_tk_after_regen']:,} cl100k** at the wrap's regen (warn {d['chain_warn']:,}, fail {d['chain_block']:,}). Declared." if p.get("chain_tk_after_regen") else "- `_CHAIN.md` after the regen: not measured.",
                           f"- **Title:** the story's `{fr['next_title']}`; `_gen_titles.py` derived `{(p.get('titles') or {}).get('derived') or 'not read'}`. Declared.", ""])
    return text


def _qcount(q):
    """Ruling-shaped questions: the `- ` items; a bare `None…` sentence is 0; any other prose is 1."""
    if q.startswith("- "):
        return len(_items(q))
    return 0 if q.strip().lower().startswith("none") else 1


def v_memory(s, f, d, stage="wrap"):
    fr = s["front"]
    def _mr(r):
        x = _ruling_parts(r)
        q = x["quote"] if '*"' in x["quote"] else f"*\"{x['quote']}\"*"
        return f"{x['gloss']} ({q}" + (f"; {x['status']}, {x['note']}" if x["status"] != "ENACTED" else "") + ")"
    rl = "; ".join(_mr(r) for r in s["rulings"]) if s["rulings"] else "no rulings this session"
    desc = (f"{d['session']} ({d['session_dow'][:3]} {d['session_date']}, {d['days']}) wrapped — {d['rulings_summary']}" + (f" ({d['rulings_ids_plain']})" if d["rulings_n"] else "") +
            f": {fr['headline']}; " + d["ci_reds_word"].lower().replace("ci red", "CI red") + f"; fill {d['fill_verdict']}; ⬛ #{d['next']}: {fr['first_beat']}. Body verbatim from {d['hook_path']}.")
    desc = desc.replace('"', "'")
    if len(desc.encode("utf-8")) > LIMITS["memory_description_bytes"]:
        cut = desc.encode("utf-8")[:LIMITS["memory_description_bytes"] - 3].decode("utf-8", "ignore").rstrip()
        desc = cut + "…"
    index_line = (f"- [★★ {d['session']} WRAPPED · {d['headline_caps']} · {d['days'].upper()} · {d['rulings_n_words']}" + (f" {d['rulings_ids_plain']}, {d['rulings_delta']}" if d["rulings_n"] else "") +
                  f" · {d['ci_reds_word']} · FILL {d['fill_now']:,} AT \"{fr['wrap_word']}\", {d['fill_verdict'].upper()} · ⬛ #{d['next']}: {fr['first_beat']}]({d['memory_name']}.md) — "
                  f"no memory read or write at the opener or while a chat is live; never run git status; handoff {d['handoff_name']}") if d["fill_now"] else \
                 (f"- [★★ {d['session']} WRAPPED · {d['headline_caps']} · ⬛ #{d['next']}: {fr['first_beat']}]({d['memory_name']}.md) — handoff {d['handoff_name']}")
    front = "\n".join(["---", f"name: {d['memory_name']}", f'description: "{desc}"', "sources: [cowork]", "metadata:", f"  provenance: {d['n']} · {d['session_date']}", "  status: observed", "---"])
    body = [f"# {d['session']} wrapped — {fr['headline']}", "",
            f"provenance: {d['n']} · {d['session_date']} · status: observed · repo record: `{d['handoff_name']}`", "", "### What landed",
            f"- **{d['days_sentence']}** Lanes: {fr['lanes']}; {d['commits_line']}.",
            f"- **{d['rulings_summary']}" + (f" ({d['rulings_ids']}):** {rl}." if d["rulings_n"] else ".**"),
            "- **Built:** " + " ".join(re.sub(r"^Built:\s*", "", x) for x in s["summary"]["outputs"]),
            f"- **CI:** {d['ci_reds_line']}.", "", "### The numbers",
            f"- {d['fill_line']} — a hand sum by `_wrap_facts.py`. {d['subs_line']}.", "", "### OPEN — each a question put at the wrap"]
    for i, o in enumerate(s["owed"][:4], 1):
        body.append(f"{i}. **{_owner_word(o)}{', first' if i == 1 else ''}:** {o['question']}")
    if stage == "post" and d["post"]:
        p = d["post"]
        body += ["", f"### After the wrap", f"- Wrap commit `{p['wrap_sha']}`" + (f", seat files `{p['seat_sha']}`" if p.get("seat_sha") else "") + f"; CI on `{p['ci']['sha8']}` {p['ci']['verdict']} (run `{p['ci']['run_id']}`)."]
    L = [f"# {d['session']} — WRAP MEMORY HOOK", "", f"provenance: {d['n']} · {d['session_date']}", "status: observed", "",
         f"*Ritual step 3, GENERATED by `_wrap_views.py` at the {fr['wrap_seat'].split(',')[0].strip()} wrap seat. The memory store is the claude.ai Project memory (#278). ⛔ **The note is placed ONLY after he says he is done. "
         "This seat called no memory tool; the CONDUCTOR reads the store's versions and places the payloads, after the wrap commit and the push.** If it is not placed, leave it: this file is the record. "
         "ONE file (limit 11): the placer cuts the index line, the front block and the body at the marked headings below; nothing is written twice.*", "",
         "⛔ **EVERY OPEN ITEM BELOW IS WRITTEN AS THE QUESTION IT IS** (`s271-D4`).", "", "---", "", "## FOR THE PLACER (the conductor)", "",
         "**Read first, and take `if_version` from those reads:** `index.md`, the newest `MEMORY-ARCHIVE-*.md`.", "",
         f"1. **Archive the oldest wrap line.** The index keeps the newest three: move the oldest VERBATIM to the newest archive shard under `## Batch {d['ritual_date']} {d['session']} (wrap)`, then remove it from `index.md` with the same string. If #{d['prev']}'s note was never placed, place it first (`notes/_lanes/{d['prev']}/WRAP-MEMORY-HOOK.md`).",
         f"2. **Put the {d['session']} line at the TOP of `index.md`** — § INDEX LINE below, verbatim.",
         f"3. **Write `{d['memory_name']}.md`** — § FRONT BLOCK followed by § BODY, verbatim.",
         "4. ⚠ **Not filed, deliberately:** window figures beyond the one line (perishable); the conductor's readings of his short answers; no preferences line unless the story's `@cold` names a standing instruction of his.", "",
         "---", "", "## INDEX LINE", "", index_line, "", "## FRONT BLOCK", "", front, "", "## BODY", ""] + body + [""]
    return "\n".join(L)


def v_carries(s, f, d):
    """new.txt + strike-<k>.txt (today's phase-1 inputs) and carries-delta.md (`_wrap_carries.py delta`, phase 5)."""
    out = {}
    new_lines = []
    for i, it in enumerate(s["new"]):
        tag = "[NEW — 0, DAVE'S]" if it["daves"] else "[NEW — 0]"
        new_lines.append(f"{it['mark']} **{CIRCLED[i] if i < len(CIRCLED) else i + 1} {it['title']}** {tag} — {it['body']}")
    out["new.txt"] = "\n".join(new_lines) + ("\n" if new_lines else "")
    for k, st in enumerate(s["struck"], 1):
        out[f"strike-{k}.txt"] = f"**STRUCK {d['session']} {d['ritual_date']} BY THE WRAP SEAT (`s183-D1` strike form, `s188-D2` receipt) — {st['verdict']}.** {st['receipt']}\n"
    import _wrap_carries as wc
    out["carries-delta.md"] = wc.delta_block(d["next"], d["n"], new_lines, [(st["title"], st["verdict"], st["receipt"]) for st in s["struck"]], d["ritual_date"])
    return out


def v_rows(s, f, d):
    fr = s["front"]
    n = d["n"]
    by = f"{d['session']} W ({d['ritual_date']})"
    ops = [{"op": "mint", "id": f"W-{n}h", "title": f"{d['session']} handoff - {fr['headline']}", "home": d["handoff_name"],
            "body": f"The {d['session']} wrap's handoff to #{d['next']}, generated from the story; OWED list of {len(s['owed'])} questions, first: {d['first_beat']}"},
           {"op": "mint", "id": f"W-{n}dh", "title": f"{d['session']} dossier - the why and the how: {fr['headline']}", "home": d["dossier_path"],
            "body": f"Step 1b dossier for {d['session']}, generated from the story's @why."},
           {"op": "mint", "id": f"W-{n}w", "title": f"{d['session']} W - the wrap, generated from one story", "home": d["report_path"],
            "body": f"s218-D7 filed report of the {d['session']} wrap seat (s306-D5: the generated report is the filed report)."},
           {"op": "mint", "id": f"W-{n}wk", "title": f"{d['session']} wrap memory hook - the one hook file (index line, front block, body) for the conductor to place after Dave is done",
            "home": d["hook_path"], "body": f"Ritual step 3 payloads for {d['session']}, one file."}]
    for r in s["rows"]:
        if r["op"] == "close":
            ops.append({"op": "close", "id": r["id"], "closed_by": f"{by}: {r['text']}"})
        else:
            ops.append({"op": r["op"], "id": r["id"], "para": f"{d['session']} ({d['ritual_date']}): {r['text']}"})
    return json.dumps({"session": n, "by": by, "ops": ops}, ensure_ascii=False, indent=1) + "\n"


def v_msg(s, f, d, stage="wrap"):
    fr = s["front"]
    if stage == "post":
        p = d["post"]
        line1 = f"{d['n']} W 5b: the post-wrap addendum - CI {p['ci']['verdict']} on {p['ci']['sha8']}, CI owed to #{d['next']}"
        body = [f"The {d['session']} post-wrap addendum (5b), by addition.", "",
                f"- The delta's 5b line filled (one --fill-token move file): wrap commit {p['wrap_sha']}" + (f" plus {p['seat_sha']}" if p.get("seat_sha") else "") + f", pushed {p['push_range']}; CI on {p['ci']['sha8']} run {p['ci']['run_id']} {p['ci']['verdict']}.",
                f"- _HANDOFF-{d['handoff_no']} POST-WRAP ADDENDUM (5b) with the CI owed line; the W report's POST-COMMIT section; the memory hook's after-the-wrap line; all regenerated by _wrap_views.py --stage post (pre-commit text byte-identical, checked)."]
    else:
        line1 = f"{d['n']} W: the {d['session']} wrap - {d['rulings_n']} rulings ({d['rulings_ids_plain']}), {fr['headline']}; handoff {d['handoff_no']}"
        if len(line1) > LIMITS["msg_line1"]:
            line1 = line1[:LIMITS["msg_line1"] - 1].rstrip() + "…"
        body = [f"The {d['session']} capture ritual on phase 3 of the wrap redesign (s306-D4): one story, every view generated; {d['days']}.", "",
                f"- Figures from {d['facts_path']} (_wrap_facts.py): " + (d["fill_line"].replace("**", "") + "; " if f.get("fill") else "") + f"rulings {d['rulings_delta']}.",
                f"- Views by _wrap_views.py from {d['story_path']}: banner, delta, stratum, stamp" + (", date-split line" if d["split"] else "") + ", handoff, dossier, W report, memory hook, carries, rows, this message, the summary.",
                f"- One move file (_wrap_ops.py --date {d['ritual_date']}) for the banner, stratum, stamp, delta and the 2c/2d/2f rolls; title for #{d['next']}.",
                f"- Carries: the residual → #{d['next']} delta block ({d['new_count']} new, {d['struck_count']} struck); rows W-{d['n']}h, W-{d['n']}dh, W-{d['n']}w, W-{d['n']}wk minted born closed" + (f"; " + ", ".join(f"{r['id']} {r['op']}" for r in s["rows"]) if s["rows"] else "") + ".",
                f"- One regen (_wrap_regen.py --session {d['n']}).", "- Decisions / Outputs / Problems for Dave: " + " ".join(s["summary"]["decisions"][:1])]
        if d["unpushed"]:
            body.append(f"- Rides the push with the conductor's unpushed " + ", ".join(d["unpushed"]) + ".")
    trailers = [t for t in (fr.get("co_authored_by") and f"Co-Authored-By: {fr['co_authored_by']}", fr.get("claude_session") and f"Claude-Session: {fr['claude_session']}") if t]
    return "\n".join([line1, ""] + body + ([""] + trailers if trailers else [])) + "\n"


def v_summary(s, f, d, stage="wrap"):
    p = d["post"] if stage == "post" else None
    post = ([f"- The wrap is committed and pushed (`{p['wrap_sha']}`" + (f", plus `{p['seat_sha']}` for the wrap seat's files" if p.get("seat_sha") else "") + "). "
             + ("The full pre-push check ran on the wrap first and came back clean. " if p.get("prepush") and p["prepush"]["fail"] == 0 else "")
             + (f"CI is {p['ci']['verdict'].lower()}" + (" on all three jobs." if p["ci"]["verdict"] == "GREEN" and len(p["ci"]["jobs"]) == 3 else "."))] if p else [])
    L = [f"# {d['session']} — summary for Dave", "", "## Decisions"] + ["- " + x for x in s["summary"]["decisions"]] + \
        ["", "## Outputs"] + ["- " + x for x in s["summary"]["outputs"]] + post + [f"- Next chat: `{s['front']['next_title']}`."] + \
        ["", "## Problems"] + ["- " + x for x in s["summary"]["problems"]]
    return "\n".join(L) + "\n"


VIEW_NAMES = ["banner", "delta", "stratum", "stamp", "datesplit", "5b", "handoff", "prior-strikes", "dossier", "report", "memory", "carries", "rows", "msg", "summary"]
FILES = {"banner": "banner.md", "delta": "delta.md", "stratum": "stratum.md", "stamp": "stamp.md", "datesplit": "datesplit.md", "5b": "5b.md",
         "handoff": "handoff.md", "prior-strikes": "prior-strikes.md", "dossier": "dossier.md", "report": "report.md", "memory": "WRAP-MEMORY-HOOK.md",
         "rows": "rows.json", "msg": "msg.txt", "summary": "SUMMARY.md"}
POST_REGEN = ("handoff", "report", "memory")        # by addition: the stage-wrap text must be a prefix
# the summary is regenerated at post too (its push and CI line sits under Outputs), but it is chat text, not a
# by-addition record, so it is rewritten whole


def generate(story, facts, stage="wrap"):
    """{filename: text} for the stage. Placeholders resolved first; the derived values computed once."""
    d = derive(story, facts)
    s = resolve_story(story, facts, d)
    d["first_beat"] = s["owed"][0]["question"]
    out = {}
    out["banner.md"] = v_banner(s, facts, d)
    out["delta.md"] = v_delta(s, facts, d)
    out["stratum.md"] = v_stratum(s, facts, d)
    out["stamp.md"] = v_stamp(s, facts, d)
    ds = v_datesplit(s, facts, d)
    if ds:
        out["datesplit.md"] = ds
    out["handoff.md"] = v_handoff(s, facts, d, stage)
    ps = v_prior_strikes(s, facts, d)
    if ps:
        out["prior-strikes.md"] = ps
    out["dossier.md"] = v_dossier(s, facts, d)
    out["report.md"] = v_report(s, facts, d, stage)
    out["WRAP-MEMORY-HOOK.md"] = v_memory(s, facts, d, stage)
    out.update(v_carries(s, facts, d))
    out["rows.json"] = v_rows(s, facts, d)
    out["msg.txt"] = v_msg(s, facts, d, "wrap")
    out["SUMMARY.md"] = v_summary(s, facts, d, stage)
    if stage == "post":
        five = v_5b(s, facts, d)
        if not five:
            raise StoryError("`--stage post` needs `post` in FACTS.json")
        out["5b.md"] = five
        out["msg-5b.txt"] = v_msg(s, facts, d, "post")
    return out, d, s


def homes(d):
    return {"handoff.md": d["handoff_name"], "dossier.md": d["dossier_path"], "report.md": d["report_path"],
            "WRAP-MEMORY-HOOK.md": d["hook_path"], "SUMMARY.md": f"notes/_lanes/{d['n']}/W/SUMMARY.md"}


# ------------------------------------------------------------------------------------ limits
def check_limits(views, story, facts, d, stage="wrap"):
    """(fails, warns) — every limit of the docstring, each named."""
    fails, warns = [], []
    b = views["banner.md"]
    blines = [l for l in b.split("\n") if l.strip() and l.strip() not in (">", "{{ROLL_STATE}}")]
    if len(blines) > LIMITS["banner"]["lines"]:
        fails.append(f"banner: {len(blines)} substantive lines, cap {LIMITS['banner']['lines']} (s241-D2)")
    btk = _tk(b.replace("{{ROLL_STATE}}", ""))
    if btk > LIMITS["banner"]["block"]:
        longest = max(blines, key=_tk)
        fails.append(f"banner: {btk:,} cl100k, cap {LIMITS['banner']['block']:,} (s241-D2) — the longest bullet is {_tk(longest):,}: {longest[:80]!r}")
    dtk = _tk(views["delta.md"])
    if dtk > LIMITS["delta"]["block"]:
        fails.append(f"delta: {dtk:,} cl100k, cap {LIMITS['delta']['block']:,} (limit 3/6, #305's delta)")
    htk = _tk(views["handoff.md"])
    if htk > LIMITS["handoff"]["block"]:
        fails.append(f"handoff: {htk:,} cl100k, BLOCK over {LIMITS['handoff']['block']:,} (limit 2; _HANDOFF-156 whole)")
    elif htk > LIMITS["handoff"]["warn"]:
        warns.append(f"handoff: {htk:,} cl100k, over the {LIMITS['handoff']['warn']:,} warn (picked)")
    dstk = _tk(views["dossier.md"])
    if dstk > LIMITS["dossier"]["warn"]:
        warns.append(f"dossier: {dstk:,} cl100k, over the {LIMITS['dossier']['warn']:,} warn (picked)")
    wtk = _tk(story["raw"]["words"])
    if wtk > LIMITS["words"]["warn"]:
        warns.append(f"@words: {wtk:,} cl100k, over the {LIMITS['words']['warn']:,} warn (limit 4: chat lines only; exports by path)")
    exports = sum(1 for w in story["words"] if "export `" in w)
    if exports > 4:
        warns.append(f"@words cites {exports} exports; limit 4 says cite by path, quote call by call")
    rep = views["report.md"]
    for must in ("COUNTS:", "## Found, not fixed", "## Ruling-shaped questions", "REPLAY-THESE:"):
        if must not in rep:
            fails.append(f"report lacks `{must}` (s218-D7)")
    mem = views["WRAP-MEMORY-HOOK.md"]
    m = re.search(r'^description: "(.*)"$', mem, re.M)
    if not m:
        fails.append("memory: no description line in the front block")
    elif len(m.group(1).encode("utf-8")) > LIMITS["memory_description_bytes"]:
        fails.append(f"memory: description {len(m.group(1).encode('utf-8'))} B, cap {LIMITS['memory_description_bytes']}")
    if mem.count("## BODY") != 1 or mem.count("## FRONT BLOCK") != 1 or mem.count("## INDEX LINE") != 1:
        fails.append("memory: the hook must carry ## INDEX LINE, ## FRONT BLOCK and ## BODY exactly once (limit 11)")
    line1 = views["msg.txt"].split("\n")[0]
    if len(line1) > LIMITS["msg_line1"]:
        fails.append(f"msg: line 1 is {len(line1)} chars, cap {LIMITS['msg_line1']}")
    if re.match(r"^(?:after )?#\d+ \d{4}-\d{2}-\d{2} — ", line1):
        fails.append("msg: line 1 carries a T3 prefix (the committer adds it)")
    cd = views["carries-delta.md"]
    if len(cd.encode("utf-8")) > LIMITS["carries_delta_bytes"]:
        fails.append(f"carries delta: {len(cd.encode('utf-8')):,} B, cap {LIMITS['carries_delta_bytes']:,} (limit 10)")
    for ln in views["new.txt"].split("\n"):
        if ln and "·" in ln:
            fails.append("new.txt: an item contains `·`")
    # the retype warn: a typed figure with a thousands separator that FACTS.json also holds
    figs = {}
    def walk(x, path):
        if isinstance(x, dict):
            for k, v in x.items():
                walk(v, f"{path}.{k}" if path else k)
        elif isinstance(x, list):
            for i, v in enumerate(x):
                walk(v, f"{path}.{i}")
        elif isinstance(x, int) and not isinstance(x, bool) and abs(x) >= 1000:
            figs.setdefault(f"{x:,}", path)
    walk(facts, "")
    raw_story = "\n".join(story["raw"][k] for k in SECTIONS)
    typed = sorted({m for m in FIG_RE.findall(raw_story) if m in figs})
    for t in typed:
        if " " in figs[t] or not figs[t].replace(".", "").replace("_", "").isalnum():
            continue   # the crossings' keys carry a space — not dotted-addressable; the derived values cover them
        warns.append(f"retype: the story types `{t}`, which is FACTS.json `{figs[t]}` — write `{{facts.{figs[t]}:,}}` (the never-retype rule, measured)")
    if story["tally"] and story["raw"]["tally"].count("\n\n") > 1:
        warns.append("@tally holds more than one block; it is ONE block, replaced in place (limit 3)")
    return fails, warns


def sizes(views):
    return {k: _tk(v) for k, v in views.items()}


# ------------------------------------------------------------------------------------ IO, check, write
def load(story_path, facts_path):
    with open(story_path, encoding="utf-8") as fh:
        story = parse_story(fh.read())
    with open(facts_path, encoding="utf-8") as fh:
        facts = json.load(fh)
    return story, facts


def _read(p):
    with open(p, encoding="utf-8") as fh:
        return fh.read()


def _first_diff(a, b):
    for i, (x, y) in enumerate(zip(a.split("\n"), b.split("\n")), 1):
        if x != y:
            return i, x, y
    la, lb = a.count("\n"), b.count("\n")
    return (min(la, lb) + 1, "<end>", "<end>") if la != lb else (None, None, None)


def newest_handoff_session(repo):
    import _wrap_facts as wf
    h = wf.handoff_facts(repo)
    m = re.search(r"^# HANDOFF #\d+ — #(\d+) → ", _read(os.path.join(repo, h["prev_name"])), re.M)
    if not m:
        raise StoryError(f"{h['prev_name']}: no `# HANDOFF #k — #N → ` title line; the session cannot be read off it")
    return int(m.group(1)), h["prev_name"]


def run_check(repo, session=None, quiet=False):
    """The freshness arm (limit 7): the NEWEST wrap only. Returns rc (0 fresh, 1 red, 0 with a declared skip)."""
    n, hname = newest_handoff_session(repo)
    if session is not None and session != n:
        print(f"⛔ --check grades the NEWEST wrap only (limit 7): the newest handoff `{hname}` is #{n}, not #{session}"); return 1
    wdir = os.path.join(repo, "notes", "_lanes", str(n), "W")
    sp, fp = os.path.join(wdir, "STORY.md"), os.path.join(wdir, "FACTS.json")
    if not os.path.exists(sp):
        print(f"wrap-views check: #{n} has no `{os.path.relpath(sp, repo)}` — the wrap ran on the phase-1 path; nothing to regenerate (declared skip)"); return 0
    story, facts = load(sp, fp)
    stage = "post" if "post" in facts else "wrap"
    views, d, s = generate(story, facts, stage)
    fails, warns = check_limits(views, story, facts, d, stage)
    vdir = os.path.join(wdir, "views")
    targets = {os.path.join(vdir, k): v for k, v in views.items()}
    for k, home in homes(d).items():
        targets[os.path.join(repo, home)] = views[k]
    red = []
    for p, text in sorted(targets.items()):
        if not os.path.exists(p):
            red.append(f"{os.path.relpath(p, repo)}: MISSING on disk")
            continue
        disk = _read(p)
        if p.endswith(d["handoff_name"]) and disk.startswith(text):
            continue      # a STRUCK addendum appended later by the next wrap is by addition
        if disk != text:
            i, x, y = _first_diff(text, disk)
            red.append(f"{os.path.relpath(p, repo)}: differs at line {i} — generated {x[:70]!r} · disk {y[:70]!r}")
    if not quiet:
        for w in warns:
            print("  ⚠", w)
        for x in fails + red:
            print("  ✗", x)
        print(f"wrap-views check #{n} ({stage}): {len(targets)} files compared · {len(red)} differ · {len(fails)} limit fails · {len(warns)} warns")
    return 1 if (fails or red) else 0


def write_views(repo, views, d, out_dir, home=True, stage="wrap"):
    os.makedirs(out_dir, exist_ok=True)
    written = []
    if stage == "post":
        for name in POST_REGEN:
            fn = FILES[name]
            p = os.path.join(out_dir, fn)
            if os.path.exists(p):
                old = _read(p)
                if not views[fn].startswith(old.rstrip("\n")):
                    i, x, y = _first_diff(old, views[fn])
                    raise StoryError(f"--stage post: the pre-commit part of {fn} is not byte-identical to the stage-wrap file (line {i}: {x[:60]!r} vs {y[:60]!r}) — by addition, nothing above is rewritten")
    for fn, text in views.items():
        p = os.path.join(out_dir, fn)
        with open(p, "w", encoding="utf-8") as fh:
            fh.write(text)
        written.append(p)
    if home:
        for fn, rel in homes(d).items():
            p = os.path.join(repo, rel)
            os.makedirs(os.path.dirname(p), exist_ok=True)
            with open(p, "w", encoding="utf-8") as fh:
                fh.write(views[fn])
            written.append(p)
        if "prior-strikes.md" in views and stage == "wrap":
            prev = os.path.join(repo, d["prev_handoff_name"])
            if os.path.exists(prev):
                cur = _read(prev)
                marker = f"## ⬛ STRUCK AT THE {d['session']} WRAP"
                if marker not in cur:
                    with open(prev, "a", encoding="utf-8") as fh:
                        fh.write(views["prior-strikes.md"])
                    written.append(prev)
    return written


# ------------------------------------------------------------------------------------ the replay diff (E3)
SHA_RE = re.compile(r"\b[0-9a-f]{8}\b")
RID_RE = re.compile(r"\bs\d{2,4}-D\d+\b")
WID_RE = re.compile(r"\bW-\d{3}[a-z0-9]*\b")
PATH_RE = re.compile(r"`([^`\s]+\.(?:md|py|json|html|txt|css|sh|jsonl))`")
NUM_RE = re.compile(r"(?<![\w.-])\d{1,3}(?:,\d{3})+(?![\w.])|(?<![\w.,-])\d{3,}(?![\w.,])")


def figures(text):
    return {"numbers": set(NUM_RE.findall(text)), "shas": set(SHA_RE.findall(text)) - {"00000000"}, "rulings": set(RID_RE.findall(text)),
            "rows": set(WID_RE.findall(text)), "paths": set(PATH_RE.findall(text))}


def headings(text, view=None):
    if view == "banner":
        return [MARK_RE.match(l[2:].strip()).group(1) if MARK_RE.match(l[2:].strip()) else "" for l in text.split("\n") if l.startswith("> - ")]
    if view == "delta":
        return [f"para{i}" for i, l in enumerate(text.split("\n")) if l.startswith("> ")]
    return [l.strip() for l in text.split("\n") if HEAD_RE.match(l)]


def diff_views(gen_text, hand_text, view=None, facts=None, story_text=None, limit=None, cut_at=None):
    """The five gradings of DESIGN.md § 8. Returns a dict with a verdict and the plain diff. `cut_at` cuts the hand
    file at a marker (a later wrap's STRUCK addendum, appended by addition, is not this wrap's view). A figure is
    SOURCED when it is in FACTS.json, the story, the derived values, or this tool's own template constants."""
    if cut_at and cut_at in hand_text:
        hand_text = hand_text[:hand_text.index(cut_at)].rstrip("\n") + "\n"
    g, h = figures(gen_text), figures(hand_text)
    src = (json.dumps(facts, ensure_ascii=False) if facts else "") + "\n" + (story_text or "")
    if facts and story_text:
        try:
            dd = derive(parse_story(story_text), facts)
            src += "\n" + json.dumps({k: v for k, v in dd.items() if k != "post"}, ensure_ascii=False, default=str)
        except StoryError:
            pass
    src += "\n" + _read(os.path.abspath(__file__))
    nums = set()
    def ints(x):
        if isinstance(x, dict):
            for v in x.values():
                ints(v)
        elif isinstance(x, list):
            for v in x:
                ints(v)
        elif isinstance(x, int) and not isinstance(x, bool):
            nums.add(f"{x:,}"); nums.add(str(x))
    ints(facts or {})
    rep = {"view": view, "figures": {}, "words": {}, "headings": {}, "size": {}, "verdict": "GREEN"}
    for k in g:
        missing = sorted(h[k] - g[k])
        extra = sorted(g[k] - h[k])
        unsourced = sorted(x for x in extra if x not in src and x not in nums) if (facts or story_text) else []
        rep["figures"][k] = {"missing": missing, "extra": extra, "extra_unsourced": unsourced}
        if missing or unsourced:
            rep["verdict"] = "RED"
    hq = QUOTE_RE.findall(hand_text)
    miss_q = [q for q in hq if q not in gen_text]
    rep["words"] = {"hand_quotes": len(hq), "missing": miss_q}
    if miss_q:
        rep["verdict"] = "RED"
    gh, hh = headings(gen_text, view), headings(hand_text, view)
    rep["headings"] = {"generated": gh, "hand": hh, "same": gh == hh}
    if gh != hh:
        rep["verdict"] = "RED"
    gt, ht = _tk(gen_text), _tk(hand_text)
    rep["size"] = {"generated": gt, "hand": ht, "ratio": round(gt / ht, 3) if ht else None, "limit": limit,
                   "over_limit": bool(limit and gt > limit), "over_ratio": bool(ht and gt > LIMITS["replay_size_ratio"] * ht)}
    if rep["size"]["over_limit"] or rep["size"]["over_ratio"]:
        rep["verdict"] = "RED"
    rep["bytes_diff"] = "".join(difflib.unified_diff(hand_text.splitlines(True), gen_text.splitlines(True), "hand", "generated"))
    return rep


def render_diff(rep):
    L = [f"## {rep['view'] or 'view'} — {rep['verdict']}", "",
         f"- SIZE: generated {rep['size']['generated']:,} · hand {rep['size']['hand']:,} · ratio {rep['size']['ratio']}" +
         (f" · limit {rep['size']['limit']:,}" if rep["size"]["limit"] else "") + (" ⛔ over the limit" if rep["size"]["over_limit"] else "") + (" ⛔ over 110% of the hand file" if rep["size"]["over_ratio"] else ""),
         f"- HIS WORDS: {rep['words']['hand_quotes']} quotations in the hand file; missing from the generated view: {len(rep['words']['missing'])}"]
    for q in rep["words"]["missing"]:
        L.append(f"  - ⛔ *\"{q[:100]}\"*")
    L.append(f"- HEADINGS: {'same' if rep['headings']['same'] else '⛔ differ'} ({len(rep['headings']['generated'])} generated · {len(rep['headings']['hand'])} hand)")
    for k, v in rep["figures"].items():
        L.append(f"- FIGURES {k}: missing {len(v['missing'])} · extra {len(v['extra'])} · extra unsourced {len(v['extra_unsourced'])}")
        if v["missing"]:
            L.append("  - ⛔ missing: " + ", ".join(v["missing"][:40]))
        if v["extra_unsourced"]:
            L.append("  - ⛔ unsourced: " + ", ".join(v["extra_unsourced"][:40]))
    L += ["", "```diff", rep["bytes_diff"].rstrip("\n"), "```", ""]
    return "\n".join(L)


# ------------------------------------------------------------------------------------ selftest
FIX_STORY = """---
session: 12
headline: the fixture wrapped, and the views were generated
one_sentence: THE FIXTURE WRAPPED AND THE VIEWS WERE GENERATED
opened_word: Good Morning!
wrap_word: wrap
conductor: Opus 5.5, a CLOUD session linked to Dave's computer
wrap_seat: delegated, Opus 5.5
lanes: A alpha (Opus 5.5)
first_beat: BUILD THE THING AND SHOW HIM
next_title: Apollo - #13: the thing, built and shown
words_files: notes/_lanes/12/DAVE-WORDS-2026-01-01-1000.md
lane_reports: notes/_subreports/2026-01-01-12-A-alpha.md
prior_handoff_struck: 1
---

## @words
- 10:00 — Good Morning!
- 10:05 — go with the thin one *(answering "thin or thick?")*
- 11:00 — wrap

## @rulings
- `s12-D1` — *"go with the thin one"* (10:05) — the thin arrow stays — ENACTED

## @summary
### decisions
- {d.rulings_summary}: the thin arrow stays.
### outputs
- Built: the thing.
### problems
- The session ran to {facts.fill.now:,}, past the hard line ({d.hard_line:,}) at {d.hard_crossed_local}.

## @did
### THE ARROW
10:05, *"go with the thin one"*: `s12-D1`, built at `aaaaaaaa`.
### THE THING
Lane A built the thing (`bbbbbbbb`).

## @problems
- ⚠ CI red on `aaaaaaaa` (step 7), fixed by `bbbbbbbb`.

## @owed
- ★★★ mine: **build the thing and show him?** — the picture page.
- ⬛ dave: **which colour?**
- ⬛ standing: **the pack re-cut** (carried)

## @struck
- **THE ARROW — THIN OR THICK?** — ANSWERED — His 10:05 line, verbatim: *"go with the thin one"*, is `s12-D1`.

## @rows
- note W-011x — the thing is built.

## @cold
- ⛔★★ **A LESSON.** sentence.

## @why
### 1. Why the arrow
Because he said so: *"go with the thin one"*.
### Resolved, and still open
Resolved: the arrow. Open: the thing.

## @findings
- **A finding.** sentence.

## @questions
None.

## @unproven
None.

## @skips
ONE DAY, NO DATE SPLIT: every figure from `_wrap_facts.py`.

## @section_usage
GM HDR:R LATEST:C

## @tally
"""
FIX_FACTS = {
    "rulings": {"total": 101, "newest": "s12-D1", "last_in_file": "s12-D1", "base": {"sha": "cccccccc", "total": 100}},
    "store": {"total": 10, "live": 5}, "carries": {"section": 12, "items": 40, "segments": 41, "struck_this_line": 1},
    "sizes": {"bytes": {}}, "git": {"head": "dddddddd" * 5, "origin_master": "bbbbbbbb" * 5, "ahead_of_origin": 1,
                                     "since": {"sha": "cccccccc", "commits": 3, "range": "cccccccc..dddddddd"},
                                     "commits": [{"sha8": "aaaaaaaa", "at": "2026-01-01T10:10:00+00:00", "subject": "a"},
                                                 {"sha8": "bbbbbbbb", "at": "2026-01-01T10:30:00+00:00", "subject": "b"},
                                                 {"sha8": "dddddddd", "at": "2026-01-01T10:50:00+00:00", "subject": "d"}],
                                     "pushed_through": "bbbbbbbb"},
    "fill": {"transcript": "knowledge/_tmp/wrap12/conductor-12.jsonl", "until": "2026-01-01T11:00:00Z", "turns": 20, "boot": 135179, "now": 372194,
             "now_at": "2026-01-01T10:59:00Z", "peak": 372194,
             "crossings": {"BUDGET_AMBER 160,000": {"message": 2, "fill": 160215, "at": "2026-01-01T10:03:00Z"},
                           "STOP_LINE_TK 300,000": {"message": 9, "fill": 301546, "at": "2026-01-01T10:20:00Z"},
                           "BUDGET_WORKING 320,000": {"message": 12, "fill": 325742, "at": "2026-01-01T10:30:00Z"},
                           "TOLERATED_TK 320,000": {"message": 12, "fill": 325742, "at": "2026-01-01T10:30:00Z"},
                           "BUDGET_HARD 350,000": {"message": 18, "fill": 354103, "at": "2026-01-01T10:45:00Z"}},
             "boot_ceiling": {"BOOT_CEILING_TK": 135000, "over_by": 179}},
    "subs": {"n": 1, "total": 1000, "largest": 1000, "smallest": 1000},
    "dates": {"tz": "Europe/London", "opened_at": "2026-01-01T10:00:00Z", "opened_local": "Thu 2026-01-01 10:00 GMT", "wrap_at": "2026-01-01T11:00:00Z",
              "wrap_local": "Thu 2026-01-01 11:00 GMT", "ritual_date": "2026-01-01", "ritual_local": "Thu 2026-01-01 11:05 GMT", "split": None},
    "handoff": {"prev_no": 20, "prev_name": "_HANDOFF-20-x.md", "no": 21},
    "ci": {"owed": {"sha8": "cccccccc", "verdict": "GREEN", "run_id": "1"}, "reds": [{"sha8": "aaaaaaaa", "step": "7", "fixed_by": "bbbbbbbb"}]},
    "chain": {"tk": 7800, "warn": 7700, "block": 10000}, "gate": {"open": "247 in scope · 0 fail · 33 warn"},
}


def selftest():
    ok = True

    def bite(name, cond):
        nonlocal ok
        print(("  ✓ " if cond else "  ✗ ") + name)
        ok = ok and bool(cond)

    def refused(name, fn):
        try:
            fn(); bite(name, False)
        except StoryError:
            bite(name, True)

    story = parse_story(FIX_STORY)
    bite("parse: front block, 17 sections known, @new derived from @owed (2 items: mine ★★★ is not ⬛; dave ⬛; standing is carried)",
         story["front"]["session"] == "12" and not story["new_explicit"] and [x["title"] for x in story["new"]] == ["WHICH COLOUR"])
    refused("parse refuses an unknown section by name", lambda: parse_story(FIX_STORY.replace("## @skips", "## @skipz")))
    refused("parse refuses a second `## @tally` (limit 3)", lambda: parse_story(FIX_STORY + "\n## @tally\nx\n"))
    refused("parse refuses a missing required section (@why)", lambda: parse_story(FIX_STORY.replace("## @why", "## @cold")))
    refused("parse refuses an owed item with an unknown owner", lambda: parse_story(FIX_STORY.replace("- ⬛ dave:", "- ⬛ bob:")))
    refused("parse refuses a @new item that types an age", lambda: parse_story(FIX_STORY.replace("## @struck", "## @new\n- ⬛ **X ITEM** [NEW — 0] — b\n\n## @struck")))
    refused("parse refuses a CAPS headline", lambda: parse_story(FIX_STORY.replace("headline: the fixture", "headline: THE fixture")))
    views, d, s = generate(story, FIX_FACTS)
    bite("derive: slug, handoff name, dossier path, report path, memory name",
         d["slug"] == "the-fixture-wrapped-and-the-views-were-generated" and d["handoff_name"] == "_HANDOFF-21-the-fixture-wrapped-and-the-views-were-generated.md"
         and d["dossier_path"] == "_DECISION-HISTORY/2026-01-01-12-the-fixture-wrapped-and-the-views-were-generated.md"
         and d["report_path"] == "notes/_subreports/2026-01-01-12-W-wrap.md" and d["memory_name"] == "wrap-12-the-fixture-wrapped-and-the-views-were-generated")
    bite("derive: the three window lines from the crossings' keys; hard crossed 10:45 GMT", (d["stop_line"], d["limit_line"], d["hard_line"]) == (300000, 320000, 350000) and d["hard_crossed_local"] == "10:45")
    bite("derive: commits line — 3 commits, 2 pushed through bbbbbbbb, dddddddd rides the wrap push", "2 pushed through `bbbbbbbb`, `dddddddd` rides the wrap push" in d["commits_line"])
    bite("placeholders: {facts.fill.now:,} → 372,194 and {d.hard_line:,} → 350,000 in the summary", "372,194" in views["SUMMARY.md"] and "350,000" in views["SUMMARY.md"] and "{" not in views["SUMMARY.md"])
    refused("a `{facts.no.such.key}` is an error, never blank", lambda: generate(parse_story(FIX_STORY.replace("{facts.fill.now:,}", "{facts.no.such.key}")), FIX_FACTS))
    bite("every view generated (15 files at stage wrap incl. new.txt, strike-1.txt, carries-delta.md; no datesplit, no 5b)",
         set(views) == {"banner.md", "delta.md", "stratum.md", "stamp.md", "handoff.md", "prior-strikes.md", "dossier.md", "report.md", "WRAP-MEMORY-HOOK.md",
                        "new.txt", "strike-1.txt", "carries-delta.md", "rows.json", "msg.txt", "SUMMARY.md"})
    bite("the fill figure shows in every view that carries it (banner, delta, stratum, handoff, report, memory, msg, summary)",
         all("372,194" in views[k] for k in ("banner.md", "delta.md", "stratum.md", "handoff.md", "report.md", "WRAP-MEMORY-HOOK.md", "msg.txt", "SUMMARY.md")))
    bite("his words are verbatim in the handoff, the delta and the dossier", all('*"go with the thin one"*' in views[k] for k in ("handoff.md", "delta.md", "dossier.md")))
    bite("new.txt carries [NEW — 0, DAVE'S] inserted by the generator, never typed", views["new.txt"].startswith("⬛ **① WHICH COLOUR** [NEW — 0, DAVE'S] —"))
    bite("rows.json: four mints born from the front block + the one note", len(json.loads(views["rows.json"])["ops"]) == 5)
    bite("the handoff's cold list = the story's 1 + the 11 standing lines", views["handoff.md"].count("\n- ⛔") + views["handoff.md"].count("\n- ⚠") + views["handoff.md"].count("\n- ✅") >= 12)
    bite("the summary is @summary verbatim under s305-D63's three headings", views["SUMMARY.md"].startswith("# #12 — summary for Dave\n\n## Decisions\n- 1 rulings, 100 → 101: the thin arrow stays.\n"))
    fails, warns = check_limits(views, story, FIX_FACTS, d)
    bite("limits: the fixture passes (no fail)", not fails)
    # mutants
    mf = json.loads(json.dumps(FIX_FACTS)); mf["fill"]["now"] = 372195
    v2, _, _ = generate(story, mf)
    bite("mutant: a fill figure changed in FACTS.json changes every view that shows it (EV's attack)",
         all(views[k] != v2[k] and "372,195" in v2[k] for k in ("banner.md", "delta.md", "stratum.md", "handoff.md", "report.md", "WRAP-MEMORY-HOOK.md", "SUMMARY.md")))
    v3, _, _ = generate(parse_story(FIX_STORY.replace("go with the thin one *(", "go with the THICK one *(")), FIX_FACTS)
    bite("mutant: a @words line changed changes the handoff", v3["handoff.md"] != views["handoff.md"])
    pad = FIX_STORY.replace("Lane A built the thing (`bbbbbbbb`).", "Lane A built the thing (`bbbbbbbb`). " + "The padding sentence goes on and on. " * 900)
    f2, _ = check_limits(generate(parse_story(pad), FIX_FACTS)[0], parse_story(pad), FIX_FACTS, d)
    bite("mutant: a handoff padded over 8,106 is BLOCKED by name", any(x.startswith("handoff:") and "BLOCK" in x for x in f2))
    _, w2 = check_limits(views, parse_story(FIX_STORY.replace("{facts.fill.now:,}", "372,194")), FIX_FACTS, d)
    bite("mutant: a typed `372,194` in a story sentence WARNS, naming the placeholder", any("retype" in w and "{facts.fill.now:,}" in w for w in w2))
    big = FIX_STORY.replace("- 11:00 — wrap", "- 11:00 — wrap\n" + "\n".join(f"- 11:{i:02d} — " + "word " * 300 for i in range(10)))
    _, w3 = check_limits(generate(parse_story(big), FIX_FACTS)[0], parse_story(big), FIX_FACTS, d)
    bite("mutant: @words over 3,000 cl100k WARNS (limit 4)", any(x.startswith("@words") for x in w3))
    # limit 1: the draft is never on the boot chain
    src = _read(os.path.join(HERE, "_gen_chain.py"))
    bite("limit 1: `_gen_chain.py` reads no `notes/_lanes` path (the story is never on the boot chain)", "notes/_lanes" not in src)
    bite("limit 1: no view is written under a `_HANDOFF-` name except the handoff itself", [k for k in views if k.startswith("_HANDOFF-")] == [])
    bite("limit 6: the chain takes only banner and delta — `_gen_chain.py` is not a path this tool writes", "_gen_chain" not in json.dumps(list(homes(d).values())))
    # post stage
    pf = json.loads(json.dumps(FIX_FACTS))
    pf["post"] = {"wrap_sha": "eeeeeeee", "seat_sha": "ffffffff", "gate_wrap": "248 in scope · 0 fail · 31 warn", "push_range": "bbbbbbbb..ffffffff",
                  "pushed_at": "2026-01-01T11:30:00Z", "launched_at": "2026-01-01T11:08:00Z", "minutes_to_push": 22.0,
                  "ci": {"run_id": "99", "verdict": "GREEN", "jobs": {"gates": "completed/success", "render": "completed/success", "release": "completed/success"}, "sha8": "ffffffff"},
                  "prepush": {"pass": 155, "fail": 0, "advisory": 3, "could_not_ask": 9, "tests": 32, "test_failures": 0, "surveys": 4},
                  "chain_tk_after_regen": 7824, "chain_tk_after_5b": None, "titles": {"brief": "T", "derived": "Apollo - #13: x"}}
    vp, dp, _ = generate(story, pf, "post")
    bite("post: 5b and msg-5b written; handoff/report/memory grow BY ADDITION (the wrap-stage text is a prefix)",
         "5b.md" in vp and "msg-5b.txt" in vp and all(vp[k].startswith(views[k].rstrip("\n")) for k in ("handoff.md", "report.md", "WRAP-MEMORY-HOOK.md")))
    bite("post: the handoff addendum carries the `CI owed:` line (s306-D7's gate)", "CI owed: this addendum's own commit — read by the next opener with python3 knowledge/_ci_readback.py --owed" in vp["handoff.md"])
    with tempfile.TemporaryDirectory() as td:
        os.makedirs(os.path.join(td, "notes", "_lanes", "12", "W"))
        open(os.path.join(td, "_HANDOFF-20-x.md"), "w").write("# HANDOFF #20 — #11 → #12 — X\n\nold\n")
        out = os.path.join(td, "notes", "_lanes", "12", "W", "views")
        w = write_views(td, views, d, out, home=True)
        bite("write: views/ plus the five homes and the prior handoff's STRUCK addendum (by addition, once)",
             os.path.exists(os.path.join(td, d["handoff_name"])) and os.path.exists(os.path.join(td, d["dossier_path"]))
             and _read(os.path.join(td, "_HANDOFF-20-x.md")).startswith("# HANDOFF #20") and "STRUCK AT THE #12 WRAP" in _read(os.path.join(td, "_HANDOFF-20-x.md")))
        write_views(td, views, d, out, home=True)
        bite("write: a second write does not append the STRUCK addendum twice", _read(os.path.join(td, "_HANDOFF-20-x.md")).count("STRUCK AT THE #12 WRAP") == 1)
        # the freshness arm
        open(os.path.join(td, "notes", "_lanes", "12", "W", "STORY.md"), "w").write(FIX_STORY)
        json.dump(FIX_FACTS, open(os.path.join(td, "notes", "_lanes", "12", "W", "FACTS.json"), "w"))
        open(os.path.join(td, d["handoff_name"]), "a").write("")
        rc0 = run_check(td, quiet=True)
        bite("--check: fresh views → green (the newest handoff names #12)", rc0 == 0)
        hp = os.path.join(td, d["handoff_name"])
        mutated = _read(hp).replace("372,194", "372,195")
        open(hp, "w").write(mutated)
        bite("mutant: a hand edit to a generated file (the handoff) turns --check red", run_check(td, quiet=True) == 1)
        open(hp, "w").write(views["handoff.md"])
        bite("--check: refuses a --session that is not the newest wrap (limit 7)", run_check(td, session=11, quiet=True) == 1)
        os.remove(os.path.join(td, "notes", "_lanes", "12", "W", "STORY.md"))
        bite("--check: a newest wrap without STORY.md is a DECLARED skip, not a red", run_check(td, quiet=True) == 0)
        # post stage refuses a rewritten pre-commit part
        open(os.path.join(out, "handoff.md"), "w").write(views["handoff.md"].replace("372,194", "372,195"))
        refused("--stage post refuses when the pre-commit part on disk is not the stage-wrap text", lambda: write_views(td, vp, dp, out, home=False, stage="post"))
    # the replay diff
    rep = diff_views(views["handoff.md"], views["handoff.md"].replace("`bbbbbbbb`", "`bbbbbbbb` `12345678`"), "handoff", FIX_FACTS, FIX_STORY)
    bite("diff: a sha in the hand file missing from the generated view is RED, named", rep["verdict"] == "RED" and rep["figures"]["shas"]["missing"] == ["12345678"])
    rep2 = diff_views(views["handoff.md"], views["handoff.md"], "handoff", FIX_FACTS, FIX_STORY)
    bite("diff: identical files are GREEN with the same headings", rep2["verdict"] == "GREEN" and rep2["headings"]["same"])
    rep3 = diff_views(views["handoff.md"].replace("go with the thin one", "x"), views["handoff.md"], "handoff")
    bite("diff: a quotation of his missing from the generated view is RED", rep3["verdict"] == "RED" and rep3["words"]["missing"])
    # the frozen fixtures, when present: regenerate and compare byte-exact
    fx = sorted(glob_fixtures())
    for fdir in fx:
        st, fc = load(os.path.join(fdir, "STORY.md"), os.path.join(fdir, "FACTS.json"))
        stage = "post" if "post" in fc else "wrap"
        vv, _, _ = generate(st, fc, stage)
        exp = os.path.join(fdir, "expected")
        bad = [k for k in vv if not os.path.exists(os.path.join(exp, k)) or _read(os.path.join(exp, k)) != vv[k]]
        bite(f"fixture {os.path.basename(fdir)}: {len(vv)} views regenerate byte-exact against expected/" + (f" — DIFFER: {', '.join(bad)}" if bad else ""), not bad)
    print("wrap-views selftest:", "PASS" if ok else "FAIL")
    return 0 if ok else 1


def glob_fixtures(repo=REPO):
    import glob
    return [p for p in glob.glob(os.path.join(repo, "knowledge", "_tests", "wrap_views", "*")) if os.path.isdir(os.path.join(p, "expected"))]


# ------------------------------------------------------------------------------------ main
def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("verb", nargs="?", choices=["diff"], help="`diff`: grade a generated view against a hand-written file (E3)")
    ap.add_argument("--selftest", action="store_true")
    ap.add_argument("--check", action="store_true", help="the freshness arm: regenerate the newest wrap's views and compare with disk")
    ap.add_argument("--session", type=int); ap.add_argument("--story"); ap.add_argument("--facts"); ap.add_argument("--out")
    ap.add_argument("--stage", choices=["wrap", "post"], default="wrap")
    ap.add_argument("--write", action="store_true"); ap.add_argument("--no-home", action="store_true")
    ap.add_argument("--repo", default=REPO)
    ap.add_argument("--generated"); ap.add_argument("--hand"); ap.add_argument("--view"); ap.add_argument("--limit", type=int)
    ap.add_argument("--story-text", help="diff: the story file, so extra figures can be sourced")
    ap.add_argument("--cut-at", help="diff: cut the hand file at this marker (a later wrap's by-addition addendum)")
    a = ap.parse_args(argv)
    if a.selftest:
        return selftest()
    try:
        if a.check:
            return run_check(a.repo, a.session)
        if a.verb == "diff":
            if not (a.generated and a.hand):
                ap.error("diff needs --generated and --hand")
            facts = json.load(open(a.facts, encoding="utf-8")) if a.facts else None
            st = _read(a.story_text) if a.story_text else None
            rep = diff_views(_read(a.generated), _read(a.hand), a.view, facts, st, a.limit, a.cut_at)
            text = render_diff(rep)
            if a.out:
                with open(a.out, "w", encoding="utf-8") as fh:
                    fh.write(text)
                print(f"{a.view or 'view'}: {rep['verdict']} → {a.out}")
            else:
                print(text)
            return 0 if rep["verdict"] == "GREEN" else 1
        if a.session is None:
            ap.error("--session N is required")
        wdir = os.path.join(a.repo, "notes", "_lanes", str(a.session), "W")
        sp = a.story or os.path.join(wdir, "STORY.md")
        fp = a.facts or os.path.join(wdir, "FACTS.json")
        out = a.out or os.path.join(wdir, "views")
        story, facts = load(sp, fp)
        if int(story["front"]["session"]) != a.session:
            raise StoryError(f"--session {a.session} but the story's front block says {story['front']['session']}")
        views, d, s = generate(story, facts, a.stage)
        fails, warns = check_limits(views, story, facts, d, a.stage)
        sz = sizes(views)
        lim = {"banner.md": LIMITS["banner"]["block"], "delta.md": LIMITS["delta"]["block"], "handoff.md": LIMITS["handoff"]["block"], "dossier.md": LIMITS["dossier"]["warn"]}
        print(f"wrap-views {d['session']} stage {a.stage}: {len(views)} views from {os.path.relpath(sp, a.repo)} + {os.path.relpath(fp, a.repo)}")
        for k in views:
            disk = os.path.join(out, k)
            state = "new" if not os.path.exists(disk) else ("same" if _read(disk) == views[k] else "DIFFERS from disk")
            print(f"  {k:22} {sz[k]:>6,} cl100k" + (f" / {lim[k]:,}" if k in lim else "        ") + f"  {state}")
        for w in warns:
            print("  ⚠", w)
        for x in fails:
            print("  ✗", x)
        if fails:
            print(f"⛔ REFUSED — {len(fails)} limit(s) fail; nothing written"); return 1
        if a.write:
            w = write_views(a.repo, views, d, out, home=not a.no_home, stage=a.stage)
            print(f"written {len(w)} file(s):")
            for p in w:
                print("  ", os.path.relpath(p, a.repo))
        else:
            print("DRY RUN — add --write to write views/ and the homes (" + ", ".join(homes(d).values()) + ")")
        return 0
    except StoryError as e:
        print("⛔ REFUSED:", e); return 1


if __name__ == "__main__":
    sys.exit(main())
