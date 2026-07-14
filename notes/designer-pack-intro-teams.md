# Designer pack — Teams intro (for the 20 Jul intro; hands-on from the 24th)

> Draft handover message to the design team. Attach **`Apollo-designer-skills.zip`**
> (the four skills + current KB; build script excluded). Experimental release.

---

Hi all,

The design-system assistant we talked about is ready for a first try. It's a set of
"skills" for GitHub Copilot in VS Code — you ask Copilot in plain English and it
generates or checks UI against our own design system, so what comes out is on-brand
and accessible by default.

Four things it can do right now:
- Generate a screen or component from our design system
- Check a design against the system (colours, spacing, accessibility)
- Run a quick usability review
- Help draft a brand-new pattern

**Please read this bit:** it's experimental and early. The component library behind it
is still small, so it *will* get things wrong — it's not a finished product. Treat it
as a sandbox: poke it, break it, and tell me what's rubbish. That feedback is the whole
point of this round.

Getting started (~5 minutes):
1. Unzip the attached **`Apollo-designer-skills.zip`** — you'll get a `designer-skills-v1` folder.
2. Drop that folder where Copilot reads skills — I'll confirm the exact spot with you.
3. Open a project in VS Code and just ask Copilot, e.g. "generate a payments summary
   screen using our design system."

No other setup — nothing to install, no Python needed.

One favour: whoever gets set up first, can you tell me (a) where your Copilot picked the
skills up from, and (b) shout the moment a skill actually runs, or refuses to? That
confirms it works on your machines, not just mine. (If it doesn't fire first time, it's
almost certainly where the folder needs to sit — a quick fix.)

This is the intro — I'd like everyone experimenting from the 24th. Happy to jump on a
call and set it up with anyone who wants a hand.
