# Agentic loop — gates-as-a-service (2026-07-14, Dave)

**The honest framing.** v1 (the designer pack) = skills + KB + one-pass retrieval, operated by a host
agent (Copilot). That's **agent-ready, not yet agentic** — no self-correction loop.

**An agentic loop = generator + verifier + iteration:**
- **Generator** = the host agent (Copilot / Claude).
- **Verifier** = Apollo's Python gates (`_validate_*.py` + `_build_all.py`): contrast, token-fidelity,
  a11y/ARIA, icon-provenance. **Already built. The expensive, differentiated half.**
- **Iteration** = agent calls the check, reads the fail, fixes, re-checks. **Cheap — but not wired yet.**

**The step that closes the loop = gates-as-a-service.** Expose the validators as callable tools
(an MCP / tool interface) so the host agent runs them **mid-task**, not only in batch CI. This is the
"v2" we discussed — Apollo's OWN checks. **NOT** the Figma MCP (ingestion, already used 2026-07-03),
**NOT** Sutherland (React build target).

**Honesty caveats (quote-safe):**
- The **repair loop is "not built"** (deep-analysis architecture diagram) — gates verify; nothing
  auto-repairs yet.
- Gates check **declared** obligations, not everything ("honesty system, not inspection system" — a
  contrast pair never listed is never computed). Real autonomy may want inspection-mode gates.
- Today the loop's middle is a **human** running `_build_all.py` and fixing.

**Why it matters:** the expensive half — a machine that authoritatively says "wrong, and why" — is
done; making it agentic is *wiring, not new judgment*. Connects to the §9 "generate-free-then-
constrain-and-verify" two-pass instinct: the gates ARE the constrain-and-verify half.

**Status:** an idea recorded 2026-07-14, NOT a spec. Recorded in `_LIVE-STATE` PLANNED/TARGET +
GOOD-MORNING queue #4. Next step if pursued: write it up as a note/ADR — scope the tool interface,
which gates go first, and the honesty→inspection upgrade.
