#!/usr/bin/env python3
"""Launchpad step three — the gates served as MCP tools over stdio (#313 lane C3; spec § 6 and § 7).

MCP is the wire (s305-D45). This is a minimal MCP server, stdlib only: JSON-RPC 2.0, one message per
line on stdin and stdout (the MCP stdio transport), nothing else ever written to stdout; diagnostics go
to stderr. It answers `initialize`, `ping`, `tools/list` and `tools/call`, and ignores notifications.

Tools (input in, the § 7 verdict object out, as structuredContent and as one text block):
  gate_surface  {surface: [A2UI v0.9.1 messages], splice?: bool}  — the surface layer S1–S9; with
                splice the page layer P0–P4 also runs on the stand-in page
  gate_page     {html: "<page>"}                                  — the page layer P0–P4

A verdict of "fail" is a successful call (isError false): the gate worked and refused the screen. A
call the server cannot carry out (unknown tool, bad arguments, an exception) is isError true, with the
reason. The gate is warmed once, at `initialize`, so no tool call pays for reading the catalogue.

Run:  PYTHONDONTWRITEBYTECODE=1 python3 apollo-launchpad/gates/server.py      (the client spawns it)
"""
import json, os, sys, traceback

sys.dont_write_bytecode = True
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

PROTOCOL = "2025-06-18"
SERVER = {"name": "apollo-gates", "version": "0.1.0"}

VERDICT_SCHEMA = {
    "type": "object",
    "properties": {
        "verdict": {"enum": ["pass", "fail"]},
        "checks": {"type": "array", "items": {"type": "object", "properties": {
            "id": {"type": "string"}, "name": {"type": "string"},
            "result": {"enum": ["pass", "fail", "unmeasured", "n/a"]},
            "reasons": {"type": "array", "items": {"type": "string"}}},
            "required": ["id", "name", "result", "reasons"]}},
        "timing_ms": {"type": "object"},
        "catalogue": {"type": "object"}},
    "required": ["verdict", "checks", "timing_ms", "catalogue"],
}

TOOLS = [
    {"name": "gate_surface",
     "title": "Gate a screen description",
     "description": "Checks one screen, described as A2UI v0.9.1 messages, against the Apollo catalogue and "
                    "Apollo's own rules: valid messages and parts, one root, unique ids, references that "
                    "resolve, slot children of the kind the slot accepts, no deprecated part, states and "
                    "data that fit. Returns pass or fail with every check and its reasons. With splice, "
                    "also checks the page the screen stands for (a stand-in splice of reference markup).",
     "inputSchema": {"type": "object", "properties": {
         "surface": {"type": "array", "items": {"type": "object"},
                     "description": "The A2UI v0.9.1 messages for one surface (createSurface, updateComponents, updateDataModel)."},
         "splice": {"type": "boolean", "default": False,
                    "description": "Also run the page checks on the stand-in page."}},
         "required": ["surface"], "additionalProperties": False},
     "outputSchema": VERDICT_SCHEMA},
    {"name": "gate_page",
     "title": "Gate a page",
     "description": "Checks one HTML page held in memory with Apollo's static screen checks: provenance "
                    "receipt, accessibility (motion per part, target size, ARIA roles), composition span "
                    "legality, icon source, and compose (canon classes, no hex, canon.css linked not "
                    "pasted, the page never sizes a part). Returns pass or fail with every check.",
     "inputSchema": {"type": "object", "properties": {
         "html": {"type": "string", "description": "The page, as one HTML string."}},
         "required": ["html"], "additionalProperties": False},
     "outputSchema": VERDICT_SCHEMA},
]

_G = [None]


def gate():
    if _G[0] is None:
        import gate_mem
        _G[0] = gate_mem.gate()
    return _G[0]


def call_tool(name, args):
    if not isinstance(args, dict):
        raise ValueError("arguments must be an object")
    if name == "gate_surface":
        s = args.get("surface")
        if not isinstance(s, list):
            raise ValueError("gate_surface needs `surface`: a list of A2UI messages")
        return gate().gate_surface(s, splice=bool(args.get("splice", False)))
    if name == "gate_page":
        h = args.get("html")
        if not isinstance(h, str):
            raise ValueError("gate_page needs `html`: a string")
        return gate().gate_page(h)
    raise KeyError("unknown tool %r" % name)


def handle(msg):
    """-> the response dict, or None for a notification."""
    mid, method, params = msg.get("id"), msg.get("method"), msg.get("params") or {}
    if mid is None:
        return None                                   # notifications (initialized, cancelled …)
    if method == "initialize":
        gate()                                        # warm once, before the first tool call
        return {"jsonrpc": "2.0", "id": mid, "result": {
            "protocolVersion": params.get("protocolVersion") or PROTOCOL,
            "capabilities": {"tools": {"listChanged": False}},
            "serverInfo": SERVER,
            "instructions": "Gates for Apollo screens: gate_surface for an A2UI description, gate_page for a page."}}
    if method == "ping":
        return {"jsonrpc": "2.0", "id": mid, "result": {}}
    if method == "tools/list":
        return {"jsonrpc": "2.0", "id": mid, "result": {"tools": TOOLS}}
    if method == "tools/call":
        name = params.get("name")
        if name not in {t["name"] for t in TOOLS}:
            return {"jsonrpc": "2.0", "id": mid, "error": {"code": -32602, "message": "unknown tool %r" % name}}
        try:
            v = call_tool(name, params.get("arguments") or {})
            return {"jsonrpc": "2.0", "id": mid, "result": {
                "content": [{"type": "text", "text": json.dumps(v, ensure_ascii=False)}],
                "structuredContent": v, "isError": False}}
        except Exception as e:                        # a crash is not a fail: say it, as an error
            traceback.print_exc(file=sys.stderr)
            return {"jsonrpc": "2.0", "id": mid, "result": {
                "content": [{"type": "text", "text": "the gate could not run: %s" % e}], "isError": True}}
    return {"jsonrpc": "2.0", "id": mid, "error": {"code": -32601, "message": "method not found: %s" % method}}


def main():
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        try:
            msg = json.loads(line)
        except Exception as e:
            out = {"jsonrpc": "2.0", "id": None, "error": {"code": -32700, "message": "parse error: %s" % e}}
        else:
            out = handle(msg) if isinstance(msg, dict) else \
                {"jsonrpc": "2.0", "id": None, "error": {"code": -32600, "message": "invalid request"}}
        if out is not None:
            sys.stdout.write(json.dumps(out, ensure_ascii=False) + "\n")
            sys.stdout.flush()


if __name__ == "__main__":
    main()
