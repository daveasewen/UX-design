"""305 B2 — format-preserving JSON edits. A tiny recursive-descent scanner records the text span of every
value by path, so an edit replaces ONLY that value's text and every other byte of the file stays as it was
(the #179 lesson: a default json.dump reformats the whole file)."""
import json, re

WS = re.compile(r"\s*")
STR = re.compile(r'"(?:[^"\\]|\\.)*"', re.S)
NUM = re.compile(r"-?\d+(?:\.\d+)?(?:[eE][+-]?\d+)?")

def _ws(s, i):
    return WS.match(s, i).end()

def scan(s, i=0):
    """returns (node, end); node = {'s': start, 'e': end, 'kind', 'kids': {key: node} | [node], 'kstart': {key: pos}}"""
    i = _ws(s, i)
    c = s[i]
    if c == "{":
        node = {"s": i, "kind": "obj", "kids": {}, "kstart": {}}
        j = _ws(s, i + 1)
        if s[j] == "}":
            node["e"] = j + 1; return node, j + 1
        while True:
            j = _ws(s, j)
            m = STR.match(s, j); key = json.loads(m.group(0)); ks = j
            j = _ws(s, m.end()); assert s[j] == ":"
            child, j = scan(s, j + 1)
            node["kids"][key] = child; node["kstart"][key] = ks
            j = _ws(s, j)
            if s[j] == ",": j += 1; continue
            assert s[j] == "}"; node["e"] = j + 1; return node, j + 1
    if c == "[":
        node = {"s": i, "kind": "arr", "kids": []}
        j = _ws(s, i + 1)
        if s[j] == "]":
            node["e"] = j + 1; return node, j + 1
        while True:
            child, j = scan(s, j)
            node["kids"].append(child)
            j = _ws(s, j)
            if s[j] == ",": j += 1; continue
            assert s[j] == "]"; node["e"] = j + 1; return node, j + 1
    if c == '"':
        m = STR.match(s, i); return {"s": i, "e": m.end(), "kind": "str"}, m.end()
    for lit in ("true", "false", "null"):
        if s.startswith(lit, i): return {"s": i, "e": i + len(lit), "kind": "lit"}, i + len(lit)
    m = NUM.match(s, i); return {"s": i, "e": m.end(), "kind": "num"}, m.end()

def node_at(s, path):
    n, _ = scan(s)
    for p in path:
        n = n["kids"][p]
    return n

def col_of(s, pos):
    return pos - (s.rfind("\n", 0, pos) + 1)

def dumps_at(obj, indent_col, step=2):
    txt = json.dumps(obj, indent=step, ensure_ascii=False)
    return txt.replace("\n", "\n" + " " * indent_col)

def replace_value(s, path, obj):
    """replace the value at path; the new text is indented to the column of the line the value sits on."""
    n = node_at(s, path)
    line_start = s.rfind("\n", 0, n["s"]) + 1
    base = len(s[line_start:n["s"]]) - len(s[line_start:n["s"]].lstrip())
    return s[:n["s"]] + dumps_at(obj, base) + s[n["e"]:]

def replace_string(s, path, new_str):
    n = node_at(s, path); assert n["kind"] == "str"
    return s[:n["s"]] + json.dumps(new_str, ensure_ascii=False) + s[n["e"]:]

def insert_after_key(s, parent_path, after_key, key, obj, step=2):
    """insert `"key": obj` as a new member directly after member `after_key` of the object at parent_path."""
    par = node_at(s, parent_path)
    ks = par["kstart"][after_key]; ve = par["kids"][after_key]["e"]
    col = col_of(s, ks)
    ins = ",\n" + " " * col + json.dumps(key) + ": " + dumps_at(obj, col, step)
    return s[:ve] + ins + s[ve:]

def insert_first(s, parent_path, key, obj):
    """insert `"key": obj` as the FIRST member of the object at parent_path (which is non-empty)."""
    par = node_at(s, parent_path)
    first = min(par["kstart"].values())
    col = col_of(s, first)
    ins = json.dumps(key) + ": " + dumps_at(obj, col) + ",\n" + " " * col
    return s[:first] + ins + s[first:]

def delete_key(s, parent_path, key):
    """delete member `key` (and the comma that joins it) from the object at parent_path."""
    par = node_at(s, parent_path)
    keys = sorted(par["kstart"], key=lambda k: par["kstart"][k])
    i = keys.index(key)
    ks, ve = par["kstart"][key], par["kids"][key]["e"]
    if i > 0:                      # take the comma + whitespace BEFORE it (from the previous value's end)
        prev_e = par["kids"][keys[i - 1]]["e"]
        return s[:prev_e] + s[ve:]
    nxt = par["kstart"][keys[i + 1]]
    return s[:ks] + s[nxt:]

def rename_key(s, parent_path, old, new):
    par = node_at(s, parent_path)
    ks = par["kstart"][old]
    m = STR.match(s, ks)
    return s[:ks] + json.dumps(new) + s[m.end():]
