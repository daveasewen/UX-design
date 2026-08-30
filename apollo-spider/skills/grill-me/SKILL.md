---
name: grill-me
description: Ask the six questions that decide how a piece of Apollo work will look, before any of it gets built — theme first, then light/dark, density, brand assets, data and constraints. Saves the answers as a short brief the other Apollo skills read. Use at the start of a new project or a new design task, and always before generate-from-canon builds anything.
---

# Grill me

Six questions, asked once, at the start. They take about two minutes and they decide
things that are expensive to change later — the first of them decides whether your
corners are round.

Skip any of them. Skip all of them. What this skill will **not** do is quietly pick for
you and say nothing: a skipped question is written down as *skipped*, and where a default
has to be used it is said out loud before anything is built.

## When to run this

- At the start of a **new project**.
- At the start of a **new design task** inside a project that already has a brief, when
  the task is different enough to want its own answers (a different product area, a
  different audience, a different surface).
- **Before `generate-from-canon` builds anything.** That skill checks for a brief first
  and will ask the theme question itself if it can't find one — running this properly is
  the better version of that.

## How to skip

| you say | what happens |
|---|---|
| *"skip the grill"* / *"skip all"* | No more questions. Every answer is recorded as `skipped`. The theme default is **announced** before the build starts. |
| *"skip"* on a single question | That one is recorded as `skipped`. The next question is asked. |
| nothing, or a shrug | Treated as a skip on that question. Never as agreement. |

A skipped question is not a wrong answer. It is a decision left open, and it stays
visible in the brief so it can be closed later instead of being discovered as a surprise
in the work.

## The six questions

Ask them **in this order**, one at a time, and stop asking as soon as a full skip is
called. Keep each one to the question plus its choices — do not stack them into a wall.

---

### 1. Which theme? *(ask this first — it changes the shape of everything)*

Four ship. They differ in colour and, crucially, in **corner shape**:

| theme | what you'll see |
|---|---|
| **Mono** | Monochrome throughout — colour appears only in status and in charts. **Square: every corner is zero radius, deliberately.** |
| **Common** *(code key: `legacy`)* | The established interface look, brand red and teal in the interactive parts. Square corners. |
| **Console** | Mono's neutrals with the brand palette on top, and the one theme with **rounded corners** — controls and surfaces both. |
| **Supercharge** | The brand-uplift look, on its own warmer neutral range. Square corners; status and chart colour identical to Mono. |

Say the theme name. If you're not sure, say what the product feels like and the choice
can be narrowed for you.

**If this one is skipped:** the build will use **Mono**, and it will say so before it
starts — in Mono every corner is square by design, so a page that looks flatter than you
expected is the theme, not a mistake. Changing the theme afterwards is one attribute, but
anything hand-adjusted around square corners has to be revisited.

---

### 2. Light, dark, or both?

Both is the usual answer and costs nothing at build time — every component ships both.
Answer "light only" or "dark only" if the product genuinely never offers the other, so
the work isn't checked against a mode nobody will see.

---

### 3. How dense, and how wide?

Two halves of one question:

- **Density** — comfortable (roomy, fewer things visible) or compact (more on screen, for
  people who live in this all day).
- **Width** — the surface you're designing for: phone, tablet, laptop, wide desktop, or a
  fixed maximum width you already work to.

---

### 4. Are there brand assets to use?

Logos, a photography set, product names, an existing colour a stakeholder will insist on,
a typeface that is already decided. Name them and say where they are. "None" and "not yet"
are both real answers — "not yet" is the one worth writing down.

---

### 5. Real data or placeholder?

- **Real** — you have actual content, figures or copy to use. Say where it is.
- **Placeholder** — invented content is fine for now.

This matters more than it sounds: real names, real currency amounts and real edge cases
change the layout, and a design that only ever held tidy placeholder text tends to break
the first time it meets a long one.

---

### 6. Anything fixed, or anything off-limits?

Both halves, in one answer:

- **Fixed** — accessibility commitments you have to meet (a contrast level above the
  default, no motion, keyboard-only operation, screen-reader specifics), regulatory or
  legal requirements, a pattern the organisation mandates.
- **Off-limits** — anything you want the system **not** to do. Common ones: don't invent
  components, don't add animation, don't touch the navigation, don't produce React, don't
  restructure content, don't get creative with colour.

Say them plainly. This is the question that saves the most rework.

---

## Save the answers

Write the answers to a small file in the project:

```
briefs/<YYYY-MM-DD>-<task-slug>-grill.md
```

e.g. `briefs/2026-08-30-payments-dashboard-grill.md`. Create `briefs/` if it isn't there.

Use the shape in `brief-template.md`, beside this file. Rules for it:

- **One line per answer.** It is a note, not a document.
- **Every one of the six appears**, in order, including the skipped ones — written as
  `skipped` with the date, so a gap is visible rather than absent.
- **Record what was actually said**, in the designer's own words where they said
  something specific. Don't tidy an answer into a category it didn't quite fit.
- **If the theme was skipped**, the brief records `skipped — proceeding with Mono
  (announced <date>)`, so the default is on the record as a default and not as a choice.

Then say, in one line, what you're about to build with — the theme, the modes, and any
constraint from question 6 — and start.

## Handing it on

`generate-from-canon` reads the newest brief in `briefs/` and **cites it** in its
used/missing note: which brief, and which of the six answers actually shaped the build.
A brief nobody cited is a brief nobody read.

When an answer changes mid-project, don't edit the old brief — run this again for the new
task and let the two sit side by side. The change is worth being able to see.

## Re-asking

Ask a single question again, out of order, whenever the work reaches something the brief
left open — "you skipped the data question and this table needs real amounts to lay out;
do you have any?" That is a good moment to ask, and a much better one than the start.

Don't re-run the whole grill on a project that already has a brief unless the designer
asks. Once is the point.

*Experimental — feedback on what's missing is the point.*
