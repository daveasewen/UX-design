/* verify_apollo_fab_227.js — structural drive of knowledge/_render/apollo-fab.js
   against a hand-rolled DOM shim (no jsdom, no browser: the #227 VM has no pip and
   no headless Chrome).

     node knowledge/_render/verify_apollo_fab_227.js <repo-root>

   WHAT THIS PROVES: the mount path executes end to end, the controls write the
   attributes canon.css actually keys on, the inspector names a component from real
   dashboard-shaped nesting, each reveal mode arms and disarms, the token probe
   branches both ways, an unreachable frame degrades instead of throwing, and the
   overlay leaves cleanly.
   WHAT IT DOES NOT PROVE: anything visual. Layout, paint, the CSS cascade, real
   pointer physics and how any of it looks in four themes remain UNPROVEN here —
   that needs Dave's eye on reviews/FAB-READINGS-2026-08-30-v1.html. */

const fs = require('fs'), vm = require('vm'), path = require('path');
const REPO = process.argv[2] || path.join(__dirname, '..', '..');
const src = fs.readFileSync(path.join(REPO, 'knowledge/_render/apollo-fab.js'), 'utf8');
const META = JSON.parse(fs.readFileSync(path.join(REPO, 'knowledge/_render/apollo-fab-meta.json'), 'utf8'));

let fails = 0, passes = 0;
function ok(label, cond, extra) {
  if (cond) { passes++; console.log('  PASS  ' + label + (extra ? '  ' + extra : '')); }
  else { fails++; console.log('  FAIL  ' + label + (extra ? '  ' + extra : '')); }
}

/* ---- the shim ------------------------------------------------------------ */
function walk(n, fn) { (n.children || []).forEach(c => { fn(c); walk(c, fn); }); }
function matches(n, sel) {
  if (!n || n.nodeType !== 1) return false;
  if (sel[0] === '[') return n.hasAttribute(sel.slice(1, -1));
  if (sel[0] === '.') return n.classList.contains(sel.slice(1));
  return n.tagName === sel.toUpperCase();
}

function mkEl(doc, tag) {
  const e = {
    nodeType: 1, tagName: tag.toUpperCase(), ownerDocument: doc,
    children: [], parentElement: null, parentNode: null,
    attrs: {}, dataset: {}, _cls: [], innerHTML: '', textContent: '',
    offsetWidth: 200, offsetHeight: 80,
    style: { _p: {}, setProperty(k, v) { this._p[k] = v; } },
    _listeners: {},
    get className() { return this._cls.join(' '); },
    set className(v) { this._cls = String(v).split(/\s+/).filter(Boolean); },
    setAttribute(k, v) {
      this.attrs[k] = String(v);
      if (k.indexOf('data-') === 0) {
        this.dataset[k.slice(5).replace(/-([a-z])/g, (m, c) => c.toUpperCase())] = String(v);
      }
    },
    getAttribute(k) { return k in this.attrs ? this.attrs[k] : null; },
    hasAttribute(k) { return k in this.attrs; },
    appendChild(c) { this.children.push(c); c.parentElement = this; c.parentNode = this; return c; },
    removeChild(c) { const i = this.children.indexOf(c); if (i > -1) this.children.splice(i, 1); return c; },
    contains(n) { let x = n; while (x) { if (x === this) return true; x = x.parentElement; } return false; },
    addEventListener(t, f) { (this._listeners[t] = this._listeners[t] || []).push(f); },
    removeEventListener(t, f) { const a = this._listeners[t] || [], i = a.indexOf(f); if (i > -1) a.splice(i, 1); },
    fire(t, ev) { (this._listeners[t] || []).slice().forEach(f => f(Object.assign({ target: this }, ev || {}))); },
    getBoundingClientRect() { return { left: 0, top: 0, width: 400, height: 300 }; },
    closest(sel) { let x = this; while (x) { if (matches(x, sel)) return x; x = x.parentElement; } return null; },
    querySelectorAll(sel) { const out = []; walk(this, n => { if (matches(n, sel)) out.push(n); }); return out; },
    querySelector(sel) { return this.querySelectorAll(sel)[0] || null; }
  };
  e.classList = {
    get length() { return e._cls.length; },
    contains: c => e._cls.indexOf(c) > -1,
    add: c => { if (e._cls.indexOf(c) < 0) e._cls.push(c); },
    remove: c => { const i = e._cls.indexOf(c); if (i > -1) e._cls.splice(i, 1); },
    toggle: (c, on) => { on ? e.classList.add(c) : e.classList.remove(c); }
  };
  /* cnClass() reads classList[i] — the real DOM's indexed access */
  return new Proxy(e, {
    get(t, k) {
      if (k === 'classList') {
        return new Proxy(t.classList, {
          get(cl, ck) { return (typeof ck === 'string' && /^\d+$/.test(ck)) ? t._cls[+ck] : cl[ck]; }
        });
      }
      return t[k];
    }
  });
}

function mkDoc() {
  const doc = { _listeners: {}, readyState: 'complete' };
  doc.createElement = tag => mkEl(doc, tag);
  doc.documentElement = mkEl(doc, 'html');
  doc.head = mkEl(doc, 'head');
  doc.body = mkEl(doc, 'body');
  doc.documentElement.appendChild(doc.head);
  doc.documentElement.appendChild(doc.body);
  doc.getElementById = () => null;
  doc.getElementsByTagName = () => [];
  doc.addEventListener = (t, f) => { (doc._listeners[t] = doc._listeners[t] || []).push(f); };
  doc.removeEventListener = (t, f) => { const a = doc._listeners[t] || [], i = a.indexOf(f); if (i > -1) a.splice(i, 1); };
  doc.fire = (t, ev) => (doc._listeners[t] || []).slice().forEach(f => f(ev || {}));
  doc.defaultView = { getComputedStyle: () => ({ getPropertyValue: () => doc._surfaceVar || '' }) };
  doc.querySelectorAll = sel => { const out = []; walk(doc.documentElement, n => { if (matches(n, sel)) out.push(n); }); return out; };
  return doc;
}

/* ---- load ---------------------------------------------------------------- */
const hostDoc = mkDoc();
const sandbox = { document: hostDoc, setTimeout, clearTimeout, Date, Math, Promise, console };
sandbox.window = sandbox;
vm.createContext(sandbox);
vm.runInContext(src, sandbox, { filename: 'apollo-fab.js' });
const ApolloFAB = sandbox.ApolloFAB;

console.log('\n[0] the global footprint');
const added = Object.keys(sandbox).filter(k =>
  ['document', 'setTimeout', 'clearTimeout', 'Date', 'Math', 'Promise', 'console', 'window'].indexOf(k) < 0);
ok('exactly one global added', added.length === 1 && added[0] === 'ApolloFAB', '(' + added.join(', ') + ')');
ok('no auto-mount without a script tag', ApolloFAB.instances.length === 0);

/* ---- 1 ------------------------------------------------------------------- */
console.log('\n[1] mount on a bare page (no canon vars, no frame)');
const before = hostDoc.body.children.length;
const f1 = ApolloFAB.mount({ reveal: 'always' });
ok('exactly one node appended to <body>', hostDoc.body.children.length === before + 1);
ok('one <style> injected into <head>', hostDoc.head.children.length === 1);
ok('node carries .apollo-fab', f1.layer.classList.contains('apollo-fab'));
ok('token probe -> fallback pair', f1.tokenMode === 'fallback');
ok('layer NOT .af-tokens', !f1.layer.classList.contains('af-tokens'));
ok('z-index from Z_DEFAULT', f1.layer.style._p['--af-z'] === String(ApolloFAB.Z_DEFAULT));
ok('corner var = the PROPOSED 72px default', f1.layer.style._p['--af-corner'] === '72px');
ok('always mode starts revealed', f1.layer.getAttribute('data-revealed') === 'true');
ok('panel starts closed', f1.layer.getAttribute('data-open') === 'false');
ok('inspector starts off', f1.layer.getAttribute('data-inspect') === 'false');
ok('corner sensor off on a normal page', f1.layer.getAttribute('data-sensor') === 'off');

/* ---- 2 ------------------------------------------------------------------- */
console.log('\n[2] controls -> the attributes canon.css keys on');
const themeBtns = f1.panel.querySelectorAll('[data-af-theme]');
ok('four theme buttons', themeBtns.length === 4, '(' + themeBtns.map(b => b.innerHTML).join(', ') + ')');
const legacyBtn = themeBtns.filter(b => b.getAttribute('data-af-theme') === 'legacy');
/* Guarded: if the rename lane ever changes the VALUE, this must fail loud and named,
   not crash on an empty match and take the rest of the run with it. */
ok('a button still carries data-af-theme="legacy"', legacyBtn.length === 1,
  '(found ' + legacyBtn.length + ')');
ok('...and it is LABELLED "Common"', legacyBtn.length === 1 && legacyBtn[0].innerHTML === 'Common',
  legacyBtn.length === 1 ? '(label="' + legacyBtn[0].innerHTML + '")' : '(no legacy button)');

const sc = themeBtns.filter(b => b.getAttribute('data-af-theme') === 'supercharge')[0];
f1.panel.fire('click', { target: sc });
ok('<html> gets data-apollo-theme=supercharge', hostDoc.documentElement.getAttribute('data-apollo-theme') === 'supercharge');
ok('<body> gets data-apollo-theme=supercharge', hostDoc.body.getAttribute('data-apollo-theme') === 'supercharge');
ok('pressed state follows', sc.getAttribute('aria-pressed') === 'true');
ok('the other three release',
  themeBtns.filter(b => b !== sc).every(b => b.getAttribute('aria-pressed') === 'false'));

const modeBtns = f1.panel.querySelectorAll('[data-af-mode]');
f1.panel.fire('click', { target: modeBtns.filter(b => b.getAttribute('data-af-mode') === 'dark')[0] });
ok('<html> gets data-theme=dark', hostDoc.documentElement.getAttribute('data-theme') === 'dark');
ok('<body> gets data-theme=dark', hostDoc.body.getAttribute('data-theme') === 'dark');

f1.btn.fire('click');
ok('FAB click opens the panel', f1.layer.getAttribute('data-open') === 'true');
ok('aria-expanded follows', f1.btn.getAttribute('aria-expanded') === 'true');
hostDoc.fire('keydown', { key: 'Escape' });
ok('Escape closes the panel', f1.layer.getAttribute('data-open') === 'false');

/* ---- 3 ------------------------------------------------------------------- */
console.log('\n[3] provenance inspector, on real dashboard nesting');
const insBtn = f1.panel.querySelectorAll('[data-af-inspect]')[0];
f1.panel.fire('click', { target: insBtn });
ok('inspector toggles on', f1.inspect === true && f1.layer.getAttribute('data-inspect') === 'true');

/* .cn-stat-card > .stat-card > .amt — copied from the canon dashboard's own markup */
const tile = mkEl(hostDoc, 'section'); tile.className = 'c-bento__tile dashboard-tile cn-stat-card';
const card = mkEl(hostDoc, 'div'); card.className = 'stat-card';
const amt = mkEl(hostDoc, 'span'); amt.className = 'amt t-cm-figure-4';
hostDoc.body.appendChild(tile); tile.appendChild(card); card.appendChild(amt);

hostDoc.fire('pointerover', { target: amt });
ok('tooltip shows for a nested descendant', f1.tip.style.display === 'block');
ok('names the ANCESTOR component', f1.tip.innerHTML.indexOf('Stat card') > -1);
ok('shows the class', f1.tip.innerHTML.indexOf('.cn-stat-card') > -1);
ok('DEFAULT-SAFE path says so, not an error', f1.tip.innerHTML.indexOf('class-name only') > -1);
ok('highlight box placed', f1.box.style.display === 'block');

f1.meta = META.components; f1.metaState = 'full';
hostDoc.fire('pointerover', { target: amt });
ok('with the REAL generated map: purpose appears',
  f1.tip.innerHTML.indexOf('The dashboard tile for one headline number') > -1);
ok('with the map: category + token verdict appear',
  f1.tip.innerHTML.indexOf('molecule') > -1 && f1.tip.innerHTML.indexOf('tokens PASS') > -1);

/* -dv suffix, as the chart family carries it */
const dv = mkEl(hostDoc, 'div'); dv.className = 'cn-chart-line-dv'; hostDoc.body.appendChild(dv);
hostDoc.fire('pointerover', { target: dv });
ok('cn-chart-line-dv resolves to the Line chart row', f1.tip.innerHTML.indexOf('Line chart') > -1);

const plain = mkEl(hostDoc, 'div'); plain.className = 'not-a-component'; hostDoc.body.appendChild(plain);
hostDoc.fire('pointerover', { target: plain });
ok('non-component hover hides the tooltip', f1.tip.style.display === 'none');
hostDoc.fire('pointerover', { target: f1.btn });
ok('the overlay never inspects its own chrome', f1.tip.style.display === 'none');

/* ---- 4 ------------------------------------------------------------------- */
console.log('\n[4] the three reveal modes');
hostDoc.documentElement.clientWidth = 1200;
hostDoc.documentElement.clientHeight = 800;

const f2 = ApolloFAB.mount({ reveal: 'hotcorner', cornerSize: 72 });
ok('B starts hidden', f2.layer.getAttribute('data-revealed') === 'false');
hostDoc.fire('pointermove', { clientX: 10, clientY: 10 });
ok('B: pointer far from the corner stays hidden', f2.layer.getAttribute('data-revealed') === 'false');
hostDoc.fire('pointermove', { clientX: 1140, clientY: 740 });
ok('B: pointer inside the 72px zone reveals', f2.layer.getAttribute('data-revealed') === 'true');

/* the zone edge, driven on a fresh instance: 1200-72 = 1128 is in, 1127 is out */
const f2b = ApolloFAB.mount({ reveal: 'hotcorner', cornerSize: 72 });
hostDoc.fire('pointermove', { clientX: 1127, clientY: 800 });
ok('B: one pixel outside the zone does NOT reveal', f2b.layer.getAttribute('data-revealed') === 'false');
hostDoc.fire('pointermove', { clientX: 1128, clientY: 728 });
ok('B: the top-left pixel OF the zone does reveal', f2b.layer.getAttribute('data-revealed') === 'true');
f2b.destroy();

const f3 = ApolloFAB.mount({ reveal: 'summon' });
ok('C starts hidden', f3.layer.getAttribute('data-revealed') === 'false');
hostDoc.fire('keydown', { key: 'Shift' });
ok('C: one Shift does nothing', f3.layer.getAttribute('data-revealed') === 'false');
hostDoc.fire('keydown', { key: 'Shift' });
ok('C: double Shift summons', f3.layer.getAttribute('data-revealed') === 'true');
hostDoc.fire('keydown', { key: 'Escape' });
ok('C: Escape dismisses', f3.layer.getAttribute('data-revealed') === 'false');
hostDoc.fire('pointerdown', { clientX: 1180, clientY: 780 });
ok('C: one corner tap is inert', f3.layer.getAttribute('data-revealed') === 'false');
hostDoc.fire('pointerdown', { clientX: 1180, clientY: 780 });
ok('C: double corner tap summons (the touch fallback)', f3.layer.getAttribute('data-revealed') === 'true');

/* ---- 5 ------------------------------------------------------------------- */
console.log('\n[5] token probe on a page that DOES carry canon vars');
hostDoc._surfaceVar = ' #FFFFFF ';
const f4 = ApolloFAB.mount({ reveal: 'always' });
ok('probe finds --surface -> .af-tokens', f4.layer.classList.contains('af-tokens') && f4.tokenMode === 'canon');

/* ---- 6 ------------------------------------------------------------------- */
console.log('\n[6] a frame that cannot be reached (the file:// case)');
const fakeFrame = mkEl(hostDoc, 'iframe');
Object.defineProperty(fakeFrame, 'contentDocument', { get() { throw new Error('cross-origin'); } });
const pane = mkEl(hostDoc, 'div'); hostDoc.body.appendChild(pane);
const f5 = ApolloFAB.mount({ reveal: 'hotcorner', frame: fakeFrame, container: pane, cornerSize: 72 });
ok('mount survives a throwing contentDocument', !!f5.layer);
ok('blocked flag set', f5.blocked === true);
ok('layer is container-absolute', f5.layer.classList.contains('af-contained'));
ok('mounted into the container, not <body>', pane.children.indexOf(f5.layer) > -1);
ok('sensor armed (the coordinate watcher is deaf over a walled-off frame)',
  f5.layer.getAttribute('data-sensor') === 'on');
ok('the panel says so in plain words', f5.note.innerHTML.indexOf('Frame unreachable') > -1);
f5.setTheme('console');
ok('controls fall back to the host document', hostDoc.documentElement.getAttribute('data-apollo-theme') === 'console');
f5.sensor.fire('pointerdown');
ok('sensor tap reveals in hotcorner mode', f5.layer.getAttribute('data-revealed') === 'true');

/* ---- 7 ------------------------------------------------------------------- */
console.log('\n[7] it leaves cleanly (one script tag deleted = gone)');
const n = hostDoc.body.children.length, before7 = (hostDoc._listeners['pointerover'] || []).length;
f1.destroy();
ok('layer removed from the DOM', hostDoc.body.children.length === n - 1);
ok('document listeners released', (hostDoc._listeners['pointerover'] || []).length === before7 - 1);
ok('instance deregistered', ApolloFAB.instances.indexOf(f1) === -1);

console.log('\n' + (fails ? 'FAILED ' + fails + ' of ' + (fails + passes) + ' structural checks'
  : 'ALL ' + passes + ' STRUCTURAL CHECKS PASS  (visual render UNPROVEN — needs Dave\'s eye)'));
process.exit(fails ? 1 : 0);
