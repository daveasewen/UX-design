#!/usr/bin/env python3
"""_board.py — the NOTICE BOARD for seats that run at the same time (idea #293, built 2026-10-02 #314-sq).

Dave, #293, verbatim: "could we have a notice board or something for agents".
Dave, #314, verbatim: "the noticeboard should have been built, thats annoying, id do it"
and, on how: "whatever has the least jeopardy".

WHAT IT IS. A present-tense board. Handoffs are serial, memento is the past on request, receipts
come after the fact; none says who is live NOW, what they touch, what they need. One append-only
JSONL file, one post per line. Nothing on it is a ruling or a receipt: a post that matters is
PROMOTED by the wrap into a handoff line or a subreport, then the wrap clears the board.

THE LEAST-JEOPARDY ANSWERS to #293's four open questions (each is Dave's to overturn):
  1. LOCAL, NOT COMMITTED — the board lives at knowledge/_tmp/_BOARD.jsonl, already gitignored
     (.gitignore line `knowledge/_tmp/`). Seats on one mount share it; no commit noise, no merge.
     Cloud worktrees do NOT see it — a cloud lane posts through its conductor.
  2. CLAIMS ADVISE, NEVER BLOCK — a seat that dies holding a blocking claim would lock the room.
  3. EXPIRY IS BY READING — `read` and `role` ignore expired posts; nothing rewrites the file
     except `sweep`, which only the wrap runs.
  4. ROLE — `role` answers "is a conductor live?" so a seat can open as a worker by itself
     instead of by Dave's word "sq". A conductor claim lasts 14 h unless released or renewed.

Usage:
  python3 knowledge/_board.py read                       # live posts, newest last (boot + seam checks)
  python3 knowledge/_board.py role                       # CONDUCTOR LIVE: … | NO LIVE CONDUCTOR
  python3 knowledge/_board.py post --who 314-sq --what "researching Hindsight" [--kind note]
        [--touching notes/_receipts/x.md ...] [--needs "a sentence"] [--expires 2h|30m|wrap|<ISO>]
  python3 knowledge/_board.py conductor --who 314        # claim the conductor role (14 h)
  python3 knowledge/_board.py release --who 314-sq       # end every earlier post by that seat
  python3 knowledge/_board.py sweep --to notes/_lanes/<n>/W/BOARD-AT-WRAP.md   # WRAP ONLY: copy all, then clear
  python3 knowledge/_board.py --selftest                 # known-answer bites on a temp board

Kinds and default expiry: claim 30m (git, a file, a render slot) · conductor 14h · note 12h ·
handup wrap · question wrap. `--expires wrap` lasts until the next sweep.
Env BOARD_PATH overrides the board path (the selftest uses it).
"""
import os as _hg_os, sys as _hg_sys  # noqa: E402 - help gate (#158 write-by-default class)
_hg_d = _hg_os.path.dirname(_hg_os.path.abspath(__file__))
while _hg_d != "/" and not _hg_os.path.exists(_hg_os.path.join(_hg_d, "_helpgate.py")):
    _hg_d = _hg_os.path.dirname(_hg_d)
_hg_sys.path.insert(0, _hg_d)
from _helpgate import help_gate as _help_gate; _help_gate(__doc__, __name__, __file__)
import argparse, json, os, re, sys, tempfile
from datetime import datetime, timedelta, timezone

HERE = os.path.dirname(os.path.abspath(__file__))
DEFAULT_BOARD = os.path.join(HERE, "_tmp", "_BOARD.jsonl")
KINDS = {"claim": "30m", "conductor": "14h", "note": "12h", "handup": "wrap", "question": "wrap", "release": "wrap"}
READ_CAP = 25          # boot cost: never print more than this many live posts
LINE_CAP = 200         # chars per printed post


def board_path():
    return os.environ.get("BOARD_PATH") or DEFAULT_BOARD


def now():
    return datetime.now(timezone.utc).replace(microsecond=0)


def parse_expiry(text, start):
    if text in (None, "", "wrap"):
        return "wrap"
    m = re.fullmatch(r"(\d+)([mh])", text)
    if m:
        n = int(m.group(1))
        return (start + (timedelta(minutes=n) if m.group(2) == "m" else timedelta(hours=n))).isoformat()
    try:
        dt = datetime.fromisoformat(text)
    except ValueError:
        sys.exit(f"REFUSED: --expires must be 30m, 2h, wrap or an ISO time, not {text!r}")
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return dt.isoformat()


def load():
    path = board_path()
    posts = []
    if not os.path.exists(path):
        return posts
    with open(path, encoding="utf-8") as fh:
        for n, line in enumerate(fh, 1):
            line = line.strip()
            if not line:
                continue
            try:
                posts.append(json.loads(line))
            except json.JSONDecodeError:
                posts.append({"ts": "", "who": "?", "kind": "note", "what": f"(unreadable line {n})", "expires": "wrap"})
    return posts


def live(posts, at=None):
    at = at or now()
    released = {}
    for p in posts:
        if p.get("kind") == "release":
            released[p.get("who")] = max(released.get(p.get("who"), ""), p.get("ts", ""))
    out = []
    for p in posts:
        if p.get("kind") == "release":
            continue
        if p.get("ts", "") <= released.get(p.get("who"), ""):
            continue
        exp = p.get("expires", "wrap")
        if exp != "wrap" and datetime.fromisoformat(exp) <= at:
            continue
        out.append(p)
    return out


def append(post):
    path = board_path()
    os.makedirs(os.path.dirname(path), exist_ok=True)
    data = (json.dumps(post, ensure_ascii=False) + "\n").encode("utf-8")
    fd = os.open(path, os.O_WRONLY | os.O_APPEND | os.O_CREAT, 0o600)
    try:
        os.write(fd, data)            # one write per post: appends from two seats do not interleave
    finally:
        os.close(fd)


def make_post(who, kind, what, touching=None, needs=None, expires=None):
    if kind not in KINDS:
        sys.exit(f"REFUSED: --kind must be one of {', '.join(KINDS)}")
    if not who or not what:
        sys.exit("REFUSED: a post needs --who and --what")
    t = now()
    return {"ts": t.isoformat(), "who": who, "kind": kind, "what": what,
            "touching": touching or [], "needs": needs or "",
            "expires": parse_expiry(expires or KINDS[kind], t)}


def fmt(p):
    exp = p.get("expires", "wrap")
    exp = "at wrap" if exp == "wrap" else "until " + exp[11:16] + "Z"
    s = f"[{p.get('ts','')[11:16]}Z] {p.get('who')} · {p.get('kind')} · {p.get('what')}"
    if p.get("touching"):
        s += " · touching " + ", ".join(p["touching"])
    if p.get("needs"):
        s += " · NEEDS " + p["needs"]
    s += f" · {exp}"
    return s if len(s) <= LINE_CAP else s[: LINE_CAP - 1] + "…"


def cmd_read(_):
    posts = live(load())
    if not posts:
        print("BOARD: empty (no live posts)")
        return 0
    shown = posts[-READ_CAP:]
    head = f"BOARD: {len(posts)} live post(s)" + (f", newest {READ_CAP} shown" if len(posts) > READ_CAP else "")
    print(head)
    for p in shown:
        print("  " + fmt(p))
    return 0


def conductors(posts):
    return [p for p in live(posts) if p.get("kind") == "conductor"]


def cmd_role(args):
    cs = conductors(load())
    if not cs:
        print("NO LIVE CONDUCTOR — this seat may conduct; claim it: _board.py conductor --who <n>")
        return 0
    c = cs[-1]
    others = f" (+{len(cs) - 1} older claim(s) still live — two conductors?)" if len(cs) > 1 else ""
    print(f"CONDUCTOR LIVE: {c['who']} since {c['ts'][11:16]}Z, until {c['expires'][11:16]}Z{others} — "
          f"open as a WORKER unless Dave says otherwise")
    return 0


def cmd_post(args):
    append(make_post(args.who, args.kind, args.what, args.touching, args.needs, args.expires))
    print("posted"); return 0


def cmd_conductor(args):
    cs = conductors(load())
    mine = [c for c in cs if c["who"] == args.who]
    theirs = [c for c in cs if c["who"] != args.who]
    if theirs:
        print(f"ADVISORY: {theirs[-1]['who']} already holds the conductor claim — posted yours anyway; "
              f"Dave decides who conducts", file=sys.stderr)
    append(make_post(args.who, "conductor", args.what or "conducting", expires=args.expires))
    print("renewed" if mine else "claimed"); return 0


def cmd_release(args):
    append(make_post(args.who, "release", args.what or "released"))
    print("released"); return 0


def cmd_sweep(args):
    posts = load()
    if not args.to:
        sys.exit("REFUSED: sweep needs --to <file>; it is the wrap's step, and it CLEARS the board")
    lv = live(posts)
    lines = [f"# Board at sweep — {now().isoformat()}", "",
             f"{len(posts)} post(s) on the board, {len(lv)} live at sweep. Verbatim JSONL below.", "", "```"]
    lines += [json.dumps(p, ensure_ascii=False) for p in posts] + ["```", ""]
    os.makedirs(os.path.dirname(os.path.abspath(args.to)) or ".", exist_ok=True)
    with open(args.to, "a", encoding="utf-8") as fh:
        fh.write("\n".join(lines))
    open(board_path(), "w").close()
    print(f"swept {len(posts)} post(s) to {args.to}; board cleared"); return 0


def selftest():
    fails = []
    with tempfile.TemporaryDirectory() as d:
        os.environ["BOARD_PATH"] = os.path.join(d, "b.jsonl")
        def check(name, cond):
            print(("  ok   " if cond else "  FAIL ") + name)
            if not cond: fails.append(name)
        check("empty board has no conductor", conductors(load()) == [])
        append(make_post("A", "conductor", "conducting"))
        check("claim makes a live conductor", [c["who"] for c in conductors(load())] == ["A"])
        append(make_post("B", "note", "researching", ["notes/x.md"], "nothing"))
        check("two live posts", len(live(load())) == 2)
        old = make_post("C", "claim", "git"); old["expires"] = (now() - timedelta(minutes=1)).isoformat()
        append(old)
        check("expired claim is not live", all(p["who"] != "C" for p in live(load())))
        append(make_post("A", "release", "done"))
        check("release ends A's conductor claim", conductors(load()) == [])
        check("release leaves B's note live", [p["who"] for p in live(load())] == ["B"])
        out = os.path.join(d, "swept.md")
        class A: to = out
        cmd_sweep(A)
        check("sweep clears the board", load() == [])
        check("sweep keeps every post verbatim", open(out).read().count('"who"') == 4)
        try:
            parse_expiry("soon", now()); check("bad expiry refused", False)
        except SystemExit:
            check("bad expiry refused", True)
    print("selftest:", "PASS" if not fails else f"FAIL ({len(fails)})")
    return 1 if fails else 0


def main(argv):
    if argv[:1] == ["--selftest"]:
        return selftest()
    ap = argparse.ArgumentParser(description="the notice board for concurrent seats")
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("read"); sub.add_parser("role")
    p = sub.add_parser("post")
    p.add_argument("--who", required=True); p.add_argument("--what", required=True)
    p.add_argument("--kind", default="note", choices=list(KINDS))
    p.add_argument("--touching", nargs="*"); p.add_argument("--needs"); p.add_argument("--expires")
    c = sub.add_parser("conductor"); c.add_argument("--who", required=True); c.add_argument("--what"); c.add_argument("--expires")
    r = sub.add_parser("release"); r.add_argument("--who", required=True); r.add_argument("--what")
    s = sub.add_parser("sweep"); s.add_argument("--to")
    a = ap.parse_args(argv)
    return {"read": cmd_read, "role": cmd_role, "post": cmd_post, "conductor": cmd_conductor,
            "release": cmd_release, "sweep": cmd_sweep}[a.cmd](a)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
