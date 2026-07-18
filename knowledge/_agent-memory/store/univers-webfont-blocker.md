---
name: univers-webfont-blocker
description: OPEN BLOCKER — no Latin Univers WEBFONT licence; desktop != webfont. Gates all shareable material. Includes the lesson from me wrongly striking it.
metadata: 
  node_type: memory
  type: project
  originSessionId: 0ca1a754-0be4-4e9b-a84b-a28410f8f19e
---

**We hold NO Latin Univers webfont pack.** Five *script* webfont packs are in the repo (Arabic, Japanese
Tazugane, Chinese M Ying Hei ×2, Armenian Helvetica — ten `.woff`/`.woff2` each). **Zero Latin.**

**Desktop ≠ webfont — different licence classes.** The Latin *desktop* set (TTF + OTF, six weights +
italics) IS present at `knowledge/assets/fonts/_desktop/`, dated 2024-03-25. Desktop covers design work
on a machine. **Webfont covers embedding and serving.** They are not interchangeable.

**Why it blocks real work — Dave, 2026-07-18:** *"we really need the webfonts, this will hinder sharing
material."* Without it: no shareable specimen sheets, no real-face review docs sent outside, no hosted
prototype in brand type.

**ACTION (Dave's):** request the **Latin "Univers Next for HSBC" webfont pack (WOFF + WOFF2)** from
brand — the same deliverable already held for the five script companions.

**Monotype terms**, now on file at `knowledge/assets/WebfontUserGuide-2024.pdf`:
- Web fonts licensed for **self-hosting**; WOFF/WOFF2; **base64 serving explicitly sanctioned** (so the
  embedding technique is fine *once licensed*).
- Fonts must **not** be distributed via a **public** Git repository.
- Remediation if already committed: `git rm`, then **BFG Repo Cleaner** for history.

**Known exposure (low, not zero):** four tracked files — `TYPE-SPECIMEN-2026-07-17` and
`TYPE-COMPOSITES-2026-07-17`, plain + REVIEW — each embed six base64 woff2 payloads (~264KB) of
`Univers Next HSBC`, entered at commit `24accd0`, pushed. **Repo is PRIVATE** (GitHub API 404
unauthenticated) and Monotype's prohibition names *public* repos — but any collaborator without their own
licence still receives the font. Dave's call: leave / `git rm --cached` / BFG purge.
**Interim control:** `reviews/*CONTACT*.html` gitignored; share outside as PDF only.

**Gated 2026-07-18:** this claim is now `ASSERT-001` in `knowledge/_assertions.json`, re-tested on every
build with a 30-day recheck window. When the webfont pack lands, the build FAILS and names every document
that still says otherwise. See [[assertion-registry]].

## ⚠️ THE LESSON — I struck this blocker as false, and Dave caught it

I found the Latin *desktop* set, matched "font" against the word "font" in the blocker, and declared it
false — without reading which **licence class** the blocker named. It named the webfont. It was right.

**A blocker that has stopped work for weeks is exactly the claim you WANT to be false — which is why
disproving one deserves MORE scrutiny than confirming it, not less.** Blockers should carry a re-test
date *and* the precise artefact that would clear them.

This is the [[memento-framing]] failure mode inverted: not a false claim believed too long, but a *true*
claim discarded too eagerly. Both end with the record wrong. Full correction + superseded text:
`knowledge/_proforma/_TYPE-DECISIONS.md` § Blockers 1. Related: [[sandbox-html-rendering]],
[[univers-measured-facts]].
