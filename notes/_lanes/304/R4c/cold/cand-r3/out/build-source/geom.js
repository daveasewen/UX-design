() => {
  const R = e => { const r = e.getBoundingClientRect(); return { x: Math.round(r.left * 10) / 10, y: Math.round(r.top * 10) / 10, r: Math.round(r.right * 10) / 10, b: Math.round(r.bottom * 10) / 10, w: Math.round(r.width * 10) / 10, h: Math.round(r.height * 10) / 10 }; };
  const sec = document.querySelector('.ceo-view:not([hidden])'), out = { view: sec.getAttribute('data-view'), issues: [], notes: [] };
  const ground = sec.querySelector('.ceo-ground'), wall = sec.querySelector('.tpl-wall'), gs = getComputedStyle(ground);
  out.groundPad = gs.paddingTop; out.wallGap = getComputedStyle(wall.querySelector(':scope > .c-bento__grid')).rowGap + ' / ' + getComputedStyle(wall.querySelector(':scope > .c-bento__grid')).columnGap;
  out.ftbWidth = R(document.querySelector('.ftb-outer')).w; out.groundWidth = R(ground).w;
  const groups = [...wall.querySelectorAll(':scope > .c-bento__grid > .tpl-group')];
  const rows = {}; groups.forEach(g => { const r = R(g); (rows[r.y] = rows[r.y] || []).push([g.getAttribute('aria-label'), r]); });
  out.groupRows = Object.keys(rows).length;
  Object.values(rows).forEach(list => { const bs = new Set(list.map(x => x[1].b)); if (bs.size > 1) out.issues.push('ragged group row: ' + list.map(x => x[0] + '@' + x[1].b).join(' | '));
    for (let i = 1; i < list.length; i++) { out.notes.push('h-gutter ' + (list[i][1].x - list[i - 1][1].r)); } });
  const ys = Object.keys(rows).map(Number).sort((a, b) => a - b);
  for (let i = 1; i < ys.length; i++) { const prevB = Math.max(...rows[ys[i - 1]].map(x => x[1].b)); out.notes.push('v-gutter ' + Math.round((ys[i] - prevB) * 10) / 10); }
  const gr = R(ground), wr = R(wall); out.notes.push('ground inset L ' + (wr.x - gr.x) + ' R ' + (gr.r - wr.r) + ' T ' + (wr.y - gr.y) + ' B ' + (Math.round((gr.b - wr.b) * 10) / 10));
  groups.forEach(g => { const tiles = [...g.querySelectorAll(':scope > .c-bento__grid > .c-bento__tile')]; const tr = {};
    tiles.forEach(t => { const r = R(t); (tr[r.y] = tr[r.y] || []).push([t, r]); });
    Object.values(tr).forEach(list => { if (new Set(list.map(x => x[1].b)).size > 1) out.issues.push('ragged tile row in ' + g.getAttribute('aria-label')); });
    const cg = getComputedStyle(g.querySelector(':scope > .c-bento__grid')); out.notes.push('sub-gutter ' + cg.columnGap);
    tiles.forEach(t => { if (t.scrollWidth > t.clientWidth + 1) out.issues.push('horizontal overflow in tile of ' + g.getAttribute('aria-label') + ' (' + t.scrollWidth + ' > ' + t.clientWidth + ')');
      const kids = [...t.children].filter(k => getComputedStyle(k).display !== 'none'); if (!kids.length) return;
      const pb = parseFloat(getComputedStyle(t).paddingBottom), cb = Math.max(...kids.map(k => R(k).b)); const slack = Math.round(R(t).b - pb - cb);
      if (slack > 24) out.notes.push('slack ' + slack + 'px below content in ' + (t.getAttribute('data-kpi') || (t.querySelector('[data-chart]') || t).getAttribute('data-chart') || t.getAttribute('data-summary') || g.getAttribute('aria-label'))); }); });
  out.kpi = [...sec.querySelectorAll('.kpi-tile')].map(k => R(k).h);
  out.pageHScroll = document.scrollingElement.scrollWidth > innerWidth;
  const sc = document.getElementById('sh-content'); out.contentHScroll = sc.scrollWidth > sc.clientWidth;
  out.svgs = [...sec.querySelectorAll('svg.dv-svg')].map(s => { const f = s.closest('figure'); return f.closest('[data-chart]').getAttribute('data-chart') + ' ' + R(s).w + 'x' + R(s).h; });
  return out;
}
