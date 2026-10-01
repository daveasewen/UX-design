# #311 overnight wave 1 · lane F1 (Fable) · the top-nav shell as an IA question (W-305e2)

COUNTS: 4 options drawn (1 flat row · 2 top nav + mega menu, open and flyout · 3 stacked with section tier · foil side nav) + 1 phone collapse + 1 hand-over map = 7 pictures · 1 recommendation (option 2) · 1 when-rule drafted · 4 calls for the page · 0 files in knowledge/ touched · rendered from d1901fa2 · commit OWED (lock contended all night; paths on disk, command in outputs/311/F1/commit_bg.sh)

Headline: the count stops choosing the frame. Recommendation is option 2 — the top nav is the default for any app whatever the count of destinations or levels; a destination opens a flyout up to six links and the mega menu over six or when grouped (the s272-D70 ceiling becomes the line); the current page's peer views are tabs in the page-header lock-up; the side nav survives for the workbench case only, chosen by the job, never by a count. Page for Dave (read-only, verified at 1440 and 390, 7 images, no side scroll): `notes/_lanes/312/F/F1-topnav-ia.html`. Lane F5 folds its four calls into the one page.

## What was built
- `notes/_lanes/312/F/render_F1.py` — scratch wireframes over `git show d1901fa2` copies of `dashboards/international-banking-dashboard.canon.html`, canon.css and type.css written to /dev/shm (the tree's canon.css is dirty tonight — A1's — and was not read). The demo's own masthead is hidden and a wireframe masthead injected; page header and bento stay real. Nothing in the tree is edited.
- `notes/_lanes/312/F/img/F1-opt1.png` flat row + tab strip · `F1-opt2a.png` mega menu open on Payments · `F1-opt2b.png` FX open as a three-link flyout · `F1-opt3.png` stacked, section tier · `F1-opt4.png` the side-nav foil · `F1-phone.png` the sheet as accordion at 390 · `F1-handover-map.png` the five-step order · `F1-facts.json`.
- The test IA: nine primaries (Overview, Accounts, Payments, Receivables, Liquidity, Trade, FX, Reports, Admin), three levels, Payments with ten leaves in three groups.
- The rule as drafted (gate, then prose), in the when-fields vocabulary: `primaryNavigation = present AND platform = app — …` (full text on the page). Yields to focused, multi-column, split, doormat unchanged; side nav and rail by the workbench test.

## Measured (F1-facts.json, wireframe type Helvetica 14px / 12px padding — narrower than the canon nav link, so these read low)
- Nine primaries in one row need 812px; the row still has 812px at 1120 and 730 at 1024 (overflow begins between the two).
- Chrome before the page title: options 1 and 2, 65px; option 3, 170px; foil, 64px plus a 248px column.

## Gates run
None of the gates read this lane's paths (notes/ only, no canon, snippet, meta or receipt change). `test_gates` was not run for the same reason; lane paths are pictures, one HTML page, one script, this report and one store row.

## Found, not fixed
1. `knowledge/when-fields.json` has no name for "links under one destination", so the flyout/mega clause is prose inside the gate. A `children` (count) field by the s273-D4 addition route would let the resolver parse it. Not added tonight (registry file, not this lane's).
2. If the rule is taken, `knowledge/roles.json` page-frame `app-shell-side-nav` when ("> 7 destinations or two nav levels") and `app-shell-top-nav` when ("default for dashboards") both change; `app-shell-side-nav.meta.json` and `app-shell-nav-rail.meta.json` carry no `when` at all at d1901fa2 (`python3` read of the metas), so the hand-over is only authored on the top-nav side today.
3. `Navigations.reference.html` has no flyout or mega-menu markup at all — the masthead's main-nav flyout exists in Figma (41407:55820, per the meta) and not in the snippet; s272-D70 ratified a ceiling for a thing the library does not yet draw. The mega menu is a build owed if Dave takes option 2.
4. Option 3's section tier is the top-nav meta's `sectionTier` prop; the meta's `$decision-1` (inline or stacked as default) is answered by this recommendation as inline, stacked only when the primaries do not fit the row.
5. Process: one `git status --short` was run at this lane's first call, before the brief's ban was read. Reported, not repeated.
6. The commit lock `/tmp/apollo-commit.lock` was held from 22:42 UTC through this lane's whole run; see the commit note below for what was done at the 30-minute line.

## Ruling-shaped questions
- Call 1: the top nav as the default frame for an app, whatever the count, mega menu for multiple levels — yes as drawn, or change.
- Call 2: six links in one column as the flyout/mega line (s272-D70), grouped always mega — yes, or change.
- Call 3: level 3 as tabs in the lock-up, or the section tier.
- Call 4: the side-nav shell kept for the workbench only, by a job test — yes, retire, or change.

## Store
Born-closed row `W-311f1` (s305-D40 form) added via `_state.add()` inside the lock, `json.dumps(indent=2, ensure_ascii=False)+'\n'`. It reached the tree in lane E0's commit 3756e3ec (that commit swept the shared `_state.json` and lane H1's staged files up with its own), so this lane's commit carries notes/ paths only.

## Commit and the lock, as it happened
The seat-wide lock was contended all night: held 23:12→23:48 UTC by a lane that released and re-took it between calls, then 23:48→00:20 unchanged. At 31 minutes this lane called it stale per the addendum, removed it and took it (00:20:04); the first commit run stopped on a stale `_CHAIN.md` (regenerated with `_gen_chain.py`), the second on the showroom gate (`links.html` stale against lane A1's uncommitted canon — passed with a declared `SHOWROOM_ACK`), the third on the Memento schematic (re-run with it appended), and that run was cut off by the device call limit, which also cut off every later foreground run of the script. The lock this lane took was then removed and re-taken by another lane (mtime 00:54:39), and lane E0 committed through it at 3756e3ec. A detached watcher (`outputs/311/F1/commit_bg.sh`) did not survive the call boundary either. At 01:41 UTC the lock had been held by another lane since 01:26:53 and this lane handed back with THE COMMIT OWED: every path is on disk in the mount, and the exact command is in `outputs/311/F1/commit_bg.sh` (notes/ paths plus the Memento schematic, `SHOWROOM_ACK` declared for A1's dirty canon). Found, not fixed: a commit run of about three minutes does not fit inside a device call tonight, and three lanes' lock discipline collided.
