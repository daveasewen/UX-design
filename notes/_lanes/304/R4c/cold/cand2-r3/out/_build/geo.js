() => {
  const r = e => { const b = e.getBoundingClientRect(); return [Math.round(b.left), Math.round(b.top), Math.round(b.width), Math.round(b.height)]; };
  const cs = (e, p) => getComputedStyle(e).getPropertyValue(p);
  const out = {};
  out.viewport = [innerWidth, innerHeight, document.documentElement.scrollWidth];
  out.appbar = r(document.querySelector('.sh-appbar'));
  out.nav = r(document.querySelector('#nav-wide'));
  out.main = [r(document.querySelector('#main-wide')), cs(document.querySelector('#main-wide'), 'padding'), cs(document.querySelector('#main-wide'), 'gap')];
  const wall = document.querySelector('.tpl-wall'); const gr = document.querySelector('.ceo-ground'); out.ground = [r(gr), cs(gr,'background-color'), cs(gr,'padding')];
  out.wall = [r(wall), cs(wall, 'background-color'), cs(wall, 'padding'), cs(wall.querySelector(':scope > .c-bento__grid'), 'gap'), cs(wall.querySelector(':scope > .c-bento__grid'), 'grid-template-columns')];
  out.groups = [...document.querySelectorAll('.tpl-group')].map(g => {
    const grid = g.querySelector(':scope > .c-bento__grid');
    const tiles = [...grid.children].map(t => {
      const inner = t.firstElementChild; let content = 0;
      [...t.querySelectorAll(':scope > * , :scope > * > *')].forEach(x => { const b = x.getBoundingClientRect(); content = Math.max(content, b.bottom); });
      return { k: t.dataset.kpi || t.dataset.chart || t.dataset.panel || (t.hasAttribute('data-grid-tile') ? 'grid' : '?'), rect: r(t), bg: cs(t, 'background-color'), pad: cs(t, 'padding'),
        over: t.scrollWidth > t.clientWidth + 1, dead: Math.round(t.getBoundingClientRect().bottom - content) };
    });
    return { cls: g.className.replace('c-bento__tile c-bento tpl-group ', ''), rect: r(g), gap: cs(grid, 'gap'), cols: cs(grid, 'grid-template-columns'), pad: cs(g, 'padding'), bg: cs(g, 'background-color'), tiles };
  });
  out.foot = r(document.querySelector('.sh-foot'));
  out.overflowX = [...document.querySelectorAll('#main-wide *')].filter(e => e.scrollWidth > e.clientWidth + 1 && getComputedStyle(e).overflowX === 'visible' && e.clientWidth > 0).slice(0, 8).map(e => e.className + ':' + e.scrollWidth + '>' + e.clientWidth);
  return out;
}
