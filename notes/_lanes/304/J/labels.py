#!/usr/bin/env python3
"""304-J hand labels — written and FROZEN before any Jev call. firm = I would defend it; soft = defensible
either way (reported separately). receipt = where the label's evidence lives in the repo."""
import json, hashlib, os
T, F = True, False
L = {
 'E01': (T,'firm','Bar chart uses lettered on-chart keys; dv-bar-004 requires a key for alphanumeric labelling','knowledge/components/chart-bar.meta.json edges.obeys $why; guidelines/_rules-index.json dv-bar-004'),
 'E02': (T,'firm','Line chart hands off below 6 cols rather than shrink — that IS "full chart at a reasonable scale"','chart-line.meta.json edges.obeys $why; dv-002'),
 'E03': (T,'firm','Link density rule is a constraint on the links molecule itself','links.meta.json; ctkl-002 (common-toolkit-links.md)'),
 'E04': (T,'firm','ctkn-009 is the notifications stack spacing; its own spacing in prose','notifications.meta.json; ctkn-009'),
 'E05': (T,'firm','fast in-chip removal raises accidental-removal risk — the speed/accuracy trade exactly','tags-input.meta.json $why; ux:pr-speed-accuracy statement'),
 'E06': (T,'soft','link-text rules trade scan speed against wrong clicks; fits the principle statement but reads closer to information scent','links.meta.json $why; ux:pr-speed-accuracy'),
 'E07': (T,'firm','44x44 targets and fixed padding set target size — Fitts','button.meta.json $why; ctkb-014'),
 'E08': (T,'firm','icon-only control is the smallest target; 44x44 is Fitts','icon-button.meta.json $why'),
 'E09': (F,'firm','ctkb-003 is button-rank cardinality; text links carry no primary/secondary rank','rule:ctkb-003 text (common-toolkit-buttons.md)'),
 'E10': (F,'firm','Eyebrow is non-interactive (meta interactive:false) — there is no target to acquire','eyebrow.meta.json interactive=false'),
 'E11': (T,'firm','Cascader is listed as an input provider','knowledge/roles.json roles.input.providers'),
 'E12': (T,'firm','Table is a record-list provider (one record per row)','roles.json roles.record-list.providers'),
 'E13': (T,'firm','all charts provide chart-panel','roles.json roles.chart-panel.providers'),
 'E14': (T,'firm','modal launcher on top of the page, must be dismissed','roles.json roles.overlay.providers'),
 'E15': (T,'firm','all charts provide chart-panel','roles.json roles.chart-panel.providers'),
 'E16': (T,'firm','Slider gives a value','roles.json roles.input.providers'),
 'E17': (F,'firm','Amount display is the money-format primitive inside a tile, not the headline tile; not in the provider list','roles.json roles.headline-metric.providers = stat-card, kpi-tile, Chart-bullet, runway-bar'),
 'E18': (F,'firm','a table is not a charted reading; chart-panel providers are the 12 charts only','roles.json roles.chart-panel.providers'),
 'E19': (T,'firm','histogram is the canonical distribution chart','chart-intents.json distribution; Chart-histogram.meta.json answers'),
 'E20': (T,'firm','donut = parts of a whole','chart-intents.json composition'),
 'E21': (T,'firm','pie = parts of a whole','chart-intents.json composition'),
 'E22': (T,'firm','headers title and frame a screen = what-is-this','chart-intents.json/intents what-is-this; headers.meta.json'),
 'E23': (T,'soft','combo shares one x, usually time; its purpose text names units not time','chart-combo.meta.json answers; chart-intents.json change-over-time'),
 'E24': (F,'firm','comparison.notFor names distribution explicitly; histogram is distribution','chart-intents.json comparison.notFor'),
 'E25': (T,'firm','button takes no data: label + action','shapes.json no-data x control used-by button'),
 'E26': (T,'firm','KPI tile = value, delta and sparkline series','shapes.json; kpi-tile.meta.json'),
 'E27': (T,'firm','one state drawn as dot + label','shapes.json; status-indicator.meta.json'),
 'E28': (T,'firm','layout utilities take no data and paint nothing','shapes.json no-data x arbitrary-blocks used-by layout-utilities'),
 'E29': (F,'firm','histogram x is continuous bins, not categories (its shape is bins x frequency)','Chart-histogram hasDataShape -> shape:bins x frequency'),
 'E30': (T,'firm','focused shell gives way to top-nav shell when the job needs navigation','app-shell-focused.meta.json when/yieldsTo'),
 'E31': (T,'firm','breadcrumbs (hierarchy) give way to tabs for peer views','breadcrumbs.meta.json yieldsTo'),
 'E32': (T,'firm','line gives way to candlestick when the data is OHLC per period','chart-line.meta.json yieldsTo'),
 'E33': (T,'firm','status indicator gives way to badge for new-activity notification','status-indicator.meta.json yieldsTo'),
 'E34': (F,'firm','eyebrow categorises a heading; badge notifies activity — no overlapping job','eyebrow.meta.json / badge.meta.json purposes'),
 'E35': (T,'soft','meta binds primary/background/default — surprising for a text link but it is the record','links.meta.json tokens block (edge paths)'),
 'E36': (T,'soft','meta binds form/background/pressed + form/border/default — via its filter controls','template-dashboard-bento.meta.json tokens block'),
 'E37': (T,'firm','masthead/nav bars bind color/primary, black, white','navigations.meta.json tokens block'),
 'E38': (T,'firm','tree binds border-radius/control + surface','tree.meta.json tokens block'),
 'E39': (T,'firm','bento binds border-radius/container','template-dashboard-bento.meta.json tokens block'),
 'E40': (F,'firm','footer tokens block has no data/* token; data colours are for charts','footer.meta.json tokens block'),
 'E41': (T,'firm','error page carries links/buttons — focus must be visible','compliance/rules/wcag-2.4.7*.json applies_to'),
 'E42': (T,'firm','any in-page heading block must reflow at 320px','compliance/rules/wcag-1.4.10*.json applies_to'),
 'E43': (T,'firm','histogram bins show hover/focus popovers','compliance/rules/wcag-1.4.13*.json applies_to; Chart-histogram Layer-2'),
 'E44': (T,'firm','dashboard carries RAG/delta colour that must be paired with text','compliance/rules/wcag-1.4.1*.json applies_to'),
 'E45': (F,'firm','2.5.8 target size applies to pointer targets; eyebrow is not interactive','eyebrow.meta.json interactive=false; WCAG 2.5.8'),
 'E46': (T,'firm','fewer options vs offer more ways — textbook opposition','_ux_principle_nodes.json polarity pl-13'),
 'E47': (T,'soft','proportional (bigger) feedback for rare actions vs hard response-time limits','polarity pl-23 (mediating: acknowledgement immediate, celebration proportional)'),
 'E48': (T,'soft','pl-04 is a 3-party polarity about evaluation; the pairwise pull on visibility is indirect','polarity pl-04 (who is measuring)'),
 'E49': (T,'soft','"put things on the F" vs "strong scent removes the F" — pl-28 says the F is a symptom','polarity pl-28'),
 'E50': (F,'firm','Hick and choice overload point the SAME way (fewer options) — agreement, not tension','ux statements pr-hick, pr-choice-overload'),
}
out = [{'eid': k, 'label': v[0], 'firmness': v[1], 'reason': v[2], 'receipt': v[3]} for k, v in sorted(L.items())]
blob = json.dumps(out, sort_keys=True, ensure_ascii=False).encode()
h = hashlib.sha256(blob).hexdigest()
here = os.path.dirname(os.path.abspath(__file__))
json.dump({'frozen_sha256': h, 'frozen_before_first_call': True, 'labels': out}, open(os.path.join(here, 'labels.json'), 'w'), indent=1, ensure_ascii=False)
print(len(out), 'labels', sum(o['label'] for o in out), 'TRUE', sum(o['firmness']=='soft' for o in out), 'soft', 'sha256', h)
