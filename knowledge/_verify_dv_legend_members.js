/* _verify_dv_legend_members — DV-D11 conformance proof for the WAVE MEMBERS.
   Sibling of _verify_dv_legend.js, which proves the donut EXEMPLAR (incl. DV-D12 sweep and the
   DV-D13 centre figure — both donut-only). This one drives the REAL canon/dv-legend.js against
   each migrated member snippet in jsdom and asserts the invariants that must hold for EVERY
   member, plus the risks each member newly introduces.

   Why a second file rather than a parameter on the first: the exemplar's checks are numeric and
   member-specific (950/41%, 147° sweep geometry). Conflating them would make the member suite
   assert things that are true of nothing but the donut.

   Run: node knowledge/_verify_dv_legend_members.js        (from the repo root)
   Requires jsdom on NODE_PATH — verification tooling only, never a build dependency. */
const fs = require('fs');
const path = require('path');
const { JSDOM } = require(process.env.JSDOM || '/tmp/node_modules/jsdom');

const ROOT = path.resolve(__dirname, '..');
const SRC = path.join(ROOT, 'knowledge/canon/dv-legend.js');

let pass = 0, fail = 0;
const ok = (name, cond, detail) => {
  if (cond) { pass++; console.log(`  ✓ ${name}`); }
  else { fail++; console.log(`  ✗ ${name}${detail ? ' — ' + detail : ''}`); }
};

/* MEMBERS — one entry per migrated snippet. `legends` lists every legend on the page, because
   carrying MORE THAN ONE is the thing Chart-bar introduces that the donut never tested. */
const MEMBERS = [
  {
    file: 'knowledge/snippets/Chart-bar.reference.html',
    name: 'Chart-bar',
    legends: [
      { id: 'cb4-legend', live: 'cb4-live', ids: ['1', '2', '3'], figure: 'grouped column' },
      { id: 'cb5-legend', live: 'cb5-live', ids: ['1', '2', '3'], figure: 'stacked column' }
    ]
  },
  {
    file: 'knowledge/snippets/Chart-combo.reference.html',
    name: 'Chart-combo',
    legends: [
      /* TWO series, TWO mark types (bar + line) on ONE plot — the first member where the swatch
         SHAPE carries meaning, so the row set is small but the mark coupling is the risk. */
      { id: 'cc1-legend', live: 'cc1-live', ids: ['1', '2'], figure: 'bar + line combo' }
    ]
  },
  {
    file: 'knowledge/snippets/Chart-line.reference.html',
    name: 'Chart-line',
    legends: [
      /* The member that EARNS the swatch shape set — its markers are circle/square/diamond. */
      { id: 'cl2-legend', live: 'cl2-live', ids: ['1', '2', '3'], figure: 'multi-line' }
    ]
  }
];

/* runScripts:'outside-only' gives window.eval a real script context WITHOUT executing the
   snippet's own injected blocks — so this exercises dv-legend.js in isolation, not the
   transitional dv-behaviour legend it must coexist with. */
function load(file) {
  const dom = new JSDOM(fs.readFileSync(path.join(ROOT, file), 'utf8'),
    { pretendToBeVisual: true, runScripts: 'outside-only' });
  dom.window.requestAnimationFrame = (fn) => 1;
  dom.window.cancelAnimationFrame = () => {};
  dom.window.eval(fs.readFileSync(SRC, 'utf8'));
  return dom.window;
}

MEMBERS.forEach((member) => {
  const window = load(member.file);
  const doc = window.document;
  const click = (el) => el.dispatchEvent(new window.MouseEvent('click', { bubbles: true }));
  const over = (el) => el.dispatchEvent(new window.MouseEvent('pointerover', { bubbles: true }));

  /* ---- per-legend conformance ---- */
  member.legends.forEach((L) => {
    const leg = doc.getElementById(L.id);
    console.log(`\n${member.name} · #${L.id} (${L.figure}) — DV-D11 conformance`);
    if (!leg) { ok(`legend #${L.id} exists`, false); return; }

    const fig = leg.closest('figure');
    const row = (id) => leg.querySelector(`.dv-legrow[data-series="${id}"]`);
    const sw = (id) => row(id).querySelector('.dv-leg-sw');
    const item = (id) => row(id).querySelector('.dv-leg-item');
    const marks = (id) => fig.querySelectorAll(`[data-series-group="${id}"]`);
    const ghosted = (id) => [].every.call(marks(id), (e) => e.classList.contains('is-ghost'));
    const anyGhost = (id) => [].some.call(marks(id), (e) => e.classList.contains('is-ghost'));
    const faded = (id) => [].some.call(marks(id), (e) => e.classList.contains('is-faded'));
    const peeked = (id) => [].some.call(marks(id), (e) => e.classList.contains('is-peek'));
    const reset = leg.querySelector('.dv-leg-reset');
    const live = doc.getElementById(L.live);
    /* ⚠ GENERALISED 2026-07-27 (lane ②). This suite was written against Chart-bar and baked TWO
       of its facts in: exactly three series (`const [a,b,c] = L.ids`) and the literal series name
       "Current" in check 13. Chart-combo has TWO series called something else, so both assumptions
       crashed or lied. The invariants are per-N, not per-bar: `a` = the first row, `last` = the
       floor, `others` = everyone else. Names come off the MARKUP, never from a literal — a suite
       that hardcodes one member's data cannot verify the next one. Bar's 23 per-legend checks are
       unchanged in number, wording and meaning. */
    const a = L.ids[0];
    const b = L.ids[1];
    const last = L.ids[L.ids.length - 1];
    const others = (x) => L.ids.filter((id) => id !== x);
    const nameOf = (id) => item(id).querySelector('.dv-leg-name').textContent.trim();
    const announces = (id) => live.textContent.indexOf(nameOf(id)) !== -1;

    /* STRUCTURE — the dual-gesture contract. The swatch must sit OUTSIDE the label button:
       nesting a checkbox inside a button is the bug the markup shape exists to prevent. */
    ok('1  every row carries a swatch and an isolate label',
      L.ids.every((id) => sw(id) && item(id)));
    ok('2  the swatch is NOT nested inside the isolate button (dual gesture)',
      L.ids.every((id) => !item(id).contains(sw(id))));
    ok('3  swatch is an ARIA checkbox, label is a toggle button',
      L.ids.every((id) => sw(id).getAttribute('role') === 'checkbox'
        && sw(id).getAttribute('tabindex') === '0'
        && item(id).tagName === 'BUTTON'));
    ok('4  the live region exists and is polite',
      !!live && live.getAttribute('aria-live') === 'polite');
    ok('5  marks carry the series channel this legend drives',
      L.ids.every((id) => marks(id).length > 0));

    /* RESTING STATE */
    ok('6  all swatches start checked', L.ids.every((id) => sw(id).getAttribute('aria-checked') === 'true'));
    ok('7  nothing starts ghosted', L.ids.every((id) => !anyGhost(id)));
    ok('8  Reset starts disabled (B-D4)', reset.disabled === true);

    /* TWO RENDER LEVELS — ghost, never hide */
    click(sw(a));
    ok('9  unchecking ghosts that series', ghosted(a) && sw(a).getAttribute('aria-checked') === 'false');
    ok('10 NOTHING is ever hidden — no opacity:0, no visibility:hidden',
      L.ids.every((id) => [].every.call(marks(id),
        (e) => e.style.opacity !== '0' && e.style.visibility !== 'hidden')));
    ok('11 the ghosted series stops taking pointer events',
      [].every.call(marks(a), (e) => e.style.pointerEvents === 'none'));
    ok('12 Reset enables once something is ghosted', reset.disabled === false);
    ok('13 the change is announced by name', announces(a));

    /* THE FLOOR — the last active series cannot be removed. `a` is already unchecked above, so
       walking the rest in order makes the FINAL click the one the floor must refuse. */
    L.ids.slice(1).forEach((id) => click(sw(id)));
    ok('14 the last active series cannot be unchecked',
      sw(last).getAttribute('aria-checked') === 'true' && !anyGhost(last));
    ok('15 the floor is announced, not silent', /at least one/i.test(live.textContent));

    /* RESET */
    click(reset);
    ok('16 Reset restores every series', L.ids.every((id) => !anyGhost(id)));
    ok('17 Reset re-disables itself once everything is shown', reset.disabled === true);

    /* ISOLATE = ADDITIVE FOCUS SET */
    click(item(a));
    ok('18 isolate ghosts the others and marks the row solo',
      !anyGhost(a) && others(a).every(ghosted) && row(a).classList.contains('is-solo'));
    ok('19 in isolate the other boxes render BLANK (focus-set membership)',
      sw(b).getAttribute('aria-checked') === 'false' && sw(a).getAttribute('aria-checked') === 'true');
    click(sw(b));
    ok('20 checking a blank swatch ADDS it at full',
      !anyGhost(b) && L.ids.slice(2).every(ghosted));   /* slice(2) is empty on a 2-series member */
    click(item(a));
    ok('21 releasing isolate restores the PRIOR mix (all shown)',
      L.ids.every((id) => !anyGhost(id)) && !row(a).classList.contains('is-solo'));

    /* HOVER — fires in BOTH modes */
    over(row(a));
    ok('22 hovering an active row fades the OTHER actives to 24%',
      others(a).every(faded) && !faded(a));
    click(sw(last));
    over(row(last));
    ok('23 hovering a GHOSTED row peeks it as an add-preview', peeked(last));
    click(reset);
  });

  /* ---- THE NEW RISK CHART-BAR INTRODUCES: two legends on one page ----
     dv-legend.js keys state on the host .dv-leg and resolves the figure by closest('figure').
     If that scoping were wrong, driving one legend would move the other chart's marks. */
  if (member.legends.length > 1) {
    console.log(`\n${member.name} — MULTI-LEGEND ISOLATION (new with this member)`);
    const [L1, L2] = member.legends;
    const leg1 = doc.getElementById(L1.id), leg2 = doc.getElementById(L2.id);
    const fig1 = leg1.closest('figure'), fig2 = leg2.closest('figure');
    const sw1 = leg1.querySelector('.dv-legrow[data-series="1"] .dv-leg-sw');
    const ghostCount = (f) => f.querySelectorAll('.is-ghost').length;

    /* the conformance pass above has already driven BOTH legends, so legend 2's live region
       holds its own last message. The invariant is that driving legend 1 leaves it UNCHANGED —
       not that it is empty. (Asserting "empty" was this suite's own first bug, 2026-07-26.) */
    const live2Before = doc.getElementById(L2.live).textContent;
    const live1Before = doc.getElementById(L1.live).textContent;

    ok('24 the two legends resolve to DIFFERENT figures', fig1 !== fig2);
    ok('25 both figures start clean', ghostCount(fig1) === 0 && ghostCount(fig2) === 0);
    click(sw1);
    ok('26 toggling legend 1 ghosts marks in ITS figure only', ghostCount(fig1) > 0);
    ok('27 the OTHER figure is untouched — no cross-talk', ghostCount(fig2) === 0);
    ok('28 the other legend\'s Reset stays disabled',
      leg2.querySelector('.dv-leg-reset').disabled === true);
    ok('29 legend 1 announces to its own live region',
      doc.getElementById(L1.live).textContent !== live1Before);
    ok('30 legend 2\'s live region is NOT written to — announcements don\'t bleed',
      doc.getElementById(L2.live).textContent === live2Before);
    click(leg1.querySelector('.dv-leg-reset'));
    ok('31 resetting legend 1 leaves legend 2 exactly as it was',
      ghostCount(fig2) === 0 && doc.getElementById(L2.live).textContent === live2Before);
  }
});

console.log(`\n${fail ? '✗' : '✓'} ${pass}/${pass + fail} checks passed`);
process.exit(fail ? 1 : 0);
