# Dark surface/border flatness gate

> Surface/background/border/divider tokens must not resolve to a flat `#FFFFFF` in dark (a white block hiding content). Intentional inversions are exempt via a `$darkNote` annotation.

**Result:** 0 failure(s) · 5 annotated exception(s).

## Annotated intentional inversions (allowed)

| Token | Why |
|---|---|
| `form/border/active` | INTENTIONAL: active field border is #FFFFFF on dark (strong active emphasis; light=#000). |
| `primary/background/pressed` | INTENTIONAL inversion: pressed primary is WHITE on dark (light pressed=#000). Not a flat-white defect. |
| `primary/border/pressed` | INTENTIONAL: matches the white pressed primary fill on dark. |
| `secondary/background/default` | INTENTIONAL inversion: secondary inverts to a light/white button on dark (light=#000). Not a defect. |
| `secondary/border/default` | INTENTIONAL inversion: white border for the inverted secondary button on dark. |
