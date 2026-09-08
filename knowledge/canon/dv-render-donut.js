/* dv-render-donut — the Chart-donut / Chart-pie's part-to-whole ring TYPE PARTIAL for the dv-render engine.
   ⛔ NOT BUILT — this is a VALID, REGISTERED STUB placed by the #259 engine-core lane so the
   parallel type lanes have a file to fill and a registry entry to consume WITHOUT touching
   knowledge/canon/dv-render.js or knowledge/component-types.json. It registers its type name(s)
   and throws a NAMED error if anything asks it to draw. A missing registration and a stub
   registration fail differently on purpose: "no type partial registered for X" means nobody has
   claimed the name, "the donut type partial is NOT BUILT yet" means someone has and has not
   finished. Fail loud, and say which.

   WHAT THE LANE THAT FILLS THIS OWES: arc paths with data-a1/data-a2 sweep hooks (dv-donut-sweep's contract), <=6 slices (dv-pie-009), a >=2px surface-coloured separating stroke (dv-004), centre figure.

   THE SEAM IT MUST HONOUR (unchanged from dv-render-bar, the reference implementation):
     · take EVERYTHING off `ctx` — ctx.PL/PR/PT/PB/VW/VH, ctx.plotW/plotH/y0, ctx.min/max/ticks,
       ctx.vy(v) / ctx.vf(v) / ctx.fx(px), ctx.fill(i), ctx.fmt(v), ctx.esc/n1/f4, ctx.GAP, ctx.HIT;
     · push STRINGS with ctx.push(); the core joins, assigns innerHTML, writes the table spine and
       dispatches the ONE resize that re-fits (ADR-0015 §4 — never add a listener);
     · every mark carries its x as a FRACTION (data-fx / data-fw / data-fxs), never a baked pixel;
     · every mark carries data-tip + tabindex="0" + role="img" + aria-label;
     · colour is a var() token only (dv-017 / DEF-004): ctx.fill(i) or the s184-D3 status vocabulary;
     · set `fn.axis = "x"` if the value axis runs across, and `fn.domain = fn(spec)` if the domain
       is not simply the min/max of the values (see dv-render-bar's stacked). */
(function () {
  'use strict';
  if (!window.dvRender) { return; }
  function donut() {
    throw new Error('dv-render-donut: the donut type partial is NOT BUILT yet — ' +
      'fill knowledge/canon/dv-render-donut.js (registered stub, #259 engine-core lane)');
  }
  window.dvRender.types['donut'] = donut;
  window.dvRender.types['pie'] = donut;
}());
