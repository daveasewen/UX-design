# M1 — How Apollo should meet other libraries and frameworks

Lane M1, Apollo session #311, desk research dated 2026-10-01. Fable, cloud workspace only. Every claim below carries a source number; the list with dates is at the end. Where a page could not be fetched or said nothing on the point, that is stated rather than filled in.

## Summary

Dave's instinct is right about the role of the snippets and wrong about the reason. The reviewed HTML snippets should not be the compiler's input, but not because they are "for the user to view". They should not be the source because HTML cannot carry what a framework target needs: state, behaviour, event contracts, slot semantics, and the ARIA promises that go with a role. Those things already live in Apollo's metas (params, variants, slots, roles, Aria contract, token references). The metas are the spec. The snippets are the rendered-output oracle, exactly the role GOV.UK Frontend gives its per-component `fixtures.json` (options in, expected HTML out) for anyone porting to another templating language [S14]. Keep the snippets, change their job: from source to fixture.

On the three placements. No mature multi-framework system does placement B (take compiled HTML and transform it into React or Angular code). Nobody found in this research does it, and Bootstrap's own documentation explains why: markup-attached behaviour and a virtual-DOM framework "may attempt to mutate the same DOM element" [S16]. Placement C (map Apollo onto MUI, Angular Material or similar) is the drift trap; Google could not keep its own two Material implementations in step and put Material Web Components into maintenance mode in June 2024 while Angular Material carried on [S9, S10]. Placement A (a neutral spec at source with per-target emitters) is what the two systems that genuinely compile once to many do: Deutsche Bahn's DB UX via Mitosis [S12], and Chakra's Zag/Ark via state machines [S7, S8]. The dominant pattern among the big corporates is a hybrid of A and the web platform: web components as the universal runtime, thin generated wrappers for React, Angular and Vue, and a shared tokens-plus-CSS layer underneath (Carbon [S4, S5], Adobe Spectrum [S2, S3], Fluent [S11], Nord [S13], Shoelace/Web Awesome [S17]). React 19, Angular, Vue, Svelte, Solid and Preact all now pass 100% of Custom Elements Everywhere [S18, S19], which removes the historic objection to that hybrid.

The token layer is the solved part. The W3C Design Tokens Community Group shipped its first stable Format Module and a stable Resolver Module on 28 October 2025 [S20, S21, S22]; Style Dictionary has read DTCG `$value`/`$type` since v4.0.0 on 28 June 2024 [S23]; Tokens Studio reads and writes it with listed gaps [S24]. Apollo's token JSON should conform to DTCG 2025.10 and remain the single source for every target. That is the one place where "do it at source" is uncontroversial.

Recommendation in one sentence: placement A at the metas, with the existing HTML+CSS emitter as target one, a Lit web-component emitter as target two, generated React and Angular wrappers as target three, and DTCG tokens under all of it; never emit from the snippets, and do not build an adapter onto a third-party library.

## 1. How mature multi-framework systems keep one source of truth

### IBM Carbon — two flagships, one styles layer, parity by policy

Carbon ships `@carbon/react` and `@carbon/web-components` as what its own contributor guidance calls "a dual-flagship model", with "Visual and functional parity are paramount, though the implementations themselves are allowed to diverge as necessary", and framework conventions taking priority over shared logic when that helps [S4]. The two flagships sit on a shared `@carbon/styles` Sass package plus the foundational packages (colors, grid, icons, themes, typography), which are "intentionally layered on top of each other" [S4]. In September 2024 Carbon moved the web-components package into the main monorepo specifically "to synchronize the two libraries more closely" [S5]. The vanilla HTML+JS library was deprecated in May 2023 and reached end of life with v10 in September 2024; from v11 Carbon "only provides styles for Vanilla JS" [S6, S26].

What this tells Apollo: the largest corporate design system on the web does not compile React from web components or vice versa. It writes both by hand, shares the CSS and tokens underneath, and holds parity by review and policy. The cost is two implementation teams; the drift risk is explicitly accepted ("allowed to diverge"). The thing it did stop maintaining was the plain-HTML component library, which is the closest analogue to Apollo's snippets being the shipped artefact.

### Adobe Spectrum — one CSS source, two consumers, one behaviour library

Spectrum CSS is "the standard CSS implementation of the Spectrum design language", depends on `@spectrum-css/tokens` ("serves up the Spectrum design tokens as CSS custom properties"), and "The Spectrum Web Components library directly imports Spectrum CSS and optimizes it for use with web components" [S2]. Spectrum Web Components (Lit) migrated to Spectrum 2 by switching the `sp-theme` system variable to `"spectrum-two"` and importing new theme modules, which is a token swap rather than a component rewrite [S3]. React Spectrum takes a different route: a three-layer stack of React Stately (state, "no assumptions about the platform"), React Aria (behaviour and accessibility "according to the WAI-ARIA Authoring Practices") and React Spectrum (Adobe styling), on the stated premise that "Most components typically found in a design system... usually have very similar behavior and logic. The main difference between design systems is styling" [S1]. The React stack does not share component code with the web components; it shares the design language and tokens.

What this tells Apollo: Adobe's answer to "one source" is tokens plus CSS as the shared substrate, and separate behaviour stacks per platform. The behaviour layer (react-aria) is the asset other companies reuse, and it is written against the ARIA Authoring Practices, which is the same contract Apollo's metas already name.

### Salesforce Lightning — blueprints as reference, base components as the product

SLDS defines blueprints as "framework-agnostic HTML or CSS that represents the visual design part of a component" and Lightning Base Components as "the set of programmatic components built according to the SLDS component blueprint library" [S27]. The developer guide is blunt about the cost of building from the blueprint: "When you create a component from a blueprint, the blueprint markup becomes part of your component's code. If SLDS updates the related blueprint, your component code isn't updated automatically", and "Before you create a component from a blueprint, make sure that there's no other way to meet your use case" [S28]. SLDS 2 moved the visual contract to styling hooks (CSS custom properties) that cross the LWC Shadow DOM boundary [S27].

What this tells Apollo: Salesforce ran the "reference HTML is the spec" pattern at scale for a decade and its own conclusion is that copying reference HTML into a target is a one-way door. The reference is a reference; the shippable unit is a component with behaviour; the thing that crosses the boundary between them is tokens expressed as custom properties.

### Material — the cautionary case for parallel implementations

Material Web Components entered maintenance mode on 10 June 2024: "New features and components are no longer planned. GitHub PRs will not be accepted by default", because "Material Design is focusing on support for Google's large-scale internal Wiz framework, and has reassigned the engineers" [S9]. Angular Material is a separate team and carried on, implementing Material 3 as "design tokens (implemented as CSS custom properties)" via `define-theme`, with mixins "guaranteed to only output CSS custom properties with no additional selector specificity" [S10]. MUI is a third, independent implementation; its January 2026 roadmap centres on Base UI as the headless foundation "for teams building their custom design systems" and does not mention web components or multi-framework output [S29].

What this tells Apollo: three Material implementations, three codebases, one shared spec document, no shared code, and the one Google did not need internally was dropped. If Google cannot afford parallel hand-written implementations, Apollo cannot. Whatever Apollo emits for a second framework must be generated from the same source as the first, or it will rot.

### Microsoft Fluent, Nordhealth, Shoelace — web components as the universal layer

Fluent UI Web Components are "built on the W3C Web Component standards, and do not create their own separate component model", and can "Integrate with many popular frameworks like .NET, Blazor, Vue, React, etc." [S11]. Nordhealth's Nord (Lit) themes across Shadow DOM by making CSS custom properties the bridge: "This ability to inherit Custom Properties, with the use of the var() function, is how we pierce through our Web Components' Shadow DOM", with global tokens on the root and per-component contextual properties as "a custom CSS API" [S13]. Shoelace (now Web Awesome) ships React wrappers because, as Lit's own documentation puts it, React "treats all JSX properties as HTML attributes" and "assumes all DOM events have corresponding event properties", so `@lit/react` `createComponent()` exists for "vendors of components" to publish "idiomatic versions" [S17]. Stencil generalises this with React, Angular and Vue output targets configured in `stencil.config.ts`, so one component source yields framework packages [S15]. The known limits as of late 2024 were SSR ("SSR is still not suitable with web components") and the fact that "custom elements are not quite the same as components" [S25].

### DB UX (Deutsche Bahn) via Mitosis — the purest placement A found

DB UX core-web writes components once in Mitosis and compiles to `@db-ux/react-core-components`, `@db-ux/ngx-core-components`, `@db-ux/v-core-components` and `@db-ux/wc-core-components` (Stencil), on top of `@db-ux/core-foundations` (tokens, CSS/SCSS/Tailwind) and `@db-ux/core-components` (framework-agnostic CSS) [S12]. Its stated principle is that the system "leverages semantic HTML, ARIA roles, states and properties to apply our styles wherever possible, thus enforcing correct, accessible markup" [S12]. Mitosis itself compiles "to React, Vue, Qwik, Solid, Angular, Svelte, and more" and cites DB UX as the design-system example; its README says it is "actively looking for folks interested in becoming contributors", which is a maintenance signal worth reading twice [S30].

What this tells Apollo: compile-once-to-many is real and in production at a national rail operator, but it still ships a CSS-only package alongside, and its compiler is a Builder.io side project seeking maintainers. The emitter is the part you own forever.

### Zag.js / Ark UI — the behaviour layer as a framework-neutral machine

Zag is "State machines for accessible, interactive and performant UI components", with "Built-in adapters that connects machine output to DOM semantics in a WAI-ARIA compliant way", for React, Vue, Solid and Svelte [S7]. Ark UI is the headless component library built on it, for React, Solid and Vue, with Svelte planned [S8]. This is the only approach found that makes behaviour, not CSS, the shared source: the machine is plain JavaScript, the framework adapter is thin, the styling is yours.

### Figma Code Connect — a mapping layer, not a source

Code Connect "connect[s] components in your repositories directly to components in your design files", supports "one-to-many connections, allowing you to map a single design component to multiple code components across different languages or frameworks", and needs an Organization or Enterprise plan [S31]. It has an HTML/web-components target that uses Figma property types to render attributes correctly ("`disabled=${disabled}` will either render `disabled` or nothing, as it is a boolean") [S32]. It is relevant to Apollo as a model of a mapping file: a small typed document that says how design props become code props per target, which is exactly what a per-target emitter needs from a meta.

## 2. Standards Apollo can lean on in 2026

Design tokens. The DTCG Format Module 2025.10 is a Final Community Group Report dated 28 October 2025, "the first stable version", backed by Style Dictionary, Tokens Studio and Terrazzo and adopted by Figma, Sketch, Framer and Penpot [S20]. It defines `$type` values for color, dimension, fontFamily, fontWeight, duration, cubicBezier, number and the composites strokeStyle, border, transition, shadow, gradient and typography; aliases by `{group.token}` or JSON Pointer `$ref`; `$extensions` that tools "MUST preserve"; and `$deprecated` [S21]. Font style, percentage/ratio and file types are explicitly deferred [S21]. The Resolver Module, same date, adds sets and modifiers for "Theming, such as light mode, dark mode, and high contrast color modes; Sizing...; Accessibility mode" and states "This specification is considered stable" [S22]. Style Dictionary v4.0.0 (28 June 2024) added "support for $value, $type and $description" with a `usesDtcg` option [S23]. Tokens Studio converts between legacy and DTCG and lists open gaps (composition tokens, boxShadow offsetX/offsetY naming, group descriptions) [S24]. Apollo's tokens JSON should be checked against 2025.10 and its theme machinery against the Resolver Module's sets/modifiers; that is cheap and it buys every downstream tool.

Component anatomy. Open UI's research pages catalogue anatomy, states and behaviours across roughly fifteen design systems per component (Atlaskit, Ant, Carbon, FAST, Lightning, Material, Shoelace, Vaadin and others) and establish shared part names, for example "Tab Set, Tab Bar, Tab List, Tab Label, and Tab Panel" [S33]. There is no normative component-spec standard; Open UI is research towards native HTML. It is useful to Apollo as a vocabulary check for slot and part names in the metas.

Accessibility. The ARIA Authoring Practices Guide lists 31 patterns [S34] and its own front matter is the caveat: "No ARIA is better than Bad ARIA", "A role is a promise", "ARIA roles do not cause browsers to provide keyboard behaviors or styling", and "Testing assistive technology interoperability is essential before using code from this guide in production" [S35]. This is the single strongest argument against treating HTML as the full spec: the role in the markup is a promise the behaviour layer must keep, and HTML alone cannot keep it.

Custom elements interop. React 19 (5 December 2024) "adds full support for custom elements and passes all tests on Custom Elements Everywhere"; on the server, primitive props become attributes and non-primitives are omitted; on the client, props matching an instance property are set as properties, otherwise attributes [S18]. Custom Elements Everywhere currently scores React ^19, Angular 16.2.10, Vue ^3.2.38, Svelte 4.2.19, Solid 1.6.8 and Preact ^10 all at 100% on attributes/properties, events and Shadow DOM handling [S19]. Remaining friction is SSR of Shadow DOM and form participation, which the 2024 commentary still flagged [S25]; this research did not find a 2026 source that declares those closed, so treat them as open.

## 3. The three placements, with hybrids

### A. Neutral component spec at source, per-target emitters

Who does it: DB UX via Mitosis [S12, S30]; Stencil with output targets [S15]; Zag/Ark for behaviour [S7, S8]; in spirit, GOV.UK Frontend, whose Nunjucks macros were chosen in 2016 because they "support conditional logic and parameters with defaults", enabling conversion to other templating languages [S36].

How it works: the source is a constrained description (Mitosis is a JSX subset; Zag is a statechart; a Stencil component is a decorated class), and each target is a generator the team maintains. Theming rides on tokens as CSS custom properties, which every target can consume unchanged.

Where it fails: the emitter is the long-term cost. Mitosis is seeking maintainers [S30]. Every target adds a test matrix. Framework idiom suffers; Carbon's "framework conventions take priority over shared logic" is a direct criticism of generated idiom [S4]. Accessibility is as good as the source's behaviour model; if the source is only markup, A degrades into B.

Fit for Apollo: strong, because the neutral spec already exists. The metas carry params/variants/slots, roles, an Aria contract and token references; that is more than Mitosis has at source. The missing piece is a behaviour model (states and transitions) per interactive component, which Zag demonstrates can be plain JSON-like data rather than framework code.

### B. Transform layer converting compiled HTML into framework code

Who does it: nobody found at design-system scale. The nearest relatives are Code Connect's HTML templates (which map props into markup for display in Figma, not for shipping) [S32] and Bootstrap's data-attribute API, which attaches behaviour to markup and which Bootstrap itself says "is not fully compatible with JavaScript frameworks like React, Vue, and Angular which assume full knowledge of the DOM", recommending React Bootstrap, BootstrapVueNext and ng-bootstrap instead — that is, hand-written ports [S16].

Where it fails: HTML is the output of a component, not its definition. A transform from HTML has to infer which attributes are props, which children are slots, which classes are state, and which event fires when; none of that is in the string. Salesforce's warning about blueprint code not updating when the blueprint changes is the same failure from the other side [S28]. ARIA roles present in the HTML are promises without the keyboard behaviour to back them [S35].

Fit for Apollo: this is the placement Dave's instinct rules out, and the research backs the instinct. It is not merely weak; it is unoccupied.

### C. Adapter onto an existing third-party library

Who does it: in practice, every in-house "design system" that is a MUI or Angular Material theme. MUI positions Base UI for "teams building their custom design systems" [S29]; Angular Material exposes system tokens as custom properties for the same reason [S10].

Where it fails: Apollo's semantics would be bounded by the host library's component set, anatomy and ARIA choices; theming is bounded by what the host exposes as tokens; drift arrives on the host's release cadence, not Apollo's. The Material Web maintenance-mode decision shows that even first-party parallel implementations lose funding [S9]; a third-party adapter inherits that risk twice. It also makes Apollo's gates meaningless at the boundary, because the host owns the DOM.

Fit for Apollo: fine as a consumer-side convenience (publish a MUI theme generated from Apollo tokens), unsound as the integration architecture.

### Hybrid: web components as the universal runtime, thin wrappers, shared tokens

Who does it: Carbon [S4], Spectrum Web Components [S2, S3], Fluent [S11], Nord [S13], Shoelace/Web Awesome [S17, S25], DB UX's wc package [S12]. Wrappers are generated (Stencil output targets [S15], `@lit/react` [S17]). Theming is CSS custom properties across Shadow DOM [S13, S27].

Costs and risks: SSR and form participation still carry caveats [S25]; wrapper generation is a maintained dependency; design-system teams report that "custom elements are not quite the same as components" [S25]. Against that, framework support is now universal by measurement [S19].

Fit for Apollo: this is the realistic shape of placement A's second emitter. Emitting Lit components from the metas gives one runtime for every host; generating React and Angular wrappers from the same metas gives idiomatic entry points; the existing HTML+CSS emitter stays as the zero-JavaScript target and as the fixture oracle.

## 4. Is "the reference HTML is the spec" a respected pattern, and where does it break

It is respected, and it is older than any of the framework debates. GOV.UK Frontend was designed in 2016 as vanilla HTML/CSS with Sass "following ITCSS and BEM" because research found "a wide range of technologies are used to deliver frontend across government services, with no one technology dominating" [S36]. Today its per-component `fixtures.json` holds `options` and the expected `html`, and the instruction to porters is "For each example, pass options into your own macro and check the generated HTML matches html", allowing tests to "ignore known differences. For example your framework may add extra whitespace or attributes" [S14]. The GOV.UK team lists community ports (Vue, ASP.NET Core, Python, Rails) while stating "The GOV.UK Design System team is not responsible for these resources and tools and we cannot support you with using them" [S37]. The React port tracks the official components but "modif[ies] markup and styling when needed for React compatibility" and looks inactive [S38]. SLDS blueprints are the same pattern with the same disclaimer [S27, S28]. Bootstrap is the same pattern with behaviour bolted onto markup by data attributes, and it names the breakage itself [S16].

Where it breaks, in order of severity for Apollo:

Behaviour and state. HTML fixes one state of a component. A tabs component has a selected tab, a focused tab, a disabled tab, keyboard arrow traversal and roving tabindex; the fixture shows one frame of that. APG says the role is a promise the markup cannot keep on its own [S35].

Framework DOM ownership. Any behaviour attached to the reference markup fights a virtual-DOM framework for the same nodes [S16]. The fix every system reached is to ship a component the framework owns (a custom element or a native component), not markup plus a script.

Update propagation. Copied reference markup "isn't updated automatically" when the reference changes [S28]. Fixtures-as-tests solve this for porters who run the tests; they do nothing for teams who copied the HTML once.

Support boundary. Every system that publishes reference HTML disclaims the ports built from it [S37, S27]. If Apollo's only framework story is "here is the HTML, port it", Apollo inherits that disclaimer.

Where it holds: as the acceptance oracle. A rendered-output fixture is framework-neutral, diffable, reviewable by eye, and it is the one artefact a designer can rule on. GOV.UK's choice to publish fixtures rather than framework packages is a deliberate scoping decision for a small central team, and it has lasted ten years.

## Challenging Dave's instinct, and its opposite

Against the instinct ("we shouldn't rely on the snippets"). The snippets are already doing a job the best-run public design system in Britain does on purpose: they are the expected-HTML fixtures. Throwing them out of the pipeline would remove the only framework-neutral acceptance test Apollo has and the only artefact Dave rules on by eye. Code Connect's HTML target shows that a markup template with typed holes is a legitimate per-target mapping [S32]. The snippets are also what the generators currently read to produce the shared stylesheet; moving that dependency is a real migration with a gate behind it. So: do not rely on the snippets as source, but do rely on them as oracle, and say which is which.

Against the opposite ("the snippets are the spec, compile from them"). HTML has no state, no transitions, no event contract, no slot typing, and ARIA roles in it are promises without keyboard behaviour [S35]. Compiling frameworks from it is placement B, which no mature system does, and whose nearest relative (Bootstrap's markup-attached JS) warns against itself in React, Vue and Angular [S16]. Salesforce's "copy the blueprint and it will not update" is the lived result [S28]. The metas already hold what the compiler needs; the snippet holds what the eye needs. Collapsing them loses one or the other.

Against the hybrid being free. Web components carry SSR and form caveats that this research could not confirm closed in 2026 [S25]; wrapper generators are a dependency; Carbon's own policy admits implementations "are allowed to diverge" [S4]. And Mitosis, the only general compile-to-many tool in production use by a design system of record, is asking for maintainers [S30]. Whatever emitter Apollo adopts, Apollo owns.

## What this means for Apollo, concretely

The metas become the declared component spec and gain a behaviour section (states, transitions, keyboard map) where a component is interactive; Zag's machines are the model to copy, APG's 31 patterns are the checklist [S7, S34]. The tokens JSON is checked against DTCG 2025.10 and the Resolver Module's sets/modifiers [S21, S22]. The snippets are reclassified as fixtures: each carries the meta options that produced it and is diffed against emitter output, GOV.UK style [S14]. The HTML+CSS emitter stays as target one. A Lit emitter becomes target two, themed by custom properties across Shadow DOM as Nord and SLDS 2 do [S13, S27]. React and Angular wrappers are generated as target three, by `@lit/react` or Stencil-style output targets [S17, S15], relying on the 100% interop scores [S19]. A MUI or Angular Material theme generated from the tokens is offered as a consumer convenience, not as the integration. Nothing is emitted from a snippet.

## Sources

- [S1] Adobe, "Introducing React Spectrum", 15 July 2020. https://react-aria.adobe.com/blog/introducing-react-spectrum
- [S2] adobe/spectrum-css README, fetched 2026-10-01. https://github.com/adobe/spectrum-css
- [S3] Spectrum Web Components, "Migrating to Spectrum 2", fetched 2026-10-01. https://opensource.adobe.com/spectrum-web-components/migrating-to-spectrum2
- [S4] carbon-design-system/carbon AGENTS.md, fetched 2026-10-01. https://raw.githubusercontent.com/carbon-design-system/carbon/main/AGENTS.md
- [S5] Anna Wen, "Carbon Design System's commitment to Web Components", Medium, September 2024 (via conffab mirror). https://conffab.com/?p=7211
- [S6] Carbon, "Moving forward: On deprecating carbon-components and carbon-components-react", 16 May 2023. https://medium.com/carbondesign/moving-forward-on-deprecating-carbon-components-and-carbon-components-react-4f2f0c3d8448
- [S7] Zag.js homepage, fetched 2026-10-01. https://www.zagjs.com
- [S8] Ark UI, "Welcome to Ark UI", fetched 2026-10-01. https://ark-ui.com/docs/vue/overview/introduction
- [S9] material-components/material-web discussion #5642, "MWC is in maintenance mode", 10 June 2024. https://github.com/material-components/material-web/discussions/5642
- [S10] Angular Blog, "Material 3 Experimental Support in Angular 17.2", 15 February 2024. https://blog.angular.dev/material-3-experimental-support-in-angular-17-2-8e681dde650e
- [S11] Microsoft Learn, "Fluent UI Web Components", fetched 2026-10-01. https://learn.microsoft.com/en-us/fluent-ui/web-components/
- [S12] db-ux-design-system/core-web README, fetched 2026-10-01. https://github.com/db-ux-design-system/core-web
- [S13] web.dev, "How Nordhealth uses Custom Properties in Web Components", 17 August 2022. https://web.dev/articles/custom-properties-web-components
- [S14] GOV.UK Frontend, "Testing your HTML", fetched 2026-10-01. https://frontend.design-system.service.gov.uk/testing-your-html
- [S15] ionic-team/stencil-ds-output-targets README, fetched 2026-10-01. https://github.com/ionic-team/stencil-ds-output-targets
- [S16] Bootstrap 5.3 docs, "JavaScript", fetched 2026-10-01. https://getbootstrap.com/docs/5.3/getting-started/javascript/
- [S17] Lit docs, "React" (@lit/react createComponent), fetched 2026-10-01. https://lit.dev/docs/frameworks/react/
- [S18] React, "React 19" release post, 5 December 2024. https://react.dev/blog/2024/12/05/react-19
- [S19] Custom Elements Everywhere, fetched 2026-10-01. https://custom-elements-everywhere.com/
- [S20] W3C DTCG, "Design Tokens specification reaches first stable version", 28 October 2025. https://www.w3.org/community/design-tokens/2025/10/28/design-tokens-specification-reaches-first-stable-version/
- [S21] W3C DTCG, "Design Tokens Format Module 2025.10", Final CG Report, 28 October 2025. https://w3c.github.io/cg-reports/design-tokens/CG-FINAL-format-20251028/
- [S22] W3C DTCG, "Design Tokens Resolver Module 2025.10", Final CG Report, 28 October 2025. https://w3c.github.io/cg-reports/design-tokens/CG-FINAL-resolver-20251028/
- [S23] style-dictionary v4.0.0 release, 28 June 2024. https://github.com/style-dictionary/style-dictionary/releases/tag/v4.0.0
- [S24] Tokens Studio docs, "Token format", fetched 2026-10-01. https://docs.tokens.studio/manage-settings/token-format
- [S25] The New Stack, "The Pros and Cons of Web Components via Lit and Shoelace", 29 September 2024. https://thenewstack.io/the-pros-and-cons-of-web-components-via-lit-and-shoelace/
- [S26] Carbon, "Vanilla" framework page, fetched 2026-10-01. https://carbondesignsystem.com/developing/frameworks/vanilla
- [S27] Salesforce Trailhead, "Explore Salesforce Lightning Design System 2", fetched 2026-10-01. https://trailhead.salesforce.com/content/learn/modules/salesforce-lightning-design-system-2-for-developers/explore-salesforce-lightning-design-system-2
- [S28] Salesforce LWC guide, "Create a Component from an SLDS Blueprint", fetched 2026-10-01. https://developer.salesforce.com/docs/platform/lwc/guide/create-components-css-slds-blueprint.html
- [S29] MUI, "2026 and beyond", 1 January 2026. https://mui.com/blog/2026-and-beyond/
- [S30] BuilderIO/mitosis README, fetched 2026-10-01. https://github.com/BuilderIO/mitosis
- [S31] Figma Help, "Code Connect", fetched 2026-10-01. https://help.figma.com/hc/en-us/articles/23920389749655-Code-Connect
- [S32] Figma Developers, "Code Connect for HTML", fetched 2026-10-01. https://developers.figma.com/docs/code-connect/html/
- [S33] Open UI, "Tabs research: parts", fetched 2026-10-01. https://open-ui.org/components/tabs.research.parts
- [S34] W3C WAI, "ARIA Authoring Practices Guide: Patterns", fetched 2026-10-01. https://www.w3.org/WAI/ARIA/apg/patterns/
- [S35] W3C WAI, APG "Read Me First", fetched 2026-10-01. https://www.w3.org/WAI/ARIA/apg/practices/read-me-first/
- [S36] GDS Design Notes, "Introducing GOV.UK Frontend alpha", 14 October 2016. https://designnotes.blog.gov.uk/2016/10/14/introducing-gov-uk-frontend-alpha
- [S37] GOV.UK Design System, "Resources and tools" (community), fetched 2026-10-01. https://design-system.service.gov.uk/community/resources-and-tools/
- [S38] govuk-react README (marksy fork of govuk-react/govuk-react), fetched 2026-10-01. https://github.com/marksy/govuk-react

Not fetched or silent on the point: react-spectrum.adobe.com/architecture.html returned marketing copy only; the Spectrum Web Components GitHub landing page returned navigation only (Lit basis taken from S3/S25 context, not confirmed on that page); nordhealth.design pages returned empty; no 2026 source was found confirming web-component SSR and form-participation caveats as closed.
