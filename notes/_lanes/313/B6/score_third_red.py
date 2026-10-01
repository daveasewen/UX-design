"""#313 B6 — contrast and the repo's bloom/dance model (reviews/_rag_bloom_model.py, v0) on every
pair the third-red candidates paint. Loaded the way notes/_lanes/310/C/bloom_options.py loads it
(functions only, demo prints not run). Scores are relative, 100 = a 40px white fill on #1A1A1A.
Widths: type 2px stroke, icon 20px (16px inline), bar 40px. Writes scores.json beside this file."""
import json, os
src = open('reviews/_rag_bloom_model.py').read(); src = src[:src.index("DPG='#1A1A1A'")]
ns = {}; exec(src, ns); B, D, wcag = ns['B'], ns['D'], ns['wcag']
PAIRS = {
 "A · keep (Mono today = Common)": [
  ("bar type, light and dark", "#FFFFFF", "#A8000B", 2),
  ("bar on the light page", "#A8000B", "#FFFFFF", 40),
  ("bar on the dark page", "#A8000B", "#1A1A1A", 40),
  ("contextual icon on its tint, light", "#A8000B", "#F9F2F3", 20),
  ("inline icon on the light page", "#A8000B", "#FFFFFF", 16)],
 "B · fold into Mono's reds": [
  ("bar type, light and dark (s149-D1)", "#1A1A1A", "#F6604C", 2),
  ("bar on the light page", "#F6604C", "#FFFFFF", 40),
  ("bar on the dark page", "#F6604C", "#1A1A1A", 40),
  ("contextual icon on its tint, light (as Alert)", "#F6604C", "#FDD9D4", 20),
  ("inline icon on the light page (s151-D1 dark red)", "#DA1A00", "#FFFFFF", 16)],
 "the trap · a bare re-point that keeps white type": [
  ("bar type, white on the light red", "#FFFFFF", "#F6604C", 2)],
}
out = {}
for cand, rows in PAIRS.items():
    out[cand] = []
    print(cand)
    for label, fg, bg, w in rows:
        r = dict(pair=label, fg=fg, bg=bg, width_px=w, wcag=round(wcag(fg, bg), 2), bloom=B(fg, bg, w), dance=D(fg, bg, w))
        out[cand].append(r)
        print(f"  {label:52} {fg} on {bg}  {r['wcag']:5.2f}:1  bloom {r['bloom']:6}  dance {r['dance']:6}")
json.dump(out, open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "scores.json"), "w"), indent=1)
