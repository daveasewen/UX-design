/* =====================================================================================
   apollo-fab.js — Apollo view-time overlay  (#227, lane 3)
   =====================================================================================

   WHAT IT IS
   Demo chrome. A floating control layer that any generated page can wear at view time
   and shed for ship. It is NOT part of the design:
     · one fixed-position (or container-absolute) layer, nothing else touches the DOM
     · its own z-index (Z_DEFAULT below), above every sticky header we ship
     · zero effect on page layout — the layer never participates in flow
     · removable by deleting the one <script> tag that loaded it
     · one global: window.ApolloFAB. Nothing else.

   HOW TO WEAR IT
     <script src="../knowledge/_render/apollo-fab.js"
             data-reveal="hotcorner"   <!-- always | hotcorner | summon — DEFAULT hotcorner -->
             data-corner="72"          <!-- corner-zone edge in px (hotcorner/summon), default 72 -->
             data-meta="apollo-fab-meta.json"></script>
   Auto-mounts on DOMContentLoaded unless data-auto="off". Programmatic:
     var fab = ApolloFAB.mount({ reveal:'hotcorner', frame:someIframe, container:pane });

   CONTROLS (v1)
     · Theme  — sets data-apollo-theme on <html> AND <body> of the target document,
                across mono / legacy / console / supercharge.
                The legacy button is LABELLED "Common" (a rename lane is queued); the
                ATTRIBUTE VALUE stays 'legacy'. Label and value are deliberately split —
                see THEMES below.
     · Mode   — sets data-theme="light|dark" on <html> AND <body> of the target document.
                That is the convention Dave's dashboards use
                (dashboards/international-banking-dashboard.canon.html:
                 <html data-apollo-theme="console"> + <body data-theme="light">),
                and it matches canon.css's alias layer, which declares the short aliases
                on :root AND [data-theme] so they re-resolve wherever the attribute sits.
     · Inspect — provenance inspector. Hovering any element carrying a cn-* class names
                the component; with apollo-fab-meta.json loaded it also gives category,
                purpose and the token-validation verdict.

   PITFALLS THIS FILE ANSWERS (replayed from the #227 brief)
     1. A page without canon's CSS vars. We PROBE for --surface at mount
        (see applyTokenMode) and fall back to a hard neutral pair lifted from
        canon.css primitives — never an invented colour. Fallback also answers
        prefers-color-scheme so a dark host does not get a white slab.
     2. z-index wars. Z_DEFAULT = 2147483000, chosen to clear anything a page
        plausibly declares; overridable per-mount.
     3. Hot corners do not exist on touch. Variant B and C both accept a TAP in the
        same corner zone (pointerdown of a non-mouse pointer type), so a finger can
        reach the FAB. Stated on the reading page too.
     4. The inspector must not intercept clicks. The tooltip and highlight live in a
        layer that is pointer-events:none at ALL times; the inspector adds only passive
        listeners and never calls preventDefault. The corner zone is detected by
        COORDINATE, not by a hit-testing element, so nothing under the corner is ever
        stolen — including in always-visible mode.

   FETCH IS OPTIONAL BY DESIGN
     file:// pages usually cannot fetch a sibling JSON. The class-name-only tooltip is
     therefore the DEFAULT-SAFE state, not an error state: the inspector renders it from
     the moment it is switched on, and the meta map upgrades it later if it ever lands.
   ===================================================================================== */

(function (global) {
  'use strict';

  if (global.ApolloFAB && global.ApolloFAB.version) { return; }

  var VERSION = '1.0.1-228';
  var Z_DEFAULT = 2147483000;   /* pitfall 2 — above every sticky/masthead we ship */

  /* L1/L2 — RULED by Dave on the #227 confirm pass, row 4: reading B, hot corner, and the
     canon settings icon on the button face. Reveal was 'always' while the three readings
     were being decided; it is now 'hotcorner' everywhere the config does not say otherwise.
     72 is his number too — the confirm card put it as "72 px stands unless you give a
     number" and he gave none. It is ~1.3x the 56 px button it reveals, so the pointer never
     has to leave the zone to reach it. Any other number is still one config value away:
     data-corner="N". */
  var REVEAL_DEFAULT = 'hotcorner';
  var CORNER_DEFAULT = 72;
  var STYLE_ID = 'apollo-fab-style';

  /* THEMES — [attribute value, button label].
     'legacy' is LABELLED "Common" per the #227 brief; the attribute value is untouched
     because canon.css keys its cascade on [data-apollo-theme="legacy"]. Renaming the
     value is a separate lane. */
  var THEMES = [
    ['mono', 'Mono'],
    ['legacy', 'Common'],
    ['console', 'Console'],
    ['supercharge', 'Supercharge']
  ];

  var MODES = [['light', 'Light'], ['dark', 'Dark']];

  /* ---------------------------------------------------------------------------------
     STYLE. Injected once per document. Every colour is a canon alias with a hard
     fallback; the fallbacks below are lifted verbatim from knowledge/canon/canon.css
     primitives (--color-mono-4, --color-grey-300/600, --color-grey-dark-mode-600,
     --color-primary, --color-grey-transparent-black-20/-85). None is invented.
     --------------------------------------------------------------------------------- */
  var CSS = [
    '.apollo-fab{',
    '  --af-surface:#FFFFFF; --af-text:#1A1A1A; --af-muted:#767676; --af-line:#D7D8D6;',
    '  --af-pri:#DB0011; --af-on-pri:#FFFFFF; --af-shadow:#00000033;',
    '  --af-focus:#305A85; --af-page:#FFFFFF;',
    '  --af-font:"Univers Next HSBC","Helvetica Neue",Arial,sans-serif;',
    '  --af-ease:140ms cubic-bezier(.4,0,.2,1);',
    '  --af-size:56px; --af-gap:16px;',
    '  position:fixed; inset:0; pointer-events:none; z-index:var(--af-z);',
    '  font-family:var(--af-font); color:var(--af-text);',
    '  -webkit-font-smoothing:antialiased;',
    '}',
    /* Host page has no canon vars -> keep the hard pair, but honour the OS scheme so a
       dark host does not get a white slab. Pitfall 1. */
    '@media (prefers-color-scheme:dark){',
    '  .apollo-fab:not(.af-tokens){',
    '    --af-surface:#1D1D1D; --af-text:#FFFFFF; --af-muted:#B7B7B7; --af-line:#404040;',
    '    --af-shadow:#000000D9; --af-focus:#4587A7; --af-page:#000000;',
    '  }',
    '}',
    /* Host page DOES carry canon's alias layer -> inherit it, so the FAB re-themes with
       the page (added by applyTokenMode after the probe). */
    '.apollo-fab.af-tokens{',
    '  --af-surface:var(--surface); --af-text:var(--text); --af-muted:var(--muted);',
    '  --af-line:var(--border); --af-page:var(--page);',
    '  --af-pri:var(--button-primary-background-default,var(--pri,#DB0011));',
    '  --af-on-pri:var(--button-primary-icon-default,var(--reverse,#FFFFFF));',
    '  --af-shadow:var(--shadow,#00000033); --af-focus:var(--focus,#305A85);',
    '  --af-font:var(--font,"Univers Next HSBC","Helvetica Neue",Arial,sans-serif);',
    '  --af-ease:var(--ease,140ms cubic-bezier(.4,0,.2,1));',
    '}',
    '.apollo-fab.af-contained{position:absolute;}',
    /* --- the button ------------------------------------------------------------- */
    '.apollo-fab .af-btn{',
    '  position:absolute; right:var(--af-gap); bottom:var(--af-gap);',
    '  width:var(--af-size); height:var(--af-size);',
    '  display:inline-flex; align-items:center; justify-content:center;',
    '  padding:0; border:0; border-radius:50%; cursor:pointer;',
    '  background:var(--af-pri); color:var(--af-on-pri);',
    '  box-shadow:0 0 16px 0 var(--af-shadow);',
    '  pointer-events:auto; font:inherit;',
    '  transition:opacity var(--af-ease), transform var(--af-ease);',
    '}',
    '.apollo-fab .af-btn svg{width:24px; height:24px; display:block; fill:currentColor; pointer-events:none;}',
    '.apollo-fab .af-btn:hover{transform:scale(1.036);}',
    '.apollo-fab .af-btn:active{transform:scale(.964); filter:brightness(.94);}',
    '.apollo-fab .af-btn:focus-visible{outline:2px solid var(--af-focus); outline-offset:3px;}',
    /* --- reveal states ---------------------------------------------------------- */
    '.apollo-fab[data-reveal="hotcorner"] .af-btn,',
    '.apollo-fab[data-reveal="summon"] .af-btn{opacity:0; pointer-events:none;}',
    '.apollo-fab[data-revealed="true"] .af-btn{opacity:1; pointer-events:auto;}',
    '.apollo-fab[data-reveal="summon"]:not([data-revealed="true"]) .af-panel{display:none;}',
    /* --- corner hint (variant B only, and only while the page is idle) ---------- */
    '.apollo-fab .af-hint{',
    '  position:absolute; right:0; bottom:0; pointer-events:none;',
    '  width:var(--af-corner); height:var(--af-corner);',
    '  border-right:2px solid var(--af-pri); border-bottom:2px solid var(--af-pri);',
    '  opacity:0; transition:opacity var(--af-ease);',
    '}',
    '.apollo-fab[data-hint="on"] .af-hint{opacity:.5;}',
    /* --- corner SENSOR: a demo aid, off by default ------------------------------
       The shipping mechanism is coordinate maths (see _inCorner) and intercepts
       nothing. But pointer events that land inside a cross-origin iframe never reach
       the host document at all, so on a file:// reading page the coordinate watcher
       goes deaf over the frame. When — and only when — a frame was named and turned
       out to be unreachable, we add a real hit zone so the reveal is still
       demonstrable. It disappears the instant the FAB is revealed. */
    '.apollo-fab .af-sensor{',
    '  position:absolute; right:0; bottom:0; display:none;',
    '  width:var(--af-corner); height:var(--af-corner); pointer-events:auto;',
    '  background:transparent; border:0; padding:0; cursor:default;',
    '}',
    '.apollo-fab[data-sensor="on"]:not([data-revealed="true"]) .af-sensor{display:block;}',
    /* --- the panel -------------------------------------------------------------- */
    '.apollo-fab .af-panel{',
    '  position:absolute; right:var(--af-gap);',
    '  bottom:calc(var(--af-gap) + var(--af-size) + 12px);',
    '  width:274px; max-width:calc(100% - (2 * var(--af-gap)));',
    '  max-height:calc(100% - (var(--af-size) + 44px));',
    '  overflow:auto; pointer-events:auto;',
    '  background:var(--af-surface); color:var(--af-text);',
    '  border:1px solid var(--af-line); box-shadow:0 0 16px 0 var(--af-shadow);',
    '  opacity:0; transform:translateY(6px); visibility:hidden;',
    '  transition:opacity var(--af-ease), transform var(--af-ease), visibility 0s linear 140ms;',
    '}',
    '.apollo-fab[data-open="true"] .af-panel{opacity:1; transform:none; visibility:visible; transition-delay:0s;}',
    '.apollo-fab .af-head{',
    '  display:flex; align-items:baseline; gap:8px; padding:12px 14px 10px;',
    '  border-bottom:1px solid var(--af-line);',
    '}',
    '.apollo-fab .af-head b{font-size:13px; font-weight:500; letter-spacing:-.01em;}',
    '.apollo-fab .af-head span{font-size:11px; color:var(--af-muted); margin-left:auto;}',
    '.apollo-fab .af-grp{padding:12px 14px; border-bottom:1px solid var(--af-line);}',
    '.apollo-fab .af-grp:last-child{border-bottom:0;}',
    '.apollo-fab .af-lbl{',
    '  display:block; font-size:11px; line-height:16px; color:var(--af-muted);',
    '  text-transform:uppercase; letter-spacing:.06em; margin:0 0 8px;',
    '}',
    '.apollo-fab .af-row{display:flex; flex-wrap:wrap; gap:0;}',
    '.apollo-fab .af-row button{',
    '  font:inherit; font-size:12px; line-height:18px; padding:6px 10px;',
    '  border:1px solid var(--af-line); background:transparent; color:var(--af-text);',
    '  cursor:pointer; margin:0 -1px -1px 0; flex:1 1 auto; min-width:64px;',
    '  transition:background var(--af-ease), color var(--af-ease);',
    '}',
    '.apollo-fab .af-row button:hover{background:color-mix(in srgb, currentColor 8%, transparent);}',
    '.apollo-fab .af-row button[aria-pressed="true"]{',
    '  background:var(--af-text); color:var(--af-surface); border-color:var(--af-text);',
    '}',
    '.apollo-fab .af-row button:focus-visible{outline:2px solid var(--af-focus); outline-offset:-2px; position:relative; z-index:1;}',
    '.apollo-fab .af-note{margin:8px 0 0; font-size:11px; line-height:15px; color:var(--af-muted);}',
    '.apollo-fab .af-note code{font-family:ui-monospace,SFMono-Regular,Menlo,monospace; font-size:10px;}',
    /* --- inspector overlay: pointer-events:none ALWAYS (pitfall 4) --------------- */
    '.apollo-fab .af-ink{position:absolute; inset:0; pointer-events:none; display:none;}',
    '.apollo-fab[data-inspect="true"] .af-ink{display:block;}',
    '.apollo-fab .af-box{',
    '  position:absolute; pointer-events:none; display:none;',
    '  outline:2px solid var(--af-pri); outline-offset:0;',
    '  background:color-mix(in srgb, var(--af-pri) 8%, transparent);',
    '}',
    '.apollo-fab .af-tip{',
    '  position:absolute; pointer-events:none; display:none; max-width:280px;',
    '  background:var(--af-surface); color:var(--af-text);',
    '  border:1px solid var(--af-line); box-shadow:0 0 16px 0 var(--af-shadow);',
    '  padding:8px 10px;',
    '}',
    '.apollo-fab .af-tip strong{display:block; font-size:12px; font-weight:500; line-height:16px;}',
    '.apollo-fab .af-tip .af-cls{',
    '  display:block; font-family:ui-monospace,SFMono-Regular,Menlo,monospace;',
    '  font-size:10px; line-height:14px; color:var(--af-muted); margin-top:2px;',
    '}',
    '.apollo-fab .af-tip .af-purpose{display:block; font-size:11px; line-height:15px; margin-top:6px;}',
    '.apollo-fab .af-tip .af-meta{display:block; font-size:10px; line-height:14px; color:var(--af-muted); margin-top:6px;}',
    '@media (prefers-reduced-motion:reduce){',
    '  .apollo-fab *{transition-duration:.01ms !important;}',
    '  .apollo-fab .af-btn:hover, .apollo-fab .af-btn:active{transform:none;}',
    '}'
  ].join('\n');

  /* THE BUTTON FACE — knowledge/assets/icons/global-controls/settings.svg, COPIED BYTE FOR
     BYTE from the library (its 18x18 viewBox, its single evenodd path, its currentColor
     fill). Dave, #227 confirm pass row 4: "use an icon from the library though". The glyph
     that stood here was hand-drawn — a gear nobody had reviewed, in a pack whose first rule
     is "never invent an icon". `settings` is the library's own name for it, and the same
     file Template-settings.reference.html already uses for its settings affordance.
     ⛔ Do not redraw or re-path this. If the library icon changes, re-copy it.
     The root `fill="none"` is dropped so the CSS `fill:currentColor` on `.af-btn svg` is
     what colours it; the path keeps its own currentColor. 18x18 is scaled to the 24px box
     by that same CSS rule. */
  var GLYPH =
    '<svg viewBox="0 0 18 18" aria-hidden="true" focusable="false">' +
    '<path fill-rule="evenodd" clip-rule="evenodd" d="M16.376 6.992C16.208 6.374 15.96 5.774 15.634 5.206L16.319 3.592L14.408 1.68L12.794 2.365C12.225 2.04 11.626 1.791 11.007 1.623L10.352 0H7.648L6.992 1.624C6.374 1.791 5.774 2.04 5.206 2.365L3.592 1.68L1.68 3.592L2.365 5.206C2.04 5.774 1.791 6.374 1.624 6.992L0 7.648V10.351L1.624 11.007C1.791 11.626 2.04 12.225 2.366 12.794L1.68 14.408L3.592 16.32L5.206 15.635C5.775 15.961 6.374 16.209 6.993 16.377L7.648 18H10.351L11.007 16.377C11.625 16.209 12.225 15.961 12.794 15.635L14.408 16.32L16.32 14.408L15.635 12.794C15.961 12.225 16.209 11.626 16.377 11.007L18 10.352V7.648L16.376 6.992ZM15.374 10.118L15.218 10.694C15.077 11.214 14.867 11.72 14.593 12.198L14.298 12.715L14.53 13.263L14.899 14.132L14.132 14.899L12.716 14.297L12.199 14.593C11.721 14.866 11.215 15.077 10.694 15.218L10.119 15.374L9.542 16.8H8.458L7.882 15.375L7.306 15.219C6.785 15.078 6.28 14.867 5.802 14.594L5.285 14.298L4.736 14.53L3.868 14.899L3.101 14.132L3.703 12.716L3.407 12.199C3.134 11.721 2.923 11.215 2.782 10.694L2.626 10.119L1.2 9.542V8.458L2.625 7.882L2.781 7.307C2.922 6.786 3.133 6.28 3.406 5.802L3.702 5.285L3.47 4.737L3.101 3.868L3.868 3.101L5.285 3.703L5.802 3.407C6.28 3.134 6.786 2.924 7.307 2.782L7.882 2.626L8.458 1.2H9.543L10.119 2.625L10.694 2.781C11.215 2.922 11.721 3.133 12.199 3.406L12.716 3.702L14.133 3.1L14.9 3.867L14.297 5.285L14.593 5.802C14.866 6.279 15.076 6.785 15.218 7.306L15.374 7.881L15.927 8.104L16.8 8.458V9.542L15.374 10.118ZM9 4.8C7.878 4.8 6.823 5.237 6.03 6.03C5.237 6.823 4.8 7.878 4.8 9C4.8 10.122 5.237 11.177 6.03 11.97C6.823 12.763 7.878 13.2 9 13.2C10.122 13.2 11.176 12.763 11.97 11.97C12.764 11.177 13.2 10.122 13.2 9C13.2 7.878 12.763 6.823 11.97 6.03C11.177 5.237 10.122 4.8 9 4.8ZM11.121 11.121C10.536 11.707 9.768 12 9 12C8.232 12 7.464 11.707 6.878 11.121C5.707 9.95 5.707 8.05 6.878 6.879C7.464 6.293 8.232 6 9 6C9.768 6 10.536 6.293 11.121 6.879C12.293 8.05 12.293 9.95 11.121 11.121Z" fill="currentColor"/>' +
    '</svg>';

  /* --------------------------------------------------------------------------------- */
  /* helpers                                                                            */
  /* --------------------------------------------------------------------------------- */

  function el(doc, tag, cls, html) {
    var n = doc.createElement(tag);
    if (cls) { n.className = cls; }
    if (html != null) { n.innerHTML = html; }
    return n;
  }

  function esc(s) {
    return String(s == null ? '' : s).replace(/[&<>"']/g, function (c) {
      return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c];
    });
  }

  function injectStyle(doc) {
    if (doc.getElementById(STYLE_ID)) { return; }
    var s = doc.createElement('style');
    s.id = STYLE_ID;
    s.textContent = CSS;
    (doc.head || doc.documentElement).appendChild(s);
  }

  /* The classlist token we care about: cn-<slug>. Returns the FIRST one found. */
  function cnClass(node) {
    if (!node || node.nodeType !== 1 || !node.classList) { return null; }
    for (var i = 0; i < node.classList.length; i++) {
      var t = node.classList[i];
      if (t.length > 3 && t.slice(0, 3) === 'cn-') { return t; }
    }
    return null;
  }

  /* Nearest ancestor-or-self carrying a cn-* class, stopping at the document. */
  function nearestComponent(node, stopDoc) {
    var n = node;
    while (n && n.nodeType === 1) {
      var c = cnClass(n);
      if (c) { return { node: n, cls: c }; }
      n = n.parentElement;
      if (stopDoc && n === stopDoc.documentElement) { break; }
    }
    return null;
  }

  /* cn-chart-line-dv -> chart-line ; cn-alert -> alert */
  function slugFromClass(cls) {
    var s = cls.slice(3);
    if (s.length > 3 && s.slice(-3) === '-dv') { s = s.slice(0, -3); }
    return s;
  }

  /* DEFAULT-SAFE name: derived from the class alone, no map needed. */
  function nameFromSlug(slug) {
    var words = slug.split('-').join(' ');
    return words.charAt(0).toUpperCase() + words.slice(1);
  }

  function readScriptConfig() {
    var s = document.currentScript;
    if (!s) {
      var all = document.getElementsByTagName('script');
      for (var i = all.length - 1; i >= 0; i--) {
        if ((all[i].src || '').indexOf('apollo-fab.js') > -1) { s = all[i]; break; }
      }
    }
    if (!s) { return { src: '' }; }
    var d = s.dataset || {};
    return {
      src: s.src || '',
      auto: d.auto !== 'off',
      reveal: d.reveal || REVEAL_DEFAULT,
      cornerSize: d.corner ? parseInt(d.corner, 10) : CORNER_DEFAULT,
      metaUrl: d.meta || null,
      zIndex: d.z ? parseInt(d.z, 10) : Z_DEFAULT
    };
  }

  var SCRIPT = readScriptConfig();

  function defaultMetaUrl() {
    if (SCRIPT.src) { return SCRIPT.src.replace(/apollo-fab\.js(\?.*)?$/, 'apollo-fab-meta.json'); }
    return 'apollo-fab-meta.json';
  }

  /* --------------------------------------------------------------------------------- */
  /* the instance                                                                       */
  /* --------------------------------------------------------------------------------- */

  function Fab(options) {
    var o = options || {};
    this.reveal = ({ always: 1, hotcorner: 1, summon: 1 })[o.reveal] ? o.reveal : REVEAL_DEFAULT;
    this.cornerSize = typeof o.cornerSize === 'number' && o.cornerSize > 0 ? o.cornerSize : CORNER_DEFAULT;
    this.zIndex = typeof o.zIndex === 'number' ? o.zIndex : Z_DEFAULT;
    this.metaUrl = o.metaUrl || defaultMetaUrl();
    this.frame = o.frame || null;                 /* an <iframe> to drive, or null      */
    this.container = o.container || null;         /* absolute inside this box, or fixed */
    this.hostDoc = (this.container ? this.container.ownerDocument : (o.hostDocument || document));
    this.label = o.label || '';
    this.showHint = o.showHint !== false && this.reveal === 'hotcorner';

    this.theme = o.theme || null;                 /* null => read it off the target     */
    this.mode = o.mode || null;
    this.open = false;
    this.revealed = this.reveal === 'always';
    this.inspect = false;
    this.meta = null;
    this.metaState = 'names';                     /* 'names' | 'loading' | 'full'       */
    this.blocked = false;                         /* frame unreachable (cross-origin)   */
    this._bound = [];
    this._shiftAt = 0;
    this._cornerAt = 0;
    this._hideTimer = null;

    this._build();
    this._readTargetState();
    this._paint();
    this._wire();
    this._loadMeta();
  }

  Fab.prototype._build = function () {
    var doc = this.hostDoc;
    injectStyle(doc);

    var layer = el(doc, 'div', 'apollo-fab');
    layer.setAttribute('data-apollo-fab', '');
    layer.setAttribute('data-reveal', this.reveal);
    layer.setAttribute('data-revealed', String(this.revealed));
    layer.setAttribute('data-open', 'false');
    layer.setAttribute('data-inspect', 'false');
    layer.style.setProperty('--af-z', String(this.zIndex));
    layer.style.setProperty('--af-corner', this.cornerSize + 'px');
    if (this.container) { layer.classList.add('af-contained'); }

    var hint = el(doc, 'div', 'af-hint');
    hint.setAttribute('aria-hidden', 'true');

    var sensor = el(doc, 'div', 'af-sensor');
    sensor.setAttribute('aria-hidden', 'true');

    var btn = el(doc, 'button', 'af-btn', GLYPH);
    btn.type = 'button';
    btn.setAttribute('aria-label', 'Apollo view controls');
    btn.setAttribute('aria-expanded', 'false');

    var panel = el(doc, 'div', 'af-panel');
    panel.setAttribute('role', 'group');
    panel.setAttribute('aria-label', 'Apollo view controls');

    panel.appendChild(el(doc, 'div', 'af-head',
      '<b>Apollo view controls</b><span>' + esc(this.label || 'v' + VERSION) + '</span>'));

    var gTheme = el(doc, 'div', 'af-grp');
    gTheme.appendChild(el(doc, 'span', 'af-lbl', 'Theme'));
    var rTheme = el(doc, 'div', 'af-row');
    rTheme.setAttribute('role', 'group');
    rTheme.setAttribute('aria-label', 'Apollo theme');
    for (var i = 0; i < THEMES.length; i++) {
      var b = el(doc, 'button', null, esc(THEMES[i][1]));
      b.type = 'button';
      b.setAttribute('data-af-theme', THEMES[i][0]);
      b.setAttribute('aria-pressed', 'false');
      rTheme.appendChild(b);
    }
    gTheme.appendChild(rTheme);

    var gMode = el(doc, 'div', 'af-grp');
    gMode.appendChild(el(doc, 'span', 'af-lbl', 'Mode'));
    var rMode = el(doc, 'div', 'af-row');
    rMode.setAttribute('role', 'group');
    rMode.setAttribute('aria-label', 'Light or dark');
    for (var j = 0; j < MODES.length; j++) {
      var m = el(doc, 'button', null, esc(MODES[j][1]));
      m.type = 'button';
      m.setAttribute('data-af-mode', MODES[j][0]);
      m.setAttribute('aria-pressed', 'false');
      rMode.appendChild(m);
    }
    gMode.appendChild(rMode);

    var gIns = el(doc, 'div', 'af-grp');
    gIns.appendChild(el(doc, 'span', 'af-lbl', 'Provenance'));
    var rIns = el(doc, 'div', 'af-row');
    var ib = el(doc, 'button', null, 'Inspect components');
    ib.type = 'button';
    ib.setAttribute('data-af-inspect', '');
    ib.setAttribute('aria-pressed', 'false');
    rIns.appendChild(ib);
    gIns.appendChild(rIns);
    gIns.appendChild(el(doc, 'p', 'af-note', ''));

    panel.appendChild(gTheme);
    panel.appendChild(gMode);
    panel.appendChild(gIns);

    var ink = el(doc, 'div', 'af-ink');
    var box = el(doc, 'div', 'af-box');
    var tip = el(doc, 'div', 'af-tip');
    ink.appendChild(box);
    ink.appendChild(tip);

    layer.appendChild(hint);
    layer.appendChild(sensor);
    layer.appendChild(panel);
    layer.appendChild(btn);
    layer.appendChild(ink);

    (this.container || doc.body || doc.documentElement).appendChild(layer);

    this.layer = layer;
    this.sensor = sensor;
    this.btn = btn;
    this.panel = panel;
    this.box = box;
    this.tip = tip;
    this.note = gIns.querySelector('.af-note');
    this.inspectBtn = ib;

    this.applyTokenMode();
  };

  /* PITFALL 1 — probe for canon's alias layer on the HOST document (the layer inherits
     from there). Empty string => the page has no canon vars => keep the hard neutral
     pair defined on .apollo-fab. Re-probeable: call again after a stylesheet lands. */
  Fab.prototype.applyTokenMode = function () {
    var has = false;
    try {
      var root = this.hostDoc.documentElement;
      var probe = this.hostDoc.defaultView.getComputedStyle(root).getPropertyValue('--surface');
      has = !!(probe && probe.trim());
    } catch (e) { has = false; }
    this.layer.classList.toggle('af-tokens', has);
    this.tokenMode = has ? 'canon' : 'fallback';
    return this.tokenMode;
  };

  /* --------------------------------------------------------------------------------- */
  /* target resolution — the document the CONTROLS drive                                 */
  /* --------------------------------------------------------------------------------- */

  /* Returns the target document, or null when a frame was named but is unreachable.
     A file:// iframe is its own origin in Chrome, so contentDocument throws or is null.
     That is not an error state: the caller falls back to the host document and the
     panel says so in plain words. */
  Fab.prototype.frameDoc = function () {
    if (!this.frame) { return null; }
    var d = null;
    try { d = this.frame.contentDocument; } catch (e) { d = null; }
    if (!d || !d.documentElement) { return null; }
    return d;
  };

  Fab.prototype.targetDoc = function () {
    if (this.frame) {
      var d = this.frameDoc();
      this.blocked = !d;
      if (d) { return d; }
    }
    return this.hostDoc;
  };

  /* Documents the inspector and the corner watcher listen on. */
  Fab.prototype.listenDocs = function () {
    var docs = [this.hostDoc];
    var d = this.frameDoc();
    if (d && docs.indexOf(d) < 0) { docs.push(d); }
    return docs;
  };

  Fab.prototype._readTargetState = function () {
    var d = this.targetDoc();
    var r = d.documentElement;
    if (!this.theme) {
      this.theme = r.getAttribute('data-apollo-theme') ||
        (d.body && d.body.getAttribute('data-apollo-theme')) || 'mono';
    }
    if (!this.mode) {
      this.mode = r.getAttribute('data-theme') ||
        (d.body && d.body.getAttribute('data-theme')) || 'light';
    }
  };

  /* --------------------------------------------------------------------------------- */
  /* painting state                                                                     */
  /* --------------------------------------------------------------------------------- */

  Fab.prototype._paint = function () {
    var d = this.targetDoc();
    var self = this;

    function set(node, attr, val) {
      if (node) { try { node.setAttribute(attr, val); } catch (e) { self.blocked = true; } }
    }
    set(d.documentElement, 'data-apollo-theme', this.theme);
    set(d.body, 'data-apollo-theme', this.theme);
    set(d.documentElement, 'data-theme', this.mode);
    set(d.body, 'data-theme', this.mode);

    var t = this.panel.querySelectorAll('[data-af-theme]');
    for (var i = 0; i < t.length; i++) {
      t[i].setAttribute('aria-pressed', String(t[i].getAttribute('data-af-theme') === this.theme));
    }
    var m = this.panel.querySelectorAll('[data-af-mode]');
    for (var j = 0; j < m.length; j++) {
      m[j].setAttribute('aria-pressed', String(m[j].getAttribute('data-af-mode') === this.mode));
    }
    /* Sensor only where the coordinate watcher cannot hear: a named frame that turned
       out to be unreachable, in a reveal mode that needs the corner. */
    this.sensorOn = !!(this.frame && this.blocked && this.reveal !== 'always');
    this.layer.setAttribute('data-sensor', this.sensorOn ? 'on' : 'off');

    this.inspectBtn.setAttribute('aria-pressed', String(this.inspect));
    this.layer.setAttribute('data-inspect', String(this.inspect));
    this.layer.setAttribute('data-open', String(this.open));
    this.layer.setAttribute('data-revealed', String(this.revealed));
    this.btn.setAttribute('aria-expanded', String(this.open));

    /* When the host page carries canon vars the FAB re-themes with it, so keep the
       probe honest after a theme change on the host itself. */
    if (this.targetDoc() === this.hostDoc) { this.applyTokenMode(); }

    this._paintNote();
  };

  Fab.prototype._paintNote = function () {
    var lines = [];
    if (this.frame && this.blocked) {
      lines.push('Frame unreachable — <code>file://</code> treats it as another origin, ' +
        'so these controls are driving <em>this</em> page instead. Serve over HTTP to drive the frame.');
      if (this.sensorOn) {
        lines.push('The corner is a real hit zone here, only because pointer events inside a ' +
          'walled-off frame never reach this page; on a normal page it is measured, and takes nothing.');
      }
    }
    if (this.metaState === 'full') {
      lines.push('Component map loaded — hover names the component, its category and its purpose.');
    } else if (this.metaState === 'loading') {
      lines.push('Loading the component map…');
    } else {
      lines.push('No component map (normal on <code>file://</code>) — hover still names ' +
        'each component from its <code>cn-*</code> class.');
    }
    this.note.innerHTML = lines.join(' ');
  };

  /* --------------------------------------------------------------------------------- */
  /* meta map — optional upgrade, never a dependency                                     */
  /* --------------------------------------------------------------------------------- */

  Fab.prototype._loadMeta = function () {
    var self = this;
    if (typeof global.fetch !== 'function') { return; }
    this.metaState = 'loading';
    this._paintNote();
    var done = function (state, data) {
      self.meta = data || null;
      self.metaState = state;
      self._paintNote();
    };
    try {
      global.fetch(this.metaUrl, { cache: 'no-cache' })
        .then(function (r) { return r.ok ? r.json() : Promise.reject(new Error(String(r.status))); })
        .then(function (j) {
          done(j && j.components ? 'full' : 'names', j && j.components ? j.components : null);
        })
        .catch(function () { done('names', null); });   /* DEFAULT-SAFE, not an error */
    } catch (e) {
      done('names', null);
    }
  };

  /* --------------------------------------------------------------------------------- */
  /* geometry                                                                           */
  /* --------------------------------------------------------------------------------- */

  /* Layer-space rect for a point/rect coming from `doc`. When doc is the frame, the
     frame's own viewport rect is added; when the layer is container-absolute, the
     container rect is subtracted. */
  Fab.prototype._offset = function (doc) {
    var ox = 0, oy = 0;
    if (this.frame && doc !== this.hostDoc) {
      var fr = this.frame.getBoundingClientRect();
      ox += fr.left; oy += fr.top;
    }
    if (this.container) {
      var cr = this.container.getBoundingClientRect();
      ox -= cr.left; oy -= cr.top;
    }
    return { x: ox, y: oy };
  };

  Fab.prototype._layerSize = function () {
    if (this.container) {
      var cr = this.container.getBoundingClientRect();
      return { w: cr.width, h: cr.height };
    }
    return { w: this.hostDoc.documentElement.clientWidth, h: this.hostDoc.documentElement.clientHeight };
  };

  /* --------------------------------------------------------------------------------- */
  /* wiring                                                                             */
  /* --------------------------------------------------------------------------------- */

  Fab.prototype._on = function (node, type, fn, opts) {
    node.addEventListener(type, fn, opts || false);
    this._bound.push([node, type, fn, opts || false]);
  };

  Fab.prototype._wire = function () {
    var self = this;

    this._on(this.btn, 'click', function () { self.toggle(); });

    this._on(this.panel, 'click', function (e) {
      var t = e.target.closest ? e.target.closest('button') : null;
      if (!t) { return; }
      if (t.hasAttribute('data-af-theme')) { self.setTheme(t.getAttribute('data-af-theme')); }
      else if (t.hasAttribute('data-af-mode')) { self.setMode(t.getAttribute('data-af-mode')); }
      else if (t.hasAttribute('data-af-inspect')) { self.setInspector(!self.inspect); }
    });

    /* Esc closes the panel; in summon mode it also puts the FAB away again. */
    this._on(this.hostDoc, 'keydown', function (e) { self._key(e); });

    /* The sensor mirrors the coordinate watcher exactly — same reveal rules, same
       double-tap rule for summon. It is hidden (display:none) unless the frame is
       walled off, so on a normal page these listeners never fire. */
    this._on(this.sensor, 'pointerenter', function (e) {
      if (self.reveal === 'hotcorner' && e.pointerType === 'mouse') { self._show(); }
    });
    /* Same blindness on the way out: with the frame walled off there is no pointermove
       to tell us the cursor left. Hotcorner therefore also retreats when the pointer
       leaves the FAB itself. Summon does not — C stays until Esc, by design. */
    var keep = function () {
      if (self._hideTimer) { clearTimeout(self._hideTimer); self._hideTimer = null; }
    };
    var leave = function () {
      if (self.sensorOn && self.reveal === 'hotcorner') { self._hideSoon(); }
    };
    this._on(this.btn, 'pointerenter', keep);
    this._on(this.panel, 'pointerenter', keep);
    this._on(this.btn, 'pointerleave', leave);
    this._on(this.panel, 'pointerleave', leave);

    this._on(this.sensor, 'pointerdown', function () {
      if (self.reveal === 'hotcorner') { self._show(); return; }
      var now = Date.now();
      if (now - self._cornerAt < 500) { self._show(); self._cornerAt = 0; }
      else { self._cornerAt = now; }
    });

    /* Re-attach to the frame each time it loads, and re-read its authored theme. */
    if (this.frame) {
      this._on(this.frame, 'load', function () {
        self._attachDocs();
        self.blocked = !self.frameDoc();
        self._paint();
      });
    }

    this._attachDocs();
  };

  /* Listeners that must live on every reachable document (host + frame). Re-entrant:
     always detaches first, so a frame reload cannot double-bind. */
  Fab.prototype._attachDocs = function () {
    var self = this;
    if (this._docBound) {
      for (var k = 0; k < this._docBound.length; k++) {
        var b = this._docBound[k];
        try { b[0].removeEventListener(b[1], b[2], b[3]); } catch (e) { /* gone */ }
      }
    }
    this._docBound = [];

    var docs = this.listenDocs();
    for (var i = 0; i < docs.length; i++) {
      var d = docs[i];
      var passive = { passive: true, capture: true };

      var move = (function (doc) {
        return function (e) { self._pointer(e, doc); };
      })(d);
      var over = (function (doc) {
        return function (e) { self._hover(e, doc); };
      })(d);
      var down = (function (doc) {
        return function (e) { self._cornerTap(e, doc); };
      })(d);
      var key = function (e) { self._key(e); };
      var away = function () { self._hideTip(); };

      d.addEventListener('pointermove', move, passive);
      d.addEventListener('pointerover', over, passive);
      d.addEventListener('pointerdown', down, passive);
      d.addEventListener('scroll', away, passive);
      if (d !== this.hostDoc) { d.addEventListener('keydown', key, passive); }

      this._docBound.push([d, 'pointermove', move, passive]);
      this._docBound.push([d, 'pointerover', over, passive]);
      this._docBound.push([d, 'pointerdown', down, passive]);
      this._docBound.push([d, 'scroll', away, passive]);
      if (d !== this.hostDoc) { this._docBound.push([d, 'keydown', key, passive]); }
    }
  };

  /* --------------------------------------------------------------------------------- */
  /* reveal behaviour                                                                   */
  /* --------------------------------------------------------------------------------- */

  /* Distance from the pointer to the bottom-right corner of the LAYER, in layer space.
     Coordinate maths, never a hit-testing element — so nothing beneath the corner is
     ever intercepted (pitfall 4, and it keeps variant B honest on a real page). */
  Fab.prototype._inCorner = function (e, doc) {
    var off = this._offset(doc);
    var size = this._layerSize();
    var x = e.clientX + off.x;
    var y = e.clientY + off.y;
    return x >= size.w - this.cornerSize && y >= size.h - this.cornerSize &&
      x <= size.w && y <= size.h;
  };

  Fab.prototype._pointer = function (e, doc) {
    if (this.reveal === 'always') { return; }
    if (this.reveal === 'hotcorner') {
      if (this._inCorner(e, doc)) {
        this._show();
      } else if (this.revealed && !this.open) {
        var off = this._offset(doc);
        var size = this._layerSize();
        var x = e.clientX + off.x, y = e.clientY + off.y;
        /* Generous exit zone so the pointer can travel to the button without losing it. */
        var slack = this.cornerSize + 88;
        if (x < size.w - slack || y < size.h - slack) { this._hideSoon(); }
      }
    }
  };

  Fab.prototype._cornerTap = function (e, doc) {
    if (this.reveal === 'always') { return; }
    /* PITFALL 3 — touch has no hover. A tap (or a click) in the same corner zone
       reveals the FAB. Passive listener, no preventDefault: whatever is under the
       corner still receives the tap. */
    if (!this._inCorner(e, doc)) { return; }
    if (this.reveal === 'hotcorner') { this._show(); return; }
    /* summon: a DOUBLE tap in the corner, so a single stray tap stays inert */
    var now = Date.now();
    if (now - this._cornerAt < 500) { this._show(); this._cornerAt = 0; }
    else { this._cornerAt = now; }
  };

  Fab.prototype._key = function (e) {
    if (e.key === 'Escape') {
      if (this.open) { this.close(); }
      else if (this.reveal !== 'always') { this._hide(); }
      return;
    }
    /* summon: double-press of Shift within 500ms */
    if (this.reveal === 'summon' && e.key === 'Shift') {
      var now = Date.now();
      if (now - this._shiftAt < 500) { this._show(); this._shiftAt = 0; }
      else { this._shiftAt = now; }
    }
  };

  Fab.prototype._show = function () {
    if (this._hideTimer) { clearTimeout(this._hideTimer); this._hideTimer = null; }
    if (this.revealed) { return; }
    this.revealed = true;
    this._paint();
  };

  Fab.prototype._hide = function () {
    if (this.reveal === 'always') { return; }
    this.revealed = false;
    this.open = false;
    this._paint();
  };

  Fab.prototype._hideSoon = function () {
    var self = this;
    if (this._hideTimer) { return; }
    this._hideTimer = setTimeout(function () {
      self._hideTimer = null;
      if (!self.open) { self._hide(); }
    }, 600);
  };

  /* --------------------------------------------------------------------------------- */
  /* the provenance inspector                                                           */
  /* --------------------------------------------------------------------------------- */

  Fab.prototype._hover = function (e, doc) {
    if (!this.inspect) { return; }
    var t = e.target;
    if (!t || t.nodeType !== 1) { return; }
    /* Never inspect our own chrome. */
    if (this.layer.contains(t)) { this._hideTip(); return; }

    var hit = nearestComponent(t, doc);
    if (!hit) { this._hideTip(); return; }

    var slug = slugFromClass(hit.cls);
    var row = (this.meta && this.meta[slug]) || null;
    var name = row && row.n ? row.n : nameFromSlug(slug);

    var html = '<strong>' + esc(name) + '</strong>' +
      '<span class="af-cls">.' + esc(hit.cls) + '</span>';
    if (row && row.p) { html += '<span class="af-purpose">' + esc(row.p) + '</span>'; }
    var bits = [];
    if (row && row.c) { bits.push(esc(row.c)); }
    if (row && row.v) { bits.push('tokens ' + esc(row.v)); }
    if (!row) { bits.push('class-name only — no component map loaded'); }
    html += '<span class="af-meta">' + bits.join(' · ') + '</span>';
    this.tip.innerHTML = html;

    var r = hit.node.getBoundingClientRect();
    var off = this._offset(doc);
    var size = this._layerSize();

    var bx = r.left + off.x, by = r.top + off.y;
    this.box.style.display = 'block';
    this.box.style.left = bx + 'px';
    this.box.style.top = by + 'px';
    this.box.style.width = r.width + 'px';
    this.box.style.height = r.height + 'px';

    this.tip.style.display = 'block';
    var tw = this.tip.offsetWidth, th = this.tip.offsetHeight;
    var tx = Math.min(Math.max(bx, 8), Math.max(8, size.w - tw - 8));
    var ty = by - th - 8;
    if (ty < 8) { ty = by + r.height + 8; }
    /* Clamp INTO the layer. The hovered element can sit entirely outside it — the
       #227 readings page inspects a strip that lives above the pane — and an
       unclamped tooltip would then be drawn off the top of its own pane. */
    ty = Math.min(Math.max(ty, 8), Math.max(8, size.h - th - 8));
    this.tip.style.left = tx + 'px';
    this.tip.style.top = ty + 'px';
  };

  Fab.prototype._hideTip = function () {
    this.box.style.display = 'none';
    this.tip.style.display = 'none';
  };

  /* --------------------------------------------------------------------------------- */
  /* public API                                                                         */
  /* --------------------------------------------------------------------------------- */

  Fab.prototype.setTheme = function (t) { this.theme = t; this._paint(); return this; };
  Fab.prototype.setMode = function (m) { this.mode = m; this._paint(); return this; };
  Fab.prototype.setInspector = function (on) {
    this.inspect = !!on;
    if (!this.inspect) { this._hideTip(); }
    this._paint();
    return this;
  };
  Fab.prototype.openPanel = function () { this.open = true; this._paint(); return this; };
  Fab.prototype.close = function () { this.open = false; this._paint(); return this; };
  Fab.prototype.toggle = function () { this.open = !this.open; this._paint(); return this; };
  Fab.prototype.setHint = function (on) {
    this.layer.setAttribute('data-hint', on ? 'on' : 'off');
    return this;
  };

  Fab.prototype.destroy = function () {
    var i, b;
    for (i = 0; i < this._bound.length; i++) {
      b = this._bound[i];
      try { b[0].removeEventListener(b[1], b[2], b[3]); } catch (e) { /* gone */ }
    }
    for (i = 0; i < (this._docBound || []).length; i++) {
      b = this._docBound[i];
      try { b[0].removeEventListener(b[1], b[2], b[3]); } catch (e) { /* gone */ }
    }
    this._bound = []; this._docBound = [];
    if (this.layer && this.layer.parentNode) { this.layer.parentNode.removeChild(this.layer); }
    var ix = ApolloFAB.instances.indexOf(this);
    if (ix > -1) { ApolloFAB.instances.splice(ix, 1); }
  };

  var ApolloFAB = {
    version: VERSION,
    THEMES: THEMES,
    CORNER_DEFAULT: CORNER_DEFAULT,
    Z_DEFAULT: Z_DEFAULT,
    instances: [],
    /* Exported so the class -> component-name derivation can be DRIVEN outside a
       browser (node), against the real cn-* classes a real page carries. Not API. */
    _util: {
      cnClass: cnClass,
      nearestComponent: nearestComponent,
      slugFromClass: slugFromClass,
      nameFromSlug: nameFromSlug
    },
    mount: function (options) {
      var f = new Fab(options);
      ApolloFAB.instances.push(f);
      return f;
    }
  };

  global.ApolloFAB = ApolloFAB;

  /* Auto-mount for the single-<script>-tag case. A page that mounts its own instances
     (like the #227 readings page) sets data-auto="off". */
  if (SCRIPT.auto) {
    var boot = function () {
      if (!ApolloFAB.instances.length) {
        ApolloFAB.mount({
          reveal: SCRIPT.reveal,
          cornerSize: SCRIPT.cornerSize,
          metaUrl: SCRIPT.metaUrl,
          zIndex: SCRIPT.zIndex
        });
      }
    };
    if (document.readyState === 'loading') {
      document.addEventListener('DOMContentLoaded', boot, { once: true });
    } else {
      boot();
    }
  }
})(typeof window !== 'undefined' ? window : this);
