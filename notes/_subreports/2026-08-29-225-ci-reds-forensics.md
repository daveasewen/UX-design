# `#225`-`ci-reds` — the three CI red classes drilled locally: render sweep, release job, chain ratio

session: `#225` · 2026-08-29
window: forensics sub (Opus), dispatched by the #225 conductor
sub index: `ci-reds`
brief: in-chat (no brief file) — READ-ONLY on the repo; writes limited to this file + `_to_delete/` scratch
tokens: `UNMEASURED — this sub has no `message.usage` reader in its own loop`
repo state at measurement: `git rev-parse HEAD` = `f971c4e` ("#225: ledger cut — apollo-spider row seeded at the bake, version v1.0.3")

## VERDICT

Three classes drilled. **Class 2 (release) and class 3 (ratio) are DONE and MEASURED. Class 1
(render) is PARTIAL, with a named binding obstacle.**

- **RENDER — the failing item is still UNREAD, and it is not reproducible on this box.** The
  sweep's inputs (`knowledge/snippets/`, `knowledge/canon/`, `knowledge/tokens/`,
  `_validate_state_contrast.py`) are **byte-identical between `f4fec54` (run #457) and HEAD** —
  `git diff --stat` prints nothing. Driven locally against that identical tree: **all 135
  snippets pass individually (rc=0, 135/135)**, one 44-snippet single-process aggregate passes
  (rc=0), and the BLOCKING selftest step passes in **2.5 s / 62 arms**. Two hypotheses that would
  have explained a CI-only red are **killed by measurement** (browser-version drift; missing
  untracked assets). What survives is a residual I could not drive: a whole-artefact (135-snippet)
  invariant that only bites at full size (exit **2**, `StateContrastReportError`), or a
  runner-layout difference. Binding obstacle: **the failing item's name lives only in the CI
  log, and this sandbox has no `gh` and the GitHub API 404s unauthenticated on a private repo**.
- **RELEASE — the red is SPLIT, and one half is fully explained and already healed.** At
  `1e028a1` (today's opener push, runs #458/#459) **two BLOCKING steps are genuinely red**, both
  reproduced in a faithful tree replica: the ship-list audit (`--check`, rc=1, sha mismatch) and
  the baked-pack audit (`--pack`, rc=1, "the manifest names a release nobody baked"). **Both are
  GREEN at HEAD** — measured — so **that red heals at the next push**. But at `f4fec54` (run
  #457, the 15–19 s failures) **all eight release steps reproduce GREEN in a faithful replica of
  that exact tree**, so the #454/#456/#457 release red is **not a content defect at that commit**
  and its step remains UNPROVEN for the same log-access reason.
- **RATIO — measured end to end, with the computing line quoted and the retirement arithmetic
  done.** `45,506 / 86,879 = 52.4%`, floor `<40%`, one failing bite. **The carry list is ONE LINE
  of `GOOD-MORNING.md` (line 31) and it measures 24,873 tk — 89.3% of the ★ LATEST banner and
  54.7% of the whole chain file.** Because that line sits in **both** numerator and denominator,
  the cut needed is **17,925 tk, not the 10,755 tk the gap suggests** — equivalently, the ★ LATEST
  banner must fall **below ~9,925 tk** (it is 27,847 tk today). `GOOD-MORNING.md`'s own estimate
  of "under ~11K tk" was close and is now replaced by a measurement.

COUNTS: findings `15` · ruling-shaped `3` · UNPROVEN `3`

---

## ENVIRONMENT AND THE LIMIT I DID NOT FIGHT

- ⛔ **NO CI LOG REACH, DECLARED AT THE TOP.** No `gh` CLI in this sandbox; the GitHub REST API
  404s unauthenticated against this private repo (recorded in `GOOD-MORNING.md`, banner: *"A wrap
  sub has no CI reach — `gh` is absent and the API 404s unauthenticated"*). Every claim below is
  from **local re-driving**, never from a log. Where the log is the only witness, the finding is
  filed as UNPROVEN rather than guessed.
- ⛔ **NOTHING SURVIVES A TOOL-CALL BOUNDARY — RE-CONFIRMED FIRST-HAND, n=1 today.** A `nohup`'d
  sweep launched in one call was gone in the next: `pgrep -af validate_state_contrast` matched
  only the grep, `pgrep -c headless_shell` = 0, and the redirect log was 0 bytes. The bash
  wrapper runs under `bwrap --unshare-pid --die-with-parent`. **Long work must be chunked, and
  the harness call cap measured today is 175 s** (a 168 s `timeout` inside it is the safe budget).
- Browser recipe that worked, first-hand (`_RUNBOOK-render-verify.md`'s fifth stratum, one
  directory over): `/var/tmp/chromelibs-s213e2` **no longer exists** on this box —
  `/var/tmp/chromelibs-220` does and carries `libXdamage.so.1`. Verified by `ldd`, not by a launch
  attempt: exactly **1 missing lib** before, **0** after.
  ```
  export PYTHONPATH=/var/tmp/pylibs:$PYTHONPATH
  export PLAYWRIGHT_BROWSERS_PATH=/var/tmp/pw-browsers-220
  export LD_LIBRARY_PATH=/var/tmp/chromelibs-220/root/usr/lib/aarch64-linux-gnu
  export TMPDIR=/sessions/<session>/tmp225      # ⛔ NOT /var/tmp — root fs is 100% full, 60M free
  ```
- ⚠ **A CONCURRENT LANE IS LIVE IN THIS TREE AND I DID NOT TOUCH IT.** `git status` throughout
  showed ` M knowledge/_release/_gate_pack_docs.py` and `?? notes/_subreports/2026-08-29-225-gumdrop-gate-widening.md`
  — the Gumdrop gate-widening sub. Neither is mine; both are untouched.
- ✅ **THE ONE REPO FILE I HAD TO WRITE WAS RESTORED BYTE-FOR-BYTE.** `_validate_state_contrast.py`
  writes `knowledge/_STATE-CONTRAST-AUDIT.md` unconditionally (`_validate_state_contrast.py:1385`),
  and that file is **tracked**. I copied it to `_to_delete/s225-forensics/AUDIT-PRISTINE.md` before
  the first run and restored it after: md5 `ad916804a69d3151b5e3d8ded8879df0` before **and** after,
  `git status --porcelain knowledge/_STATE-CONTRAST-AUDIT.md` empty at the close. Every other
  sweep run used a scratch **replica** of `knowledge/` (rsync minus `assets/`, `assets` symlinked)
  so the repo's own audit was written exactly once and put back.
- ⚠ **BRIEF vs TEMPLATE, DECLARED.** `_TEMPLATE.md` requires evidence beside the report at
  `notes/_subreports/assets/<report-stem>/`. **The brief's fence forbids that write**, so evidence
  is at `_to_delete/s225-forensics/evidence/` (gitignored, 21 files incl. `ALL-135-snippet-rc.txt`)
  and every load-bearing figure is **quoted inline below** so nothing depends on scratch surviving.

---

## CLASS 1 — RENDER: the `s218-D4` state-contrast sweep

### What the job actually runs

`.github/workflows/gates.yml:346` opens the `render` job. Its two BLOCKING gate steps:

- `.github/workflows/gates.yml:386-387`
  ```yaml
  - name: State-contrast selftest — every arm, mutation controls included (BLOCKING)
    run: python3 knowledge/_validate_state_contrast.py --selftest
  ```
- `.github/workflows/gates.yml:389-390`
  ```yaml
  - name: Full state-contrast sweep — BLOCKING (s218-D4; 0 text failures over 135)
    run: python3 knowledge/_validate_state_contrast.py
  ```

The probe-registry step below them is `continue-on-error: true` (`gates.yml:427`), and the job's
own header already records that this was **measured** at #209: *"the Actions API reports job
`render` conclusion=**success**"* with that step exiting 1. So the red is one of the two BLOCKING
steps above.

### F1 — the selftest step is NOT the long pole and it is green

```
$ python3 <replica>/knowledge/_validate_state_contrast.py --selftest
RC=0     real 0m2.552s
selftest OK — 62 arms. …
```

2.5 s, 62 arms, rc=0. The render job's 13 m is therefore **install + sweep**, and the sweep is the
only step big enough to hold it. The brief's premise stands.

### F2 — the sweep's inputs are byte-identical between run #457's commit and HEAD

```
$ git diff --stat f4fec54 HEAD -- knowledge/snippets/ knowledge/canon/ knowledge/tokens/ knowledge/_validate_state_contrast.py
(no output)
```

⇒ whatever CI measured at `f4fec54`, I am measuring the **same bytes**. This is what makes the
next finding load-bearing instead of a version mismatch.

### F3 — all 135 snippets pass individually; the failing item is not a per-snippet failure

Every snippet driven as its own process against the real browser. Full table at
`_to_delete/s225-forensics/evidence/ALL-135-snippet-rc.txt` (135 lines, `rc elapsed name`).

```
$ cat percheck.txt w1.txt w2.txt w3.txt | wc -l
135
$ cat percheck.txt w*.txt | grep -v "^0 "
(none nonzero)
```

**135 / 135 rc=0.** Serial cost measured: `snippets=135  serial_total=873.6 s (14.6 min)`.
Slowest five: `App-shell-doormat 52,970 ms · App-shell-top-nav 33,367 ms · App-shell-split
25,969 ms · Button 18,349 ms · App-shell-nav-rail 15,828 ms`.

### F4 — a 44-snippet single-process aggregate also passes

The per-snippet runs each build their own report, so they cannot see a whole-artefact invariant.
One large aggregate was driven to narrow that:

```
BATCH3 RC=0
**0 text failure(s) across 44 snippet(s).**
**34 DECLARED HOLE(s) — un-hit-testable box(es), reported UNMEASURABLE by name (s129-D3).**
**0 CARRIER failure(s) …**
```

Two further aggregates (44 and 48 snippets) were **not** completed — `rc=124`, killed by the 168 s
`timeout`, because those slices carry the App-shell heavies (their measured individual times sum
to **207.9 s** on their own). Not a failure signal: a timeout, named.

### F5 — the exit-code map, so the conductor knows what the CI number can mean

`_validate_state_contrast.py:1397` and `:1409-1414`:

```python
    return 1 if (total or refused or carrier_fails) else 0
...
    except (StateContrastArgError, StateContrastReportError, StateContrastSelftestError,
            StateContrastCarrierError) as e:
        print(f"{type(e).__name__}: {e}", file=sys.stderr)
        sys.exit(2)
```

- **exit 1** = text failures **or** `StateContrastParseError` refusals **or** s151-D1 carrier
  failures. F3 rules out all three *per snippet*.
- **exit 2** = a report-level invariant tripped. The audit's own body states the invariant:
  *"The count above is RE-READ off this artefact and asserted equal to the number of ⬛ lines on
  every write — a hole that goes quiet is a failed write, not a clean run."* This can only bite at
  **full artefact size**, which is exactly the arm F3/F4 cannot reach.
- **exit 77** = browser unreachable (`COULD-NOT-ASK`), which the render job installs against.

### F6 — HYPOTHESIS KILLED: browser-version drift

CI runs unpinned `pip install playwright` (`gates.yml:380`). PyPI, read today:

```
latest playwright: 1.62.0
uploaded: 2026-07-31T17:00:44
```

Local: `playwright 1.62.0`, browsers `chromium-1234`, `Chromium 151.0.7922.34`. **The same version
is the newest one available**, so a CI install on 2026-08-29 gets the same chromium build as this
box. A "newer Chrome serializes colours differently" story does **not** hold.

### F7 — HYPOTHESIS KILLED: assets present locally, absent in CI

`knowledge/assets/` holds 1,298 files on disk but only **986 tracked** — so a snippet pointing at
an untracked asset would render differently in CI. It does not happen:

```
asset refs in snippets: 2      (both tracked — the untracked-check printed nothing)
url() in knowledge/canon/*.css: 0
```

### RENDER — verdict

**The failing item is UNREAD and I could not name it.** Honest classification of what remains:

1. a **whole-artefact invariant** (exit 2) that only bites at 135 snippets — F4 got to 44;
2. a **runner-layout difference** — fonts resolve by family name with no `@font-face` (F7), so
   `ubuntu-latest`'s fallback face differs from this sandbox's, wrapping differs, and hit-stack
   sample points can land on a different paint stack. This would make the red an **instrument
   sensitivity**, not a contrast defect — but I did not drive it and will not claim it.

⛔ **I cannot classify it as "real contrast defect" or "instrument artifact" without the item.**
What I *can* say with a measurement behind it: **it is not any single snippet's contrast**, on the
identical bytes CI ran.

**Price to close, both routes named:**
(a) **cheapest and permanent** — tee the sweep in CI so the item is never virtualized again:
`run: python3 knowledge/_validate_state_contrast.py 2>&1 | tee sweep.log` plus an
`actions/upload-artifact` of `knowledge/_STATE-CONTRAST-AUDIT.md`. One yaml edit; ⬛ workflow edits
were outside this sub's fence.
(b) **local** — one machine with a >15 min uninterrupted wall (the 873.6 s serial figure is
measured), running the sweep un-chunked in one process.

---

## CLASS 2 — RELEASE: the job that exits 1 in 15–19 s

### Method

Because the gates read the **working tree** (not only git blobs — `_gen_pack_manifest.py:293`
imports `knowledge/_render/gen_bento_roles_217.py` at generation time), a partial extract refuses.
So a **faithful full-tree replica** was built per commit: `git archive <sha> | tar -x -C <dir>`
(227 MB, ~9 s) with the real `.git` symlinked in. Nothing was written to the repo.

### F8 — at `f4fec54` (run #457) ALL EIGHT release steps are GREEN

| step (yaml name, abbreviated) | argv | rc at `f4fec54` |
|---|---|---|
| Frozen-release gate | `_gate_frozen_release.py --check --at f4fec54 --no-worktree` | **0** |
| Frozen-release selftest | `_gate_frozen_release.py --selftest` | **0** (14 bites, 0 fail) |
| Pack ship-list audit | `_gate_release_audit.py --check` | **0** |
| Release-audit selftest | `_gate_release_audit.py --selftest` | **0** (10 bites, 0 fail) |
| Baked-pack audit | `_gate_release_audit.py --pack` | **0** |
| Pack-side CI template | `_gate_ci_template.py --check` | **0** |
| CI-template selftest | `_gate_ci_template.py --selftest` | **0** (10 bites, 0 fail) |
| Build-script selftest | `bash apollo-spider/build-designer-pack.sh --selftest` | **0** |

Quoted from the replica:

```
PASS — the manifest at knowledge/_release/_pack_manifest.json is byte-identical to a fresh
generation at 14af4d76c2ea (1647 files, sha256 dfb9603b94065076)
PASS — apollo-spider/dist/Apollo-Spider-v1.0.2.zip matches the manifest at 14af4d76c2ea
PASS — 2 arm(s) asked, no frozen surface moved.
```

⚠ The frozen gate's **worktree arm** is not askable in a replica (the symlinked `.git` makes
`git status` compare against the real HEAD), so it was run `--no-worktree`; the two commit arms
are faithful. Declared, not waived.

⇒ **the #454/#456/#457 release red is not a content defect at that tree.** One hypothesis was
tested and killed on the way: `_gen_pack_manifest.py` **did** change between the manifest's own
commit `14af4d7` and `f4fec54` (at `e33ea1b`), which would have made the ship-list audit red — but
the replica proves it did not: byte-identical, rc=0.

### F9 — at `1e028a1` (today's opener push → runs #458/#459) TWO steps are genuinely RED

```
### audit_check
audit_check RC=1
❌ THE SHIP LIST ON DISK IS NOT WHAT THE GENERATOR PRODUCES at 333deee78844.
   on disk: 1648 files, sha256 bd463c34d22d63c0
   fresh:   1648 files, sha256 285cb4f035dbef5b
### audit_pack
audit_pack RC=1
❌ the manifest reads version 'v1.0.3' and NO zip in dist/ carries it (zips present:
   Apollo-Spider-v1.0.0.zip, Apollo-Spider-v1.0.1.zip, Apollo-Spider-v1.0.2.zip)
   — the manifest names a release nobody baked.
```

Both are correct behaviour, not gate bugs. The first is `1e028a1` adding `RATIFY_IDS["v1.0.3"] = "s224-D1"`
to the generator while the on-disk manifest still read `PROPOSED` — a one-commit window that
`a9e6f37` closed by regenerating. The second is the pre-bake window.

### F10 — the yaml's own comment understates when the `--pack` arm bites

`.github/workflows/gates.yml:475` names the step
*"Baked-pack audit — a zip in dist/ must match the manifest (BLOCKING; refuses while nothing is baked)"*
and maps only 77 to 0. But the **refusal** path (`_gate_release_audit.py:148-154`) fires only when
`dist/` is **empty**. With any zip present and the manifest naming an unbaked version, the arm
returns **1**, by design:

`knowledge/_release/_gate_release_audit.py:166-169`
```python
    if not current:
        print("❌ the manifest reads version %r and NO zip in dist/ carries it "
              "(zips present: %s) — the manifest names a release nobody baked."
              % (want, ", ".join(os.path.basename(z) for z in zips)))
        return 1
```

And the gate's own selftest asserts exactly that (`_gate_release_audit.py:280-282`):
`bite("pack/unbaked-version-is-red", _mut_rc == 1, …)`. ⇒ **every commit between a version bump
and its bake is structurally red on this step.** That is a design choice with a consequence, not a
defect — and it is the shape the conductor should price.

### F11 — the #458/#459 half HEALS at the next push, MEASURED at HEAD

All eight steps re-run against the working tree at HEAD (`f971c4e`, v1.0.3 baked at `3d7c115`):

```
frozen --check           rc=0   PASS — 3 arm(s) asked, no frozen surface moved.
frozen --selftest        rc=0   selftest: 14 bites, 0 fail(s)
audit --check            rc=0   PASS — byte-identical to a fresh generation at 1e028a1b5bf9
                                (1648 files, sha256 f1003d9e9a794db8)
audit --selftest         rc=0   selftest: 10 bites, 0 fail(s)
audit --pack             rc=0   PASS — Apollo-Spider-v1.0.3.zip matches the manifest at 1e028a1b5bf9
ci_template --check      rc=0   PASS — the template parses, ships what it calls, and hides nothing.
ci_template --selftest   rc=0   selftest: 10 bites, 0 fail(s)
build-designer-pack.sh --selftest  rc=0   216 bites, 0 fail(s)
```

### F12 — measured step costs, for reading the 15–19 s figure

```
0.30 s  _gate_frozen_release.py --check
0.43 s  _gate_frozen_release.py --selftest
7.71 s  _gate_release_audit.py --check
16.42 s _gate_release_audit.py --selftest
7.93 s  _gate_release_audit.py --pack
0.04 s  _gate_ci_template.py --check
0.10 s  _gate_ci_template.py --selftest
```

The gate steps alone cost **~33 s** on this box. A job that ends at **15–19 s total** — checkout at
`fetch-depth: 0` (1.1 GB of history, 234 MB / 4,671 tracked files), `setup-python`, and
`pip install pyyaml` all included — **cannot have reached the release-audit selftest**. That
narrows #454/#456/#457's failing step to the **setup half plus at most the first two or three
gates** — and F8 proves those gates are green on that tree. So the most likely remaining causes
are environmental (checkout, `setup-python`, or the `pip install`), and I am not going to name one
without the log.

### RELEASE — verdict

**SPLIT.** The `1e028a1` red (runs #458/#459) is **fully explained and already healed** at HEAD.
The `f4fec54` red (runs #454/#456/#457) is **not a content defect** — proved by replica — and its
step is **UNPROVEN**, blocked on log access.

---

## CLASS 3 — CHAIN-RATIO: the numbers, measured, with the computing line

⛔ `_gen_chain.py` was run **only** with `--check` and `--selftest`. `_CHAIN.md` was never written:
`git status --porcelain` after both runs showed no `_CHAIN.md` entry.

### F13 — the current reading, and what the ratio actually compares

```
$ python3 knowledge/_gen_chain.py --check           # rc=0
✅ _CHAIN.md is FRESH — byte-matches the live chain · GM header+LATEST 30597 tk ·
   LS LATEST delta only (of 41 delta lines) 2318 tk ·
   FILE 45,506 tiktoken cl100k_base = slice 32,915 + wrapper 12,591 · fixed point in 2 pass(es)

$ python3 knowledge/_gen_chain.py --selftest        # rc=1 — exactly ONE bite fails
    ✗ is materially smaller than GOOD-MORNING.md (45,506 vs 86,879 real, 52.4% of it,
      floor <40%; tier measured, not assumed: tiktoken cl100k_base)
    ✓ BOTH SIDES OF THE RATIO ARE ON ONE MEASURER — chain `tiktoken cl100k_base` vs
      GOOD-MORNING `tiktoken cl100k_base`, so the percentage above has a unit
  ✗ _gen_chain selftest: 1 bite(s) failed
```

⚠ The two other `✗` lines in the selftest output (`_CHAIN.md is STALE`, `_CHAIN.md is MISSING`) are
**mutant arms printing their expected output**; each is followed by its own `✓`. **One** bite fails.

**What the ratio compares** — numerator and denominator, in what unit:

- **numerator** `out_tk` = tokens of the **whole generated `_CHAIN.md` text, wrapper included** —
  not the slice. (`out_tk, out_tier = cg.measure_tokens(text)`, `_gen_chain.py:751`.)
- **denominator** `gm_tk` = tokens of the **whole `GOOD-MORNING.md` file**
  (`cg.measure_tokens(open(.../GOOD-MORNING.md).read())`, `_gen_chain.py:726-727`).
- **unit** = whatever tier `_capture_gate.measure_tokens` reaches; today **`tiktoken cl100k_base`
  on both sides**, and a dedicated bite asserts both sides share a measurer.

**The computing line, quoted:**

`knowledge/_gen_chain.py:752`
```python
        ratio = out_tk / gm_tk if gm_tk else float("inf")
```

**The assertion, quoted:**

`knowledge/_gen_chain.py:753-756`
```python
        bite(f"is materially smaller than GOOD-MORNING.md ({out_tk:,} vs {gm_tk:,} "
             f"{unit_word(cg)}, {ratio:.1%} of it, floor <40%; tier measured, not assumed: "
             f"{out_tier})",
             out_tk < 0.40 * gm_tk)
```

**The floor, in prose, quoted:** `knowledge/_gen_chain.py:176`
```
{chain_pct:.0f}% of it. Under 40% is this generator's own floor — above it, the wrapper is
```

### F14 — the composition, measured (all figures `tiktoken cl100k_base`)

| part | tokens | share |
|---|---:|---:|
| `GOOD-MORNING.md` — WHOLE FILE (the denominator) | **86,879** | 100% of denom |
| ↳ header, file top → ★ LATEST (lines 0–18) | 2,274 | 2.6% |
| ↳ **★ LATEST banner (lines 18–36, 18 lines)** | **27,847** | 32.1% |
| ↳ everything below the banner | 56,758 | 65.3% |
| `_CHAIN.md` — WHOLE FILE (the numerator) | **45,506** | 52.4% of denom |
| ↳ slice (GM header + ★ LATEST + presence index + LS delta) | 32,915 | 72.3% of file |
| ↳ **wrapper** (generator boilerplate) | **12,591** | 27.7% of file |
| ↳ *of which* LS ⏱ LATEST delta only (of 41 delta lines) | 2,318 | — |

**THE CARRY LIST IS ONE LINE.** Inside the ★ LATEST banner, exactly one line matches `residual →`:

```
line 31   24,873 tk   > **residual → #225:** ⬛ **① RATIFY AND BAKE v1.0.3: THE RATIFY LINE IS DAVE'S…
```

**24,873 tk = 89.3% of the ★ LATEST banner, 54.7% of the whole chain file, 28.6% of GOOD-MORNING.**
The next-biggest line in the banner is **349 tk**. This is not a distribution with a tail; it is
one line and then noise.

### F15 — the retirement arithmetic, and why the obvious number is WRONG

The gap looks like `45,506 − (0.40 × 86,879) = 45,506 − 34,751.6 = 10,754.4 tk`. **It is not.**
The carry list sits in **both** the numerator (via the slice) and the denominator (it is part of
`GOOD-MORNING.md`), so retiring `x` tokens from it removes `x` from **both** sides:

```
(45,506 − x) < 0.40 × (86,879 − x)
45,506 − x   < 34,751.6 − 0.4x
0.6x         > 10,754.4
x            > 17,924
```

⇒ **≥ 17,925 tk must come out of the carry list** — 72.1% of its 24,873 tk. Stated the other way,
solving for the banner size `B` (chain ≈ `B + 17,658`, GM ≈ `59,032 + B`):

⇒ **the ★ LATEST banner must land under ~9,925 tk**, down from **27,847 tk**.

`GOOD-MORNING.md`'s own ④ said *"the bite needs a ★ LATEST banner under ~11K tk, and the carry list
alone is ~20K"*. Both were the right shape; the measured figures are **~9,925 tk** and **24,873 tk**.

**Three independent levers, priced:**

| lever | what moves | threshold | touches |
|---|---|---|---|
| **A — retire the carry list** | cut GM line 31 | **≥ 17,925 tk** (72.1% of it) | ⬛ DAVE'S — a carry-retirement rule |
| **B — shrink the wrapper** | generator boilerplate only | **> 10,754 tk of 12,591** (85.4%) | numerator only; GM untouched |
| **C — let GM grow below the banner** | denominator only | GM must reach **> 113,765 tk** (+26,886) | heals by accretion, retires nothing |

⚠ Lever B is arithmetically sufficient but would leave **~1,837 tk of wrapper** — read that as
"the wrapper cannot survive as a wrapper", i.e. B is a real option only if the wrapper is
genuinely mostly disposable. Lever C heals the *bite* while the underlying carry keeps growing,
which is the shape the generator's own floor comment exists to refuse.

⛔ **NOTHING WAS RETIRED, RULED OR PROPOSED HERE.** These are measurements for the conductor to
price and for Dave to rule on.

---

## UNPROVEN

1. **The render sweep's failing item.** Not named. Binding obstacle: the item exists only in the
   CI job log; no `gh` in this sandbox, GitHub API 404s unauthenticated on a private repo.
   Proven around it: 135/135 snippets pass individually and a 44-snippet aggregate passes, on
   **byte-identical inputs** to run #457. **Price to close:** one yaml edit adding `| tee` +
   `upload-artifact` to the sweep step (⬛ workflow edits were fenced out of this sub), or one
   machine with >15 min uninterrupted wall (873.6 s measured serial) to run it un-chunked.
2. **The failing step of the release job at `f4fec54` (#454/#456/#457).** All eight steps
   reproduce GREEN on a faithful replica of that tree, and the 15–19 s duration is too short to
   have reached the release-audit selftest (F12), so the cause is most likely environmental —
   but **which** environmental step is unproven. Same binding obstacle. **Price to close:** the
   job log, or a `--rerun` with per-step timing visible.
3. **A whole-artefact (135-snippet) invariant in the sweep.** `StateContrastReportError` → exit 2
   can only bite at full artefact size; the largest aggregate driven here was 44 snippets. The
   178 s call boundary (measured; background processes are killed by `--die-with-parent`) is the
   binding obstacle on this box. **Price to close:** as (1)(b).

---

## REPLAY-THESE

```bash
cd /sessions/<session>/mnt/UX-design

# ---- environment for anything that drives the browser (measured working, this box) ----
export PYTHONPATH=/var/tmp/pylibs:$PYTHONPATH
export PLAYWRIGHT_BROWSERS_PATH=/var/tmp/pw-browsers-220
export LD_LIBRARY_PATH=/var/tmp/chromelibs-220/root/usr/lib/aarch64-linux-gnu
export TMPDIR=/sessions/<session>/tmp225        # ⛔ NOT /var/tmp — root fs 100% full
ldd $PLAYWRIGHT_BROWSERS_PATH/chromium_headless_shell-1234/chrome-linux/headless_shell | grep "not found"   # must print nothing

# ---- CLASS 1 ----
# ⛔ BACK THE AUDIT UP FIRST — the sweep writes a TRACKED file (_validate_state_contrast.py:1385)
cp knowledge/_STATE-CONTRAST-AUDIT.md _to_delete/AUDIT-PRISTINE.md
python3 knowledge/_validate_state_contrast.py --selftest              # 2.5 s, 62 arms, rc=0
python3 knowledge/_validate_state_contrast.py <SnippetName>           # one item, ~1.4 s
python3 knowledge/_validate_state_contrast.py                         # FULL sweep — 873.6 s, needs >15 min wall
cp _to_delete/AUDIT-PRISTINE.md knowledge/_STATE-CONTRAST-AUDIT.md    # restore, then confirm:
git status --porcelain knowledge/_STATE-CONTRAST-AUDIT.md             # must be empty
git diff --stat f4fec54 HEAD -- knowledge/snippets/ knowledge/canon/ knowledge/tokens/ knowledge/_validate_state_contrast.py

# ---- CLASS 2: faithful per-commit replica (writes NOTHING to the repo) ----
RR=/sessions/<session>/relrep; rm -rf $RR; mkdir -p $RR
git archive <SHA> | tar -x -C $RR                 # ~227 MB, ~9 s
ln -sfn "$PWD/.git" $RR/.git
cd $RR
python3 knowledge/_release/_gate_frozen_release.py --check --at <SHA> --no-worktree
python3 knowledge/_release/_gate_frozen_release.py --selftest
python3 knowledge/_release/_gate_release_audit.py --check
python3 knowledge/_release/_gate_release_audit.py --selftest
python3 knowledge/_release/_gate_release_audit.py --pack
python3 knowledge/_release/_gate_ci_template.py --check
python3 knowledge/_release/_gate_ci_template.py --selftest
bash apollo-spider/build-designer-pack.sh --selftest

# ---- CLASS 3 (⛔ --check / --selftest ONLY; the bare generator REWRITES _CHAIN.md) ----
python3 knowledge/_gen_chain.py --check
python3 knowledge/_gen_chain.py --selftest
python3 _to_delete/s225-forensics/measure_chain.py      # the banner / carry-list decomposition
sed -n '751,757p' knowledge/_gen_chain.py               # the computing line + the assertion
```

---

## CONSEQUENCES-AND-PITFALLS (Dave #165 — mandatory)

1. ⛔ **THE SWEEP WRITES A TRACKED FILE ON EVERY RUN, INCLUDING A FILTERED ONE.**
   `_validate_state_contrast.py:1385` writes `knowledge/_STATE-CONTRAST-AUDIT.md` unconditionally,
   and a **name-filtered** run writes an audit containing **only the filtered snippets**. Anyone
   who runs one snippet to debug and then commits has replaced a 135-snippet audit with a
   1-snippet one. Back it up first; restore and `git status` after. (Done here: md5 identical
   before and after.)
2. ⛔ **DO NOT RUN THE SWEEP AND THE REAL AUDIT CONCURRENTLY.** The report body asserts its own
   headline counts are re-read off the artefact it just wrote. Two processes writing the same
   audit can trip that assert and produce a **FALSE red at exit 2**. The chunked runs here used
   separate `knowledge/` replicas for exactly this reason.
3. ⛔ **`_gen_chain.py` WITHOUT `--check` REWRITES `_CHAIN.md`.** The selftest exits 1 today, so a
   habitual "run it again to see" is one keystroke from a chain rewrite in a session that did not
   intend one.
4. ⚠ **THE 15–19 s FIGURE IS THE STRONGEST CLUE AND IT IS EASY TO MISREAD.** The gate steps cost
   ~33 s locally (F12). Reading "the release job failed" as "a release gate failed" is the
   available wrong turn: on the tree it ran, every gate is green. The next drill should start at
   checkout / `setup-python` / `pip`, not at the gates.
5. ⚠ **`_gate_release_audit.py --pack` IS STRUCTURALLY RED IN THE BUMP→BAKE WINDOW** (F10). Any
   session that bumps `VERSION` and pushes before baking has bought itself a red CI on that step,
   for every commit until the zip lands. This is by design and selftest-asserted — but it means
   "CI is red" during a release day is expected noise unless someone reads *which* step.
6. ⚠ **A FROZEN-GATE RUN IN A REPLICA WITH A SYMLINKED `.git` WILL LIE ABOUT THE WORKTREE ARM.**
   Run it `--at <SHA> --no-worktree`. Run it without and it reports "FROZEN RELEASE MOVED" and
   "DIRTY IN THE WORKING TREE" for files the replica simply does not have — a convincing false
   red that cost a call here before it was named.
7. ⚠ **BACKGROUND WORK IS IMPOSSIBLE IN THIS SANDBOX, AND IT FAILS SILENTLY.** A `nohup`'d job
   returns a PID, leaves a 0-byte log, and is gone next call — it looks like "still running", not
   like "killed". Anyone chunking long work should verify with `pgrep`, not with a log tail.
8. ⚠ **ROOT FS IS 100% FULL (60 MB free).** `TMPDIR=/var/tmp` will ENOSPC mid-render and, per the
   render runbook's own history, that surfaces as a network-shaped error. `/sessions` had 3.7 GB
   and is the right scratch home today.
9. ⚠ **A CONCURRENT LANE IS EDITING `knowledge/_release/_gate_pack_docs.py` IN THIS SAME TREE.**
   Anyone reconciling should not read that modification, or
   `notes/_subreports/2026-08-29-225-gumdrop-gate-widening.md`, as belonging to this report.
10. ⛔ **THE RATIO'S OBVIOUS ARITHMETIC IS WRONG BY 7,170 tk** (F15). The carry list is in both
    numerator and denominator; pricing a retirement off the 10,754 tk gap would under-cut by 40%
    and the bite would stay red after the work was done.

## RULING-SHAPED (named, NOT ruled — ⬛ these are Dave's / the conductor's)

1. **The carry-retirement rule** (`GOOD-MORNING.md` ④ already names it as Dave's). This report
   supplies only the threshold: **≥ 17,925 tk out of the carry list**, or a **★ LATEST banner
   under ~9,925 tk**.
2. **Whether the bump→bake window is allowed to be CI-red** (F10) — i.e. whether the `--pack`
   step's contract should distinguish "nothing baked yet" from "manifest names a release nobody
   baked", or whether a red release day is the intended cost of `s219-D4(2)`.
3. **Whether the sweep step gets a log tee + artefact upload in `gates.yml`** so the failing item
   is never virtualized again. This is the instrument change that would have made this whole sub
   unnecessary; it was outside this sub's write fence.
