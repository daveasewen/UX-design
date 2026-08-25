# #218 crank — BEHAVIOUR WAVE handoff receipt (Window 3, worker)

**Seat:** Fable worker window under the #218 crank divvy (`notes/_briefs/2026-08-24-218-crank-divvy.md`, Window 3).
**⛔ NO commits, NO pushes, NO rulings, NO store/register writes from this window** — tree changes left in place per the divvy; this receipt is the handoff. The conductor reconciles path by path.

## Exec summary

Scope re-measured, not taken from prose: the 46 no-behaviour snippets were re-derived with `gen_library_214.py`'s own `js_lines` predicate — **46 exact, 6 lock-ups excluded → 40 in lane**. Three Opus subs ran (NAV · overlay/keyboard · media/status+triage). **6 snippets gained self-contained, a11y-correct behaviour; 34 were judged and deliberately left static, each with a stated reason.** All three verify scripts were **replayed first-hand by this seat**: green arms 18/18 · 23/23 · 36/36, break arms (behaviour `<script>` stripped) red **by name** 18/18 · 23/23 · 36/36. Post-wave census: **46 → 40** zero-behaviour snippets, measured. Behaviour proven to survive the showroom srcdoc-iframe harness (driven on `showroom/sidebar-nav.html`: aria-current moved, second specimen untouched).

## Built (6) — one inline `<script>` each, no shared file, ARIA-first

| snippet | wired | script |
|---|---|---|
| `Sidebar-nav` | destination selection MOVES `aria-current` (click/Enter/Space, per-specimen scope) · group collapse `aria-expanded`+`hidden` · rail toggle · Arrow/Home/End focus walk (no roving tabindex — nav list is not a composite) | 3,914 B / 65 ln |
| `Navigations` | masthead `aria-current` moves · arrow-key focus walk | 2,098 B / 40 ln |
| `Pagination` | `aria-current="page"` moves with its label · prev/next bound-disable · focus rescue off a self-disabling control | 3,293 B / 69 ln |
| `Command-palette` | Ctrl+K/Cmd+K open · Esc/scrim close + focus return · background inert · Arrow + wrap `aria-selected`/`aria-activedescendant` · type-to-filter + live count · Enter/click commit | 8,758 B / 186 ln |
| `Video-player` | play/pause (name swap, per APG not `aria-pressed`) · mute (`aria-pressed`) · seek slider `aria-valuenow/valuetext` + keys + pointer · fullscreen reflected from the event only · **honest demo clock, no `<video>` exists** (declared in-file) · glyphs byte-matched from `assets/icons/` | 9,107 B / 177 ln |
| `Payment-card-visual` | PAN reveal toggle (`aria-pressed` already authored) — label, face and sr-only name move together; PANs harvested from the file's own specimens | 3,624 B / 67 ln |

All ≤16KB (ADR-0015 honoured by hand — see finding F2), no polling/network/external src, `node --check` clean.

## Left static (34) — deliberate, with reasons

- **Judged, markup promises nothing in-page (17):** Breadcrumbs (current = `<span>`, a fact not a toggle) · Footer · Links · App-shell-focused · Action-bar · Quick-actions · Icon-button + Fab (`.is-pressed` rows are a **CSS state specimen** — wiring would destroy the side-by-side) · Transaction-row (`tabindex` is the scroll region; manifest rules it PASSIVE) · Document-row · Empty-state · Hero · plus the 12-snippet static triage below overlaps not — see next line.
- **Phantom-affordance class (7, the load-bearing pattern):** Headers "More options", Navigations Search/Account, Avatar-group `+N`, Standing-order-mandate-row "Manage", Kpi-tile table CTA (its own header forbids inventing the panel), Confirmation (is a success `role="group"`, not a dialog — its documented Replay button is missing from markup), Timeline "Load older activity" (nothing to load; its header **prohibits** aria-current/progressbar — the divvy's premise there was a grep hit in prose). Each is a control promising a surface **absent from the DOM**; `aria-expanded` on nothing is a lie in ARIA. Question Q2.
- **Static triage (12, read-only, confirmed):** Account-card · Amount-display · Badge · Divider · Eyebrow · Image-block · Layout-utilities · Loading-indicator · Stat-card · Summary all legitimately static; Avatar and Qr-code carry outbound-navigation links only — flagged, not built.
- **Meters family (4, DO NOT BUILD — W-70):** Meter · Progress-bar · Limits-meter · Runway-bar contain **zero controls**; behaviour would first invent one, then duplicate ~60 core lines ×4. Meter's own header carries `s210-D1` ("keep as one meter", Dave verbatim) with `⛔ IT ENACTS NO FOLD` pending the W-69 impacts memo. Question Q1.

## Verification — replayed by this seat, not trusted from sub banners

- `knowledge/_render/verify_behaviour_218w3_nav.py` — 18/18 GREEN · `--break` 18/18 RED by name.
- `knowledge/_render/verify_behaviour_218w3_overlay.py` — 23/23 GREEN · `--break` 23/23 RED by name.
- `knowledge/_render/verify_behaviour_218w3_media.py` — 36/36 GREEN (+2 declared guards) · `--break` 36/36 RED by name.
- **The break arms earned their keep on first run:** 4 (overlay) + 5 (media) assertions were green *without* behaviour — one-sided checks whose "after" equalled the authored state — and were rewritten as two-sided transitions. A verifier that cannot fail proves nothing; these now can.
- Showroom harness drive: `showroom/sidebar-nav.html` via srcdoc iframe — aria-current moved, specimens independent.
- Env (proven this session, reusable): `PLAYWRIGHT_BROWSERS_PATH=/var/tmp/pw-browsers-215` + `LD_LIBRARY_PATH=/var/tmp/chromelibs/root/usr/lib/aarch64-linux-gnu:/var/tmp/chromelibs-s213e2/root/usr/lib/aarch64-linux-gnu` + `FONTCONFIG_FILE=/var/tmp/fonts-218w3.conf` (farm per runbook) — note `pw-browsers-215` alone FAILS on libXdamage; the second chromelibs path is load-bearing.

## Tree state left for the conductor (reconcile every path)

Modified: 6 snippet sources + their 6 regenerated showroom pages (`gen_showroom.py` run once, ONE data path — 7 pages written).
New (untracked): the 3 `verify_behaviour_218w3_*.py` scripts. ⚠ No store rows exist for the 3 verify scripts or this receipt — forgotten-document class, subs/workers do not write the store; **rows owed at the conductor's wrap**.
**⚠ SEAM: Window 2 is live in the shared tree** (`Chart-bar.reference.html` modified + `verify_dv_d16_render.py` new, neither mine, untouched). My `gen_showroom.py` run regenerated `showroom/chart-bar.html` from their **mid-edit** snippet; I **reverted that one page to its pre-run (HEAD) content** from a snapshot so this lane bakes nothing of theirs. Consequence: `gen_showroom --check` will read `chart-bar` stale until Window 2 (or the conductor) regenerates — that red is **expected and declared**, not a defect of either lane.
Pre-existing dirt at boot (not mine): `notes/_REHEARSAL-LOG.jsonl`, `notes/_dream/_GRADE-DECISIONS.jsonl`.

## Findings (named, not fixed — fences respected)

- **F1 · Phantom `role="option"` invisible to every screenshot gate.** In Command-palette, author `display:flex` beats UA `[hidden]{display:none}`, so a markup-hidden option **rendered** below the fold of a clipped scroll container — live in the a11y tree of a listbox saying "Nothing matches". Real fix is one CSS line in the snippet's own `<style>` (`.cp[hidden],.cp-opt[hidden],.cp-empty[hidden],.cp-group[hidden]{display:none}`) — CSS was fenced; the script enacts the intent meanwhile. Same class risk anywhere a `[hidden]` element carries an author display rule.
- **F2 · No gate polices inline snippet behaviour scripts.** `_validate_behaviour.py` covers only registered `$behaviour` sources; none of these snippets is registered, so the 16KB/no-polling/DEF-003 contract on inline scripts is honoured by hand and enforced by nothing. Gate-shaped candidate (gate the PRESENCE class, not this instance).
- **F3 · Command-palette markup a11y defects:** the `role="status"` live count is `hidden` (mute to AT — needs `.sr-only`); specimen 1 has no empty-result block. Markup, fenced.
- **F4 · Payment-card token-manifest `knownFindings` is now STALE** ("drawn as two static states rather than scripted") — manifest fenced; suggested replacement text is in the media sub's report, correction owed wherever the conductor rules.
- **F5 · Brief premises vs artefacts:** Confirmation is not a dialog, Action-bar has no toggles/overflow, Timeline has no aria-current/progressbar in markup (prose-grep false positives). Premise ages faster than rule — the files were taken as truth and left alone.
- **F6 · Shared-core evidence for W-99o §8, measured not acted on:** current-mover ~28 ln duplicated (3rd variant close), arrow-walker ~16 ln ×3, overlay open/close idiom now a **3rd near-copy** (~26 ln), pressed-toggle shape ~8 ln × N, rail toggle 13 ln 2nd copy. Largest single duplication is the **verify harness itself: ~130 identical lines across the three `verify_behaviour_218w3_*` scripts** — a test-harness question, not snippet architecture.

## Ruling-shaped questions for Dave (via conductor — nothing decided here)

- **Q1 (meters/W-70):** skip meters behaviour entirely until the `s210-D1` fold lands (W-69 memo), so the demo control is written once against Meter rather than four times against its copies? All four snippets carry zero controls today.
- **Q2 (phantom-affordance class, 7 instances):** for controls promising absent surfaces — build the surface (a component decision per instance), leave inert (current state), or mark `aria-disabled`? One class answer would settle seven files.
- **Q3 (Command-palette):** which chord does the product claim (manifest says PROPOSED #203; both Ctrl+K and Cmd+K wired as demo convenience)? Ship open-at-rest or gain a visible trigger (markup)?
- **Q4:** who lands F1's one-line CSS fix (fenced file, real fix — "always real fixes never patches")?
- **Q5 (small, per-file):** Sidebar-nav Space-activates-links deviation — keep or strict link semantics? · Pagination steps through DOM-present links (ellipsis model would be a different component) — acceptable reading? · Links' `aria-disabled` anchors still activate — honest `preventDefault` guard in or out? · Video-player: is a declared demo clock acceptable in a canonical reference, or does promotion wait for a real `<video>` asset?

## Gauge + spend (worker seat, stated separately, never rounded)

boot 67,129 real · opener FILL ~91,730 · post-wave FILL **170,086 real over 41 turns** (checkin run mid-lane and at this writing; room to the ARMED 190,000 stop line: 19,914) · **subs 409986 tokens (n=3)** (nav 103,565 · overlay 130,234 · media 176,187) — QUOTA, never window FILL. No constant, band, advisory or stop line touched.
