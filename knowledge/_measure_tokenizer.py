#!/usr/bin/env python3
"""D1 — measure `tape` (tiktoken cl100k) against Claude's REAL token count.

RULED #52 (D1 (a)): *"spend a window measuring `tape` against real
`client.messages.count_tokens()`, then re-denominate."* Open 26. ★ Dave raised the tokenizer
at P3, SEVEN sessions before it was ruled: the claim was never *wrong*, so
[[assertion-propagation-gap]] — which fires on a FLIP — never chased it.

WHY IT MATTERS: every `tape` figure this project has ever published is `cl100k`, which is
OpenAI's tokenizer. `p50k` reads +8.6–11.1% on this corpus. Every cap, every band edge and
every price is denominated in a unit nobody has checked against the model doing the reading.

METHOD — measure, never convert [[measure-dont-convert-units]]:
  Take real samples ACROSS THE CORPUS's registers, not one blob — banner prose (★ ⚠ ⛔ dense),
  ordinary prose, Python source, JSON. A single ratio from a single sample would be a
  conversion wearing a measurement's clothes. Report PER-SAMPLE and only then the aggregate,
  so a register that behaves differently is visible rather than averaged away.

THE KEY never appears in output, in the repo, or in any log. `API-KEY.txt` is gitignored.
"""
from __future__ import annotations

import json
import os
import sys
import urllib.error
import urllib.request

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODEL = "claude-opus-5"
ENDPOINT = "https://api.anthropic.com/v1/messages/count_tokens"


def read_key() -> str:
    for name in ("API-KEY.txt", ".env.local"):
        p = os.path.join(REPO, name)
        if not os.path.exists(p):
            continue
        for line in open(p, encoding="utf-8"):
            s = line.strip().strip('"').strip("'")
            if s.startswith("ANTHROPIC_API_KEY="):
                s = s.split("=", 1)[1].strip().strip('"').strip("'")
            if s.startswith("sk-ant-"):
                return s
    sys.exit("NO KEY FOUND. Put it in API-KEY.txt (gitignored) on a line of its own.")


def real_tokens(key: str, text: str) -> int:
    body = json.dumps({"model": MODEL,
                       "messages": [{"role": "user", "content": text}]}).encode()
    req = urllib.request.Request(ENDPOINT, data=body, method="POST", headers={
        "x-api-key": key, "anthropic-version": "2023-06-01",
        "content-type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            return json.load(r)["input_tokens"]
    except urllib.error.HTTPError as e:
        sys.exit(f"API refused ({e.code}): {e.read().decode()[:200]}")


def main() -> int:
    import tiktoken
    enc = tiktoken.get_encoding("cl100k_base")
    key = read_key()

    def slab(path, start=0, n=120):
        with open(os.path.join(REPO, path), encoding="utf-8") as f:
            return "".join(f.read().splitlines(True)[start:start + n])

    samples = [
        ("banner prose (★⚠⛔ dense)", slab("_CHAIN.md", 27, 25)),
        ("runbook prose",             slab("knowledge/_RUNBOOK-capture-ritual.md", 130, 90)),
        ("ledger prose",              slab("notes/_MEMENTO-DECISIONS.md", 1324, 90)),
        ("python source",             slab("knowledge/_checkin.py", 0, 120)),
        ("§A orientation",            slab("GOOD-MORNING.md", 60, 90)),
    ]

    print(f"D1 — tape (cl100k) vs REAL tokens   model={MODEL}\n")
    print(f"  {'sample':<28} {'tape':>8} {'real':>8} {'ratio':>7}  {'drift':>7}")
    print("  " + "-" * 62)
    tot_t = tot_r = 0
    for name, text in samples:
        if not text.strip():
            print(f"  {name:<28} {'EMPTY — sample slab missed; not counted':>0}")
            continue
        t = len(enc.encode(text))
        r = real_tokens(key, text)
        tot_t += t
        tot_r += r
        print(f"  {name:<28} {t:>8,} {r:>8,} {r/t:>7.3f}  {r/t-1:>+6.1%}")
    print("  " + "-" * 62)
    print(f"  {'AGGREGATE':<28} {tot_t:>8,} {tot_r:>8,} {tot_r/tot_t:>7.3f}  {tot_r/tot_t-1:>+6.1%}")
    print(f"\n  ⇒ TAPE_TO_REAL = {tot_r/tot_t:.4f}   (n={len(samples)} registers)")
    print("  ⚠ Per-sample spread is the finding, not the aggregate: if the registers disagree,")
    print("    one ratio cannot re-denominate the corpus and each region needs its own.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
