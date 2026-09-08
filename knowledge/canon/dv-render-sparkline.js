/* dv-render-sparkline — the Chart-sparkline's in-line trend atom TYPE PARTIAL for the dv-render engine.
   ⛔ NOT BUILT — this is a VALID, REGISTERED STUB placed by the #259 engine-core lane so the
   parallel type lanes have a file to fill and a registry entry to consume WITHOUT touching
   knowledge/canon/dv-render.js or knowledge/component-types.json. It registers its type name(s)
   and throws a NAMED error if anything asks it to draw. A missing registration and a stub
   registration fail differently on purpose: "no type partial registered for X" means nobody has
   claimed the name, "the sparkline type partial is NOT BUILT yet" means someone has and has not
   finished. Fail loud, and say which.

   WHAT THE LANE THAT FILLS THIS OWES: one polyline data-fxs + data-ys, no axis furniture at all (the atom is axis-free, s182-D2), exactly ONE data-tip mark.

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
  function sparkline() {
    throw new Error('dv-render-sparkline: the sparkline type partial is NOT BUILT yet — ' +
      'fill knowledge/canon/dv-render-sparkline.js (registered stub, #259 engine-core lane)');
  }
  sparkline.axis = 'y';
  window.dvRender.types['sparkline'] = sparkline;
  window.dvRender.types['spark'] = sparkline;
}());
