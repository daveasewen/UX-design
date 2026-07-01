# Component library — target inventory & the case for an extensive build

*Drafted 2026-07-01. The proposal: a **comprehensive** component library makes the engine reliable for the bulk grunt work (interfaces that pass as bang-on standard), and — because more components means more valid combinations — it produces **natural UX variance** across a journey. Creativity then lives in a separate, tunable **ideation mode**, not as a workaround for missing parts.*

---

## The argument, grounded

Mature systems carry **~65–70 base components**; commercial Figma kits scale to **thousands of variants** on top. We're at **~38**.

| Library | Base components | Notes |
|---|---|---|
| **Ours (HSBC Common Toolkit, gated)** | **~38** | 32 reviewed + 5 gap-patterns + account-card |
| Material Design 3 (Google) | ~40 | leaner, mobile-first |
| Ant Design | ~65 | the most complete open system |
| Carbon (IBM) | 67 | enterprise, data-dense |
| Untitled UI (commercial Figma) | ~50–60 base → **10,000+ variants**, 900+ styles, 420+ page templates, 2,000+ icons | the "way bigger than 32" you saw |

So the instinct is right: **we're at roughly half a comprehensive base library**, and the fintech-specific set on top of that barely exists yet.

## Why "comprehensive" is the unlock (two modes)

- **Standard mode — the grunt work.** With a full kit, the engine *retrieves* the right part for almost any screen and the output reads as house-standard by default. Today, when a part is missing, the model invents (the cold-B run fabricated account numbers + status chips to fill a table it needed) — that's where drift and "needs a tidy" come from. **Coverage removes the reason to invent.**
- **Ideation mode — the workshop lane.** Creativity becomes a deliberate, tuned setting (the register dial, gradient/motion unlocked, gap-pattern generation) — *on top of* a solid base, not a substitute for it.
- **The variance bonus.** More components = more valid ways to compose a journey. Run the same brief and you get genuine, on-brand UX variance simply because there's more legitimate choice — the multi-variant idea gets richer for free.

---

## Target inventory (union of the mature systems, mapped to us)

✓ = gated today · **GAP** = to build · P1 (reliability-critical) · P2 (common) · P3 (nice-to-have)

### Actions
| Component | Status |
|---|---|
| Button · Links · Quick-actions · Segmented (View-options) | ✓ |
| Icon button | **GAP · P1** |
| Split button · FAB (mobile) | **GAP · P3** |

### Inputs & forms *(our biggest gap area)*
| Component | Status |
|---|---|
| Text input · Search · Select · Checkbox/Radio/Switch · Slider | ✓ |
| **Form layout + validation** (field groups, inline + form-level errors) | **GAP · P1** |
| **Date picker · date-range · time picker** | **GAP · P1** |
| **Number / currency (amount) input** | **GAP · P1** |
| **File upload / dropzone** | **GAP · P1** |
| **OTP / PIN / secure entry** | **GAP · P1** (banking) |
| Textarea | **GAP · P1** |
| Combobox / autocomplete · Multi-select · Tags input | **GAP · P2** |
| Range slider · Rating · Cascader/tree-select · Transfer | **GAP · P3** |

### Navigation
| Component | Status |
|---|---|
| Tabs · Tab-bar · Breadcrumb · Pagination · Nav/Menu · Dropdown-menu | ✓ |
| **Stepper** (interactive multi-step; Progress-tracker is display-only) | **GAP · P1** |
| Command palette / global search · Sidebar / nav rail | **GAP · P2** |
| Anchor / scrollspy · Back-to-top | **GAP · P3** |

### Data display
| Component | Status |
|---|---|
| Table · List-items · Cards · Account-card · Summary · Accordion · Tag · Badge · Status-indicator · Avatar · Segmented | ✓ |
| **Data grid** (sort / filter / select / edit) | **GAP · P1** |
| **Stat / metric card** (gated; only a util today) | **GAP · P1** |
| **Charts / data-viz kit** (bar · line · donut · sparkline) | **GAP · P1** |
| **Empty state** | **GAP · P1** |
| KPI / trend tile · Timeline / activity feed · Avatar group | **GAP · P2** |
| Tree · Calendar · Carousel · QR code | **GAP · P3** |

### Feedback & status
| Component | Status |
|---|---|
| Notifications · Modal/Dialog · Tooltip · Spinner (Loading) · Confirmation · Countdown | ✓ |
| **Alert / inline message / callout** | **GAP · P1** (already logged) |
| **Toast / snackbar** (transient; distinct from persistent Notifications) | **GAP · P1** |
| **Drawer / side sheet** | **GAP · P1** |
| **Popover** (distinct from Tooltip) | **GAP · P1** |
| **Skeleton loader** | **GAP · P1** |
| Banner · Progress bar (linear/circular) · Popconfirm | **GAP · P2** |

### Layout & containers
| Component | Status |
|---|---|
| Divider · Header · Hero · Eyebrow · Action-bar | ✓ |
| Footer · Grid/stack utilities · Page templates/scaffolds | **GAP · P2** |
| Splitter / resizable | **GAP · P3** |

### Media & identity
| Component | Status |
|---|---|
| Avatar · Video-player · Icon system | ✓ |
| **Brand mark / logo (official asset)** | **GAP · P1** |
| Image/media block | partial |

### Fintech-specific *(a genuine differentiator — generic systems don't have these)*
| Component | Status |
|---|---|
| RAG / status chips | ✓ |
| **Amount / currency display + money format** | **GAP · P1** |
| **Account selector / masked account chip** | partial (Account-card) |
| Transaction / ledger row · Statement/document row | partial |
| Payment-card visual · Coverage/runway bar · Standing-order / mandate row · Limits meter | **GAP · P2–P3** |

---

## What this adds up to

- **~20 P1 gaps** — the set that has to exist before "standard mode" is genuinely reliable (forms, dates, amount/OTP inputs, data grid, stat, charts, empty/skeleton, alert/toast, drawer/popover, stepper).
- Target base: **~38 → ~75–85** components, which lands us alongside Ant/Carbon and gives the fintech layer real depth.
- Each new component runs the **existing gated pipeline** we already built (snippet → meta → gate → `.cn-*`), so the machine to build them is proven — this is a content build, not new infrastructure.

## Layer 2 — shells, templates & lock-ups (the multiplier)

Base components (Layer 1, above) are only half the library. On top sit the things you can't automate a real screen without — and this is where the big kits get their numbers: **Tailwind UI** ~500+ blocks (23 app-shell variants + 25 header/heading lock-ups alone); **Untitled UI** 420+ page templates, 1,500+ sections, 10,000+ variants. This layer **doubles or triples** the base. Tailwind UI is the cleanest reference — it's organised exactly this way.

**App shells** (the frame content lives in) — Tailwind ships ~23 variants:
- Top / stacked nav · Side nav · Multi-column · Split · Focused / full-page · **Doormat** (mega-footer) nav · Nav rail.

**Page templates / scaffolds:**
- Dashboard · List / index · Detail · Create / edit form · Settings · Multi-step wizard · Empty · Error (404 / 500) · Auth (login / register / OTP) · Report · Confirmation.

**Section lock-ups** (configured arrangements):
- Page headers (× tabs / actions / breadcrumb / avatar / meta) · Section headings · Card headers · Hero · Stats band · Filter / toolbar bar · Footer / doormat · CTA · Feature grid.

**Nav variants** (your examples): top · side · doormat · rail · breadcrumb · tab-bar · mega-menu · command palette.

**Per-component variants:** every base × emphasis / size / state / density — the Untitled-UI multiplier (Header alone → page / section / card / detail / with-tabs / with-actions).

**The maths:** ~75–85 bases × variants + ~40–50 shells / templates / lock-ups → a **200–300+ item catalog**, in line with the commercial kits. And this is a **program**, not a side-quest: the automation can only compose what exists, so the inventory *is* the prerequisite for the machine.

## For the team proposal

1. **Fund an extensive component build**, P1 gaps first — this is what makes "bang-on standard" output the default and cuts the "needs a tidy" / invented-content failure mode at the source.
2. Frame it as **two modes**: comprehensive library → reliable standard interfaces; ideation mode → tuned creativity for workshops.
3. Sell the **variance dividend**: a bigger kit doesn't just cover more — it makes generated journeys legitimately varied, because there's more valid choice on the same curbs.

---

*Related: `_COMPONENT-GAPS.md` (specific gaps already logged) · `_FIXED-FLEX-CHARTER.md` (standard vs ideation = the register dial) · `_RUNBOOK-gated-component.md` (the build pipeline each new component runs).*

Sources: [Ant Design components](https://ant.design/components/overview/) · [Carbon Design System](https://carbondesignsystem.com/components/overview/components/) · [Material Design 3 components](https://m3.material.io/components) · [Untitled UI Figma kit](https://www.untitledui.com/figma)
