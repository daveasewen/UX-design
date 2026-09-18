#!/usr/bin/env python3
"""Inscribe s282-D5 at the END of knowledge/_rulings.json by TEXTUAL SPAN (N 0).
Reads the file, asserts the tail is exactly '\n ]\n}\n', inserts '\n ,\n <obj>'
before it. Idempotent: refuses if s282-D5 already present."""
import json, sys, pathlib

P = pathlib.Path("/sessions/tender-hopeful-allen/mnt/UX-design/knowledge/_rulings.json")
txt = P.read_text(encoding="utf-8")
if '"s282-D5"' in txt:
    print("already inscribed — no-op"); sys.exit(0)

TAIL = "\n ]\n}"
assert txt.endswith(TAIL), repr(txt[-20:])

says = (
 "HIS OWN EXPORT of the #282 logo-review page, notes/_lanes/282/logo-review/"
 "DAVE-EXPORT-2026-09-18.json, exportedAt 2026-09-18T08:20:48.214Z, page "
 "LOGO-REVIEW-2026-09-17, following REVIEW-icons-2026-09-16-v2 — TWELVE rows, NINE "
 "answered, THREE moot under s282-D4 (q1-colour, q1-mono, q1-light-mono: the identifier "
 "defect rows). THE NINE CHOICES, each the option sentence printed for that row on "
 "notes/_lanes/282/logo-review/LOGO-REVIEW-2026-09-17.html: "
 "q1-hexagon-pair = (a) 'Keep both files and both nodes' (recommended (a), not overruled); "
 "q2-legacy = (a) 'Full colour both grounds — masterbrand-light-colour on light, "
 "masterbrand-dark-colour on dark' (recommended (a)); q2-mono = (a) same sentence; "
 "q2-console = (a) same sentence; q2-supercharge = (a) same sentence — four themes, four "
 "times (a); q3-clearspace = (c) 'Leave it unruled and keep the pointer' — OVERRULED "
 "against the recommended (a) 'Author it from create.hsbc — your authenticated fetch, then "
 "the number is the refresh's'; q4-hexagon-only = (a) 'Permit the hexagon on the nav-rail "
 "head, app tile and favicon — each conditional on Create Direct approval and ‘HSBC’ in "
 "view' (recommended (a)); q5-guideline-shape = (a) 'Merge into one logo guideline' — "
 "OVERRULED against the recommended (b) 'logos.md becomes a pointer: the asset inventory "
 "and the export receipt stay, the standard points at brand-refresh-assets.md and "
 "create.hsbc'; q6-unreferenced = (b) 'Retire the four identifier variants until a real "
 "identifier exists' — OVERRULED against the recommended (a) 'Keep all eight as library; "
 "the declared null stands'. "
 "HIS FOUR NOTES, VERBATIM, exactly as the export carries them (trailing whitespace and "
 "spelling his): "
 "q3-clearspace: \"The logo dimension based clear space is really for print, we have a rule "
 "of thumb for digital is half of this dimension, but it isn't a rule, maybe we have it set "
 "as a floor of 0.25 snap-up to the 4px grid, so at 24 height we have 8px as the floor fer "
 "the vertical clearspace, as long as it snaps to 4px above that I'm comfortable    \" · "
 "q4-hexagon-only: \"The pure logomark can also be used in responsive layouts when we get to "
 "smaller sizes, tablet-portrait and mobile \" · "
 "q5-guideline-shape: \"our decisions here over-ride the refresh\" · "
 "q6-unreferenced: \"The identifier versions are placeholders for customised logos they "
 "aren't needed here, for our purposes. However in the future we will re-integrate this "
 "material as an AI readable version of create, we might have something like 'Ask create' "
 "assistant bot\". "
 "The same four notes are copied verbatim in notes/_lanes/282/DAVE-RULINGS-2026-09-17.md "
 "(last bullet). The export's own _note: \"question strings stripped; they are on the page. "
 "Choices and notes verbatim from the chat paste.\""
)

ruled = (
 "THE LOGO REVIEW IS LANDED ON HIS OWN EXPORT. Six things are ruled, and one is filed "
 "rather than enacted.\n\n"

 "1. MASTHEAD DEFAULT = FULL COLOUR ON BOTH GROUNDS, IN ALL FOUR THEMES. He answered (a) "
 "four times — Apollo Legacy, Apollo Mono, Apollo Console, Apollo Supercharge — and the "
 "sentence he picked each time is 'Full colour both grounds — masterbrand-light-colour on "
 "light, masterbrand-dark-colour on dark'. va25-015's masthead contract (the Masterbrand "
 "logo appears in ALL digital mastheads; clicking it always returns to the root of the "
 "CURRENT business line) STANDS UNCHANGED — it says a Masterbrand is there; this ruling "
 "names WHICH VARIANT. Mono is not the masthead lockup in any theme, including Apollo Mono "
 "and Apollo Console: a monochrome theme does not make a monochrome masthead. Inscribed as "
 "a new BLOCKING rule in the logo26- series in the merged guideline.\n\n"

 "2. DIGITAL CLEAR SPACE IS A FLOOR, NOT THE PRINT RULE. He picked (c) 'Leave it unruled "
 "and keep the pointer' AND THEN WROTE A RULE IN THE NOTE, so the note governs and the "
 "choice is the frame it is written against: the logo-dimension clear space (va25-014's 1× "
 "hexagon height on all sides) is the PRINT rule and stays exactly as it is, in "
 "visual-assets.md, untouched. For DIGITAL there is now a FLOOR: vertical clear space ≥ "
 "0.25 × logo height, SNAPPED UP to the 4px grid. Across the five s282-D3 steps that is "
 "24 → 8 · 28 → 8 · 32 → 8 · 36 → 12 · 40 → 12 px (0.25×24=6→8, 0.25×28=7→8, "
 "0.25×32=8→8, 0.25×36=9→12, 0.25×40=10→12). It is a FLOOR and not a value: anything at "
 "or above the floor that itself sits on the 4px grid is legal — his 'as long as it snaps "
 "to 4px above that I'm comfortable'. HIS NOTE SAYS VERTICAL. HORIZONTAL CLEAR SPACE IS NOT "
 "STATED AND IS NOT RULED HERE — the rule line says so in its own text, the report says so, "
 "and it is carried as an open item (W-282ll) rather than completed by symmetry. His 'rule "
 "of thumb for digital is half of this dimension' is recorded as the thumb it is, not "
 "inscribed as a second number: he ruled the floor, not the thumb. Inscribed as a new "
 "BLOCKING rule in the logo26- series.\n\n"

 "3. THE HEXAGON ALONE IS PERMITTED, ON FOUR NAMED USES PLUS RESPONSIVE. He picked (a): "
 "the hexagon may be used on the NAV-RAIL HEAD, the APP TILE and the FAVICON, each "
 "conditional on Create Direct approval AND 'HSBC' in view — va25-016's two conditions are "
 "not relaxed, they are carried through verbatim. His note adds a fourth licence, in his "
 "words: 'The pure logomark can also be used in responsive layouts when we get to smaller "
 "sizes, tablet-portrait and mobile'. So the hexagon alone is also legal in RESPONSIVE "
 "LAYOUTS at the smaller sizes — tablet-portrait and mobile — where the masterbrand does "
 "not fit. This is the answer to s230-D2's declared residue ('App-shell-nav-rail "
 "deliberately NOT rebound (56px rail head, no lockup fits)') — a lockup now fits, and it "
 "is the hexagon. Inscribed as a new ADVISORY rule in the logo26- series; ADVISORY because "
 "every use of it is gated on a human approval this repo cannot check.\n\n"

 "4. ONE LOGO GUIDELINE, AND APOLLO'S DECISIONS OVERRIDE THE REFRESH. He picked (a) 'Merge "
 "into one logo guideline', overruling the recommended pointer shape, and wrote 'our "
 "decisions here over-ride the refresh'. knowledge/guidelines/logos.md IS that one file: "
 "the 2025 sticker sheet it already was, plus the eight-variant set (s282-D4), plus the "
 "five-step height scale (s282-D3), plus the three rules above, plus the logo26-001..007 "
 "bullets MOVED OUT of brand-refresh-assets.md and the va25-015, va25-016, va25-017 bullets "
 "MOVED OUT of visual-assets.md — every one of them byte-for-byte, every {#id} surviving "
 "the move so the index and the 27 restsOn/obeys references to them do not break. THE "
 "PRECEDENCE IS HIS: where an Apollo decision and the brand refresh differ, the Apollo "
 "decision governs, and the merged file states that in its own front matter. Photography "
 "and Creative Hexagons STAY in brand-refresh-assets.md — only the logo section moved, and "
 "a one-line pointer is left where each moved section was. va25-014 (the print clear space "
 "and the 105×20px minimum) is NOT moved: it is the print rule, it was not named, and it "
 "stays in visual-assets.md. bra26-003's vintage boundary — the against-case the option "
 "sentence printed — is answered by labelling each moved block with its vintage inside the "
 "merged file, not by keeping two files.\n\n"

 "5. THE IDENTIFIER LOCKUPS ARE RETIRED. He picked (b) 'Retire the four identifier variants "
 "until a real identifier exists', overruling the recommended keep-all-eight. This is "
 "ALREADY ENACTED by s282-D4 on his 'scrap the identifier versions' the same morning; this "
 "ruling is the export agreeing with the chat, and nothing further is done to the files. "
 "HIS FORWARD NOTE IS FILED, NOT ENACTED: 'However in the future we will re-integrate this "
 "material as an AI readable version of create, we might have something like \\'Ask create\\' "
 "assistant bot' — that is a direction, not an instruction, and it becomes a carry "
 "(W-282ll) that closes only when he rules on it. No create.hsbc material is ingested, no "
 "assistant is built, no rule is written from it.\n\n"

 "6. THE HEXAGON PAIR IS KEPT. He picked (a) 'Keep both files and both nodes' for the "
 "hexagon-dark-colour / hexagon-light-colour duplicate (one drawing exported twice, 619 "
 "bytes each, diff = 1 float literal). Both files stay, both nodes stay, no alias and no "
 "activeVariantOf edge is minted. The 3×2×2 symmetry the option sentence defends is the "
 "reason, and it is his.\n\n"

 "THE EIGHT LOGO NODES ARE BOUND. The four hexagon nodes' governedBy nulls — declared null "
 "since #277 with the reason 'NOTHING binds this lockup ... logos.md says the standard "
 "lives on create.hsbc — blocker B3, and it is not ours' — RESOLVE against the new "
 "hexagon-only rule, because the standard is now ours and it is in logos.md. The four "
 "masterbrand nodes gain governedBy to the masthead-default and clear-space rules. B3 is "
 "closed by this ruling, not by a measurement."
)

obj = {
 "id": "s282-D5",
 "date": "2026-09-18",
 "by": "Dave",
 "status": "ruled",
 "ruled": ruled,
 "says": says,
 "governs": [
   "knowledge/guidelines/logos.md",
   "knowledge/guidelines/brand-refresh-assets.md",
   "knowledge/guidelines/visual-assets.md",
   "knowledge/guidelines/_rules-index.json",
   "knowledge/_logo_nodes.json",
   "knowledge/assets/logos/hexagon-dark-colour.svg",
   "knowledge/assets/logos/hexagon-dark-mono.svg",
   "knowledge/assets/logos/hexagon-light-colour.svg",
   "knowledge/assets/logos/hexagon-light-mono.svg",
   "knowledge/assets/logos/masterbrand-dark-colour.svg",
   "knowledge/assets/logos/masterbrand-dark-mono.svg",
   "knowledge/assets/logos/masterbrand-light-colour.svg",
   "knowledge/assets/logos/masterbrand-light-mono.svg",
   "notes/_lanes/282/logo-review/DAVE-EXPORT-2026-09-18.json"
 ],
 "evidence": [
   "notes/_lanes/282/logo-review/DAVE-EXPORT-2026-09-18.json - his own export, 08:20:48.214Z, 12 rows, 9 answered, 4 notes, 3 overrules",
   "notes/_lanes/282/logo-review/LOGO-REVIEW-2026-09-17.html - the page he answered; the option sentences quoted in `says` are its own <label> text",
   "notes/_lanes/282/DAVE-RULINGS-2026-09-17.md - his four notes copied verbatim (last bullet)",
   "notes/_lanes/282/logo-review/bindings.json - the #282 lane LR measurement this ruling binds against",
   "notes/_subreports/2026-09-18-282-LL-logo-land.md - this lane's report",
   "notes/_lanes/282/logo-land/ - the lane's evidence dir (index diff, edge diff, merge receipt)"
 ]
}

body = json.dumps(obj, indent=2, ensure_ascii=False)
body = "\n".join((" " + ln) if ln else ln for ln in body.split("\n")).lstrip()
new = txt[: -len(TAIL)] + "\n ,\n " + body + TAIL
P.write_text(new, encoding="utf-8")
print("inserted bytes:", len(new) - len(txt))
