() => {
  const vw = document.documentElement.clientWidth, R = (e) => e.getBoundingClientRect();
  const out = { hscroll: document.documentElement.scrollWidth > vw };
  // left edge alignment of the page's content columns
  const xs = {}; [['crumbs', '.tpl-crumbs'], ['h1', 'h1'], ['ftb', '.ftb-outer'], ['wall', '.tpl-wall'], ['section', '.page-section .tpl-panel-head'], ['grid', '.dg'], ['footer', '.sh-legal']].forEach(([k, s]) => { const e = document.querySelector(s); if (e) xs[k] = Math.round(R(e).left); });
  out.align = xs;
  const nav = document.querySelector('.sh-nav'), act = document.querySelector('.sh-actions');
  out.navFit = nav && act ? Math.round(R(act).left - R(nav).right) : null;
  // chart category/axis label overlaps inside each chart
  let ov = {}; document.querySelectorAll('figure.dv').forEach(f => { const t = [...f.querySelectorAll('svg text.dv-label, svg text.dv-axis')].map(R).filter(r => r.width); let c = 0; for (let i = 0; i < t.length; i++) for (let j = i + 1; j < t.length; j++) { const a = t[i], b = t[j]; if (a.left < b.right - 1 && b.left < a.right - 1 && a.top < b.bottom - 1 && b.top < a.bottom - 1) c++; } if (c) ov[f.id] = c; });
  out.labelOverlaps = ov;
  // clipped text: elements whose content overflows horizontally (excluding scroll containers)
  const clip = []; document.querySelectorAll('.kpi-tile .amt, .kpi-tile .delta, .summary__v, .summary__k, .dv-title, .sh-nav a, .trigger, .tag, .status, .chip, .btn, .dbtn, h1, .tpl-strip-plain, .dg-count, td span').forEach(e => { if (e.scrollWidth > e.clientWidth + 1 && getComputedStyle(e).overflow !== 'visible') clip.push((e.className || e.tagName).toString().slice(0, 30) + ':' + e.textContent.trim().slice(0, 24)); });
  document.querySelectorAll('.kpi-tile, .stat-card').forEach(t => { const tr = R(t); t.querySelectorAll('*').forEach(c => { const r = R(c); if (r.width && (r.right > tr.right + 1 || r.left < tr.left - 1) && !c.closest('.dv-tablepanel') && !c.closest('details:not([open])')) clip.push('OUTSIDE-TILE ' + (c.className.baseVal !== undefined ? c.className.baseVal : c.className).toString().slice(0, 24)); }); });
  out.textClip = [...new Set(clip)];
  // hit targets under 24px (visible, interactive)
  const small = []; document.querySelectorAll('a, button, input, select, [role=checkbox], [tabindex="0"]').forEach(e => { const r = R(e); if (!r.width || !r.height || e.closest('.sheet,.overlay,.menu,.dv-tablepanel')) return; if (getComputedStyle(e).visibility === 'hidden') return; if ((r.width < 24 || r.height < 24) && !e.matches('svg *, rect, path, g, circle')) small.push((e.className.baseVal !== undefined ? e.className.baseVal : e.className || e.tagName).toString().slice(0, 28) + ' ' + Math.round(r.width) + 'x' + Math.round(r.height)); });
  out.smallTargets = [...new Set(small)];
  // bento gutters and tile padding
  const lead = [...document.querySelectorAll('.tpl-group-lead > .c-bento__grid > .kpi-tile')].map(R);
  out.tileGaps = lead.length > 1 ? [...new Set(lead.slice(1).map((r, i) => Math.round(r.left - lead[i].right)))] : [];
  const groups = [...document.querySelectorAll('.tpl-wall > .c-bento__grid > .c-bento')].map(R);
  out.groupGaps = groups.length > 1 ? [...new Set(groups.slice(1).map((r, i) => Math.round(r.top - groups[i].bottom > 0 ? r.top - groups[i].bottom : r.left - groups[i].right)))] : [];
  const sc = document.querySelector('.stat-card'); out.tilePad = sc ? getComputedStyle(sc).padding : null;
  const kt = document.querySelector('.kpi-tile'); out.kpiPad = kt ? getComputedStyle(kt).padding : null;
  // vertical rhythm between major bands
  const band = (s) => { const e = document.querySelector(s); return e ? R(e) : null; };
  const h = band('.tpl-header'), f = band('.cn-filter-toolbar-bar'), w = band('.wall-ground'), s = band('.page-section'), ft = band('.sh-foot');
  out.bands = { headerToFtb: h && f ? Math.round(f.top - h.bottom) : null, ftbToWall: f && w ? Math.round(w.top - f.bottom) : null, wallToSection: w && s ? Math.round(s.top - w.bottom) : null };
  out.charts = [...document.querySelectorAll('figure.dv')].map(f => { const sv = f.querySelector('svg.dv-svg'), r = R(sv); return f.id + ' ' + Math.round(r.width) + 'x' + Math.round(r.height) + ' marks=' + f.querySelectorAll('.dv-series,.dv-marker,.dv-donut-seg').length + ' leg=' + f.querySelectorAll('.dv-legrow').length + ' rows=' + f.querySelectorAll('.dv-table tbody tr').length; });
  return out;
}
