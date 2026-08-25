# #218 build brief — quality wave, lane 1: the forms family (wave-3's real successor)

Wave-3's existence premise was discharged by measurement (all 17 gated); its successor, per the
conductor's adopted recommendation, is a QUALITY pass — lane β's method proved the model by
finding four live defects in five gated files just by driving them hard.

**Subjects: the 8 forms-family components** (form layout+validation · date-picker · date-range ·
time-picker · number/currency · file-upload · OTP · textarea — resolve exact filenames from the
store, don't trust this list's spelling).

**Method (β's, now the pattern):** DRIVE every interactive promise in the file — real clicks,
keys, focus order, dismissal, error/validation flows, in Chromium via the established render env —
and fix what fails AT CAUSE in the snippet. Specifically sweep for the known classes:
1. **`{once:true}` guarded-listener class** (β's R1) — REPO-WIDE grep first (all 135 snippets,
   not just forms): a one-shot listener with a `propertyName`/condition guard counts deliveries,
   not matches. Fix instances; propose (don't build) the static gate shape in your report.
2. **Focus stranding** on dismiss/disable (WCAG 2.4.3) — the class β fixed twice.
3. **`[hidden]` vs author-display** (W3's F1 class).
4. **aria-live/announce coverage** on validation errors — flag, fix only where the file's own
   documented pattern supports it (the Toast lesson: contradicting documented canon is Dave's).
5. **file-upload `aria-invalid` 0 vs siblings 2–7** (α's question) — answer by DRIVING its
   error states; if it's a real gap, fix in the file's own idiom; if correct-for-a-dropzone,
   say why with the measurement.
6. **γ's two TYPE-002 component-scope fixes** ride along (Data-grid `.dgseg button[aria-pressed]`
   and Empty-state `.empty a`, font-weight:500 → the right composite) — small, ruled-adjacent
   (type composites are FIRM), the ratchet must shrink or hold.

**Proof:** per-component drive log (what was driven, what failed, what changed); one verify
script `verify_quality_forms_218.py`, green + break arm red by name, two-sided transitions only
(both prior waves shipped one-siders on first cut — don't be the third); affected gates re-run
(snippet · a11y · behaviour · type ratchet); showroom pages for changed snippets are the
CONDUCTOR's serial — do not run gen_showroom.

**Discipline:** file your FULL report at `notes/_subreports/2026-08-25-218-cB-quality-forms.md`
(the s218-D7 shape — header with token spend, COUNTS line, RULING-SHAPED QUESTIONS, REPLAY-THESE;
evidence beside it under `notes/_subreports/assets/`), return ONLY the stub to chat. Fence: no
rulings, no tokens/canon (needs → `_DS-IMPROVEMENTS.md` row proposals in the report), no
registry/serial, no store/lane/GM/LS/memory edits, no commit/push. /var/tmp -s218qf.
