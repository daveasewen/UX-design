/* PREP — runs BEFORE the Filter-toolbar-bar's own script (which wires its menus at parse time),
   so the bar's option lists are DATA from CEO_DATA rather than the specimen's. Only option DATA
   and labels change; the component's markup, classes and behaviour are the pack's. */
(function () {
  'use strict';
  var D = window.CEO_DATA, bar = document.getElementById('ftbA');
  if (!bar || !D) { return; }
  bar.setAttribute('data-apollo-filter-target', '#ceo-consumer');
  var form = bar.querySelector('form'); if (form) { form.setAttribute('aria-label', 'Filter this view'); }
  var q = bar.querySelector('#ftbQ');
  if (q) { q.setAttribute('aria-label', 'Search this view'); q.setAttribute('placeholder', 'Search names, references and counterparties'); }
  var menu = bar.querySelector('#ftbAdd .menu'), grpTpl = menu && menu.querySelector('.optgrp');
  if (menu && grpTpl) {
    var optTpl = grpTpl.querySelector('.opt');
    var groups = [
      ['Entity', 'entity', D.entities.map(function (e) { return [e.id, e.short]; })],
      ['Region', 'region', D.regions.map(function (r) { return [r.id, r.name]; })],
      ['Currency', 'currency', D.currencies.map(function (c) { return [c, c]; })]];
    menu.textContent = '';
    groups.forEach(function (g, gi) {
      var node = grpTpl.cloneNode(true), head = node.querySelector('.grp'), list = node.querySelector('.grp-list');
      head.id = 'ftbGrp' + gi; head.textContent = g[0]; node.setAttribute('aria-labelledby', head.id);
      list.textContent = '';
      g[2].forEach(function (o) {
        var li = optTpl.cloneNode(true);
        li.setAttribute('data-facet', g[1]); li.setAttribute('data-value', o[0]); li.setAttribute('aria-selected', 'false');
        li.firstChild.textContent = o[1] + ' ';
        list.appendChild(li);
      });
      menu.appendChild(node);
    });
  }
  /* The custom-range option hands off to the Date-range-picker, which this prototype does not wire:
     it is removed rather than left as a control that opens nothing (named in the Gaps list). */
  var custom = bar.querySelector('#ftbRange [data-days="custom"]');
  if (custom) { var sep = custom.previousElementSibling; if (sep && sep.classList.contains('sep')) { sep.remove(); } custom.remove(); }
}());
