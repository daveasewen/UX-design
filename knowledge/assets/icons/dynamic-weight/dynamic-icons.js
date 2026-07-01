/*
  dynamic-icons.js — builder-usable source for the dynamic-weight icon set.

  77 icons on a 24x24 grid (HSBC catalogue used as visual reference; the HSBC
  originals are FILLED and can't be re-weighted). Everything is controllable from CSS:

    --icon-stroke   line thickness  (bind it to the label's font-weight + size)
    --icon-color    colour          (applied via currentColor, inherits your tokens)
    --icon-size     scale           (any length)

  CALIBRATED THICKNESS (from icon-weight-decisions.json, locked 2026-06-23):
    ICON_STROKE[weight][size] gives the agreed on-screen stroke in px.
    strokeFor(weight, size) interpolates for in-between sizes.

  THREE WAYS TO USE
  -----------------
  1) Auto component — <dyn-icon name="search" weight="400" size="24"></dyn-icon>
     Looks up the calibrated thickness automatically. (color="..." optional.)
  2) Raw markup + your own CSS — DYN_ICONS["search"] is a full <svg> string.
  3) CSS vars — see snippet at the bottom of this comment.

  RECOMMENDED CSS (manual route):
    .icon{
      --icon-stroke:1.4;          // e.g. ICON_STROKE[400][16]
      --icon-color:#333333;
      --icon-size:16px;
      display:inline-flex; width:var(--icon-size); height:var(--icon-size); color:var(--icon-color);
    }
    .icon svg{ fill:none; stroke:currentColor; stroke-linecap:round; stroke-linejoin:round; }
    .icon svg *{ stroke-width:var(--icon-stroke); vector-effect:non-scaling-stroke; }
*/

(function (global) {

  // ---- calibrated stroke table (px), from icon-weight-decisions.json ----
  var ICON_STROKE = {
    300: { 14: 0.6,  16: 0.7,  20: 0.85, 24: 1.0,  32: 1.35 },
    400: { 14: 1.2,  16: 1.4,  20: 1.7,  24: 2.05, 32: 2.75 },
    500: { 14: 1.65, 16: 1.9,  20: 2.35, 24: 2.8,  32: 3.75 },
    700: { 14: 2.1,  16: 2.4,  20: 3.0,  24: 3.6,  32: 4.8  }
  };
  var WEIGHTS = [300, 400, 500, 700];

  // nearest weight + linear interpolation across size (proportional beyond the table)
  function strokeFor(weight, size) {
    var w = WEIGHTS.reduce(function (a, b) { return Math.abs(b - weight) < Math.abs(a - weight) ? b : a; });
    var row = ICON_STROKE[w];
    var sizes = Object.keys(row).map(Number).sort(function (a, b) { return a - b; });
    var lo = sizes[0], hi = sizes[sizes.length - 1], px;
    if (size <= lo) px = row[lo] * (size / lo);
    else if (size >= hi) px = row[hi] * (size / hi);
    else {
      for (var i = 0; i < sizes.length - 1; i++) {
        if (size >= sizes[i] && size <= sizes[i + 1]) {
          var t = (size - sizes[i]) / (sizes[i + 1] - sizes[i]);
          px = row[sizes[i]] + (row[sizes[i + 1]] - row[sizes[i]]) * t;
          break;
        }
      }
    }
    return Math.round(px * 100) / 100;
  }

  // ---- gear path generated so the geometry is exact ----
  function gearOuterD() {
    var cx = 12, cy = 12, n = 8, Rt = 9.5, Rb = 6.7, step = 2 * Math.PI / n, tip = step * 0.26;
    var P = function (a, r) { return [(cx + r * Math.cos(a)).toFixed(2), (cy + r * Math.sin(a)).toFixed(2)]; };
    var d = '';
    for (var k = 0; k < n; k++) {
      var a = k * step;
      var v1 = P(a - step / 2, Rb), t1 = P(a - tip, Rt), t2 = P(a + tip, Rt), v2 = P(a + step / 2, Rb);
      d += (k === 0 ? 'M' + v1[0] + ' ' + v1[1] : 'L' + v1[0] + ' ' + v1[1]) +
           'L' + t1[0] + ' ' + t1[1] + 'L' + t2[0] + ' ' + t2[1] + 'L' + v2[0] + ' ' + v2[1];
    }
    return d + 'Z';
  }
  function gearPath() { return '<path d="' + gearOuterD() + '"/><circle cx="12" cy="12" r="3"/>'; }

  // ---- geometry only (no stroke/fill/size baked in; CSS drives all of that) ----
  var PATHS = {
    // core 8
    close:        '<path d="M6 6L18 18M18 6L6 18"/>',
    plus:         '<path d="M12 5V19M5 12H19"/>',
    check:        '<path d="M5 12.5L9.5 17L19.5 6"/>',
    chevron:      '<path d="M9 6L15 12L9 18"/>',
    search:       '<circle cx="10.5" cy="10.5" r="6.5"/><path d="M15.2 15.2L20 20"/>',
    arrow:        '<path d="M4 12H20"/><path d="M14 6L20 12L14 18"/>',
    info:         '<circle cx="12" cy="12" r="9"/><path d="M12 10.5V16"/><path d="M12 7.8V7.81"/>',
    menu:         '<path d="M4 7H20M4 12H20M4 17H20"/>',

    // essential actions
    settings:     gearPath(),
    filter:       '<path d="M4 5L20 5L13.5 13L13.5 18.5L10.5 20.5L10.5 13L4 5Z"/>',
    edit:         '<path d="M4 20L4 15.5L15.5 4L20 8.5L8.5 20L4 20Z"/><path d="M13 6.5L17.5 11"/>',
    trash:        '<path d="M5 7H19"/><path d="M9 7V4.8H15V7"/><path d="M6.6 7L7.6 20H16.4L17.4 7"/><path d="M10 10.5V16.5M14 10.5V16.5"/>',
    download:     '<path d="M12 4V15"/><path d="M7 10.5L12 15.5L17 10.5"/><path d="M5 19H19"/>',
    upload:       '<path d="M12 15.5V4.5"/><path d="M7 9.5L12 4.5L17 9.5"/><path d="M5 19H19"/>',
    share:        '<circle cx="6" cy="12" r="2.6"/><circle cx="18" cy="6" r="2.6"/><circle cx="18" cy="18" r="2.6"/><path d="M8.3 10.8L15.7 7.2M8.3 13.2L15.7 16.8"/>',
    copy:         '<path d="M8 8H20V20H8Z"/><path d="M16 8V4H4V16H8"/>',
    refresh:      '<path d="M19.5 7.5A8 8 0 1 0 21 13"/><path d="M19.5 3V8H14.5"/>',
    more:         '<path d="M12 5V5.01M12 12V12.01M12 19V19.01"/>',
    'external-link':'<path d="M13 5H19V11"/><path d="M19 5L10.5 13.5"/><path d="M17 13.5V19H5V7H10.5"/>',
    'plus-circle':'<circle cx="12" cy="12" r="8.5"/><path d="M12 8V16M8 12H16"/>',

    // navigation & arrows
    'chevron-up':   '<path d="M6 15L12 9L18 15"/>',
    'chevron-down': '<path d="M6 9L12 15L18 9"/>',
    'chevron-left': '<path d="M15 6L9 12L15 18"/>',
    'arrow-up':     '<path d="M12 20V4"/><path d="M6 10L12 4L18 10"/>',
    'arrow-down':   '<path d="M12 4V20"/><path d="M6 14L12 20L18 14"/>',
    'arrow-left':   '<path d="M20 12H4"/><path d="M10 6L4 12L10 18"/>',
    home:           '<path d="M4 11L12 4L20 11"/><path d="M6 9.5V20H18V9.5"/><path d="M10 20V14H14V20"/>',
    expand:         '<path d="M4 9V4H9"/><path d="M20 9V4H15"/><path d="M4 15V20H9"/><path d="M20 15V20H15"/>',
    collapse:       '<path d="M9 4V9H4"/><path d="M15 4V9H20"/><path d="M9 20V15H4"/><path d="M15 20V15H20"/>',
    back:           '<path d="M10 6L4 12L10 18"/><path d="M4 12H14A5 5 0 0 1 14 22H12.5"/>',

    // status & alerts
    'check-circle': '<circle cx="12" cy="12" r="8.5"/><path d="M8 12.5L11 15.5L16.5 9"/>',
    'x-circle':     '<circle cx="12" cy="12" r="8.5"/><path d="M9 9L15 15M15 9L9 15"/>',
    'alert-triangle':'<path d="M12 4L21 19H3L12 4Z"/><path d="M12 10V14"/><path d="M12 16.4V16.41"/>',
    'alert-circle': '<circle cx="12" cy="12" r="8.5"/><path d="M12 7.5V13"/><path d="M12 15.6V15.61"/>',
    'help-circle':  '<circle cx="12" cy="12" r="8.5"/><path d="M9.4 9.6A2.7 2.7 0 1 1 12.4 12.4C11.9 12.7 11.9 13.2 11.9 13.9"/><path d="M12 16.4V16.41"/>',
    bell:           '<path d="M6 17.5H18"/><path d="M8 17.5V11A4 4 0 0 1 16 11V17.5"/><path d="M12 6.6V4.6"/><path d="M10.2 20.5A2 2 0 0 0 13.8 20.5"/>',
    eye:            '<path d="M2.5 12C2.5 12 6 6.5 12 6.5C18 6.5 21.5 12 21.5 12C21.5 12 18 17.5 12 17.5C6 17.5 2.5 12 2.5 12Z"/><circle cx="12" cy="12" r="2.6"/>',
    'eye-off':      '<path d="M2.5 12C2.5 12 6 6.5 12 6.5C18 6.5 21.5 12 21.5 12C21.5 12 18 17.5 12 17.5C6 17.5 2.5 12 2.5 12Z"/><circle cx="12" cy="12" r="2.6"/><path d="M4 4L20 20"/>',
    lock:           '<path d="M6 11H18V20H6Z"/><path d="M8.5 11V8A3.5 3.5 0 0 1 15.5 8V11"/><path d="M12 14.3V16.6"/>',
    unlock:         '<path d="M6 11H18V20H6Z"/><path d="M8.5 11V8A3.5 3.5 0 0 1 15.3 6.6"/><path d="M12 14.3V16.6"/>',
    'shield-check': '<path d="M12 3L19 6V11C19 16 12 21 12 21C12 21 5 16 5 11V6L12 3Z"/><path d="M9 12L11.2 14.2L15.2 9.8"/>',
    ban:            '<circle cx="12" cy="12" r="8.5"/><path d="M6 6L18 18"/>',

    // people & comms
    user:           '<circle cx="12" cy="8" r="4"/><path d="M4.5 20C4.5 16 7.5 14 12 14C16.5 14 19.5 16 19.5 20"/>',
    users:          '<circle cx="9" cy="8.5" r="3.3"/><path d="M3 19.5C3 16 5.5 14.3 9 14.3C12.5 14.3 15 16 15 19.5"/><path d="M16 5.6A3.3 3.3 0 0 1 16 11.4"/><path d="M17.2 14.4C19.5 14.9 21 16.5 21 19.5"/>',
    mail:           '<path d="M3.5 6H20.5V18H3.5V6Z"/><path d="M4 6.5L12 12.5L20 6.5"/>',
    phone:          '<path d="M21 16.9V19a2 2 0 0 1-2.2 2 19.8 19.8 0 0 1-8.6-3.1 19.5 19.5 0 0 1-6-6A19.8 19.8 0 0 1 1.1 3.3 2 2 0 0 1 3.1 1h2.8a2 2 0 0 1 2 1.7c.1 1 .4 1.9.7 2.8a2 2 0 0 1-.5 2.1L6.9 10.8a16 16 0 0 0 6 6l1.2-1.2a2 2 0 0 1 2.1-.5c.9.3 1.8.6 2.8.7a2 2 0 0 1 1.7 2Z"/>',
    message:        '<path d="M4 5H20V16H8L4 20V5Z"/>',
    calendar:       '<path d="M4.5 6H19.5V20H4.5V6Z"/><path d="M4.5 10H19.5"/><path d="M8 4V7M16 4V7"/>',
    clock:          '<circle cx="12" cy="12" r="8.5"/><path d="M12 7V12L15.5 14"/>',
    star:           '<path d="M12 3.5L14.6 9.2L20.8 9.9L16.2 14.1L17.5 20.2L12 17.05L6.5 20.2L7.8 14.1L3.2 9.9L9.4 9.2L12 3.5Z"/>',
    heart:          '<path d="M12 20.5C12 20.5 3.5 15 3.5 8.8C3.5 6 5.7 4 8.2 4C10 4 11.4 5.1 12 6.4C12.6 5.1 14 4 15.8 4C18.3 4 20.5 6 20.5 8.8C20.5 15 12 20.5 12 20.5Z"/>',
    bookmark:       '<path d="M7 4H17V20L12 16L7 20V4Z"/>',

    // media & common
    play:           '<path d="M7 5L19 12L7 19V5Z"/>',
    pause:          '<path d="M9 5V19M15 5V19"/>',
    stop:           '<path d="M6 6H18V18H6Z"/>',
    volume:         '<path d="M4 9.5H7L11.5 5.5V18.5L7 14.5H4V9.5Z"/><path d="M15 9A4 4 0 0 1 15 15"/>',
    mute:           '<path d="M4 9.5H7L11.5 5.5V18.5L7 14.5H4V9.5Z"/><path d="M15.5 9.5L20.5 14.5M20.5 9.5L15.5 14.5"/>',
    image:          '<path d="M4 5H20V19H4V5Z"/><circle cx="9" cy="10" r="1.8"/><path d="M4 16.5L9.5 12L13.5 15.5L16.5 13L20 16.5"/>',
    file:           '<path d="M6 3.5H14L19 8.5V20.5H6V3.5Z"/><path d="M14 3.5V8.5H19"/>',
    folder:         '<path d="M3.5 6.5H10L12 9H20.5V18.5H3.5V6.5Z"/>',
    link:           '<path d="M9.5 14.5L14.5 9.5"/><path d="M11 7L13 5A4 4 0 0 1 19 11L17 13"/><path d="M13 17L11 19A4 4 0 0 1 5 13L7 11"/>',
    tag:            '<path d="M4 4H11L20 13L13 20L4 11V4Z"/><circle cx="7.6" cy="7.6" r="1.3"/>',
    'map-pin':      '<path d="M12 21C12 21 18.5 14.5 18.5 9.5A6.5 6.5 0 0 0 5.5 9.5C5.5 14.5 12 21 12 21Z"/><circle cx="12" cy="9.5" r="2.4"/>',
    globe:          '<circle cx="12" cy="12" r="8.5"/><path d="M3.5 12H20.5"/><path d="M12 3.5C14.6 6 14.6 18 12 20.5C9.4 18 9.4 6 12 3.5Z"/>',
    camera:         '<path d="M3.5 8H7L8.5 5.5H15.5L17 8H20.5V19H3.5V8Z"/><circle cx="12" cy="13" r="3.3"/>',
    send:           '<path d="M21 4L3 11.5L10 13.5L12.5 20.5L21 4Z"/><path d="M10 13.5L21 4"/>',
    minus:          '<path d="M5 12H19"/>',
    'minus-circle': '<circle cx="12" cy="12" r="8.5"/><path d="M8 12H16"/>',

    // arrows & chevrons (HSBC catalogue group)
    // chevrons = outline / variable weight (the -thick source files collapse into the weight axis)
    'chevron-right':       '<path d="M9 6L15 12L9 18"/>',
    'chevron-double-up':   '<path d="M6 12L12 7L18 12"/><path d="M6 17L12 12L18 17"/>',
    'chevron-double-down': '<path d="M6 7L12 12L18 7"/><path d="M6 12L12 17L18 12"/>',
    'chevron-double-left': '<path d="M18 7L13 12L18 17"/><path d="M12 7L7 12L12 17"/>',
    'chevron-double-right':'<path d="M6 7L11 12L6 17"/><path d="M12 7L17 12L12 17"/>',
    // carets = HSBC's solid "Arrow" triangles (inherently solid — see SOLID set)
    'caret-up':    '<path d="M4 16H20L12 8Z"/>',
    'caret-down':  '<path d="M4 8H20L12 16Z"/>',
    'caret-left':  '<path d="M16 4V20L8 12Z"/>',
    'caret-right': '<path d="M8 4V20L16 12Z"/>'
  };

  // Icons that are always rendered SOLID (filled), no stroke weight (e.g. carets).
  var SOLID = new Set(['caret-up', 'caret-down', 'caret-left', 'caret-right']);

  // Optional filled-state overrides. When an icon's "active" (filled) silhouette differs from
  // its outline path, put the filled path here. Otherwise active simply fills the closed default
  // path (works for closed shapes: bookmark, star, heart, bell, etc.).
  var ACTIVE_PATHS = {
    // gear: filled with the centre punched out (evenodd)
    settings: '<path fill-rule="evenodd" clip-rule="evenodd" d="' + gearOuterD() +
              ' M9 12A3 3 0 1 0 15 12A3 3 0 1 0 9 12Z"/>'
  };

  // ---- ACTIVE-STATE STRATEGY ------------------------------------------------
  // The active state should keep BOTH the fill AND the lines — interior detail is reversed out
  // of the solid, never a featureless blob. Each icon resolves to one of:
  //   "knockout"   — solid silhouette with an authored interior reversed out (best quality)
  //   "bold"       — line-only icon with no enclosed area (cross, burger, chevron) → heavier stroke
  //   "fill"       — clean single silhouette, no interior detail → plain solid (star, play…)
  //   "fill-detail"— solid silhouette with the icon's own lines reversed out (general fallback)
  var ACTIVE_BOLD_FACTOR = 1.6; // how much heavier "bold" active is vs the default stroke

  // line-only icons (nothing to fill) → active = heavier stroke
  var ACTIVE_BOLD = new Set([
    'close','plus','minus','check','menu','search','refresh','more','link','share',
    'expand','collapse','back','external-link','download','upload','pause',
    'chevron','chevron-right','chevron-up','chevron-down','chevron-left',
    'chevron-double-up','chevron-double-down','chevron-double-left','chevron-double-right',
    'arrow','arrow-up','arrow-down','arrow-left'
  ]);

  // clean single silhouettes → plain solid fill (reversing their own thin outline would hollow them)
  var PLAIN_FILL = new Set(['star','heart','bookmark','play','stop','send','filter','phone','edit','bell','volume','mute']);

  // outer = the shape(s) to fill; sym = the interior reversed out; symFill=true if sym is a closed
  // shape (e.g. a lens circle) rather than a stroked line.
  var ACTIVE_KNOCKOUT = {
    info:            { outer:'<circle cx="12" cy="12" r="9"/>',   sym:'<path d="M12 10.5V16"/><path d="M12 7.8V7.81"/>', sw:2.2 },
    'plus-circle':   { outer:'<circle cx="12" cy="12" r="8.5"/>', sym:'<path d="M12 8.5V15.5M8.5 12H15.5"/>', sw:2.2 },
    'minus-circle':  { outer:'<circle cx="12" cy="12" r="8.5"/>', sym:'<path d="M8.5 12H15.5"/>', sw:2.2 },
    'check-circle':  { outer:'<circle cx="12" cy="12" r="8.5"/>', sym:'<path d="M8 12.5L11 15.5L16.5 9"/>', sw:2.2 },
    'x-circle':      { outer:'<circle cx="12" cy="12" r="8.5"/>', sym:'<path d="M9 9L15 15M15 9L9 15"/>', sw:2.2 },
    'alert-circle':  { outer:'<circle cx="12" cy="12" r="8.5"/>', sym:'<path d="M12 7.5V13"/><path d="M12 15.6V15.61"/>', sw:2.2 },
    'help-circle':   { outer:'<circle cx="12" cy="12" r="8.5"/>', sym:'<path d="M9.4 9.6A2.7 2.7 0 1 1 12.4 12.4C11.9 12.7 11.9 13.2 11.9 13.9"/><path d="M12 16.4V16.41"/>', sw:2 },
    ban:             { outer:'<circle cx="12" cy="12" r="8.5"/>', sym:'<path d="M6 6L18 18"/>', sw:2.2 },
    'alert-triangle':{ outer:'<path d="M12 4L21 19H3L12 4Z"/>',  sym:'<path d="M12 10V14"/><path d="M12 16.4V16.41"/>', sw:2.2 },
    clock:           { outer:'<circle cx="12" cy="12" r="8.5"/>', sym:'<path d="M12 7V12L15.5 14"/>', sw:2.2 },
    mail:            { outer:'<path d="M3.5 6H20.5V18H3.5V6Z"/>', sym:'<path d="M4 6.5L12 12.5L20 6.5"/>', sw:1.6 },
    calendar:        { outer:'<path d="M4.5 6H19.5V20H4.5V6Z"/>', sym:'<path d="M4.5 10H19.5"/><path d="M8 4V7M16 4V7"/>', sw:1.7 },
    file:            { outer:'<path d="M6 3.5H14L19 8.5V20.5H6V3.5Z"/>', sym:'<path d="M14 3.5V8.5H19"/>', sw:1.6 },
    'shield-check':  { outer:'<path d="M12 3L19 6V11C19 16 12 21 12 21C12 21 5 16 5 11V6L12 3Z"/>', sym:'<path d="M9 12L11.2 14.2L15.2 9.8"/>', sw:2.2 },
    camera:          { outer:'<path d="M3.5 8H7L8.5 5.5H15.5L17 8H20.5V19H3.5V8Z"/>', sym:'<circle cx="12" cy="13" r="3.3"/>', symFill:true },
    eye:             { outer:'<path d="M2.5 12C2.5 12 6 6.5 12 6.5C18 6.5 21.5 12 21.5 12C21.5 12 18 17.5 12 17.5C6 17.5 2.5 12 2.5 12Z"/>', sym:'<circle cx="12" cy="12" r="2.6"/>', symFill:true },
    tag:             { outer:'<path d="M4 4H11L20 13L13 20L4 11V4Z"/>', sym:'<circle cx="7.6" cy="7.6" r="1.3"/>', symFill:true },
    'map-pin':       { outer:'<path d="M12 21C12 21 18.5 14.5 18.5 9.5A6.5 6.5 0 0 0 5.5 9.5C5.5 14.5 12 21 12 21Z"/>', sym:'<circle cx="12" cy="9.5" r="2.4"/>', symFill:true },
    // trash (the example): solid can + lid, slots reversed out
    trash:           { outer:'<path d="M6.6 7L7.6 20H16.4L17.4 7Z"/><path d="M5 6.1H19V7.5H5Z"/><path d="M9.3 6.1V4.8H14.7V6.1Z"/>', sym:'<path d="M10 10.5V16.5M14 10.5V16.5"/>', sw:1.8 }
  };

  function activeMode(name) {
    if (SOLID.has(name)) return 'fill';
    if (ACTIVE_KNOCKOUT[name]) return 'knockout';
    if (ACTIVE_BOLD.has(name)) return 'bold';
    if (ACTIVE_PATHS[name] || PLAIN_FILL.has(name)) return 'fill';
    return 'fill-detail';
  }

  var _uid = 0;
  // Canonical renderer used by the component AND the playground so they never drift.
  //   opts.state  "default" | "active"
  //   opts.strokePx  stroke-width in viewBox(24) units for the default/outline render
  //   opts.badge  boolean
  function buildIconSVG(name, opts) {
    opts = opts || {};
    var sw = (opts.strokePx != null) ? opts.strokePx : 2;
    var open = '<svg viewBox="0 0 24 24" width="100%" height="100%" aria-hidden="true" focusable="false">';
    var badge = opts.badge
      ? '<circle cx="18.5" cy="5.5" r="3.2" fill="var(--dyn-badge, #DB0011)" stroke="none"/>'
      : '';
    var active = opts.state === 'active';

    if (SOLID.has(name)) {
      return open + '<g fill="currentColor" stroke="none">' + (PATHS[name] || '') + '</g>' + badge + '</svg>';
    }
    if (active) {
      var mode = activeMode(name);
      if (mode === 'knockout') {
        var k = ACTIVE_KNOCKOUT[name]; var id = 'ko' + (++_uid);
        var symG = k.symFill
          ? '<g fill="black" stroke="none">' + k.sym + '</g>'
          : '<g fill="none" stroke="black" stroke-width="' + (k.sw || 2.2) + '" stroke-linecap="round" stroke-linejoin="round">' + k.sym + '</g>';
        return open
          + '<defs><mask id="' + id + '" maskUnits="userSpaceOnUse" x="0" y="0" width="24" height="24">'
          + '<rect x="0" y="0" width="24" height="24" fill="white"/>' + symG + '</mask></defs>'
          + '<g fill="currentColor" stroke="none" mask="url(#' + id + ')">' + k.outer + '</g>'
          + badge + '</svg>';
      }
      if (mode === 'bold') {
        return open + '<g fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="'
          + (sw * ACTIVE_BOLD_FACTOR) + '">' + (PATHS[name] || '') + '</g>' + badge + '</svg>';
      }
      if (mode === 'fill') {
        // clean solid (no interior detail), or an authored filled shape (e.g. gear with hole)
        return open + '<g fill="currentColor" stroke="none" fill-rule="evenodd" clip-rule="evenodd">'
          + (ACTIVE_PATHS[name] || PATHS[name] || '') + '</g>' + badge + '</svg>';
      }
      // fill-detail: solid silhouette with the icon's OWN lines reversed out (keeps the detail)
      var fid = 'fd' + (++_uid);
      return open
        + '<defs><mask id="' + fid + '" maskUnits="userSpaceOnUse" x="0" y="0" width="24" height="24">'
        + '<rect x="0" y="0" width="24" height="24" fill="white"/>'
        + '<g fill="none" stroke="black" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round">' + (PATHS[name] || '') + '</g>'
        + '</mask></defs>'
        + '<g fill="currentColor" stroke="none" fill-rule="evenodd" clip-rule="evenodd" mask="url(#' + fid + ')">' + (PATHS[name] || '') + '</g>'
        + badge + '</svg>';
    }
    // default outline
    return open + '<g fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="'
      + sw + '">' + (PATHS[name] || '') + '</g>' + badge + '</svg>';
  }

  // ordered list (handy for catalogues / pickers)
  var ICON_NAMES = Object.keys(PATHS);

  function svg(name) {
    var inner = PATHS[name];
    if (!inner) return '';
    return '<svg viewBox="0 0 24 24" aria-hidden="true" focusable="false">' + inner + '</svg>';
  }

  // map of full <svg> strings (handy for innerHTML / SSR)
  var DYN_ICONS = {};
  ICON_NAMES.forEach(function (k) { DYN_ICONS[k] = svg(k); });

  // ---- auto web component: <dyn-icon name weight size color state badge> ----
  //   weight  300|400|500|700   (default 400)  — calibrated stroke, looked up automatically
  //   size    px                (default 24)
  //   color   any CSS colour    (optional; else inherits currentColor)
  //   state   default|active    (default "default"; "active" = filled silhouette, HSBC convention)
  //   badge   (boolean attr)    — adds a notification dot (top-right); recolour via --dyn-badge
  // stroke-width is set on <svg> and inherits to child shapes (stroke-width is inherited in SVG).
  if (typeof customElements !== 'undefined' && !customElements.get('dyn-icon')) {
    customElements.define('dyn-icon', class extends HTMLElement {
      static get observedAttributes() { return ['name', 'weight', 'size', 'color', 'state', 'badge']; }
      connectedCallback() { this.render(); }
      attributeChangedCallback() { this.render(); }
      render() {
        var name = this.getAttribute('name');
        if (!PATHS[name]) { this.innerHTML = ''; return; }
        var size = +(this.getAttribute('size') || 24);
        var weight = +(this.getAttribute('weight') || 400);
        var color = this.getAttribute('color');
        var state = this.getAttribute('state') || 'default';
        var strokePx = strokeFor(weight, size) * 24 / size;   // viewBox units -> renders as t px
        this.style.display = 'inline-flex';
        this.style.width = size + 'px';
        this.style.height = size + 'px';
        if (color) this.style.color = color;
        this.innerHTML = buildIconSVG(name, { state: state, strokePx: strokePx, badge: this.hasAttribute('badge') });
      }
    });
  }

  // expose for classic <script> (global), CommonJS, ES interop
  global.DYN_ICONS = DYN_ICONS;
  global.DYN_ICON_PATHS = PATHS;
  global.ICON_NAMES = ICON_NAMES;
  global.ICON_STROKE = ICON_STROKE;
  global.SOLID_ICONS = SOLID;
  global.ACTIVE_BOLD = ACTIVE_BOLD;
  global.ACTIVE_KNOCKOUT = ACTIVE_KNOCKOUT;
  global.activeMode = activeMode;
  global.buildIconSVG = buildIconSVG;
  global.strokeFor = strokeFor;
  if (typeof module !== 'undefined' && module.exports) {
    module.exports = { DYN_ICONS: DYN_ICONS, PATHS: PATHS, ICON_NAMES: ICON_NAMES, ICON_STROKE: ICON_STROKE, SOLID: SOLID, ACTIVE_PATHS: ACTIVE_PATHS, ACTIVE_BOLD: ACTIVE_BOLD, ACTIVE_KNOCKOUT: ACTIVE_KNOCKOUT, activeMode: activeMode, buildIconSVG: buildIconSVG, strokeFor: strokeFor, svg: svg };
  }
})(typeof window !== 'undefined' ? window : globalThis);
