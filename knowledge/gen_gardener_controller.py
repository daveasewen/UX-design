#!/usr/bin/env python3
"""
gen_gardener_controller.py — the REVIEW-QUEUE CONTROLLER deck (brief §3c-②, RULED s179-D1(4)).

WHY THIS EXISTS. The #179 promotion probe measured the binding constraint: proposals
files were written and never promoted, because reading six 20KB prose files is a wall.
s179-D1(4) therefore made this the priority build — cadence enactment waits on it.
This generator turns `notes/_dream/_GARDENER-QUEUE.json` into ONE self-contained live
HTML deck: one DECISION CONTROL per item, clicks compile into a single copy-able ruling
message. Target: ten items ~ two minutes of taps.

★ THE DECK NEVER WRITES ANYTHING. It is not a fifth register (P3). It compiles a MESSAGE
that Dave pastes to the conductor; the CONDUCTOR enacts. There is no fetch, no storage,
no write-back — the queue data is EMBEDDED at generation time.

★ PROVENANCE IS STAMPED, VISIBLY. A deck rendered from a stale queue lies with confidence
(P23), so the source path, its mtime, its size, the pass_id and the item count are printed
on the page itself. And a missing/unreadable/wrong-schema queue makes this generator FAIL
LOUD with a nonzero rc and NO deck written — never a plausible-looking empty deck.

STYLING is deliberately plain and local: neutral greys, hairline rules, light+dark via
`prefers-color-scheme`. ⛔ It binds NO canon tokens (this is a throwaway review surface, not
a component) and uses NO red at all — the two-red law (s151-D1) and the green mirror
(s155-D1) govern MONO product surfaces and this page must not entangle with them. PAUSED is
a WORD in a neutral inverse badge; no meaning is carried by hue anywhere on the page.

Usage:
  python3 knowledge/gen_gardener_controller.py --write             # emit _GARDENER-REVIEW.html
  python3 knowledge/gen_gardener_controller.py --write --queue P --out F
  python3 knowledge/gen_gardener_controller.py --print             # HTML to stdout, no write
"""
import argparse
import datetime
import html
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from _helpgate import help_gate as _help_gate  # noqa: E402
_help_gate(__doc__, __name__, __file__)

REPO = os.path.dirname(HERE)
QUEUE = os.path.join(REPO, "notes", "_dream", "_GARDENER-QUEUE.json")
OUT = os.path.join(REPO, "_GARDENER-REVIEW.html")
SCHEMA = "gardener-queue/1"


class QueueUnreadable(RuntimeError):
    """⚠ LOUD AND NAMED (same shape as _governs.IndexUnreadable, deliberately).

    A deck built from a queue that could not be read would be indistinguishable, on the
    page, from a deck built from a queue with nothing in it. Refuse instead."""


def load_queue(path):
    if not os.path.isfile(path):
        raise QueueUnreadable(
            f"⛔ QUEUE MISSING — {path} is not there. No deck written: a review surface with "
            f"no provenance is worse than no review surface (P23). Run "
            f"`python3 knowledge/_gardener.py --sweep` first.")
    try:
        with open(path, encoding="utf-8") as fh:
            data = json.load(fh)
    except (json.JSONDecodeError, UnicodeDecodeError) as e:
        raise QueueUnreadable(f"⛔ QUEUE UNPARSEABLE — {path}: {e}. No deck written.")
    if not isinstance(data, dict) or data.get("$schema") != SCHEMA:
        raise QueueUnreadable(
            f"⛔ QUEUE SCHEMA MISMATCH — {path} declares "
            f"{data.get('$schema') if isinstance(data, dict) else type(data).__name__!r}, "
            f"expected {SCHEMA!r}. No deck written.")
    for key in ("items", "backpressure", "queue_cap_q", "cap_n", "pass_id"):
        if key not in data:
            raise QueueUnreadable(f"⛔ QUEUE INCOMPLETE — {path} has no {key!r}. No deck written.")
    if not isinstance(data["items"], list):
        raise QueueUnreadable(f"⛔ QUEUE MALFORMED — {path}: 'items' is not a list. No deck written.")
    return data


def _days_since(datestr):
    try:
        d = datetime.date.fromisoformat(str(datestr)[:10])
    except (ValueError, TypeError):
        return None
    return (datetime.date.today() - d).days


def deferment_line(data):
    """§3c-③ deferment pricing — visible age, stated cost. True cost, no alarm, no deadline."""
    bp = data.get("backpressure", {}) or {}
    n = len(data.get("items", []))
    oldest = bp.get("oldest_open")
    age = _days_since(oldest)
    age_txt = "none open" if not oldest else (
        f"oldest {age} day{'' if age == 1 else 's'}" if age is not None else f"oldest {oldest}")
    arm = str(bp.get("proposal_arm", "UNKNOWN"))
    tail = "proposal arm paused." if arm.upper() == "PAUSED" else "proposal arm running."
    return f"Review queue: {n} item{'' if n == 1 else 's'}, {age_txt} — while it waits: {tail}"


def is_paused(data):
    """PAUSED = the s179-D1(3) rule as MEASURED here, or as declared by the generator.

    Measured first: `open_count > Q` is the ruled condition. The declared `proposal_arm`
    is honoured too, so a gardener that pauses for its own reason still shows through."""
    bp = data.get("backpressure", {}) or {}
    q = data.get("queue_cap_q")
    oc = bp.get("open_count")
    measured = isinstance(oc, int) and isinstance(q, int) and oc > q
    declared = str(bp.get("proposal_arm", "")).upper() == "PAUSED"
    return measured or declared, measured, declared


def e(s):
    return html.escape("" if s is None else str(s), quote=True)


CSS = """
:root{
  --gc-ink:#1A1A1A; --gc-mute:#565656; --gc-rule:#D7D8D6; --gc-band:#F4F4F3;
  --gc-bg:#FFFFFF; --gc-card:#FFFFFF; --gc-sel:#1A1A1A; --gc-selink:#FFFFFF;
  --gc-mono:ui-monospace,SFMono-Regular,Menlo,Consolas,monospace;
  --gc-font:"Helvetica Neue",Helvetica,Arial,sans-serif;
}
@media (prefers-color-scheme: dark){
  :root{ --gc-ink:#ECECEC; --gc-mute:#A6A6A6; --gc-rule:#3A3A3A; --gc-band:#1E1E1E;
         --gc-bg:#141414; --gc-card:#191919; --gc-sel:#ECECEC; --gc-selink:#141414; }
}
*{box-sizing:border-box}
body{margin:0;background:var(--gc-bg);color:var(--gc-ink);font-family:var(--gc-font);
  font-size:16px;line-height:1.5;-webkit-font-smoothing:antialiased}
.wrap{max-width:960px;margin:0 auto;padding:2rem 1.5rem 6rem}
h1{font-size:1.6rem;margin:0 0 .25rem;letter-spacing:-.01em}
.sub{color:var(--gc-mute);margin:0 0 1.5rem}
.prov{font-family:var(--gc-mono);font-size:.72rem;color:var(--gc-mute);
  background:var(--gc-band);border:1px solid var(--gc-rule);padding:.6rem .75rem;
  border-radius:2px;margin:0 0 1.5rem;white-space:pre-wrap}
.strip{border-top:2px solid var(--gc-ink);border-bottom:1px solid var(--gc-rule);
  padding:.9rem 0;margin:0 0 1.25rem;display:flex;flex-wrap:wrap;gap:1.75rem}
.strip .k{font-size:.68rem;text-transform:uppercase;letter-spacing:.09em;color:var(--gc-mute)}
.strip .v{font-size:1.15rem;font-variant-numeric:tabular-nums}
.badge{display:inline-block;font-size:.68rem;letter-spacing:.09em;text-transform:uppercase;
  border:1px solid var(--gc-rule);padding:.15rem .45rem;border-radius:2px;color:var(--gc-mute)}
.badge.on{background:var(--gc-sel);color:var(--gc-selink);border-color:var(--gc-sel)}
.pausebar{background:var(--gc-sel);color:var(--gc-selink);padding:.85rem 1rem;border-radius:2px;
  margin:0 0 1.25rem;font-weight:700;letter-spacing:.03em}
.pausebar span{font-weight:400;display:block;letter-spacing:0;opacity:.85;margin-top:.2rem}
.defer{border-left:3px solid var(--gc-ink);padding:.5rem .85rem;margin:0 0 2rem;color:var(--gc-mute)}
.card{border:1px solid var(--gc-rule);background:var(--gc-card);border-radius:2px;
  padding:1.1rem 1.25rem;margin:0 0 1rem}
.card h2{font-size:.82rem;font-family:var(--gc-mono);margin:0 0 .5rem;letter-spacing:.02em}
.meta{font-size:.72rem;color:var(--gc-mute);margin:0 0 .75rem;display:flex;gap:.5rem;flex-wrap:wrap;align-items:center}
.q{font-family:var(--gc-mono);font-size:.8rem;background:var(--gc-band);border-left:2px solid var(--gc-rule);
  padding:.5rem .7rem;margin:.35rem 0 .75rem;white-space:pre-wrap;word-break:break-word}
.lbl{font-size:.65rem;text-transform:uppercase;letter-spacing:.09em;color:var(--gc-mute);margin-top:.6rem}
.btns{display:flex;gap:.5rem;margin-top:.9rem;flex-wrap:wrap}
button{font:inherit;font-size:.85rem;padding:.45rem 1rem;border:1px solid var(--gc-rule);
  background:transparent;color:var(--gc-ink);border-radius:2px;cursor:pointer}
button[aria-pressed="true"]{background:var(--gc-sel);color:var(--gc-selink);border-color:var(--gc-sel);font-weight:700}
button[disabled]{opacity:.35;cursor:not-allowed}
.empty{border:1px dashed var(--gc-rule);padding:2rem;text-align:center;color:var(--gc-mute);border-radius:2px}
.compile{position:sticky;bottom:0;background:var(--gc-bg);border-top:2px solid var(--gc-ink);
  padding:1rem 0;margin-top:2rem}
textarea{width:100%;min-height:9rem;font-family:var(--gc-mono);font-size:.8rem;padding:.7rem;
  border:1px solid var(--gc-rule);background:var(--gc-band);color:var(--gc-ink);border-radius:2px}
.count{font-size:.75rem;color:var(--gc-mute);margin:.4rem 0 0}
"""

JS = r"""
(function(){
  var picks = {};
  function render(){
    var ids = window.__GQ_IDS__ || [];
    var lines = [], done = 0;
    for (var i=0;i<ids.length;i++){
      var id = ids[i];
      if (picks[id]) { lines.push(id + ": " + picks[id]); done++; }
    }
    var out = document.getElementById("compiled");
    var head = "Gardener review — pass " + window.__GQ_PASS__ + " (" + done + " of " + ids.length + " ruled)";
    out.value = done ? (head + "\n" + lines.join("\n")) : "";
    document.getElementById("count").textContent = done + " of " + ids.length + " ruled" +
      (done === ids.length && ids.length ? " — complete, copy and paste to the conductor." : "");
  }
  document.addEventListener("click", function(ev){
    var b = ev.target.closest("button[data-gq]");
    if (b){
      var id = b.getAttribute("data-gq"), v = b.getAttribute("data-v");
      picks[id] = (picks[id] === v) ? null : v;
      var group = document.querySelectorAll('button[data-gq="'+id+'"]');
      for (var i=0;i<group.length;i++){
        group[i].setAttribute("aria-pressed", String(group[i].getAttribute("data-v") === picks[id]));
      }
      render(); return;
    }
    if (ev.target.id === "copybtn"){
      var ta = document.getElementById("compiled");
      ta.select(); try { document.execCommand("copy"); } catch(e){}
      ev.target.textContent = "copied";
      setTimeout(function(){ ev.target.textContent = "copy ruling message"; }, 1400);
    }
  });
  // flag_only items: the flag is PRESELECTED — P7 is mechanical, not a judgment.
  (window.__GQ_PRESET__ || []).forEach(function(id){
    var b = document.querySelector('button[data-gq="'+id+'"][data-v="flag"]');
    if (b) b.click();
  });
  render();
})();
"""


def card(item):
    iid = item.get("id", "?")
    canon = item.get("canon", {}) or {}
    ev = item.get("evidence", {}) or {}
    prop = item.get("proposed")
    flag_only = bool(item.get("flag_only"))
    tier = item.get("tier", "?")
    parts = []
    parts.append(f'<article class="card" id="card-{e(iid)}">')
    parts.append(f'<h2>{e(iid)}</h2>')
    meta = [f'<span class="badge">tier {e(tier)}</span>',
            f'<span class="badge">{e(item.get("detector", "?"))}</span>',
            f'<span class="badge">{e(item.get("disposition", ""))}</span>']
    if flag_only:
        meta.append('<span class="badge on">flag-only</span>')
    meta.append(f'<span>{e(canon.get("path", ""))}:{e(canon.get("line", ""))}'
                f' · ★w {e(canon.get("star_weight", 0))}'
                f' · {"ratified" if canon.get("ratified") else "unratified"}'
                f' · first seen {e(item.get("first_seen", ""))}</span>')
    parts.append('<div class="meta">' + "".join(meta) + '</div>')
    parts.append('<div class="lbl">canon says</div>')
    parts.append(f'<div class="q">{e(canon.get("quote", ""))}</div>')
    parts.append('<div class="lbl">evidence</div>')
    parts.append(f'<div class="q">{e(ev.get("quote", ""))}</div>')
    parts.append('<div class="lbl">probe</div>')
    parts.append(f'<div class="q">{e(ev.get("probe", ""))}</div>')
    if isinstance(prop, dict):
        parts.append('<div class="lbl">proposed before → after</div>')
        parts.append(f'<div class="q">{e(prop.get("before", ""))}\n→ {e(prop.get("after", ""))}</div>')
    if item.get("tier_reason"):
        parts.append(f'<p class="count">{e(item["tier_reason"])}</p>')
    acc = ' disabled title="flag-only — accept is not available on this item"' if flag_only else ''
    parts.append('<div class="btns">'
                 f'<button data-gq="{e(iid)}" data-v="accept" aria-pressed="false"{acc}>accept</button>'
                 f'<button data-gq="{e(iid)}" data-v="flag" aria-pressed="false">flag-only</button>'
                 f'<button data-gq="{e(iid)}" data-v="reject" aria-pressed="false">reject</button>'
                 '</div>')
    parts.append('</article>')
    return "\n".join(parts)


def build(data, src, stat):
    items = data.get("items", [])
    bp = data.get("backpressure", {}) or {}
    paused, measured, declared = is_paused(data)
    mtime = datetime.datetime.fromtimestamp(stat.st_mtime).isoformat(timespec="seconds")
    prov = (f"SOURCE   {os.path.relpath(src, REPO)}\n"
            f"MTIME    {mtime}   ({stat.st_size} bytes)\n"
            f"PASS     {data.get('pass_id', '?')}   generated {data.get('generated', '?')}\n"
            f"ITEMS    {len(items)} embedded   (cap N={data.get('cap_n')}, queue cap Q={data.get('queue_cap_q')})\n"
            f"DECK     rendered {datetime.datetime.now().isoformat(timespec='seconds')} "
            f"by knowledge/gen_gardener_controller.py — this deck WRITES NOTHING")
    trunc = data.get("truncated", {}) or {}
    if trunc.get("declared"):
        prov += (f"\nTRUNCATED  declared: found {trunc.get('found')}, filed {trunc.get('filed')}, "
                 f"dropped {trunc.get('dropped')} — {trunc.get('note', '')}")

    body = []
    body.append('<div class="wrap">')
    body.append('<h1>Gardener review queue</h1>')
    body.append('<p class="sub">One decision per card. Clicks compile into a single ruling message '
                'at the bottom — copy it to the conductor, who enacts. This page writes nothing.</p>')
    body.append(f'<pre class="prov">{e(prov)}</pre>')

    if paused:
        why = []
        if measured:
            why.append(f"open_count {bp.get('open_count')} &gt; Q={data.get('queue_cap_q')}")
        if declared:
            why.append("queue declares proposal_arm PAUSED")
        body.append('<div class="pausebar">PROPOSAL ARM PAUSED'
                    f'<span>{" · ".join(why)}. Per s179-D1(3): while the queue is over cap the '
                    'proposal arm pauses; Tier-1 repairs and refreshes CONTINUE, and queued items '
                    'never expire or auto-close. Clearing this queue restarts the arm.</span></div>')

    oldest = bp.get("oldest_open")
    age = _days_since(oldest)
    body.append('<div class="strip">'
                f'<div><div class="k">open</div><div class="v">{e(bp.get("open_count", len(items)))}'
                f' / Q={e(data.get("queue_cap_q"))}</div></div>'
                f'<div><div class="k">oldest open</div><div class="v">{e(oldest or "—")}'
                f'{f" ({age}d)" if age is not None else ""}</div></div>'
                f'<div><div class="k">proposal arm</div><div class="v">'
                f'{e(bp.get("proposal_arm", "UNKNOWN"))}</div></div>'
                f'<div><div class="k">added this pass</div><div class="v">'
                f'{e(bp.get("added_this_pass", 0))}</div></div>'
                f'<div><div class="k">files swept</div><div class="v">'
                f'{e(len(data.get("swept", [])))}</div></div>'
                '</div>')

    body.append(f'<p class="defer">§3c-③ deferment price: {e(deferment_line(data))}</p>')

    if not items:
        body.append('<div class="empty"><strong>Queue empty — nothing to review.</strong><br>'
                    'The gardener swept and filed zero findings this pass. This is an HONEST '
                    'empty state, not a render failure: the provenance block above names the '
                    'source file and its mtime, so an empty deck and a stale deck are '
                    'distinguishable. Nothing to compile.</div>')
    else:
        body.extend(card(it) for it in items)

    body.append('<div class="compile">'
                '<div class="lbl">compiled ruling message — paste to the conductor</div>'
                '<textarea id="compiled" readonly placeholder="No decisions yet — tap a button on any card."></textarea>'
                '<p class="count" id="count"></p>'
                '<button id="copybtn">copy ruling message</button>'
                '</div>')
    body.append('</div>')

    ids = json.dumps([it.get("id") for it in items])
    preset = json.dumps([it.get("id") for it in items if it.get("flag_only")])
    return (
        '<!doctype html>\n<html lang="en"><head><meta charset="utf-8">\n'
        '<meta name="viewport" content="width=device-width,initial-scale=1">\n'
        f'<title>Gardener review queue — {e(data.get("pass_id", ""))}</title>\n'
        f'<style>{CSS}</style>\n</head>\n<body>\n'
        + "\n".join(body)
        + f'\n<script>window.__GQ_IDS__={ids};window.__GQ_PRESET__={preset};'
          f'window.__GQ_PASS__={json.dumps(data.get("pass_id", ""))};</script>\n'
        + f'<script>{JS}</script>\n</body></html>\n'
    )


def main():
    ap = argparse.ArgumentParser(description="Generate the gardener review-queue controller deck.")
    ap.add_argument("--queue", default=QUEUE)
    ap.add_argument("--out", default=OUT)
    ap.add_argument("--write", action="store_true", help="write the deck (required to write)")
    ap.add_argument("--print", dest="to_stdout", action="store_true", help="HTML to stdout, no write")
    a = ap.parse_args()

    try:
        data = load_queue(a.queue)
    except QueueUnreadable as ex:
        print(str(ex), file=sys.stderr)
        return 3

    stat = os.stat(a.queue)
    doc = build(data, a.queue, stat)

    if a.to_stdout:
        sys.stdout.write(doc)
        return 0
    if not a.write:
        print("gen_gardener_controller: nothing written (pass --write or --print). "
              f"Queue OK: {len(data['items'])} items, pass {data.get('pass_id')}.")
        return 0
    with open(a.out, "w", encoding="utf-8") as fh:
        fh.write(doc)
    n = len(data["items"])
    print(f"gen_gardener_controller: wrote {a.out} ({len(doc)} bytes) — {n} item(s)"
          + (" — HONEST EMPTY STATE rendered, rc=0" if n == 0 else "")
          + (" — PAUSED banner rendered" if is_paused(data)[0] else ""))
    return 0


if __name__ == "__main__":
    sys.exit(main())
