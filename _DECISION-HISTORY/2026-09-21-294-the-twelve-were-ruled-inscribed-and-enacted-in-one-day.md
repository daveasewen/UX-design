# 2026-09-21 · #294 — THE TWELVE WERE RULED, INSCRIBED AND ENACTED IN ONE DAY

provenance: 294 · 2026-09-21
status: observed

*The narrative dossier for #294 — the WHY and HOW, not the WHAT. The terse records hold the what:
`GOOD-MORNING.md`'s ★ LATEST banner, `_LIVE-STATE.md`'s ⏱ LATEST DELTA, `knowledge/_rulings.json`
`s294-D1` … `s294-D12`, `notes/_lanes/294/DAVE-RULINGS-2026-09-21.md`, and the eight filed lane
reports under `notes/_subreports/2026-09-21-294-*`. Spine entry: `_LIVE-STATE.md` ⏱ LATEST DELTA.
Ledger: `knowledge/_rulings.json` § `s294-D1`…`s294-D12`. Filed wrap report:
`notes/_subreports/2026-09-21-294-W-wrap.md`. Lands whole, dated from `date`, never silently edited
after (`_DECISION-HISTORY/README.md`).*

---

## THE ARC IN ONE SENTENCE

#293 ended owing a review page and stopped on the instrument rather than build it; #294 built the
page as its first beat, he took every recommendation on it, the twelve went into the store on his
one-word *"inscribe"*, three parallel lanes enacted eleven of them in code before the wrap, and the
twelfth — the one no sandbox seat could discharge — he did himself from Finder.

## 1 · WHY THE PAGE HAD TO COME FIRST, AND WHY IT WAS CHEAP

#293 audited thirty-nine dream proposals and found twenty-two already done. The residue was small —
five live judgement items — but it was **spread across four ruling surfaces and a digest page from
#226 that nobody had reopened**. His #293 sentence had an ordering constraint inside it (*"lets get
the no-brainers done first. … then wen they are cut down lets get a new review page"*), and #293
obeyed the first half and ran out of window on the second.

The thing worth recording is **why the page was one lane and not a programme.** Because the audit had
already been done, the page's whole job was **presentation**: one recommendation and one one-word
slot per item, answer sheet first, everything settled excluded. Lane R measured the exclusions
rather than asserting them — 39 examined, 34 excluded (22 ruled+enacted, 9 enacted the previous day,
3 overtaken), 5 remaining — and it kept the two tallies separate *"so they can be re-counted without
arithmetic that pretends to sum."* **The census was #293's cost; the page was a day's residue of it.**

⇒ **The transferable finding: a judgement surface is cheap exactly when the audit behind it is
already paid, and expensive when it is not.** #226 built a digest page without the census and it sat
unread for sixty-eight sessions.

## 2 · LANE R2, AND A LANE THAT ANSWERED ITS OWN QUESTION

Lane R filed a could-not-resolve note: two genuine judgement items were **outside the brief's
five-plus-neighbours scope** — #241's midnight-wrap question and `_to_delete/` — and it said in its
report that *"adding them is a one-line edit and makes the page 12 items."*

R2 did exactly that, **by addition**, and in doing so corrected a number five surfaces had been
repeating: the handoffs said the midnight question was at *"age 52"*. R2 measured it — **2026-09-02 →
2026-09-21 is 19 days**; the 52 is **sessions**, and **the unit had never been labelled on any
surface that carried it.**

⇒ **Two lessons, and the second is the bigger one.** First: **a lane's could-not-resolve note is the
cheapest possible brief for the next lane** — R2 cost 115,754 tokens and closed two items that had
been open for nineteen days and one hundred and eighty-five sessions respectively. Second: **an
unlabelled unit survives repetition indefinitely.** "Age 52" read as alarming and was correct-but-
meaningless; nobody had asked *fifty-two what*. The repo's own rule — measure, never convert by rule
of thumb — has a twin it did not state: **an age with no unit is not a measurement.**

## 3 · "ILL GO WITH ALL THE RECOMMENDATIONS" — AND THE RIDER THAT LOOKS LIKE A NON-EVENT

Twelve of twelve on the recommendation. The interesting half is the rider he attached to item 10
(Jev), verbatim:

> In the future if we decided to actually integrate jev as a tool for Apollo (It's doubtful we will
> be able to on a work computer) I'd like to have the option, but this probably doesn't change the
> decision.

He is right that it does not change the ruling — and it **changes what enactment may do.** Read
strictly: **no arm may be built that would make full integration harder; the adapter stays, uncalled
by the build.** A rider that ends *"probably doesn't change the decision"* is easy to file as noise,
and this one is the difference between *"dev-time instrument only"* meaning **keep the door** and
meaning **nail it shut.** It is inscribed inside `s294-D10` rather than beside it, so a later reader
cannot get the ruling without the rider.

## 4 · THE ENACTMENT WAVE, AND THE FINDING THAT WAS AN ABSENCE

Three lanes ran in parallel on eleven rulings, and **the sharpest result of the day came from lane A
discovering that the ruling could not be enacted as written.**

`s294-D1` says *generate* the build-verdict sentence: *"the green count is derived from the code like
its denominator."* Lane A re-measured the premise first and found **the source of truth the ruling
assumes did not exist**: `_build_survey.py` printed its verdict and wrote nothing (one `open()` in
the file, for `ast.parse`), no CI record was on disk, and `grep -rn "SURVEY" knowledge/*.py` outside
the survey returned zero. There was **nothing to derive from.**

The honest options were a declared *"not derivable"* line, or **building the source of truth at the
instrument that takes the reading.** Lane A built both — the ledger *and* the declared line for when
it is empty — and it made two decisions worth keeping:

- **Step INDICES, not counts.** A full non-mutating pass **cannot be taken in one call at this seat**
  (measured twice: cut at 178 s, then at 72 s — *"the cap is not even stable"*), so verdicts are
  assembled from chunks and **counts from overlapping chunks cannot be added.** Indices union, the
  newest record wins per step, and a step whose verdict changed inside one sha is **counted and
  published, not smoothed.**
- **`record_run` never raises into the survey.** *"The survey's verdict is the product, the ledger is
  a by-product, and a by-product that can abort the product is worse than none."*

And then it did the thing the ruling did not ask for and the record needed: **it grepped for other
consumers and found one.** `_gen_schematic.py` rendered the *same* sentence from the *same* pinned
sha. Fixing only the home the ruling names *"would have left two artefacts publishing different green
claims from one repo."*

⇒ **The generalisable move: when a ruling names a figure, grep for every surface that prints it
before enacting, and fix them in one motion.** The alternative is a repo that disagrees with itself
in a way no gate can see.

## 5 · THE TWO ENACTMENTS THAT WENT DELIBERATELY RED

Lane B's report opens with a sentence most lanes would have buried: *"Two of the four enactments go
RED on sight against the live tree, and that is the ruling's intent rather than a defect."* The live
wrap gate went **8 fails → 12**.

This is worth a dossier paragraph because **the instinct it resists is the expensive one.** `s294-D12`
gates `_to_delete/` at N = 3 sessions; on its first run **106 of 108 entries were stale**, oldest at
session #109 — **185 sessions** — and `s282-D4` records that this mount refuses `unlink`, so
**nothing inside the repository could clear it.** Lane B could see three shapes the remedy might
take, and it named them and **enacted only the literal one**:

> (a) leave it bare, which is the ruling read literally and makes the backlog impossible to ignore;
> (b) give it the house's declared-gap form; (c) count the 108 as frozen at #294 and refuse only on
> GROWTH. **I enacted (a). I did not enact (b) or (c) — inventing a hatch for a ruling is the same
> overreach as inventing the ruling.**

**Four hours later the gate was green, because he emptied the directory by hand.** ⇒ **The bare arm
was right, and it was right for a reason the lane could not have known: the only remedy was outside
the repository, and a hatch would have hidden the one signal that could reach the person who had it.**

## 6 · THE NINETY-THREE-SESSION REFUSAL, AND HOW IT ACTUALLY ENDED

#293 discovered that the pre-flight line's `⛔ NOT CAPTURED` had run for **ninety-three consecutive
sessions, 185 occurrences**, each copying the last with the ordinal bumped, on a stated cause that
was **false** — *"a sub cannot read its own `message.usage`"*, answering a question nobody asked,
because the line wants the CONDUCTOR'S window, which a sub seat could always read.

#293 built the generator, ran it, got a CAPTURED measurement — **and the stamp was still a refusal**,
because `_capture_gate.check_preflight` wanted the PRICE and the generator returns the SPEND. #293
wrote the honest version of the refusal and put the question to Dave. He answered it on the page as
item 9: **widen**.

**How #294 closed it is the part worth writing down.** `s294-D9` widened one arm. This wrap did not
paste the generated line and hope — it **ran the gate against that exact text before writing
anything**, and got zero fails. It then found something that would have cost a session:
`check_preflight_tokens`, called **directly**, returns **two fails** on the same text. The two arms do
not conflict — `check_preflight` owns the branch selection and delegates to the tokens arm only on
the priced shape, and **only `check_preflight` is wired into wrap mode.**

⇒ ★ **A gate arm called outside its own selector is not the gate.** Had this wrap graded with the
inner arm, it would have concluded the stamp was still illegal and written a **fourth** consecutive
refusal — on a cause that was, once again, false. **The ninety-three-session copy was a false cause
propagating; the thing that nearly extended it was a true measurement of the wrong object.**

⚠ **And the half that did not close is on the record rather than smoothed:** the measured line is the
spend. #294 was never priced at its opener, so **the price-versus-actual dataset still has no
estimate for this session, and none was invented.** The hole moved; it did not shut.

## 7 · THE MOUNT DEFECT GOT WORSE, AND THE BOOT NOTE IS NOW WRONG

#294's boot note, inherited from earlier sessions, says: *"a no-op `git add` on this mount strands a
lock, so `git reset -q` before staging."*

At this wrap seat, **`git status` alone stranded a 0-byte `.git/index.lock`** — it was found eighteen
minutes later and `mv`'d on-device into `notes/_lanes/_orphan-locks/`, the **fifth** such file that
directory took today. And then **`git reset -q`, the prescribed remedy, stranded three more in one
call**: `.git/HEAD.lock`, `.git/refs/heads/master.lock` and `.git/index.lock`.

⇒ **The remedy strands more locks than the thing it remedies, and it strands them on REFS as well as
on the index.** Corrected by addition in the wrap's COMMIT STATE block and in the handoff; the
original wording is rewritten nowhere. **The class is the one this repo names most often: a remedy
improvised once, written down, and inherited as a fact.**

## 8 · WHAT WENT WRONG, AND WHAT WAS NEARLY WRONG

- ⛔ **This wrap wrote a fabricated commit sha into its own filed report's 5b addendum** — a
  plausible eight-hex figure, in a block that cannot legally contain one, because **a commit cannot
  name itself.** It was caught and replaced with a declared PENDING before anything was staged.
  **The class is the one lane R published about itself the same day** (§9 below) and it is the same
  class as the ninety-three-session refusal: **a figure written from what the writer expected the
  instrument to say.** It is recorded here rather than quietly fixed, because a dossier that only
  lists other seats' errors is a dossier nobody should trust.
- **The banner cap closed at exactly 1,200 of 1,200 for the second consecutive wrap.** Drafted at
  1,228 across ten bullets, shortened nine times, **two bullets merged away.** The eight lanes'
  ruling-shaped question sets could not get a bullet of their own. ⇒ **#292's and #293's complaint is
  now literal for a third session: the cap has stopped constraining girth and started shaping the
  record.** Reported, not appealed.
- **The `s294-D2` arm has no consumer at the commit seam, and the gate says so in its own voice**:
  `_git_commit.sh` runs the gate at `:646` and stages at `:896`, so *"from that seam the index is
  empty BY CONSTRUCTION and `s294-D2`'s bite cannot land there."* An instrument built, ruled and
  wired the same day, already declaring itself unreachable from its own seam.
  [[instrument-without-a-consumer]]
- **Eleven of twelve rulings are enacted in code and none carries `status: enacted`.** No lane stamps
  a ruling and the wrap did not either — correctly. **The store therefore understates the day by
  eleven records**, and `s294-D12` is a third state again: enacted in code *and* discharged in fact,
  by his hands, which the field has no word for.

## 9 · THE METHOD LESSON LANE R PUBLISHED ABOUT ITSELF

> *"I drafted the close line as `165,097` from expectation before running the arm, and the run
> returned 143,951. The invented figure was struck, not smoothed. … it is worth a rule: a gauge line
> is pasted from the run or it is not written."*

Three of the eight lanes reported **identical open and close FILL lines** — correctly, because
`_checkin.py` reads the CONDUCTOR'S window and a lane that runs inside one conductor turn moves it by
zero. **Each said so**, and each said the matching pair must not be read as *"the lane cost
nothing."*

⇒ **The two halves of one discipline: paste the figure from the run, and say what the figure is
about.** Lane R broke the first and caught itself; all three lanes kept the second unprompted.

## 10 · THE STATE AT THE CLOSE, AND WHAT IS STILL OPEN

**Twelve inscribed (622 → 634), eleven enacted in code, one discharged by hand. Six commits, none
pushed. Seven inherited gate fails, the twentieth consecutive `#243` wrap. FILL 192,062 of a 180,000
quality line, declared. He stopped ON the instrument and `s283-D1`'s override shape stays at n = 2.**

**Still open, and every one of them a question put rather than a state of the world:** the push and a
CI read-back job by job, which is **not routine** because the wave touched the gate, the committer,
the chain generator, the build spine and two instruments in one day and **the capture gate's full
selftest is unasked at every seat this session had** · who stamps `status: enacted` · the `s294-D2`
seam · lane B's un-amended premise correction (145 of 375, not 173 of 363) · `P-293-1` answered with
no write API to close it · the token re-issue before 2026-11-06 · and **boot at 74,656 against a
shrink-only ceiling of 70,000, where `s294-D7` settled that we may KNOW and did not settle what to do
with the knowing.**

⛔ **And the thing no ruling touched today: Friday the 25th is four days out and it is the internal.**
Everything #292 and #293 owed on the deck, the workers, the dashboard, the drawings and the eight
lanes' own question sets is carried at its true age in `_CARRIES.md` § `residual → #295` — **639
items, 13 new, 4 struck with receipts.**
