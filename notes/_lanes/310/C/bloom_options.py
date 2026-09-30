"""#310 — the repo's bloom/dance model (reviews/_rag_bloom_model.py, v0, 2026-07-19) run on
lane B's five white-ink options. Only the model's functions are loaded; its demo prints are not run.
Scores are relative, 100 = a 40px white FILL on #1A1A1A (the model's own reference)."""
src=open('reviews/_rag_bloom_model.py').read(); src=src[:src.index("DPG='#1A1A1A'")]
ns={}; exec(src,ns); B,D,wcag=ns['B'],ns['D'],ns['wcag']
opts=[("As built: white on black","#FFFFFF","#000000","#1F1F1F"),
      ("#F0F0F0 on black","#F0F0F0","#000000","#1F1F1F"),
      ("#E1E1E1 on black","#E1E1E1","#000000","#1F1F1F"),
      ("Grey tiles (the reverse): white on #1F1F1F","#FFFFFF","#1F1F1F","#000000"),
      ("#0F0F0F tile: white","#FFFFFF","#0F0F0F","#1F1F1F"),
      ("Before #310: white on #1F1F1F tile, #1F1F1F ground","#FFFFFF","#1F1F1F","#1F1F1F")]
inks={"rise":"#66CC8D","fall":"#F6604C"}
print(f"{'option':52} {'text 2px':>9} {'value 5px':>9} {'wcag':>6} | {'rise 1.2px bloom/dance':>22} {'fall 1.2px bloom/dance':>22}")
for lab,fg,tile,ground in opts:
    r=f"{B(inks['rise'],tile,1.2)}/{D(inks['rise'],tile,1.2)}"; f=f"{B(inks['fall'],tile,1.2)}/{D(inks['fall'],tile,1.2)}"
    print(f"{lab:52} {B(fg,tile,2):9} {B(fg,tile,5):9} {wcag(fg,tile):6.2f} | {r:>22} {f:>22}")
