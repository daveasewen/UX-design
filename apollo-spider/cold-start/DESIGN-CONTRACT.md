# Design contract — read this before you build anything in this project

**1. Declare the lane, in your first reply.** Before you build, say which one you are in: *on-canon* — working through the design skills in `skills/` — or *freestyle*. On-canon is the default. Freestyle happens only when the designer asks for it in words. Never change lanes silently; if you cannot reach the skills, say so plainly and follow the five rules below by hand.

**2. Grill first.** At the start of a new project or a new design task, look in `briefs/`. If there is no current brief for this task, run `skills/grill-me/SKILL.md` before you build — the theme question first. If you cannot reach that skill, ask the six questions at the foot of this file yourself. The designer may skip any question, or all of them. Record every skip in the brief beside the default it causes, and say that default out loud before anything is built.

**3. The five rules.** These hold even when no skill is open.

- **Never invent.** No new component, variant, colour or icon. If the system does not have it, stop and name the gap. Improvising is the failure this contract exists to prevent.
- **Copy the markup.** Component HTML comes from `knowledge/snippets/`, never from memory.
- **Ask the theme, never assume it.** Four themes ship and they disagree about corner shape. A guess gets every corner on the page wrong.
- **Dashboards are bento-first.** Layout comes from the rails in `knowledge/_render/_bento_edit_rails.json`, not from taste.
- **Check before you show.** Run `skills/check-with-gates/SKILL.md` before you put a screen in front of anyone. An unchecked screen is a guess.

**4. Scope.** This contract governs design and UI output in this project. Other work may use whatever skills suit it. If you use a non-Apollo skill to produce design output, say so in the same reply — an undeclared source is what turns a design problem into an unreadable bug report.

**5. When something looks wrong**, fill in `cold-start/REPORT-TEMPLATE.md`. Name the lane you declared. Most reports turn out to be a lane nobody declared.

---

**The six questions.** Ask them in this order, one at a time, and stop as soon as a full skip is called. *"Skip"* is a real answer to any of them; a shrug counts as a skip, never as agreement. Record each answer, skips included, in `briefs/<date>-<task>-grill.md`.

1. **Which theme** — Mono, Common, Console or Supercharge? *Skipped: the build uses Mono, whose corners are square by design, and says so before it starts.*
2. **Light, dark, or both?** Both is the usual answer and costs nothing.
3. **How dense, and how wide?** Comfortable or compact; phone, tablet, laptop, wide desktop, or a fixed width.
4. **Any brand assets?** Logos, photography, product names, a colour someone will insist on, a typeface already chosen. "None" and "not yet" are both answers.
5. **Real data or placeholder?** Real content changes layouts that tidy placeholder text never tested.
6. **Anything fixed, or anything off-limits?** Accessibility commitments, mandated patterns, and anything the designer wants left alone.

For questions 2 to 6 there is no silent default: if an answer is skipped and the work needs one, say what you are falling back to before you build, and write it in the brief as a fallback rather than as a choice.
