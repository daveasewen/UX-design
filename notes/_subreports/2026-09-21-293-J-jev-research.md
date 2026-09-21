# 293 · lane J — Jev integration research

**Filed** 2026-09-21 · **Scope** research only, no build, no commit · **Deliverable**
`notes/_lanes/293/J/jev-integration-brief.html`

Standing rule applied throughout: measured and declared are both published, never smoothed.
Every number below is labelled one or the other.

---

## 1 · What I read (URLs)

TypeSafe first-party:

- https://docs.typesafe.ai/ → redirects to `/introduction.md` — primitives table, atomic-question guidance
- https://docs.typesafe.ai/llms.txt — full doc index (~90 pages; cookbooks list read for measured claims)
- https://docs.typesafe.ai/introduction/quickstart.md — playground, cURL, request/response JSON, Python SDK, agent skill
- https://docs.typesafe.ai/api.md — full HTTP schema: endpoint, question types, answer types, error codes
- https://docs.typesafe.ai/models.md — price, rate limits, context budget, aliases, customisation, `GET /v1/models`
- https://docs.typesafe.ai/model-jaggedness/jev-1.13.md — nine named failure modes, last reviewed 2026-09-17
- https://docs.typesafe.ai/agent-skill.md — Claude Code plugin install, "good vibe coding principles", common issues
- https://typesafe.ai/blog/introducing-system-one-models-and-jev — launch post, 2026-09-15, Diogo Almeida

Ecosystem:

- https://raw.githubusercontent.com/rahulrajaram/jev-mcp/main/README.md — fork 0.5.0, five MCP tools, plugin internals
- https://raw.githubusercontent.com/NiazMorshed2007/jev-review/main/README.md — one tool, 19 quality dimensions, Agent Plugins 1.0 packaging

Apollo repo (read to name concrete judgment points, not re-derived):

- `knowledge/_gate_dataviz_vars.py`, `knowledge/_gate_scratch_hygiene.py` — docstring house style, CAN/CANNOT blocks, advisory-vs-blocking precedent
- `knowledge/_rulings.json` — `{_README, rulings}`, 622 records, fields `id · ruled · date · by · says · governs[] · evidence[]`
- `notes/_dream/_GRADE-DECISIONS.jsonl` — 187,612 bytes, records carry `kind · counts{FRESH/AGING/STALE/UNPROVABLE} · drive_note`
- `notes/_lanes/292/D/overview-dashboard-definition.html` — 29,393 chars, seven `<h2>` sections; the nine pass conditions live in §"What a one-shot has to do to pass" at byte 23383
- `knowledge/_memento_search.py` and `knowledge/_search_core.py` — `score_record` is lexical token overlap; `search()` buckets, sorts by `(-_score, len(text), id)`, caps per bucket
- `knowledge/_checkin.py` — STOP figure now from `gauge.STOP_LINE_TK` (`s271-D1`); regex demoted to declared fallback
- `reviews/APOLLO-MONO-PRIMARY-ACTION-2026-07-20-v2.REVIEW.html` — 39,137 chars, mostly inline CSS and live-editor markup

---

## 2 · What I measured in the sandbox

All run in the Cowork Linux sandbox, 2026-09-21, ~13:58–14:00 UTC. Commands and output verbatim.

### 2.1 — API host reachable

```
$ curl -sSI --max-time 20 https://api.typesafe.ai
HTTP/2 404
date: Mon, 21 Sep 2026 13:58:46 GMT
server: istio-envoy
content-length: 22
content-type: application/json
x-typesafe-request-id: req_01a0c4431ca87c3e9217a97755353886
x-envoy-upstream-service-time: 5
```

Measured: the allowlist reaches the host. 404 is the bare root; the endpoint is `/v1/systemone`.

### 2.2 — Endpoint answers, and the auth error is typed

```
$ curl -s --max-time 25 -X POST https://api.typesafe.ai/v1/systemone \
    -H "Content-Type: application/json" \
    -d '{"state":"test","model":"jev-latest","questions":{"q":{"type":"noul","instructions":"This is a test"}}}' \
    -w '\nHTTP=%{http_code}\n'
{"detail":{"error_type":"authentication_error","message":"Must supply an API key! Check your request and try again."}}
HTTP=403
```

```
$ curl -s --max-time 20 https://api.typesafe.ai/v1/models -w '\nHTTP=%{http_code}\n'
{"detail":{"error_type":"authentication_error","message":"Must supply an API key! Check your request and try again."}}
HTTP=403
```

**Measured-vs-declared mismatch, recorded not smoothed.** `docs.typesafe.ai/api.md` declares a
missing key returns **401 Unauthorized**. Both live calls returned **403** with
`error_type: authentication_error`. Any Apollo error handling must branch on the body's
`error_type`, not on the documented status code.

### 2.3 — Python SDK installs and imports

```
$ pip download typesafe-sdk --no-deps -d /tmp/x
Collecting typesafe-sdk
  Downloading typesafe_sdk-0.7.0-py3-none-any.whl.metadata (2.6 kB)
Downloading typesafe_sdk-0.7.0-py3-none-any.whl (35 kB)
Saved /tmp/x/typesafe_sdk-0.7.0-py3-none-any.whl
Successfully downloaded typesafe-sdk
```

```
$ pip install --quiet --target /tmp/tsx typesafe_sdk
$ PYTHONPATH=/tmp/tsx python3 -c "import typesafe_sdk as t; print(t.__version__); print([n for n in dir(t) if not n.startswith('_')][:20])"
0.7.0
['Answer', 'AsyncModels', 'AsyncTypeSafeClient', 'Choice', 'ChoiceAnswer', 'ChoiceModel',
 'JSONContent', 'JSONValue', 'ListModelsResponse', 'ModelMetadata', 'Models', 'Noul',
 'NoulAnswer', 'NoulCriteria', 'NoulModel', 'Question', 'QuestionModel', 'Questions',
 'RetryPolicy', 'Score']
```

Measured: PyPI reachable, SDK 0.7.0 installs and imports clean. Wheel is 35 KB, pure Python.
Note the package name split — **install** `typesafe-sdk`, **import** `typesafe_sdk`.

### 2.4 — npm, node, GitHub raw

```
$ node --version
v22.23.2

$ npm view @typesafe-ai/sdk version dist-tags
version = '0.6.0'
dist-tags = { bootstrap: '0.0.0-bootstrap.0', latest: '0.6.0' }

$ npm view github:rahulrajaram/jev-mcp name version
name = 'jev-mcp'
version = '0.5.0'

$ curl -sI --max-time 15 https://raw.githubusercontent.com/typesafe-ai/skills/main/skills/typesafe-ai/SKILL.md
HTTP/2 200

$ curl -sI --max-time 15 https://openrouter.ai/api/alpha/decisions
HTTP/2 404
```

Measured: Node 22.23.2 present; npm registry and a git-spec resolve both work, so
`npx -y github:rahulrajaram/jev-mcp#main` could run in the sandbox. OpenRouter's host is
reachable (404 is a GET on a POST-only path, not a block), so jev-mcp's second access path
is open too. JS SDK is `@typesafe-ai/sdk` 0.6.0 — one minor behind the Python SDK's 0.7.0.

**Trap recorded:** `npm view typesafe-sdk version` returns `0.0.0` — an unrelated squatted npm
package, not the TypeSafe SDK. The JS package is scoped: `@typesafe-ai/sdk`.

### 2.5 — Repo baseline

```
$ grep -ril 'typesafe\|jev-mcp\|jev_classify' --include=*.py --include=*.md --include=*.json knowledge notes
(no output)
```

Measured: zero existing Jev or TypeSafe references anywhere in `knowledge/` or `notes/`.
Greenfield.

### 2.6 — No live Jev call was made

No API key is present in the sandbox and I did not request one. **Every claim about Jev's
behaviour in the brief is the vendor's declared claim, not an Apollo measurement.** The only
things measured here are reachability, packaging and the auth-error shape.

---

## 3 · What I concluded

1. **Feasible today except for the key.** Network, packaging and runtime all check out from
   the Cowork sandbox. The single blocker is an early-access API key, which is Dave's to
   request at console.typesafe.ai/keys.

2. **The adapter beats the MCP for Apollo specifically.** A `knowledge/_jev.py` with a
   receipts log leaves a file behind; an MCP tool answers into a transcript. Apollo built the
   trigger index precisely because knowledge that exists only where someone already knew to
   look gets re-derived twenty-six sessions later. Routing judgments through a tool result
   would rebuild that failure with better latency.

3. **Cowork cannot load the MCP from a lane.** Cowork supports plugins as bundles of MCP
   servers plus skills, installed through the app. The sandbox shell has no route to register
   a server into the running session — `claude mcp add` and `/plugin install` are client-side
   actions. So path three is a Dave action in the client, not an agent action in a lane. I did
   not attempt an install, since that would change the user's session configuration.

4. **Most of Apollo's gates should not call Jev.** Eight of the nine dashboard pass conditions
   are DOM measurements; the stop line is arithmetic; scratch hygiene is a stat call. Jev's own
   jaggedness page rules itself out of all three classes — counting, arithmetic, date
   comparison. The genuine candidates are retrieval ranking, ruling-trigger recall, duplicate
   detection, citation classification and proposal triage: repeated, enumerable, prose-shaped.

5. **P4 is the one condition with no instrument.** "Every structural decision carries the
   ruling, principle or token it rests on" cannot be read by any gate in the tree. It is the
   clearest single place a typed classifier would add an instrument Apollo does not have. I
   still ranked the retrieval experiment first, because it has a right answer that predates
   the test and P4 does not.

6. **Recommended first experiment:** re-rank memento search on a known-answer fixture, using
   the ds-021 / #80 / #81 retrieval failure the trigger-index README already documents.
   Measure rank-of-correct-answer before and after. Writes only to the lane directory.

---

## 4 · What I could not verify

- **Any accuracy or calibration claim.** No key, no live call. 40–200×, 193.6×, 444.6×,
  70–500 ms, "calibrated", "cannot hallucinate" — all declared by TypeSafe, none measured here.
  The launch post itself flags that the eval workflows were written by TypeSafe's own
  capabilities team.
- **Jev's behaviour on design artefacts.** No published number exists on rendered interfaces,
  CSS, or design rulings. Every cookbook is tickets, legal text, filings, patents, beer.
- **Whether the waitlist is open.** The launch post says developers are being brought off "as
  quickly as we can"; I did not sign up and cannot say what the current wait is.
- **Current rate limits in practice.** Declared at 250k tok/s and 1,200 req/min, with an
  explicit vendor warning that these "can change without notice".
- **Whether `jev-mcp` or `jev-review` actually work.** READMEs read; neither installed, neither
  run. Both are third-party forks, MIT, unaffiliated with TypeSafe.
- **Claude's MCP connector registry** returned no Jev connector (established before this lane;
  not re-tested).
- **Token cost of this lane.** Not readable from inside the subagent — no instrument reached me.
  Declared estimate only: roughly 90–110K tokens, dominated by the four large doc fetches
  (api.md, models.md, jaggedness, the two READMEs at ~6K each) plus the launch post. Treat as
  unmeasured.

---

## 5 · Deliberate choices worth a line

- **canon.css is not linked from the brief.** It is 1,998,816 bytes and would override the
  Swiss token set the brief is built on. Checked first: the lane documents in
  `notes/_lanes/292/D/` cite `knowledge/canon/canon.css` as text in code spans and tables, and
  do not `<link>` it either. The brief follows that existing precedent rather than inventing a
  new one. Swiss system applied from
  `.claude/skills/swiss-design-system/SKILL.md` v2.0, accent kept at the documented
  `#DB0011` (5.08:1 on white) rather than swapped, so the contrast claim in the skill still
  holds without a re-check.
- **Nothing was committed, and `_CHAIN.md`, `GOOD-MORNING.md`, `_LIVE-STATE.md` and
  `_state.json` were not opened or touched.**
- **Two files created, both new:** the brief and this subreport. `notes/_lanes/293/J/` was
  created by this lane; `notes/_lanes/293/` previously held only `DA/`.
