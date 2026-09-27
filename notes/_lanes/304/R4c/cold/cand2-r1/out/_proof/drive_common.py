import os, json
W = os.path.expanduser("~/cold/cand2-r1"); OUT = W + "/out"
URL = lambda n, q="": "file://%s/%s.html%s" % (OUT, n, q)
LOG = []
def check(name, ok, detail=""):
    LOG.append({"check": name, "ok": bool(ok), "detail": detail}); print(("PASS " if ok else "FAIL ") + name + ((" — " + str(detail)) if detail != "" else ""))
def attach(pg, errs):
    pg.on("console", lambda m: errs.append(m.type + ": " + m.text) if m.type in ("error",) else None)
    pg.on("pageerror", lambda e: errs.append("pageerror: " + str(e)))
def choose(pg, dd, value):
    pg.click("#%s-t" % dd); pg.wait_for_timeout(120)
    pg.click('#%s-m [data-value="%s"]' % (dd, value)); pg.wait_for_timeout(300)
def seg(pg, sid, value):
    pg.click('#%s button[data-value="%s"]' % (sid, value)); pg.wait_for_timeout(300)
def tbl_rows(pg, fid):
    return pg.eval_on_selector_all("#%s .dv-table tbody tr" % fid, "els => els.map(e => e.textContent.trim())")
def save(name):
    json.dump(LOG, open(W + "/proof/%s.json" % name, "w"), indent=1)
