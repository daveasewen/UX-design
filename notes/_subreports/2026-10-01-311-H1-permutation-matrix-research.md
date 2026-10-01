# Lane H1 (#311 overnight wave 1, Fable research lane) - the permutation matrix researched: morphological analysis and option matrices as decision instruments, for lane H3's proposal page

COUNTS: sources 21 (all named and dated in the findings §9; 13 fetched 2026-09-30, 8 bibliographic) · repo inputs 5 · axes found on the CEO brief 7 (3 closed by the brief, 2 open, 1 slice, 1 dependent) · matrix 3 × 2 with 1 cell struck · rulings touched 0 · files written 2

Findings: `notes/_lanes/312/H/H1/FINDINGS.md` (about 5,600 words, nine sections). Headline: a matrix is a map, not a sample — two named axes found from a fixed vocabulary by asking of each "does the brief settle this?", three values at most, six cells working size, one struck by cross-consistency and shown struck, one recommended with a sentence quoted from the brief, one foil that is Assembly's own default. Picks are their own record (proposed fields in §6) and never go in `_rulings.json`, whose every field is his; promotion is by accumulation with sentences onto a review page, by his word, through `_inscribe_ruling.py`. The #291 test says the instrument's honest limit: a matrix compresses the choice of kind (rounds one and two), not the tuning of the chosen one (rounds three to six).

## What was done

1. Read the receipt (his 10:35–10:46 words), the #280 layout-matrix report (the precedent), the CEO international-banking brief (the standing test brief), the #291 rulings file (the six rounds), and the shape of one `_rulings.json` row (s311-D2) to check the receipt's "unverified" claim about where a pick could live.
2. Researched the lineage with WebSearch/WebFetch: Zwicky, Ritchey's cross-consistency assessment, Heller et al.'s "dilemma" (DESIGN 2014), Pugh, Sobek/Ward/Liker set-based design, orthogonal arrays, TRIZ, conjoint, Bradley–Terry and Christiano et al.; the HCI record of rendered alternatives: Design Galleries 1997, Tohidi et al. 2006, Dow et al. 2010, Scout 2020, Luminate 2024; the choice-overload meta-analyses (Scheibehenne 2010, Chernev 2015); current tooling (Midjourney's four-up, v0's three, Stable Diffusion's X/Y/Z plot, Figma variants).
3. Wrote the axis-finder procedure (§3), the help/noise boundary (§4), the matrix spec (§5), the pick record and the promotion path Explore → Assembly (§6), the worked example on the CEO brief (§7) and eight recommendations to H3 (§8).

## Gates run

None apply: no file under `knowledge/`, no snippet, no canon, no meta was touched. `test_gates` was not run for two Markdown files under `notes/`; the commit script's own gates ran at commit (verdict in the commit line below).

## Found, not fixed

- The receipt's "unverified" is now verified from the store's shape: `_rulings.json` rows are id/ruled/date/by/says/governs/evidence/status, every field his, so picks cannot live there. The pick file's home (`notes/_matrices/` or `knowledge/_picks.jsonl`) is a question for the proposal page, not a lane's call.
- The Sloan article (Sobek/Ward/Liker 1999) is paywalled; its three principles are quoted from standard summaries, marked as such in §1.
- Whether the #246/#258 cold runs actually landed on the "tile wall × counts first" foil is checkable in `reviews/COLDRUN-258-*.html`; not checked tonight, marked as such in §7.3.
- The axis vocabulary (§3, eight to ten named axes with three or four values) is proposed from Scout's list plus the repo's own history; it exists nowhere as a file yet. H3 should draw it as a table for him; a lane should not mint it.
- The seat-wide commit lock `/tmp/apollo-commit.lock` was taken at 22:10:52 UTC by a lane that never committed (HEAD stayed at d1901fa2 the whole time); this lane waited from 22:17 to 22:42 UTC, and at age 1,898 s (past the addendum's 30 minutes) removed it as stale and took it for its own commit. Whichever lane held it should check its own commit landed.

## Ruling-shaped questions

1. Whether the matrix is "as standard" for any brief with two open structure/emphasis axes, or only on request. (The research says the former, with §4's noise cases excluded.)
2. Where the pick record lives, and whether a click-only pick is recorded at all.
3. The promotion threshold: three sentences on the same value of the same axis is this lane's proposal.
4. Whether a struck cell is shown struck (this lane says yes: the strike is evidence the axes were real).

## Second pass (Wed 2026-09-30 22:17–22:30 UTC, second H1 seat)
The first H1 seat wrote the findings, this report and the `W-311h1` row at 21:25–21:26 UTC and reached the seat-wide lock without committing. The second seat re-read the chain addendum and the brief, spot-checked two sources (Luminate confirmed at arxiv.org/abs/2310.12953 on 2026-09-30: title, five authors, CHI '24, "structured generation of design space"; the Stanford PDF of Dow et al. 2010 returned 404 tonight, so its numbers stand on the first seat's fetch, and a secondary page only confirmed the direction of the result), found nothing to change in the findings, and did the commit.

## Commit
Own paths only, under `/tmp/apollo-commit.lock`: `notes/_lanes/312/H/H1/FINDINGS.md`, this report, the born-closed row `W-311h1` in `knowledge/_state.json` (plus whatever the commit script regenerates). No push. Sha: see the chain read-back (`git log -1 -- notes/_lanes/312/H/H1/FINDINGS.md`).
