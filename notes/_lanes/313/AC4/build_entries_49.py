"""#313 AC4 — build s313-D49.. entries from Dave's 23:17 and 23:18 exports and the two pages' own text.
One ruling per call; nothing retyped: question, recommendation and his choice/comment are lifted verbatim.
Writes notes/_lanes/313/AC4/s313-D<n>.entry.json. Run at the repo root."""
import html, json, os, re

OUT = "notes/_lanes/313/AC4"
PAGES = [
    ("notes/_lanes/313/DAVE-RULINGS-2026-10-01-2317-seven-trees-redone.md",
     "notes/_REVIEW-313-L4-seven-trees-redone-2026-10-01-v1.html", "23:17"),
    ("notes/_lanes/313/DAVE-RULINGS-2026-10-01-2318-what-tonight-asked-you.md",
     "notes/_REVIEW-313-Q-what-tonight-asked-you-2026-10-01-v1.html", "23:18"),
]
META = {"button": "button", "table": "table", "date-picker": "date-picker", "metric": "metric", "slider": "slider",
        "switch": "selection-controls", "dialog": "modals", "family": "selection-controls",
        "selection-controls": "selection-controls", "modals": "modals", "four": "selection-controls"}
EXTRA = {"bottom-edge": ["knowledge/snippets/Navigations.reference.html", "knowledge/snippets/Dropdown.reference.html"],
         "square-name": ["knowledge/tokens/layout.json"], "fork-rows": ["knowledge/_TOKEN-FORK-LEDGER.json"]}


def text(x):
    return re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", "", x))).strip()


def calls_of(page):
    s = open(page, encoding="utf-8").read()
    out = []
    for m in re.finditer(r'<div class="call[^"]*"([^>]*)>(.*?)<div class="stamp">', s, re.S):
        attrs, body = m.group(1), m.group(2)
        cid = re.search(r'data-id="([^"]+)"', attrs).group(1)
        q = html.unescape(re.search(r'data-q="([^"]+)"', attrs).group(1))
        para = re.search(r'<p class="q">(.*?)</p>', body, re.S)
        rec = re.search(r'<p class="rec">(.*?)</p>', body, re.S)
        out.append(dict(id=cid, q=q, para=text(para.group(1)) if para else "", rec=text(rec.group(1)) if rec else ""))
    return out


def answers_of(export):
    s = open(export, encoding="utf-8").read()
    out = {}
    for m in re.finditer(r"(?m)^(\d+)\. (.+)\n((?:   .+\n?)+)", s):
        n, q, block = m.group(1), m.group(2), m.group(3)
        f = dict(re.findall(r"(?m)^   (Recommended|Chose|Comment): (.*)$", block))
        out[n] = dict(q=q.strip(), **f)
    return out


n = 49
made = []
for export, page, hhmm in PAGES:
    calls = calls_of(page)
    ans = answers_of(export)
    for c in calls:
        num = c["q"].split(".")[0]
        a = ans.get(num)
        if not a:
            continue
        chose, comment = a.get("Chose", ""), a.get("Comment", "none")
        against = "(not the recommendation)" in chose
        head = re.sub(r"^\d+\.\s*", "", c["q"]).rstrip("?")
        pick = re.sub(r"\s*\((the recommendation|not the recommendation)\)\s*$", "", chose)
        headline = ("%s: %s." % (head, comment if pick.startswith("None of these") else pick)).upper()
        parts = [headline, "The page asked, verbatim: '%s'" % (c["para"] or c["q"]) + ";"]
        if c["rec"]:
            parts.append("its recommendation, verbatim: '%s';" % c["rec"])
        elif a.get("Recommended"):
            parts.append("its recommendation, verbatim: '%s';" % a["Recommended"])
        parts.append("Dave, by click, verbatim: '%s'%s; comment%s." % (
            pick, " — AGAINST the recommendation" if against else " (the recommendation)",
            ", verbatim: '%s'" % comment if comment != "none" else ": none"))
        if "Hold" in pick:
            parts.append("Held at his word: nothing is decided by this ruling but the hold.")
        rid = "s313-D%d" % n
        meta = META.get(c["id"]) or META.get(c["id"].split("-")[0])
        governs = (["knowledge/components/%s.meta.json" % meta] if meta and page.endswith("seven-trees-redone-2026-10-01-v1.html") else []) \
            + EXTRA.get(c["id"], []) + [page]
        e = {"id": rid, "ruled": " ".join(parts), "date": "2026-10-01", "by": "Dave",
             "says": "review page export, Thu 2026-10-01 %s BST ('Copy as text' of %s pasted into chat #313, saved verbatim as %s) · call %s, verbatim: '%s' — chose, by click, verbatim: '%s' · comment: %s"
                     % (hhmm, page, export, num, re.sub(r"^\d+\.\s*", "", a["q"]), chose, comment if comment == "none" else "'%s'" % comment),
             "governs": governs,
             "evidence": ["chat #313 2026-10-01 (live) - his %s BST export, quoted verbatim in `says`" % hhmm, export, page],
             "status": "ruled"}
        os.makedirs(OUT, exist_ok=True)
        json.dump(e, open(os.path.join(OUT, rid + ".entry.json"), "w", encoding="utf-8"), indent=1, ensure_ascii=False)
        made.append((rid, c["id"], "AGAINST" if against else "rec"))
        n += 1
for m in made:
    print(*m)
print(len(made), "entries")
