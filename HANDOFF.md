# HANDOFF — your day-one runbook on the agency machine

Plain, step-by-step. Assumes you can use a terminal a little and can drive the AI
agent tool, but nothing fancy. Designed to be done in a day. If you only have a
few hours, jump to **"The minimum path"** near the bottom.

> **The big idea:** you're not building from scratch on the agency machine. You're
> (1) getting this repo onto it, (2) feeding the agent the real design system so
> it stops guessing, and (3) running the UX/UI pipeline on one real example to
> prove it works. The thinking is already done — this is execution.

---

## Before you start — 15-minute checklist

Have these ready. If one is missing, note it and carry on; most stages still work.

- [ ] **This repo on GitHub.** (See Stage 0 if you haven't pushed yet.)
- [ ] **The AI agent tool** you'll use on the agency machine (Claude is ideal — the repo is written in its idiom — but it's model-agnostic).
- [ ] **Figma access** + the **Figma Dev Mode MCP** connected in that tool.
- [ ] **The React component library** — the repo/folder path on the machine, or its Git URL.
- [ ] **The published design-standards website** URL.
- [ ] A **real, small example to design** — one screen or feature. Small on purpose.
- [ ] Anything Promenaut gave you: docs, a workspace, login.

---

## Stage 0 — get the repo onto the machine (10 min)

If you haven't pushed from home yet, do this at home first (in this folder):

```bash
git init
git add .
git commit -m "feat: planning + harness scaffold for Promenaut design workflow"
# create an empty repo on github.com, then:
git remote add origin https://github.com/<you>/promenaut-design-workflow.git
git push -u origin main
```

On the agency machine:

```bash
git clone https://github.com/<you>/promenaut-design-workflow.git
cd promenaut-design-workflow
```

Open the folder in your AI agent tool. **Done when** you can see `AGENTS.md` in
the file list.

---

## Stage 1 — orient the agent (5 min)

Open a new agent session in the repo folder and paste **Prompt 1**
(`prompts/01-kickoff.md`). It tells the agent to read `AGENTS.md` and the dossier
and report back its understanding.

**Done when** the agent correctly says: it's a two-layer harness, UX/UI is the
working pipeline, it must never invent components, and it builds to WCAG 2.2 AA.
If it says anything off, correct it now — don't proceed until it's oriented.

---

## Stage 2 — build the knowledge layer (the big one, 1–3 hrs)

This is where the real company assets come in, and the most time-variable step.
Paste **Prompt 2** (`prompts/02-ingest-knowledge.md`). It will:

1. Read the published standards site → fill `knowledge/guidelines/`.
2. Read the Figma library (via MCP) and the React components → write one
   `knowledge/components/<name>.meta.json` per component, matching the schema.
3. Build the compliance records in `knowledge/compliance/`.
4. Pull/confirm tokens into `knowledge/tokens/`.

**Do it in small batches.** Start with **one component** (the button) end to end.
Read the generated `button.meta.json` yourself. The first one will be ~80% right
and 20% generic — fix the **anti-patterns** especially, because those are the
rules only you know ("never a destructive button in onboarding"). Once the shape
is right, let it do 5–10 more, then the rest.

**Done when** you have ~10+ real component metadata files you've eyeballed, and
the tokens + a handful of compliance rules are in place.

> ⚠️ This stage's length depends entirely on how tidy your Figma/React library is.
> If it's messy, ingest fewer components — you only need enough to run one real
> example. Quality over coverage today.

---

## Stage 3 — dry run, then real run of the UX/UI pipeline (1–2 hrs)

Paste **Prompt 3** (`prompts/03-run-pipeline.md`) with your real example.

It walks the pipeline: Framing → (you approve the brief) → Generator → Critic
craft gate → parallel Heuristic/A11y/Brand review → (you, the taste gate) →
Handoff. You sit at the three human gates — that's the design, not a limitation.

Watch for the **craft gate** doing its job: if the Generator invents a component
or hard-codes a colour, the Critic should fail it. If it doesn't, your metadata
needs tightening (back to Stage 2 for that component).

**Done when** you have a real prototype (React preferred, Figma Make fallback), a
passing accessibility review citing actual WCAG criteria, and a handoff spec.

---

## Stage 4 — close the Promenaut question (30–45 min)

Open Promenaut's documentation. With the agent, answer: what does their runtime
give you for free — state, logging, human-in-the-loop, scheduling? How would our
orchestrator (`harness/orchestrator.md`) map onto it? Write the answer as
`docs/decisions/ADR-0005-promenaut-runtime-mapping.md`. This is the one decision
we deliberately left open because it needs their docs.

---

## Stage 5 — commit, push, and you're ready (15 min)

```bash
git add .
git commit -m "feat: ingest real design system + first working UX/UI run"
git push
```

That's the artifact you show Promenaut and your company: a working, documented,
standards-compliant pipeline that ran on real assets — with your judgment encoded
at the gates.

---

## The minimum path (if you only have ~3 hours)

1. Stage 0 (clone). 2. Stage 1 (orient). 3. Stage 2 but **only the button + 2–3
components**. 4. Stage 3 on **one tiny screen**. Skip Stages 4–5 until later.
A single real, working example beats broad coverage. Ship the proof.

---

## If something goes wrong

- **Agent invents components / variants** → its metadata is too thin. Add explicit `antiPatterns` and confirm the component exists in `knowledge/components/`. The Critic only catches what canon defines.
- **Figma MCP won't connect** → ingest from the React library source instead; note Figma as a follow-up. The pipeline still runs.
- **Agent drifts from the plan** → re-paste Prompt 1 to re-orient; point it back at `AGENTS.md`.
- **Accessibility review is vague** → make sure `knowledge/compliance/` has real rules with SC + EN 301 549 clauses; the reviewer cites what's in canon.
- **Running low on time** → switch to the minimum path. Depth on one example, not breadth.

---

## So — docs + prompt, or this runbook?

Both, and they're complementary. The docs + Prompt 1 alone will orient any capable
agent correctly. This runbook is the connective tissue that keeps *you* moving
fast and stops the two risky stages (ingestion, Promenaut mapping) from eating
your day. Follow the stages; lean on the prompts in `prompts/`.
