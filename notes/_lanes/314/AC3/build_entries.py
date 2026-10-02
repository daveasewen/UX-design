"""#314 lane AC3: build one ruling entry per call of Dave's 14:55 export, from the export and the
page HTML, so nothing is retyped (the #313 AC3 route). Writes notes/_lanes/314/AC3/s314-D<n>.entry.json."""
import json, re, os
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..", ".."))
EXP = "notes/_lanes/314/DAVE-RULINGS-2026-10-02-1455-borders-switch-templates.md"
PAGE = "notes/_REVIEW-314-the-borders-the-switch-family-the-templates-2026-10-02-v1.html"
calls_page = json.load(open(os.path.join(ROOT, "notes/_lanes/314/AC3/page-calls.json"), encoding="utf-8"))
txt = open(os.path.join(ROOT, EXP), encoding="utf-8").read()

exp = {}
for b in re.finditer(r"^(\d+)\. (.*?)\n   Recommended: (.*?)\n   Chose: (.*?)\n   Comment: (.*?)(?=\n\n\d+\. |\n*\Z)", txt, re.S | re.M):
    n = int(b.group(1))
    exp[n] = dict(title=b.group(2), rec=b.group(3), chose=b.group(4), comment=b.group(5).rstrip("\n"))
assert len(exp) == 28, len(exp)
T = lambda s: "knowledge/components/template-%s.meta.json" % s
S = lambda s: "knowledge/snippets/%s.reference.html" % s
M = lambda s: "knowledge/components/%s.meta.json" % s
PAGES10 = ["auth", "confirmation", "create-edit", "dashboard", "detail", "empty", "error", "list-index", "report", "settings"]
H = {
 1: ("THE EDGE IN LIGHT MODE STAYS AS RULED: INVISIBLE IN LIGHT, GREY IN DARK; AND, BY HIS COMMENT, THERE IS NEVER A FOCUS STATE UNLESS THE PERSON IS USING KEYBOARD CONTROLS (his comment is the word lane AM enacted under s313-D71)", [S("Dropdown"), S("Navigations"), PAGE]),
 2: ("THE ACCOUNT MENU KEEPS THE SAME EDGE AS EVERY OTHER FLOATING SURFACE; ITS OLD GREY LINE DOES NOT COME BACK (the tree already draws this, s313-D58 at 4d62f3c0; nothing to build)", [S("Navigations"), PAGE]),
 3: ("THE BANKING DASHBOARD'S ACCOUNT MENU IS FIXED AT THE SOURCE", ["dashboards/international-banking-dashboard.canon.html"]),
 4: ("SWITCH, CHECKBOX, RADIO AND CHIP ARE EACH OFFERED FOR THE INPUT ROLE, BESIDE SELECTION CONTROLS", ["knowledge/roles.json", M("switch"), M("checkbox"), M("radio"), M("chip")]),
 5: ("THE PARTS THAT BORROW A CONTROL POINT AT IT BY NAME", [M("data-grid"), M("transfer-list"), M("rating")]),
 6: ("THE SELECTION-CONTROLS FAMILY KEEPS ONLY WHAT THE FOUR SHARE", [M("selection-controls")]),
 7: ("THE PAGE TEMPLATES ARE ONLY EXAMPLE OR INSPIRATION FOR DESIGNERS, PROPERLY BUILT, AND AUTOMATED BUILDS IGNORE THEM AND NEVER TRACE A PAGE, by his comment; NOT the page's recommendation (he chose none of the options)", ["knowledge/_validate_example_fence.py", "knowledge/components/meta.schema.json", "apollo-spider/skills/generate-from-canon/SKILL.md"]),
 8: ("THE REBUILT DASHBOARD TEMPLATE LOOKS RIGHT", [T("dashboard")]),
 9: ("THE REBUILT LIST INDEX TEMPLATE LOOKS RIGHT", [T("list-index")]),
 10: ("THE REBUILT DETAIL TEMPLATE CHANGES: THE SUMMARY AND THE TIMELINE FILL THEIR CONTAINER AND THE TOP SECTION'S LAYOUT CHANGES, by his comment; NOT the page's recommendation", [T("detail"), S("Summary"), S("Timeline")]),
 11: ("THE REBUILT CREATE AND EDIT TEMPLATE CHANGES: HELP TEXT IS SHORT AND DOES NOT WRAP, AND EXTRA INFORMATION GOES IN A HELP POPOVER OR TOOLTIP, by his comment; NOT the page's recommendation. The rule he says needs defining is DRAFTED by lane TP2 (notes/_subreports/2026-10-02-314-TP2.md section 4, R1) and is NOT part of this ruling", [T("create-edit"), M("form-layout"), M("input-fields")]),
 12: ("THE REBUILT SETTINGS TEMPLATE LOOKS RIGHT", [T("settings")]),
 13: ("THE WIZARD TEMPLATE IS PARKED, by his comment; NOT the page's recommendation", [T("wizard")]),
 14: ("THE REBUILT SIGN-IN TEMPLATE LOOKS RIGHT; NOT the page's recommendation, which was Change it", [T("auth")]),
 15: ("THE CONFIRMATION TEMPLATE: NO OPTION CLICKED; HIS COMMENT IS THE WORD: AN AMBER PENDING ROUNDEL, THE SUMMARY FILLS ITS CONTAINER, THE ACTIONS COME AFTER THE SUMMARY, BELOW THE DATA. The amber roundel CLASHES with his call 26 (s314-D26, 'No pending kind; the chip carries it'); both are inscribed verbatim and neither is resolved here: Dave's open question W-314d1", [T("confirmation"), M("confirmation")]),
 16: ("THE EMPTY TEMPLATE CHANGES: IT DOES NOT NEED THE BORDER, by his comment; NOT the page's recommendation", [T("empty"), S("Empty-state")]),
 17: ("THE ERROR TEMPLATE CHANGES: IT DOES NOT NEED THE BORDER, by his comment; NOT the page's recommendation", [T("error"), S("Empty-state")]),
 18: ("THE REPORT TEMPLATE CHANGES: THE KPI ROW HAS NO ORPHAN AT ANY WIDTH (FIVE IN A ROW, A 2x2 GRID OR A COLUMN STACK, IN HIS WORDS), by his comment; NOT the page's recommendation", [T("report"), S("Metric")]),
 19: ("THE ERROR PAGE'S COLUMN IS THE EMPTY-STATE PART", [T("error")]),
 20: ("SECTIONS ON ORDINARY PAGES SIT ON RULES, NOT ON A SURFACE; THE SETTINGS WORDING IS AMENDED. The page gives no amended wording: lane TP2's draft of the settings `when` (notes/_subreports/2026-10-02-314-TP2.md section 4, R2) is a PROPOSED text for Dave, not part of this ruling, and s272-D91's text is unchanged in the store", [T("settings"), T("detail"), T("create-edit")]),
 21: ("EVERY PAGE TEMPLATE CARRIES THE APP FRAME", [T(p) for p in PAGES10]),
 22: ("THE LIST INDEX KEEPS BOTH FORMS, EACH CHOSEN BY ITS JOB", [T("list-index")]),
 23: ("THE SIGN-IN PAGE'S LOGO STAYS AT 40", [T("auth")]),
 24: ("A PASSWORD REVEAL: NO OPTION CLICKED; HIS COMMENT IS THE WORD: THE ICON LIBRARY DOES HAVE AN EYE, PERHAPS LABELLED VISIBLE AND HIDDEN, correcting the page's premise that it has none", [M("input-fields"), S("Input-fields"), T("auth")]),
 25: ("THE DOWNLOAD LIVES ON THE DETAIL PAGE, NOT ON EACH TRANSACTION ROW", [T("detail"), T("list-index")]),
 26: ("NO PENDING KIND ON THE CONFIRMATION PART; THE STATUS CHIP CARRIES PENDING. This CLASHES with his call 15 comment (s314-D15, 'We should have an amber pending roundel'); both are inscribed verbatim and neither is resolved here: Dave's open question W-314d1", [M("confirmation"), S("Confirmation")]),
 27: ("THE BENTO DASHBOARD TEMPLATE GETS ITS OWN LANE, REBUILT THE SAME WAY; the lane is owed (work row W-314b1, owner claude)", [T("dashboard-bento")]),
 28: ("THE LIBRARY FINDINGS ARE FIXED AT THE PART, BY ONE LANE", [S(x) for x in ["Empty-state", "Form-layout", "Segmented-control", "Stepper", "Input-fields", "Confirmation", "Summary", "Dropdown", "Metric", "Anchor-nav", "Action-bar", "Page-header-lockup", "Timeline"]]),
}
STATUS = {
 15: "ruled — no option clicked; his comment is the word. Its amber pending roundel clashes with s314-D26 and is held as Dave's open question W-314d1; the roundel is built at 75798e51 as a separable hunk, the rest of his comment (the summary fills, the actions after it) is built there too",
 26: "ruled — clashes with s314-D15's amber pending roundel; Dave's open question W-314d1. The chip is on the page; the roundel hunk is held at 75798e51 until he picks",
}
os.makedirs(os.path.join(ROOT, "notes/_lanes/314/AC3"), exist_ok=True)
for c in calls_page:
    n = int(c["title"].split(".")[0]); e = exp[n]
    assert e["title"] == c["title"].split(". ", 1)[1], (n, e["title"], c["title"])
    head, gov = H[n]
    for g in gov:
        assert os.path.exists(os.path.join(ROOT, g)), g
    comment_lines = e["comment"].split("\n")
    is_rec = e["chose"].endswith("(the recommendation)")
    if e["chose"] == "not answered":
        pick = "Dave picked no option (his export, verbatim: 'Chose: not answered')"
        pick_says = "chose, verbatim: 'not answered'"
    else:
        val = re.sub(r" \((the recommendation|not the recommendation)\)$", "", e["chose"])
        pick = "Dave, by click, verbatim: '%s' (%s)" % (val, "the recommendation" if is_rec else "against the recommendation; the page recommended '%s'" % e["rec"])
        pick_says = "chose, by click, verbatim: '%s'" % e["chose"]
    if e["comment"] == "none":
        com, com_says = "comment: none", "comment: none"
    else:
        com = "his comment, verbatim: '%s'" % " ".join(comment_lines)
        com_says = "comment, verbatim: '%s'" % " / ".join(comment_lines)
        if len(comment_lines) > 1:
            com += ". His comment spans two lines in the export; `says` marks the break with ' / ', `ruled` joins them with a space"
    ruled = "%s. The page asked, verbatim: '%s'; its recommendation, verbatim: '%s'. %s; %s." % (head, c["q"], c["rec"], pick, com)
    says = ("review page export, Fri 2026-10-02 14:55 BST ('Copy as text' of %s, saved verbatim as %s) · call %d, verbatim: '%s' — %s · %s"
            % (PAGE, EXP, n, e["title"], pick_says, com_says))
    entry = {"id": "s314-D%d" % n, "ruled": ruled, "date": "2026-10-02", "by": "Dave", "says": says,
             "governs": gov,
             "evidence": ["chat #314 2026-10-02 (live) - his 14:55 BST export of the review page, quoted verbatim in `says`", EXP, PAGE],
             "status": STATUS.get(n, "ruled")}
    json.dump(entry, open(os.path.join(ROOT, "notes/_lanes/314/AC3/s314-D%d.entry.json" % n), "w", encoding="utf-8"), indent=1, ensure_ascii=False)
    open(os.path.join(ROOT, "notes/_lanes/314/AC3/s314-D%d.entry.json" % n), "a").write("\n")
print("built", len(calls_page))
