/* dp08-anchor — the status-strip → Needs-attention ARRIVAL behaviour (ADR-0015 behaviour
   partial, hand-authored SOURCE). ONE file, injected between AUTO-BEHAVIOUR markers by
   knowledge/gen_component_partials.py into every member that declares it in `consumes`.

   WHY IT EXISTS. s251-D1 (Dave, #251): the header status STRIP is the orientation layer and
   the Needs-attention card is the detail — "the user might even click on the chip and it
   anchor links to the needs attention panel". A bare `href="#id"` jumps, and a jump inside a
   long dashboard leaves the reader with no idea WHICH card answered them. This partial makes
   the jump an ARRIVAL: scroll, focus, and one transient highlight on the card itself.

   CONTRACT (ADR-0015 §4, gated by knowledge/_validate_behaviour.py):
     · no polling (setInterval), no network, no JS scale-physics (DEF-003) — none used here.
     · ZERO resize listeners of its own. This behaviour has nothing to reflow; the group's ONE
       rAF-debounced listener lives in dv-behaviour.js and stays the group's only one.
     · code-only bytes are what the gate measures (s250-D1 / ADR-0015 Amendment 3), so this
       comment costs the page nothing.

   ACCESSIBILITY. The card takes `tabindex="-1"` only at the moment it is addressed, so the
   card never enters the tab order; focus is what carries the arrival to a screen reader and
   to the keyboard, and the highlight is the sighted echo of the same event (never the only
   channel — 1.4.1). `prefers-reduced-motion: reduce` drops BOTH the smooth scroll and the
   highlight; nothing is left animating.

   PROGRESSIVE ENHANCEMENT. With JS off the chip is still a real in-page link to a real id:
   the browser jumps to the card and the page still works, minus the focus and the highlight.
   That is the `fallback` string in the meta's typed `behaviour` (s234-D5). */
(function () {
  "use strict";
  var SEL = '[data-dp08-anchor]';          /* the strip chip(s) that address a card */
  var TARGET = 'data-dp08-target';         /* the card that may be arrived at */
  var CLS = 'is-dp08-arrived';             /* transient; the page owns the keyframes */
  var reduce = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)');

  function targetOf(a) {
    var href = a.getAttribute('href') || '';
    if (href.charAt(0) !== '#' || href.length < 2) return null;
    return document.getElementById(href.slice(1));
  }

  function arrive(card) {
    if (!card) return;
    if (!card.hasAttribute('tabindex')) card.setAttribute('tabindex', '-1');
    card.focus({ preventScroll: true });
    card.classList.add(CLS);
    if (reduce && reduce.matches) { card.classList.remove(CLS); return; }
    var done = function (e) {
      if (e && e.target !== card) return;
      card.classList.remove(CLS);
      card.removeEventListener('animationend', done);
    };
    card.addEventListener('animationend', done);
  }

  function onClick(e) {
    var a = e.target && e.target.closest ? e.target.closest(SEL) : null;
    if (!a) return;
    var card = targetOf(a);
    if (!card) return;                     /* no target ⇒ leave the link alone */
    e.preventDefault();
    card.scrollIntoView({ block: 'start',
                         behavior: (reduce && reduce.matches) ? 'auto' : 'smooth' });
    if (history && history.replaceState) history.replaceState(null, '', a.getAttribute('href'));
    arrive(card);
  }

  function onHash() {
    var id = (location.hash || '').slice(1);
    if (!id) return;
    var card = document.getElementById(id);
    if (card && card.hasAttribute(TARGET)) arrive(card);
  }

  document.addEventListener('click', onClick, false);
  window.addEventListener('hashchange', onHash, false);
  if (document.readyState !== 'loading') onHash();
  else document.addEventListener('DOMContentLoaded', onHash, false);
}());
