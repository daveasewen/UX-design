#!/usr/bin/env python3
"""PROTOTYPE (#300 lane C, work file — NOT wired, NOT a gate yet): generate the BOOT CARD.

The card is what a cold conductor reads at the opener instead of the handoff + chain + memory
index + hook. It is GENERATED at the wrap (after 5b) from files that already exist:
  - the newest _HANDOFF-<k>-*.md  (H1 → session number, OWED list, section map)
  - _CHAIN.md                      ("YOU ARE #N. TITLE THIS CHAT →" line — the routing witness)
  - an optional '## FIRST BEAT' section in the handoff, authored by the wrap seat
Usage:
  python3 gen_boot_card_proto.py                 # write the card, print its size
  python3 gen_boot_card_proto.py --check         # fresh? size cap? routing agrees? owed complete?
  python3 gen_boot_card_proto.py --section OWED  # print one handoff section by heading substring
"""
import glob, os, re, sys

REPO = os.environ.get("APOLLO_REPO") or os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../.."))
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "BOOT-CARD-300-prototype.md")
CAP_TAPE = 900           # cl100k; ×1.62 MEASURED for a card read (lane C report §2) ⇒ ≤ ~1,460 real

def newest_handoff():
    hs = [(int(m.group(1)), p) for p in glob.glob(os.path.join(REPO, "_HANDOFF-*.md"))
          if (m := re.match(r"_HANDOFF-(\d+)-", os.path.basename(p)))]
    return max(hs)[1]

def sections(text):
    """[(heading, body)] split on '## ' headings; the preamble is ('', ...)."""
    out, head, buf = [], "", []
    for line in text.split("\n"):
        if line.startswith("## "):
            out.append((head, "\n".join(buf))); head, buf = line[3:].strip(), []
        else:
            buf.append(line)
    out.append((head, "\n".join(buf)))
    return out

def tape(s):
    import tiktoken
    return len(tiktoken.get_encoding("cl100k_base").encode(s, disallowed_special=()))

def first_bold(item, words=28):
    """The item's question/headline in words: markdown and status glyphs stripped, first sentence, capped."""
    t = re.sub(r"^\s*(\d+\.|[-*])\s*", "", item)
    t = re.sub(r"\*\*|[\u2B1B\u2605\u26D4\u26A0\u2705\uFE0F]", "", t).strip()
    m = re.match(r"(.+?[?.!])(\s|$)", t)
    t = (m.group(1) if m else t).strip()
    w = t.split()
    return " ".join(w[:words]) + (" …" if len(w) > words else "")

def build():
    hp = newest_handoff(); ht = open(hp, encoding="utf-8").read()
    h1 = next(l for l in ht.split("\n") if l.startswith("# "))
    m = re.search(r"#(\d+)\s*→\s*#(\d+)\s*—\s*(.+)$", h1)
    prev_n, n, last_title = int(m.group(1)), int(m.group(2)), m.group(3).strip()
    secs = sections(ht)
    owed = next((b for h, b in secs if h.upper().find("OWED") >= 0), "")
    items = [l for l in owed.split("\n") if re.match(r"^\d+\.\s", l)]
    beat = next((b.strip() for h, b in secs if h.upper().startswith("FIRST BEAT")), None)
    chain = open(os.path.join(REPO, "_CHAIN.md"), encoding="utf-8").read()
    tm = re.search(r"YOU ARE #(\d+)\. TITLE THIS CHAT →\*\*\s*`([^`]+)`", chain)
    chain_n, title = (int(tm.group(1)), tm.group(2)) if tm else (None, "(no title line in _CHAIN.md)")
    fmap = " · ".join(f"{re.sub(r'[^A-Za-z0-9 ]', '', h).strip()[:22] or 'top'} {tape(b):,}"
                      for h, b in secs if h or b.strip())
    rel = os.path.basename(hp)
    L = []
    L.append(f"<!-- GENERATED at the wrap from {rel} + _CHAIN.md — DO NOT HAND-EDIT. "
             f"Check: python3 knowledge/_gen_boot_card.py --check -->")
    L.append(f"# BOOT CARD — you are #{n}")
    L.append(f"**Title this chat →** `{title}`  ")
    L.append("**Repo:** `$HOME/mnt/Projects--UX-design` (the empty `UX-design--UX-design` is not it)  ")
    L.append(f"**Last session #{prev_n}:** {last_title.capitalize()}")
    L.append("")
    L.append("## First beat")
    L.append(beat if beat else f"(FALLBACK — the wrap wrote no FIRST BEAT) Open on owed item 1: "
             f"{first_bold(items[0]) if items else '(none)'}")
    L.append("")
    L.append(f"## Owed to Dave — {len(items)} questions, in order (ask in plain words, never ID codes)")
    for i, it in enumerate(items, 1):
        L.append(f"{i}. {first_bold(it)}")
    L.append("")
    cold = next((b for h, b in secs if "COLD SEAT" in h.upper()), "")
    cold_items = [l for l in cold.split("\n") if re.match(r"^(\d+\.|[-*])\s", l)][:4]
    post = next((b for h, b in secs if "POST-WRAP" in h.upper()), "")
    post_items = [l for l in post.split("\n") if re.match(r"^\d+\.\s", l)][:3]
    if cold_items:
        L.append("## Before you touch anything")
        L += [f"- {first_bold(x, 16)}" for x in cold_items]
        L.append("")
    if post_items:
        L.append("## Since the wrap (post-wrap addendum)")
        L += [f"- {first_bold(x, 16)}" for x in post_items]
        L.append("")
    L.append("## Fetch on demand — never at boot")
    L.append(f"- handoff section: `python3 knowledge/_gen_boot_card.py --section <HEADING>` · map (tape): {fmap}")
    L.append("- chain banner: `python3 knowledge/_memento_search.py --fetch gm:LATEST` · whole chain: `cat _CHAIN.md`")
    L.append("- every open item across handoffs: `_CARRIES.md` § residual (fetch the section, not the file)")
    L.append("- how hot (cloud seat, container shell): sum input+cache_creation+cache_read of the newest message in the newest `/root/.claude/projects/*/*.jsonl`")
    L.append("- render: `export TMPDIR=/dev/shm; bash knowledge/_render/ensure_env.sh; source knowledge/_render/seat_env.sh`")
    return "\n".join(L) + "\n", {"n": n, "chain_n": chain_n, "items": len(items), "beat": bool(beat), "handoff": rel}

def main(argv):
    if "--section" in argv:
        key = argv[argv.index("--section") + 1].upper()
        for h, b in sections(open(newest_handoff(), encoding="utf-8").read()):
            if key in h.upper():
                print("## " + h + "\n" + b); return 0
        print(f"NO SECTION matching {key!r}"); return 1
    card, meta = build()
    if "--check" in argv:
        fails = []
        if not os.path.exists(OUT) or open(OUT, encoding="utf-8").read() != card:
            fails.append("STALE — the card on disk is not what the sources generate now")
        t = tape(card)
        if t > CAP_TAPE: fails.append(f"OVER CAP — {t:,} tape > {CAP_TAPE:,}")
        if meta["chain_n"] != meta["n"]:
            fails.append(f"ROUTING — handoff says #{meta['n']}, chain says #{meta['chain_n']}")
        if meta["items"] == 0: fails.append("NO OWED ITEMS parsed from the handoff")
        if not meta["beat"]: fails.append("NO FIRST BEAT section in the handoff (fallback used)")
        print("BOOT CARD:", "OK" if not fails else "FAIL", f"({t:,} tape · #{meta['n']} · {meta['items']} owed)")
        for f in fails: print("  -", f)
        return 1 if fails else 0
    open(OUT, "w", encoding="utf-8").write(card)
    print(f"wrote {os.path.relpath(OUT, REPO)} · {len(card.encode()):,} B · {tape(card):,} tape · meta {meta}")
    return 0

if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
