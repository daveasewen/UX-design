/* _verify_dv_legend — numeric interaction proof for the DV-D11/12/13 legend model.
   Drives the REAL canon/dv-legend.js against the REAL Chart-donut.reference.html in jsdom, so
   this verifies shipped code, not a re-implementation of it. The v5.4/v5.5 review sessions
   asserted 14/14 checks in-render; this is the same standard, run in the build sandbox.

   Run: node knowledge/_verify_dv_legend.js            (from the repo root)
   Requires jsdom on NODE_PATH — verification tooling only, never a build dependency. */
const fs = require('fs');
const path = require('path');
const { JSDOM } = require(process.env.JSDOM || '/tmp/node_modules/jsdom');

const ROOT = path.resolve(__dirname, '..');
const SNIP = path.join(ROOT, 'knowledge/snippets/Chart-donut.reference.html');
/* overridable so the BITE-THE-BITE run can point at a neutered copy and prove these checks can
   go red, without ever mutating canon to do it. Default is always the real canon source. */
const SRC = process.env.DVLEGEND || path.join(ROOT, 'knowledge/canon/dv-legend.js');

let pass = 0, fail = 0;
const ok = (name, cond, detail) => {
  if (cond) { pass++; console.log(`  ✓ ${name}`); }
  else { fail++; console.log(`  ✗ ${name}${detail ? ' — ' + detail : ''}`); }
};

/* runScripts:'outside-only' gives window.eval a real script context WITHOUT executing the
   snippet's own injected blocks — so this exercises dv-legend.js in isolation. */
const dom = new JSDOM(fs.readFileSync(SNIP, 'utf8'), { pretendToBeVisual: true, runScripts: 'outside-only' });
const { window } = dom;
const doc = window.document;

/* drive rAF by hand so the sweep is deterministic and inspectable */
let rafQ = [];
window.requestAnimationFrame = (fn) => { rafQ.push(fn); return rafQ.length; };
window.cancelAnimationFrame = () => {};

const leg = doc.getElementById('cd1-legend');
const fig = leg.closest('figure');
const seg = (id) => fig.querySelector(`.dv-series[data-series-group="${id}"]`);
const row = (id) => leg.querySelector(`.dv-legrow[data-series="${id}"]`);
const sw = (id) => row(id).querySelector('.dv-leg-sw');
const item = (id) => row(id).querySelector('.dv-leg-item');
const reset = leg.querySelector('.dv-leg-reset');
const live = doc.getElementById('cd1-live');
const centre = (v) => fig.querySelector(`[data-dv-view="${v}"] .dv-val`).textContent;
const ghosted = (id) => seg(id).classList.contains('is-ghost');
const click = (el) => el.dispatchEvent(new window.MouseEvent('click', { bubbles: true }));
const over = (el) => el.dispatchEvent(new window.MouseEvent('pointerover', { bubbles: true }));

/* capture the baked geometry BEFORE the sweep rewrites it */
const fullD = {};
[1, 2, 3, 4, 5].forEach((i) => { fullD[i] = seg(i).getAttribute('d'); });

window.eval(fs.readFileSync(SRC, 'utf8'));

console.log('\nDV-D11 — resting state + two render levels');
ok('1  all five swatches start checked', [1, 2, 3, 4, 5].every((i) => sw(i).getAttribute('aria-checked') === 'true'));
ok('2  no series starts ghosted', [1, 2, 3, 4, 5].every((i) => !ghosted(i)));
ok('3  Reset starts disabled (B-D4)', reset.disabled === true);

click(sw(1));
ok('4  unchecking ghosts that series', ghosted(1) && sw(1).getAttribute('aria-checked') === 'false');
ok('5  NOTHING is ever hidden — no opacity:0 / visibility:hidden',
  [1, 2, 3, 4, 5].every((i) => seg(i).style.opacity !== '0' && seg(i).style.visibility !== 'hidden'),
  'the dead hide-at-0% model must not survive anywhere');
ok('6  other series untouched', [2, 3, 4, 5].every((i) => !ghosted(i)));
ok('7  Reset enables on any ghost', reset.disabled === false);
click(sw(1));
ok('8  re-checking restores full', !ghosted(1) && reset.disabled === true);

console.log('\nDV-D11 + ★ DV-D17 — isolate is a ONE-SERIES mode the next check-on ENDS');
click(item(2));
ok('9  isolate marks its row solo', item(2).getAttribute('aria-pressed') === 'true' && row(2).classList.contains('is-solo'));
ok('10 other boxes render BLANK in isolate', [1, 3, 4, 5].every((i) => sw(i).getAttribute('aria-checked') === 'false'));
ok('11 non-focused series ghost, focus stays full', !ghosted(2) && [1, 3, 4, 5].every((i) => ghosted(i)));
/* ⚠ 12 and 13 ASSERTED THE SUPERSEDED MODEL — rewritten, not deleted. They read
   "12 checking ADDS to the focus set" (!ghosted(4) && !ghosted(2) && ghosted(1) && ghosted(3))
   and "13 release restores the prior mix exactly". DV-D17 (Dave, 2026-07-27) ends the mode on
   that click instead. Both wordings: _DATAVIZ-DECISIONS.md § Batch 10. */
click(sw(4));
ok('12 DV-D17 — checking a blank swatch RELEASES isolation entirely',
  !row(2).classList.contains('is-solo') && item(2).getAttribute('aria-pressed') === 'false'
    && [1, 2, 3, 4, 5].every((i) => !ghosted(i)));
ok('13 DV-D17 — the release is ANNOUNCED on the add path', /isolation released/i.test(live.textContent));

console.log('\nDV-D11 — guards, hover ladder, live region');
/* isolation is already released above (it used to need the click that stood here), so the walk
   below starts from the all-shown state exactly as it did before DV-D17. */
[2, 3, 4, 5].forEach((i) => click(sw(i)));
click(sw(1));
ok('14 the last active series cannot be unchecked', !ghosted(1) && /must stay shown/i.test(live.textContent));
click(reset);
ok('15 Reset restores everything', [1, 2, 3, 4, 5].every((i) => !ghosted(i)) && reset.disabled === true);
over(row(1));
ok('16 hovering an active row fades the OTHER actives to 24%',
  !seg(1).classList.contains('is-faded') && [2, 3, 4, 5].every((i) => seg(i).classList.contains('is-faded')));
click(sw(3));
over(row(3));
ok('17 hovering a GHOSTED row peeks it (add-preview)', seg(3).classList.contains('is-peek'));
click(sw(3));

console.log('\nDV-D13 — typed tooltip + selection-following centre');
ok('18 centre starts at the grand total', centre('value') === '2320' && centre('percent') === '100%');
click(item(1));
ok('19 isolate Housing → 950 / 41%', centre('value') === '950' && centre('percent') === '41%', `got ${centre('value')} / ${centre('percent')}`);
/* ⚠ DV-D17 CHANGES WHAT THIS CHECK MEASURES, and the change is worth naming. It read
   "20 +Savings → 1250 / 54%": under additive focus, checking a second series GREW the centre
   readout. Under DV-D17 that same click ends isolation, so the selection becomes the whole
   visible set and the centre returns to the grand total. DV-D13 is intact — the centre still
   follows the SELECTION; the selection is simply everything again. */
click(sw(3));
ok('20 DV-D17 — the add-click releases, so the centre returns to the grand total',
  centre('value') === '2320' && centre('percent') === '100%', `got ${centre('value')} / ${centre('percent')}`);
click(reset);
const segBtn = (v) => fig.querySelector(`button[data-dv-view-btn="${v}"]`);
ok('21 marks carry BOTH typed tips', !!seg(1).getAttribute('data-tip-value') && !!seg(1).getAttribute('data-tip-percent'));
if (segBtn('percent')) {
  click(segBtn('percent'));
  ok('22 the seg rewrites data-tip to the selected type ONLY',
    seg(1).getAttribute('data-tip') === seg(1).getAttribute('data-tip-percent') && !/£/.test(seg(1).getAttribute('data-tip')),
    `got ${seg(1).getAttribute('data-tip')}`);
  click(segBtn('value'));
  ok('23 switching back restores the value form', seg(1).getAttribute('data-tip') === seg(1).getAttribute('data-tip-value'));
}
ok('24 aria-labels deliberately keep BOTH forms (DV-D13 ⚠)',
  /950/.test(seg(1).getAttribute('aria-label')) && /41/.test(seg(1).getAttribute('aria-label')));

console.log('\nDV-D12 — trapezoidal sweep keyed to segment spans');
const angles = [];
const readSpan = () => {
  /* the swept arc's angular reach, recovered from the first segment's own geometry */
  const d = seg(1).getAttribute('d');
  return d === fullD[1] ? Infinity : d.length;
};
if (rafQ.length) {
  const step = (ts) => { const q = rafQ; rafQ = []; q.forEach((fn) => fn(ts)); };
  step(0);
  ok('25 sweep starts collapsed (segments at zero width)', seg(1).getAttribute('d') !== fullD[1]);
  let prev = -1, monotonic = true;
  for (const ts of [100, 200, 300, 425, 550, 700, 849]) {
    step(ts);
    const a = parseFloat((seg(5).getAttribute('d').match(/A\s*100\s+100[^L]*L/) || [''])[0].length || 0);
    angles.push(a);
  }
  step(850); step(900);
  ok('26 sweep lands EXACTLY on the baked geometry',
    [1, 2, 3, 4, 5].every((i) => seg(i).getAttribute('d') === fullD[i]),
    'rest-to-rest: the animation must not leave the chart off its baked answer');
  ok('27 annotations are revealed by the end', [...fig.querySelectorAll('.dv-anno')].every((a) => a.classList.contains('show')));
} else {
  ok('25 sweep scheduled a frame', false, 'no rAF queued — the donut sweep did not start');
}

console.log(`\n${pass}/${pass + fail} checks passed`);
process.exit(fail ? 1 : 0);
