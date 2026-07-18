# Pro-forma glyph-presence gate (DEF-002) — report

Enforces rule 12: a painted glyph/ink-on-surface pair (rule setting both a non-transparent
`background:var(--Y)` and `color:var(--X)`/`fill:var(--X)` in the same declaration block)
must read at >= 1.3:1 in BOTH themes. Computed via `_contrast_utils.contrast_ratio`.

## ✓ _proforma/Tranche-1-interactive.html — PASS
-   --ink on --page  light=12.63:1  dark=21.0:1  min=12.63:1  (1x, e.g. body)
-   --ink2 on --page  light=7.57:1  dark=7.56:1  min=7.56:1  (1x, e.g. .dot)
-   --icon-rev on --pri  light=17.4:1  dark=15.55:1  min=15.55:1  (2x, e.g. .ib.pri)
-   --pri-lbl on --pri  light=17.4:1  dark=15.55:1  min=15.55:1  (4x, e.g. .btn.pri)
-   --disi on --surf  light=1.81:1  dark=3.55:1  min=1.81:1  (1x, e.g. .ib:disabled)
-   --ink2 on --surf  light=6.82:1  dark=5.79:1  min=5.79:1  (1x, e.g. .real .av)

## ✓ _proforma/Tranche-2-interactive.html — PASS
-   --ink on --page  light=12.63:1  dark=21.0:1  min=12.63:1  (1x, e.g. body)
-   --icon-rev on --pri  light=17.4:1  dark=15.55:1  min=15.55:1  (1x, e.g. .ib.pri)
-   --pri-lbl on --pri  light=17.4:1  dark=15.55:1  min=15.55:1  (4x, e.g. .btn.pri)
-   --disi on --surf  light=1.81:1  dark=3.55:1  min=1.81:1  (1x, e.g. .ib:disabled)

## ✓ _proforma/Tranche-3-interactive.html — PASS
-   --ink on --page  light=12.63:1  dark=21.0:1  min=12.63:1  (1x, e.g. body)
-   --icon-rev on --pri  light=17.4:1  dark=15.55:1  min=15.55:1  (2x, e.g. .ib.pri)
-   --pri-lbl on --pri  light=17.4:1  dark=15.55:1  min=15.55:1  (3x, e.g. .btn.pri)
-   --ink on --raised  light=12.63:1  dark=16.86:1  min=12.63:1  (1x, e.g. .sel-trigger)
-   --disi on --surf  light=1.81:1  dark=3.55:1  min=1.81:1  (1x, e.g. .ib:disabled)
-   --ink on --surf  light=11.39:1  dark=16.1:1  min=11.39:1  (1x, e.g. .sub code)

## ✓ _proforma/Tranche-4-interactive.html — PASS
-   --ink on --page  light=12.63:1  dark=21.0:1  min=12.63:1  (1x, e.g. body)
-   --icon-rev on --pri  light=17.4:1  dark=15.55:1  min=15.55:1  (1x, e.g. .ib.pri)
-   --pri-lbl on --pri  light=17.4:1  dark=15.55:1  min=15.55:1  (4x, e.g. .btn.pri)
-   --disi on --surf  light=1.81:1  dark=3.55:1  min=1.81:1  (1x, e.g. .ib:disabled)
-   --ink on --surf  light=11.39:1  dark=16.1:1  min=11.39:1  (2x, e.g. .tab:hover)

## ✓ _proforma/Tranche-5-interactive.html — PASS
-   --ink on --info-t  light=10.94:1  dark=19.56:1  min=10.94:1  (1x, e.g. .pbanner.info)
-   --page on --ink  light=12.63:1  dark=21.0:1  min=12.63:1  (1x, e.g. .pbanner.info .pb-action:hover)
-   --ink on --page  light=12.63:1  dark=21.0:1  min=12.63:1  (1x, e.g. body)
-   --icon-rev on --pri  light=17.4:1  dark=15.55:1  min=15.55:1  (1x, e.g. .ib.pri)
-   --pri-lbl on --pri  light=17.4:1  dark=15.55:1  min=15.55:1  (6x, e.g. .btn.pri)
-   --pri on --pri-lbl  light=17.4:1  dark=15.55:1  min=15.55:1  (1x, e.g. .pbanner.neutral .pb-action:hover)
-   --disi on --surf  light=1.81:1  dark=3.55:1  min=1.81:1  (1x, e.g. .ib:disabled)
-   --ink on --surf  light=11.39:1  dark=16.1:1  min=11.39:1  (4x, e.g. .card-link-ic)

## ✓ _proforma/Tranche-6-interactive.html — PASS
-   --ink on --page  light=12.63:1  dark=21.0:1  min=12.63:1  (1x, e.g. body)
-   --icon-rev on --pri  light=17.4:1  dark=15.55:1  min=15.55:1  (1x, e.g. .ib.pri)
-   --pri-lbl on --pri  light=17.4:1  dark=15.55:1  min=15.55:1  (3x, e.g. .btn.pri)
-   --disi on --surf  light=1.81:1  dark=3.55:1  min=1.81:1  (1x, e.g. .ib:disabled)

---
Floor: 1.3:1 (rule 12 "~1.3"). Below floor in either theme = FAIL (DEF-002).
