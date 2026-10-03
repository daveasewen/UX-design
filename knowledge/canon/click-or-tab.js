/* click-or-tab — tells a click from a Tab for the whole page (s315-D26, Dave by click
   2026-10-02: "Yes, one shared script"; the rule it serves is s313-D71 / s314-D1 — the focus
   ring never shows unless the user is on the keyboard).

   ONE source, hand-authored HERE. Every page built from parts loads it once:
     · a composed page links it once, beside canon.css, as a script element whose src ends
       knowledge/canon/click-or-tab.js (written in the head, before any part);
     · a snippet carries it between AUTO-BEHAVIOUR click-or-tab markers, injected by
       knowledge/gen_component_partials.py (registry: knowledge/component-types.json, group
       "click-or-tab"). Edit HERE and regenerate — never between a snippet's markers.
   A hand-written copy anywhere in knowledge/snippets/ is refused by that generator's --check.

   What it does: Tab marks the page keyboard; a mouse press, a pen or a touch marks it pointer,
   on <html data-modality>. canon.css hides the ring under :root[data-modality="pointer"], so a
   click never draws it and Tab always does. Listeners sit on window in the CAPTURE phase, so
   the flag is set before the browser moves focus, and a part that stops propagation or cancels
   pointerdown (the video seek bar does — which suppresses the mousedown) cannot hide the press.
   Runs once per page however many copies the page carries. */
(function () {
  'use strict';
  if (window.__clickOrTab) { return; } window.__clickOrTab = true;
  var root = document.documentElement;
  function pointer() { root.dataset.modality = 'pointer'; }
  addEventListener('keydown', function (e) { if (e.key === 'Tab') { root.dataset.modality = 'keyboard'; } }, true);
  addEventListener('pointerdown', pointer, true);
  addEventListener('mousedown', pointer, true);
  addEventListener('touchstart', pointer, { capture: true, passive: true });
}());
