() => {
  const pick = (sel, f) => { const e = [...document.querySelectorAll(sel)].find(x => x.getClientRects().length && x.getBoundingClientRect().height > 0 && getComputedStyle(x).visibility !== 'hidden'); return e ? f(e) : null; };
  const H = e => Math.round(e.getBoundingClientRect().height * 10) / 10, Wd = e => Math.round(e.getBoundingClientRect().width * 10) / 10;
  const cs = (e, p) => getComputedStyle(e).getPropertyValue(p);
  return {
    kpiTile: pick('.kpi-tile.as-link', e => [H(e), cs(e, 'padding'), cs(e, 'gap')]),
    kpiVal: pick('.kpi-tile .kpi-val', e => [H(e), cs(e, 'font-size')]),
    ddTrigger: pick('.dd.boxed .trigger', e => [H(e), cs(e, 'padding')]),
    segButton: pick('.seg.md button', e => [H(e), cs(e, 'padding')]),
    btnPrimary: pick('.btn.primary', e => [H(e), cs(e, 'padding')]),
    btnSecondary: pick('.btn.secondary', e => [H(e), cs(e, 'padding')]),
    listRow: pick('ul.list button.row', e => [H(e), cs(e, 'padding')]),
    summaryRow: pick('.summary__row', e => [H(e), cs(e, 'padding')]),
    gridRow: pick('#tbody tr[data-id]', e => [H(e)]),
    gridCell: pick('#tbody tr[data-id] td:nth-child(2)', e => [cs(e, 'padding')]),
    pbtn: pick('.pbtn', e => [H(e), Wd(e)]),
    sheet: pick('.sheet', e => [Wd(e), cs(e, 'padding')]),
    appbar: pick('.sh-appbar', e => [H(e), cs(e, 'padding')]),
    snLink: pick('.sn-link', e => [H(e), cs(e, 'padding')]),
    lineSvg: pick('figure[data-dv-type="multiline"] svg.dv-svg', e => [H(e)]),
    barSvg: pick('figure[data-dv-type="grouped-column"] svg.dv-svg, figure[data-dv-type="column"] svg.dv-svg', e => [H(e)]),
    field: pick('.field .box', e => [H(e), cs(e, 'padding')]),
    txBox: pick('#live .tx-box, .tx-group .tx-box', e => [H(e)]),
    toast: pick('.toast', e => [H(e), cs(e, 'padding')])
  };
}
