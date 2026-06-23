/*
  dynamic-icons.js — builder-usable source for the dynamic-weight icon set.

  Core 8 outline icons drawn on a 24x24 grid, using the HSBC catalogue as visual
  reference. Unlike the HSBC originals (which are FILLED and can't be re-weighted),
  these are pure outlines, so three things are controllable from CSS:

    --icon-stroke   line thickness  (a number; bind it to the label's font-weight)
    --icon-color    colour          (applied via currentColor, so it inherits tokens)
    --icon-size     scale           (any length)

  TWO WAYS TO USE
  ---------------
  1) Raw markup — DYN_ICONS["search"] gives a full <svg> string. Drop it in a box and
     style it (see CSS at bottom of this comment).
  2) Web component — <dyn-icon name="search"></dyn-icon>. Same styling hooks.

  RECOMMENDED CSS (also printed live in playground.html → "For the builder"):

    .icon, dyn-icon{
      --icon-stroke:1.7;          // 1.3=Light 1.7=Regular 2.1=Medium 2.7=Bold
      --icon-color:#333333;       // icon/default; or a token / currentColor
      --icon-size:24px;
      display:inline-flex; width:var(--icon-size); height:var(--icon-size);
      color:var(--icon-color);
    }
    .icon svg, dyn-icon svg{
      width:100%; height:100%; fill:none; stroke:currentColor;
      stroke-linecap:round; stroke-linejoin:round;
    }
    .icon svg *, dyn-icon svg *{
      stroke-width:var(--icon-stroke);
      vector-effect:non-scaling-stroke;   // keep line px constant as the icon scales
    }

  WEIGHT <-> FONT MAP (starting point — tune to taste):
    Light 300 -> 1.3 | Regular 400 -> 1.7 | Medium 500 -> 2.1 | Bold 700 -> 2.7
*/

(function (global) {
  // Geometry only — no stroke/fill/size baked in; CSS drives all of that.
  var PATHS = {
    close:   '<path d="M6 6L18 18M18 6L6 18"/>',
    plus:    '<path d="M12 5V19M5 12H19"/>',
    check:   '<path d="M5 12.5L9.5 17L19.5 6"/>',
    chevron: '<path d="M9 6L15 12L9 18"/>',
    search:  '<circle cx="10.5" cy="10.5" r="6.5"/><path d="M15.2 15.2L20 20"/>',
    arrow:   '<path d="M4 12H20"/><path d="M14 6L20 12L14 18"/>',
    info:    '<circle cx="12" cy="12" r="9"/><path d="M12 10.5V16"/><path d="M12 7.8V7.81"/>',
    menu:    '<path d="M4 7H20M4 12H20M4 17H20"/>'
  };

  function svg(name) {
    var inner = PATHS[name];
    if (!inner) return '';
    return '<svg viewBox="0 0 24 24" aria-hidden="true" focusable="false">' + inner + '</svg>';
  }

  // Map of full <svg> strings (handy for innerHTML / SSR).
  var DYN_ICONS = {};
  Object.keys(PATHS).forEach(function (k) { DYN_ICONS[k] = svg(k); });

  // Optional web component: <dyn-icon name="search"></dyn-icon>
  if (typeof customElements !== 'undefined' && !customElements.get('dyn-icon')) {
    customElements.define('dyn-icon', class extends HTMLElement {
      static get observedAttributes() { return ['name']; }
      connectedCallback() { this.render(); }
      attributeChangedCallback() { this.render(); }
      render() {
        var n = this.getAttribute('name');
        this.innerHTML = DYN_ICONS[n] || '';
      }
    });
  }

  // Expose for: classic <script> (global), CommonJS, and ES interop.
  global.DYN_ICONS = DYN_ICONS;
  global.DYN_ICON_PATHS = PATHS;
  if (typeof module !== 'undefined' && module.exports) {
    module.exports = { DYN_ICONS: DYN_ICONS, PATHS: PATHS, svg: svg };
  }
})(typeof window !== 'undefined' ? window : globalThis);
