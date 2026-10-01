#!/usr/bin/env python3
"""
extract_spec.py — lift a FIRST DRAFT of the four neutral-spec fields (s311-D4) out of a part's
reference snippet and meta, and write it into the meta with the `$extracted` marker.

RULED: s311-D4 (Dave, #311, 2026-10-01, by click: "In the meta: four new fields") — the neutral
spec lives in the meta as `anatomy`, `states`, `emits`, `bindings`. s311-D9: phase 1 starts now —
fields ADDED, nothing renamed, nothing renders from them yet. Born #312 lane L2 (brief:
notes/_lanes/312/L/BRIEF.md). The schema for the four fields: knowledge/components/meta.schema.json
(#312 L1); the proven-accepted shape is `SPEC_DRAFT` in knowledge/_probe_registry/probe_meta_schema.py.

WHAT IT READS, per part
  • the snippet's body markup (knowledge/snippets/<Name>.reference.html) → `anatomy`: one element
    tree from the part's ROOT element (see "how the root is found"), repeated siblings collapsed
    to the first with a `$repeat` count, demo chrome (captions, section headings) pruned, state
    attributes written as holes (`"aria-selected": "{state.selected}"`), a variant class written
    as a prop hole when the meta's props name it (`"class": "btn {props.type}"`). Every node
    carries `$sel`, the tag.class path from the root, so the coverage check can re-find it.
  • the snippet's <style> state selectors (pseudo-classes, `.is-*`/`.s-*`, `[aria-*]`,
    `[data-state]`/`[data-open]`/`[open]`/`[hidden]`), the state attributes on the markup, the
    meta's `stateModel.states` and its `state`-shaped enum prop, and the inline <script>'s
    listeners (addEventListener) with the state operations their handlers perform (classList
    add/remove/toggle, setAttribute aria-*, .hidden/.disabled/.inert =) → `states`: the state
    names (the corpus's OWN words — `:hover` → hover, `.is-pressed` → pressed, `[aria-expanded]`
    → expanded), the initial, the transitions the CSS and the script imply, and the `keys` map
    (key names read from the script; the action words are the APG defaults for those keys and
    are DECLARED as such in `$keys-source`). `$sources` names the selector/attribute/script line
    each state was read from.
  • the inline <script>'s `dispatchEvent(new CustomEvent(...))` calls → `emits`. A snippet that
    dispatches nothing gets `[]` — the positive declaration the schema asks for — and the
    listener list it DOES attach is kept in `$extracted.$listeners` so the review page can show
    "listens: click, keydown · fires: nothing".
  • the snippet's `#token-manifest` `vars` → `bindings`: `--var` → `{a.b.c}` (today's slash path
    with `/` → `.`); every value is RESOLVED against knowledge/tokens/ through
    gen_snippet_tokens.resolve (dot → slash until s311-D8's DTCG generator lands).

THE COVERAGE RULE (s311-D4 phase-1 gate, brief L2): a meta is at FULL coverage only when all four
fields are present, every anatomy node's `$sel` resolves to an element in the snippet, and every
binding resolves to a token in knowledge/tokens/. Below that the extractor REFUSES to write the
meta (a draft is all-or-nothing per part; nothing partial lands) and names the refusal.
`--report` prints `COUNTS: n of 139 at full coverage` and the refusals by name.

HOW THE ROOT IS FOUND (declared, so the next session does not re-derive it): candidates are body
descendants with a styled class or a role, tag not a heading/paragraph/inline-text tag; the first
candidate whose tag, implicit role or class has a NAME AFFINITY with the meta name wins (exact
token, initials, prefix/suffix/substring ≥ 3, or the consonant skeleton: btn ← button, pg ←
pagination); failing that the first candidate inside the first non-harness container. From there
it climbs while the parent is styled, carries a role or ≥ 2 rules, has no caption/heading child
and is not a gallery (≥ 2 children of the chosen element's own shallow signature). Where the
heuristic cannot see the root, ROOT_HINTS names it and the draft says so in `$extracted.$root`.

WRITES: by TEXTUAL ADDITION ONLY. Most metas are hand-formatted and do not round-trip through
json.dumps, so the five keys are appended before the file's closing brace as an indented block;
the file is then re-parsed and every pre-existing key is proven EQUAL to the original (a changed
field refuses the write). A re-run finds its own block (`\\n  "anatomy":` at top level) and
replaces it, so a second run is byte-identical. A meta whose `$extracted.reviewed` is true is
never overwritten without `--force`. An `aliasOf` meta is refused (s210-D5 fence). The snippet
is NEVER edited.

USAGE
  python3 knowledge/components/extract_spec.py --only button tabs …          # dry run: drafts + coverage to stdout
  python3 knowledge/components/extract_spec.py --only button tabs … --write  # write the drafts into the metas
  python3 knowledge/components/extract_spec.py --only button --json          # print the draft block as JSON
  python3 knowledge/components/extract_spec.py --report                      # n of 139 at full coverage + refusals
  python3 knowledge/components/extract_spec.py --selftest                    # proofs (schema, refusal, idempotence, no field changed)
EXIT: 0 clean · 1 a refusal or a failed proof · 2 bad invocation.
"""
import os as _hg_os, sys as _hg_sys  # noqa: E402 - help gate (#158 write-by-default class)
_hg_d = _hg_os.path.dirname(_hg_os.path.abspath(__file__))
while _hg_d != "/" and not _hg_os.path.exists(_hg_os.path.join(_hg_d, "_helpgate.py")):
    _hg_d = _hg_os.path.dirname(_hg_d)
_hg_sys.path.insert(0, _hg_d)
from _helpgate import help_gate as _help_gate; _help_gate(__doc__, __name__, __file__)

import argparse, datetime, glob, json, os, re, shutil, sys, tempfile
from html.parser import HTMLParser

HERE = os.path.dirname(os.path.abspath(__file__))          # knowledge/components
KNOW = os.path.dirname(HERE)                               # knowledge
ROOT = os.path.dirname(KNOW)
SNIPPETS = os.path.join(KNOW, "snippets")
SCHEMA = os.path.join(HERE, "meta.schema.json")
sys.path.insert(0, KNOW)

BY = "extract_spec.py @ 312-L2"
FIELDS = ("anatomy", "states", "emits", "bindings")
MARK = "$extracted"
EXEMPT = ("EXAMPLE-button.meta.json",)

# Where the name-affinity heuristic cannot see the root, the root is NAMED here, and the draft
# says so in `$extracted.$root` ("hint"). Keep this list short and say why.
ROOT_HINTS = {
    "modals": ("div.overlay", "the meta is the Modals family, the snippet's root class is `overlay` > `dialog`; "
                               "no class or role shares a token with 'modals' (aria-modal is an attribute)"),
}

VOID = {"br", "img", "input", "hr", "meta", "link", "area", "base", "col", "embed", "source",
        "track", "wbr", "path", "circle", "rect", "line", "polyline", "polygon", "use", "stop"}
LEAF_TAGS = {"svg"}                                          # kept as one node, subtree dropped
SKIP_TAGS = {"script", "style", "template", "symbol", "defs"}
NOT_ROOT_TAGS = {"p", "h1", "h2", "h3", "h4", "h5", "h6", "small", "code", "kbd", "strong", "em",
                 "b", "i", "br", "hr", "svg", "label", "span", "a", "li", "ul", "ol", "option"}
FORM_ROOT_TAGS = {"input", "button", "select", "textarea", "table", "nav", "dialog", "details", "fieldset"}
CAPTION_CLASSES = {"cap", "spec-h", "sec", "hint", "demo-h", "demo-controls", "stateLabel", "note"}
CONTAINER_HARNESS = {"gallery", "row", "board", "nwrap", "bar-wrap", "actionbar", "wrap", "page", "bg-content"}
HARNESS_CLASSES = CAPTION_CLASSES | CONTAINER_HARNESS
# `note` is a harness class only on a paragraph (p.note is a demo note; div.note is the Notification)
HARNESS_ONLY_ON = {"note": {"p"}}
STATE_CLASS_RE = re.compile(r"^(is|s)-[a-z0-9-]+$|^(open|active|selected|expanded|show|shown|visible|closed|collapsed)$")
IMPLICIT_ROLE = {"nav": "navigation", "table": "table", "dialog": "dialog", "details": "group",
                 "button": "button", "select": "listbox", "textarea": "textbox", "progress": "progressbar",
                 "fieldset": "group"}
INPUT_ROLE = {"range": "slider", "checkbox": "checkbox", "radio": "radio", "text": "textbox",
              "search": "searchbox", "number": "spinbutton"}
STATE_ATTRS = {"aria-selected": "selected", "aria-expanded": "expanded", "aria-pressed": "pressed",
               "aria-checked": "checked", "aria-invalid": "invalid", "aria-current": "current",
               "aria-busy": "busy", "aria-disabled": "disabled", "disabled": "disabled",
               "checked": "checked", "hidden": "hidden", "open": "open", "data-open": "open",
               "inert": "inert", "aria-hidden": None}       # aria-hidden on a decoration is literal
PSEUDO_STATES = {"hover": "hover", "active": "active", "focus": "focus", "focus-visible": "focus",
                 "focus-within": "focus", "disabled": "disabled", "checked": "checked", "invalid": "invalid",
                 "indeterminate": "indeterminate", "placeholder-shown": "empty", "enabled": None, "valid": None}
APG_KEY_ACTIONS = {"Escape": "close", "Enter": "activate", "Space": "activate", "ArrowRight": "next",
                   "ArrowLeft": "previous", "ArrowDown": "next", "ArrowUp": "previous", "Home": "first",
                   "End": "last", "Tab": "focus-next", "PageUp": "previous-page", "PageDown": "next-page",
                   "Delete": "delete", "Backspace": "delete"}


# ───────────────────────────────── DOM ─────────────────────────────────
class Node:
    __slots__ = ("tag", "attrs", "children", "text", "parent")

    def __init__(self, tag, attrs, parent):
        self.tag, self.attrs, self.children, self.text, self.parent = tag, attrs, [], "", parent

    def classes(self):
        return self.attrs.get("class", "").split()

    def role(self):
        r = self.attrs.get("role")
        if r:
            return r
        if self.tag == "input":
            return INPUT_ROLE.get(self.attrs.get("type", "text"))
        return IMPLICIT_ROLE.get(self.tag)

    def walk(self):
        yield self
        for c in self.children:
            yield from c.walk()


class _Parser(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.root = Node("body", {}, None)
        self.cur = self.root
        self.skip = 0

    def handle_starttag(self, tag, attrs):
        if self.skip:
            if tag not in VOID:
                self.skip += 1
            return
        if tag in SKIP_TAGS:
            self.skip = 1
            return
        d = {}
        for k, v in attrs:
            d[k] = "" if v is None else v
        n = Node(tag, d, self.cur)
        self.cur.children.append(n)
        if tag in LEAF_TAGS:
            self.skip = 1          # keep the node, drop its subtree
            return
        if tag not in VOID:
            self.cur = n

    def handle_startendtag(self, tag, attrs):
        if self.skip:
            return
        if tag in SKIP_TAGS:
            return
        d = {k: ("" if v is None else v) for k, v in attrs}
        self.cur.children.append(Node(tag, d, self.cur))

    def handle_endtag(self, tag):
        if self.skip:
            if tag not in VOID:
                self.skip -= 1
            return
        if tag in VOID:
            return
        n = self.cur
        while n is not None and n.tag != tag:
            n = n.parent
        if n is not None and n.parent is not None:
            self.cur = n.parent

    def handle_data(self, data):
        if self.skip:
            return
        self.cur.text += data


def parse_body(html):
    m = re.search(r"<body[^>]*>(.*)</body>", html, re.S)
    body = m.group(1) if m else html
    p = _Parser()
    p.feed(body)
    p.close()
    return p.root


# ─────────────────────────────── <style> ───────────────────────────────
def style_text(html):
    return "\n".join(re.findall(r"<style[^>]*>(.*?)</style>", html, re.S))


def selectors(css):
    """Every selector list in the sheet (comments stripped, at-rule preludes skipped)."""
    css = re.sub(r"/\*.*?\*/", "", css, flags=re.S)
    out, buf, stack = [], "", []          # stack: True for a @keyframes block, False otherwise
    for ch in css:
        if ch == "{":
            sel = buf.strip()
            buf = ""
            if sel.startswith("@"):
                stack.append(sel.startswith("@keyframes"))
            else:
                stack.append(False)
                if sel and not any(stack):    # inside @media/@container a selector still counts; inside @keyframes it is a stop
                    out.append(sel)
        elif ch == "}":
            buf = ""
            if stack:
                stack.pop()
        elif ch == ";":
            buf = ""
        else:
            buf += ch
    return out


def class_rules(sels):
    """class → number of selector lists mentioning it (harness selectors excluded)."""
    counts = {}
    for sel in sels:
        first = sel.split(",")[0].strip()
        if first.startswith((":root", "body", "html", "*", "[data-theme")):
            continue
        for c in set(re.findall(r"\.([A-Za-z_][\w-]*)", sel)):
            counts[c] = counts.get(c, 0) + 1
    return counts


def style_states(sels):
    """state word → sorted list of the selectors it was read from."""
    found = {}

    def add(word, sel):
        if word:
            found.setdefault(word, set()).add(sel.strip())

    for sel in sels:
        for one in sel.split(","):
            one = one.strip()
            for p in re.findall(r":([a-z-]+)(?![\w(-])", one):
                if p in PSEUDO_STATES:
                    add(PSEUDO_STATES[p], one)
            for c in re.findall(r"\.(is-[a-z0-9-]+|s-[a-z0-9-]+)", one):
                add(c.split("-", 1)[1], one)
            for c in re.findall(r"\.(open|selected|expanded|show|shown|visible|closed|collapsed|current)(?![\w-])", one):
                add(c, one)
            for attr, val in re.findall(r"\[(aria-[a-z]+|data-state|data-open|open|hidden|inert|disabled|checked)"
                                        r"(?:[~|^$*]?=[\"']?([^\"'\]]*)[\"']?)?\]", one):
                if attr == "aria-hidden":
                    continue
                if attr == "data-state":
                    add(val or "state", one)
                elif attr.startswith("aria-"):
                    word = STATE_ATTRS.get(attr, attr[5:])
                    if val in ("false", "mixed"):
                        word = {"false": None, "mixed": "indeterminate"}[val]
                    add(word, one)
                else:
                    add(STATE_ATTRS.get(attr, attr), one)
    return {k: sorted(v) for k, v in found.items()}


# ─────────────────────────────── <script> ───────────────────────────────
def script_text(html):
    return "\n".join(re.findall(r"<script(?![^>]*application/json)[^>]*>(.*?)</script>", html, re.S))


def _balanced(src, i, open_ch="(", close_ch=")"):
    """src[i] == open_ch → index just past the matching close, honouring quotes."""
    depth, q, j = 0, None, i
    while j < len(src):
        ch = src[j]
        if q:
            if ch == "\\":
                j += 1
            elif ch == q:
                q = None
        elif ch in "'\"`":
            q = ch
        elif ch == open_ch:
            depth += 1
        elif ch == close_ch:
            depth -= 1
            if depth == 0:
                return j + 1
        j += 1
    return len(src)


def _named_body(src, name, depth=0):
    """The body of `function name(){…}`, `const name = (…) => {…}` or `const name = () => expr`;
    a body that is one bare call `other(…)` is followed one level (show = () => place())."""
    m = re.search(r"function\s+" + re.escape(name) + r"\s*\(", src) or \
        re.search(r"(?:const|let|var|,)\s*" + re.escape(name) + r"\s*=\s*(?:\([^)]*\)|\w+)\s*=>\s*", src)
    if not m:
        return ""
    rest = src[m.end():]
    if src[m.end() - 1] == "(" or rest.lstrip().startswith("{"):
        k = src.find("{", m.end() - 1)
        body = src[k:_balanced(src, k, "{", "}")] if k >= 0 else ""
    else:
        j, d, q = 0, 0, None
        while j < len(rest):
            ch = rest[j]
            if q:
                if ch == "\\":
                    j += 1
                elif ch == q:
                    q = None
            elif ch in "'\"`":
                q = ch
            elif ch in "([{":
                d += 1
            elif ch in ")]}":
                if d == 0:
                    break
                d -= 1
            elif ch in ",;\n" and d == 0:
                break
            j += 1
        body = rest[:j]
    cm = re.match(r"^\s*([A-Za-z_$][\w$]*)\s*\([^()]*\)\s*;?\s*$", body)
    if cm and depth < 2:
        inner = _named_body(src, cm.group(1), depth + 1)
        if inner:
            return inner
    return body


def listeners(js):
    """[(event, handler_text)] for every addEventListener in the script."""
    out = []
    for m in re.finditer(r"addEventListener\s*\(", js):
        end = _balanced(js, m.end() - 1)
        args = js[m.end():end - 1]
        em = re.match(r"\s*['\"]([\w-]+)['\"]\s*,\s*(.*)$", args, re.S)
        if not em:
            continue
        ev, handler = em.group(1), em.group(2).strip()
        nm = re.match(r"^([A-Za-z_$][\w$]*)\s*(?:,\s*\{[^}]*\})?\s*$", handler)
        if nm:
            handler = _named_body(js, nm.group(1)) or handler
        out.append((ev, handler))
    return out


def state_ops(handler):
    """(to_state, kind) pairs a handler performs; kind = 'enter' | 'leave'."""
    ops = []
    for op, cls in re.findall(r"classList\.(add|remove|toggle)\(\s*['\"]([\w-]+)['\"]", handler):
        word = cls.split("-", 1)[1] if STATE_CLASS_RE.match(cls) and "-" in cls else cls
        ops.append((word, "leave" if op == "remove" else "enter"))
    for attr, val in re.findall(r"setAttribute\(\s*['\"](aria-[a-z]+)['\"]\s*,\s*([^)]*)\)", handler):
        word = STATE_ATTRS.get(attr, attr[5:])
        if not word:
            continue
        v = val.strip()
        if re.match(r"^['\"]?true['\"]?$", v) or "!" in v or "on" in v or "===" in v or "!==" in v:
            ops.append((word, "enter"))
        if re.match(r"^['\"]?false['\"]?$", v) or "!" in v or "on" in v:
            ops.append((word, "leave"))
        if not ops or ops[-1][0] != word:
            ops.append((word, "enter"))
    for attr in re.findall(r"removeAttribute\(\s*['\"](aria-[a-z]+)['\"]", handler):
        word = STATE_ATTRS.get(attr, attr[5:])
        if word:
            ops.append((word, "leave"))
    for prop, val in re.findall(r"\.(hidden|disabled|inert|indeterminate)\s*=\s*([^;]+)", handler):
        v = val.strip()
        if v.startswith("false"):
            ops.append((prop, "leave"))
        else:
            ops.append((prop, "enter"))
            if "!" in v or "?" in v or "<" in v or ">" in v:
                ops.append((prop, "leave"))
    seen, uniq = set(), []
    for o in ops:
        if o not in seen:
            seen.add(o)
            uniq.append(o)
    return uniq


def script_keys(js):
    keys = set()
    for k in re.findall(r"\.key\s*[!=]==?\s*['\"]([^'\"]+)['\"]", js):
        keys.add(k)
    for k in re.findall(r"case\s*['\"]([^'\"]+)['\"]\s*:", js):
        keys.add(k)
    for lst in re.findall(r"\[((?:\s*['\"][A-Za-z ]+['\"]\s*,?)+)\]\s*\.includes\(\s*\w+\.key", js):
        for k in re.findall(r"['\"]([^'\"]+)['\"]", lst):
            keys.add(k)
    for k in re.findall(r"\.key\s*\)\s*\)?\s*\{?", js):
        pass
    out = {}
    for k in sorted(keys):
        name = "Space" if k in (" ", "Spacebar") else k
        if name in APG_KEY_ACTIONS:
            out[name] = APG_KEY_ACTIONS[name]
    return out


def script_emits(js):
    out = []
    for m in re.finditer(r"new\s+CustomEvent\s*\(", js):
        end = _balanced(js, m.end() - 1)
        args = js[m.end():end - 1]
        nm = re.match(r"\s*['\"]([\w:-]+)['\"]", args)
        if not nm:
            continue
        name = nm.group(1).lower()
        detail = {}
        dm = re.search(r"detail\s*:\s*\{", args)
        if dm:
            k = dm.end() - 1
            body = args[k + 1:_balanced(args, k, "{", "}") - 1]
            for key, val in re.findall(r"([A-Za-z_$][\w$]*)\s*:\s*([^,}]+)", body):
                v = val.strip()
                t = "string" if re.match(r"^['\"`]", v) else "number" if re.match(r"^-?\d", v) else \
                    "boolean" if v in ("true", "false") else "array" if v.startswith("[") else \
                    "object" if v.startswith("{") else "unknown"
                detail[key] = t
            for key in re.findall(r"(?:^|,)\s*([A-Za-z_$][\w$]*)\s*(?=,|$)", body):
                detail.setdefault(key, "unknown")
        if re.match(r"^[a-z][a-z0-9-]*$", name):
            out.append({"name": name, "detail": detail})
    return out


# ───────────────────────────── the root ─────────────────────────────
def _tokens(name):
    return [t for t in re.split(r"[^a-z0-9]+", name.lower()) if t]


def _skeleton(word):
    s = re.sub(r"[aeiou]", "", word)
    return re.sub(r"(.)\1+", r"\1", s)


def affinity(node, name_tokens):
    """0 none · 3 exact token · 2 initials / prefix / suffix / substring(≥3) · 1 consonant skeleton."""
    best = 0
    words = node.classes() + [node.tag]
    r = node.role()
    if r:
        words.append(r)
    initials = "".join(t[0] for t in name_tokens)
    joined = "".join(name_tokens)
    for w in words:
        w = w.lower()
        if STATE_CLASS_RE.match(w) or w in HARNESS_CLASSES:
            continue
        wt = [t for t in re.split(r"[^a-z0-9]+", w) if t]
        for t in wt:
            if t in name_tokens:
                best = max(best, 3)
            elif len(name_tokens) > 1 and t == initials:
                best = max(best, 2)
            elif len(t) >= 3 and any(t in nt for nt in name_tokens):
                best = max(best, 2)
            elif len(t) >= 2 and any(_skeleton(nt).startswith(t) or _skeleton(nt) == t for nt in name_tokens):
                best = max(best, 1)
        if len(wt) > 1 and all(any((t in nt) or _skeleton(nt).startswith(t) for nt in name_tokens) for t in wt):
            best = max(best, 2)
    if r and r in joined:
        best = max(best, 2)
    return best


def is_harness_class(c, tag):
    if c not in HARNESS_CLASSES:
        return False
    only = HARNESS_ONLY_ON.get(c)
    return True if only is None else tag in only


def is_caption(n):
    """Demo chrome that is never part of the tree: an id-less heading, a p/span/div captioned by class."""
    if n.tag in ("h1", "h2", "h3", "h4", "h5", "h6") and not n.attrs.get("id"):
        return True
    return any(c in CAPTION_CLASSES and is_harness_class(c, n.tag) for c in n.classes()) \
        and n.tag in ("p", "span", "small", "div", "h2")


def component_kids(n):
    """Element children that could be component roots, seen through unstyled wrappers."""
    out = []
    for c in n.children:
        if c.tag in SKIP_TAGS or c.tag == "svg" or is_caption(c):
            continue
        if not c.classes() and not c.attrs.get("role") and c.tag in ("div", "section", "main"):
            out.extend(component_kids(c))
        else:
            out.append(c)
    return out


def shallow_sig(n):
    return (n.tag, tuple(sorted(c for c in n.classes() if not STATE_CLASS_RE.match(c))), n.attrs.get("role"))


def find_root(body, name, rules, meta_id):
    name_tokens = _tokens(name)
    if meta_id in ROOT_HINTS:
        sel, why = ROOT_HINTS[meta_id]
        for n in body.walk():
            if _matches(n, sel):
                return n, "hint: " + why
        return None, "hint selector %r matched nothing" % sel

    def candidate(n):
        if n is body or n.tag in NOT_ROOT_TAGS and not n.attrs.get("role"):
            return False
        if is_caption(n):
            return False
        styled = any(c in rules and not is_harness_class(c, n.tag) for c in n.classes())
        return styled or bool(n.attrs.get("role")) or n.tag in FORM_ROOT_TAGS

    cands = [n for n in body.walk() if candidate(n)]
    pick, how = None, ""
    for level in (3, 2, 1):
        for n in cands:
            if affinity(n, name_tokens) >= level:
                pick, how = n, "name affinity %d (%s.%s)" % (level, n.tag, ".".join(n.classes()) or n.role() or "")
                break
        if pick:
            break
    if pick is None:
        def descend(container):
            for k in component_kids(container):
                harness = any(is_harness_class(c, k.tag) for c in k.classes()) or \
                    any(is_caption(x) for x in k.children) or not candidate(k)
                if harness:
                    r = descend(k)
                    if r:
                        return r
                else:
                    return k
            return None
        pick = descend(body)
        how = "first non-harness candidate"
    if pick is None:
        return None, "no candidate element (no styled class, no role, no form tag)"
    # the richest instance of the same shallow signature (a gallery shows the part in several states;
    # the fullest one carries every part)
    sig = shallow_sig(pick)
    twins = [n for n in body.walk() if shallow_sig(n) == sig]
    richest = max(twins, key=lambda n: sum(1 for _ in n.walk()))
    if richest is not pick and sum(1 for _ in richest.walk()) > sum(1 for _ in pick.walk()):
        pick = richest
        how += " → richest of %d instances" % len(twins)
    # climb
    n = pick
    while n.parent is not None and n.parent is not body:
        p = n.parent
        pr = sum(rules.get(c, 0) for c in p.classes() if not is_harness_class(c, p.tag))
        if any(is_harness_class(c, p.tag) for c in p.classes()):
            break
        if any(is_caption(x) for x in p.children):
            break
        if not (p.attrs.get("role") or pr >= 2 or (pr >= 1 and len(component_kids(p)) >= 2)):
            break
        same = [k for k in component_kids(p) if shallow_sig(k) == shallow_sig(n)]
        if len(same) >= 2 and not p.attrs.get("role"):
            break
        n = p
        how += " → climbed to %s.%s" % (p.tag, ".".join(p.classes()) or p.role() or "")
    return n, how


def _matches(n, sel):
    """`tag.a.b[role=x]` — one compound selector against one node."""
    m = re.match(r"^([a-z0-9-]*)((?:\.[\w-]+)*)(?:\[role=([\w-]+)\])?$", sel)
    if not m:
        return False
    tag, cls, role = m.group(1), [c for c in m.group(2).split(".") if c], m.group(3)
    if tag and n.tag != tag:
        return False
    if any(c not in n.classes() for c in cls):
        return False
    if role and n.attrs.get("role") != role:
        return False
    return True


def resolve_sel(body, path):
    """`body > div.tabs > div.tablist > button.tab` → the first node on that path, or None."""
    steps = [s.strip() for s in path.split(">")]
    cur = [body]
    for s in steps[1:]:
        nxt = []
        for c in cur:
            for k in c.children:
                if _matches(k, s):
                    nxt.append(k)
        if not nxt:
            return None
        cur = nxt
    return cur[0]


# ─────────────────────────── the anatomy tree ───────────────────────────
def deep_sig(n):
    return shallow_sig(n) + (tuple(deep_sig(c) for c in n.children if c.tag not in SKIP_TAGS),)


def _sel_step(n):
    cls = [c for c in n.classes() if not STATE_CLASS_RE.match(c)]
    return n.tag + "".join("." + c for c in cls)


def build_tree(root, meta, rules, states_seen, used_parts):
    variants = {}
    for p in meta.get("props", []) or []:
        if isinstance(p, dict) and p.get("type") == "enum" and isinstance(p.get("values"), list):
            for v in p["values"]:
                if isinstance(v, str) and re.match(r"^[a-z][a-z0-9-]*$", v):
                    variants.setdefault(v, p["name"])
    slot_keys = list((meta.get("slots") or {}).keys()) if isinstance(meta.get("slots"), dict) else []

    def part_name(n):
        base = None
        for c in n.classes():
            if STATE_CLASS_RE.match(c) or c in variants or c.startswith("t-"):
                continue
            base = c
            break
        if base is None:
            base = n.attrs.get("role") or (n.tag if n.tag != "svg" else "icon")
        base = re.sub(r"[^a-z0-9-]+", "-", base.lower()).strip("-") or n.tag
        if not re.match(r"^[a-z]", base):
            base = n.tag + "-" + base
        name, i = base, 2
        while name in used_parts:
            name = "%s-%d" % (base, i)
            i += 1
        used_parts.add(name)
        return name

    def node(n, path, twins=()):
        out = {"part": part_name(n), "tag": n.tag}
        attrs, aria, state_classes = {}, {}, []
        for k, v in n.attrs.items():
            if k == "style":
                continue
            if k == "class":
                keep = []
                for c in n.classes():
                    if STATE_CLASS_RE.match(c):
                        state_classes.append(c)
                        w = c.split("-", 1)[1] if "-" in c else c
                        states_seen.setdefault(w, set()).add("class ." + c + " on " + path)
                    elif c in variants:
                        hole = "{props.%s}" % variants[c]
                        if hole not in keep:
                            keep.append(hole)
                    else:
                        keep.append(c)
                if keep:
                    attrs["class"] = " ".join(keep)
                continue
            if k == "role" or k.startswith("aria-"):
                if k in STATE_ATTRS and STATE_ATTRS[k]:
                    aria[k] = "{state.%s}" % STATE_ATTRS[k]
                    states_seen.setdefault(STATE_ATTRS[k], set()).add("attribute %s on %s" % (k, path))
                else:
                    aria[k] = v
                continue
            if k in STATE_ATTRS and STATE_ATTRS[k]:
                attrs[k] = "{state.%s}" % STATE_ATTRS[k]
                states_seen.setdefault(STATE_ATTRS[k], set()).add("attribute %s on %s" % (k, path))
                continue
            if k == "data-state":
                attrs[k] = "{state.current}"
                continue
            attrs[k] = v
        # the collapsed twins (the same part in another state) lend their state attributes and classes
        for t in twins:
            for k in t.attrs:
                if k in STATE_ATTRS and STATE_ATTRS[k] and k not in attrs and k not in aria:
                    (aria if k.startswith("aria-") else attrs)[k] = "{state.%s}" % STATE_ATTRS[k]
                    states_seen.setdefault(STATE_ATTRS[k], set()).add("attribute %s on a twin of %s" % (k, path))
            for c in t.classes():
                if STATE_CLASS_RE.match(c) and c not in state_classes:
                    state_classes.append(c)
                    w = c.split("-", 1)[1] if "-" in c else c
                    states_seen.setdefault(w, set()).add("class ." + c + " on a twin of " + path)
        if attrs:
            out["attrs"] = attrs
        if aria:
            out["aria"] = aria
        for s in slot_keys:
            if s == out["part"] or out["part"].endswith("-" + s) or s in n.classes():
                out["slot"] = s
                break
        text = re.sub(r"\s+", " ", n.text).strip()
        if text:
            out["text"] = text if len(text) <= 80 else text[:77] + "…"
        if state_classes:
            out["$stateClasses"] = state_classes
        out["$sel"] = path
        kids, groups, order_ = [], {}, []
        for c in n.children:
            if c.tag in SKIP_TAGS or is_caption(c):
                continue
            sig = deep_sig(c)
            if sig not in groups:
                groups[sig] = []
                order_.append(sig)
            groups[sig].append(c)
        for sig in order_:
            g = groups[sig]
            # twins of this child: its later same-signature siblings, and the matching children of n's twins
            # (deep_sig equality means the twins carry the same children in the same shape)
            ctwins = g[1:] + [c for t in twins for c in t.children if c.tag not in SKIP_TAGS and deep_sig(c) == sig]
            child = node(g[0], path + " > " + _sel_step(g[0]), ctwins)
            if len(g) > 1:
                child["$repeat"] = len(g)
            kids.append(child)
        if kids:
            out["children"] = kids
        return out

    chain, n = [], root
    while n is not None and n.tag != "body":
        chain.append(_sel_step(n))
        n = n.parent
    sig = shallow_sig(root)
    twins = [t for t in root_body(root).walk() if t is not root and shallow_sig(t) == sig]
    return node(root, " > ".join(["body"] + chain[::-1]), twins)


def root_body(n):
    while n.parent is not None:
        n = n.parent
    return n


# ─────────────────────────────── states ───────────────────────────────
def build_states(meta, css_states, markup_states, js_listeners, js, root_open=False):
    sources = {}
    for w, sels in css_states.items():
        if w:
            sources.setdefault(w, []).extend("style " + s for s in sels)
    for w, where in markup_states.items():
        sources.setdefault(w, []).extend(sorted(where))
    for ev, handler in js_listeners:
        for word, kind in state_ops(handler):
            if kind == "enter":
                sources.setdefault(word, []).append("script %s handler" % ev)
    model = meta.get("stateModel")
    model_states = model.get("states") if isinstance(model, dict) and isinstance(model.get("states"), list) else []
    prop_default, prop_states = None, []
    open_prop = False
    for p in meta.get("props", []) or []:
        if not isinstance(p, dict):
            continue
        if p.get("type") == "enum" and p.get("name") == "state":
            prop_states = [v for v in p.get("values", []) if isinstance(v, str)]
            prop_default = p.get("default")
        if p.get("name") == "open" and p.get("type") == "boolean":
            open_prop = True
    if "active" in sources and "pressed" in sources:        # :active and .is-pressed name one state
        sources["pressed"] = sources["pressed"] + sources.pop("active")
    if model_states:
        initial, initial_why = model_states[0], "meta.stateModel.states, in its order; initial = its first"
    elif prop_default:
        initial, initial_why = prop_default, "meta prop `state` enum; initial = its default"
    elif open_prop or root_open:
        initial, initial_why = "closed", ("meta has a boolean prop `open`" if open_prop else
                                          "the root element itself carries an open/expanded state, so the rest state is closed")
    else:
        initial, initial_why = "default", "no stateModel, no `state` prop, no open state: rest state named default"
    order = [initial]
    for w in model_states + prop_states:
        if w not in order:
            order.append(w)
    for w in ("hover", "focus", "active", "pressed", "selected", "checked", "indeterminate", "expanded",
              "open", "current", "disabled", "invalid", "error", "busy", "hidden"):
        if w in sources and w not in order:
            order.append(w)
    for w in sorted(sources):
        if w not in order:
            order.append(w)
    transitions = []

    def arrow(f, on, t, guard=None):
        a = {"from": f, "on": on, "to": t}
        if guard:
            a["guard"] = guard
        if a not in transitions:
            transitions.append(a)

    rest = initial
    if "hover" in order:
        arrow(rest, "pointerenter", "hover")
        arrow("hover", "pointerleave", rest)
    pressed = "pressed" if "pressed" in order else "active" if "active" in order else None
    if pressed:
        arrow("hover" if "hover" in order else rest, "pointerdown", pressed)
        arrow(pressed, "pointerup", "hover" if "hover" in order else rest)
    if "focus" in order:
        arrow("*", "focus", "focus")
        arrow("focus", "blur", rest)
    if "disabled" in order:
        arrow("*", "props.disabled", "disabled", "{props.disabled}")
    for ev, handler in js_listeners:
        for word, kind in state_ops(handler):
            if word in order:
                if kind == "enter":
                    arrow("*", ev, word)
                else:
                    arrow(word, ev, rest)
    keys = script_keys(js)
    out = {"states": order, "initial": initial}
    if transitions:
        out["transitions"] = transitions
    if keys:
        out["keys"] = keys
        out["$keys-source"] = ("key names read from the snippet's script; action words are the APG defaults "
                               "for those keys, not read from the snippet")
    out["$sources"] = {w: sorted(set(s))[:6] for w, s in sources.items() if w in order}
    out["$sources"]["$initial"] = initial_why
    return out


# ─────────────────────────────── bindings ───────────────────────────────
MANIFEST_RE = re.compile(r'<script[^>]*id="token-manifest"[^>]*>(.*?)</script>', re.S)


def manifest(html):
    m = MANIFEST_RE.search(html)
    if not m:
        return None
    try:
        return json.loads(m.group(1))
    except json.JSONDecodeError:
        return None


def resolve_token(path):
    """True when the slash path resolves in knowledge/tokens/ (light, dark or modeless)."""
    try:
        import gen_snippet_tokens as gst
    except Exception as e:                                   # pragma: no cover
        raise SystemExit("⛔ cannot import knowledge/gen_snippet_tokens.py — %s" % e)
    for mode in ("light", "dark"):
        try:
            gst.resolve(path, mode)
            return True
        except (KeyError, TypeError):
            continue
    return False


def build_bindings(mani):
    out, unresolved = {}, []
    for var, path in (mani or {}).get("vars", {}).items():
        if not isinstance(path, str) or not re.match(r"^--[A-Za-z0-9_-]+$", var):
            unresolved.append("%s: not a var→path pair" % var)
            continue
        ref = "{%s}" % path.replace("/", ".")
        if not re.match(r"^\{[^{}\s]+\}$", ref):
            unresolved.append("%s: %r is not a path" % (var, path))
            continue
        out[var] = ref
        if not resolve_token(path):
            unresolved.append("%s: %s does not resolve in knowledge/tokens/" % (var, path))
    return out, unresolved


# ─────────────────────────────── the draft ───────────────────────────────
def snippet_for(meta, meta_id):
    want = {re.sub(r"[^a-z0-9]+", "-", meta.get("name", "").lower()).strip("-"), meta_id.lower()}
    for f in sorted(os.listdir(SNIPPETS)):
        if not f.endswith(".reference.html"):
            continue
        stem = re.sub(r"[^a-z0-9]+", "-", f[:-len(".reference.html")].lower()).strip("-")
        if stem in want:
            return os.path.join(SNIPPETS, f)
    return None


def draft(meta_path, date=None, sha=None):
    """→ (block or None, coverage dict). block = the five keys; coverage names what was found/refused."""
    meta_id = os.path.basename(meta_path)[:-len(".meta.json")]
    meta = json.load(open(meta_path, encoding="utf-8"))
    cov = {"id": meta_id, "refusals": [], "found": {}}
    if meta.get("aliasOf"):
        cov["refusals"].append("aliasOf meta — the s210-D5 fence bans the four fields")
        return None, cov
    snip = snippet_for(meta, meta_id)
    if not snip:
        cov["refusals"].append("no snippet found for name %r" % meta.get("name"))
        return None, cov
    html = open(snip, encoding="utf-8").read()
    body = parse_body(html)
    css = style_text(html)
    sels = selectors(css)
    rules = class_rules(sels)
    root, how = find_root(body, meta.get("name", meta_id), rules, meta_id)
    if root is None:
        cov["refusals"].append("anatomy: root not found — " + how)
        return None, cov
    states_seen, used = {}, set()
    anatomy = build_tree(root, meta, rules, states_seen, used)
    js = script_text(html)
    ls = listeners(js)
    root_cls = [c for c in root.classes() if not STATE_CLASS_RE.match(c)][:1]
    root_open = any(v in ("{state.open}", "{state.expanded}") for d in (anatomy.get("attrs", {}), anatomy.get("aria", {}))
                    for v in d.values()) or \
        bool(root_cls and any(re.search(r"\." + re.escape(root_cls[0]) + r"(?:\.[\w-]+|\[[^\]]*\])*(?:\.open|\.is-open|\.show|\[open\]|\[data-open)", one)
                              for sel in sels for one in sel.split(",")))
    states = build_states(meta, style_states(sels), states_seen, ls, js, root_open)
    emits = script_emits(js)
    bindings, unresolved = build_bindings(manifest(html))
    # coverage: every $sel resolves; every binding resolves; four fields present
    nodes = list(_walk_tree(anatomy))
    bad_sel = [n["part"] for n in nodes if resolve_sel(body, n["$sel"]) is None]
    if bad_sel:
        cov["refusals"].append("anatomy: %d part(s) do not resolve to an element: %s" % (len(bad_sel), ", ".join(bad_sel)))
    if not bindings and manifest(html) is None:
        cov["refusals"].append("bindings: no #token-manifest in the snippet")
    for u in unresolved:
        cov["refusals"].append("bindings: " + u)
    marker = {"by": BY, "date": date or datetime.date.today().isoformat(), "reviewed": False,
              "source": os.path.relpath(snip, ROOT), "fields": list(FIELDS),
              "$root": how,
              "$listeners": sorted(set(ev for ev, _ in ls)),
              "$emits-note": ("the snippet dispatches no CustomEvent, so `emits` is the positive empty list; "
                              "what the part should fire is Dave's call on the review page") if not emits else
                             "read from the snippet's dispatchEvent(new CustomEvent(…)) calls"}
    if sha:
        marker["sha"] = sha
    existing = meta.get(MARK)
    if isinstance(existing, dict) and existing.get("by") == BY and existing.get("date"):
        marker["date"] = existing["date"]                   # idempotent across days
        if not sha and existing.get("sha"):
            marker["sha"] = existing["sha"]
    block = {"anatomy": anatomy, "states": states, "emits": emits, "bindings": bindings, MARK: marker}
    cov["found"] = {"root": anatomy["$sel"], "nodes": len(nodes),
                    "repeats-collapsed": sum(n.get("$repeat", 1) - 1 for n in nodes),
                    "states": len(states["states"]), "transitions": len(states.get("transitions", [])),
                    "keys": len(states.get("keys", {})), "listeners": len(set(ev for ev, _ in ls)),
                    "emits": len(emits), "bindings": len(bindings), "bindings-unresolved": len(unresolved),
                    "script-bytes": len(js.strip())}
    return block, cov


def _walk_tree(n):
    yield n
    for c in n.get("children", []):
        yield from _walk_tree(c)


# ─────────────────────────────── the write ───────────────────────────────
def split_block(raw):
    """(head, tail) — head is the text before an earlier draft block (or before the closing brace),
    tail is the closing `\\n}\\n`. Refuses when any of the five keys exists outside that shape."""
    doc = json.loads(raw)
    stripped = raw.rstrip()
    if not stripped.endswith("}"):
        raise ValueError("meta does not end with a closing brace")
    tail = raw[len(stripped) - 1:]
    head = stripped[:-1]
    present = [k for k in FIELDS + (MARK,) if k in doc]
    if present:
        i = head.find('\n  "anatomy":')
        if i < 0:
            raise ValueError("meta carries %s but not in the extractor's block shape — hand-edited; refusing" % present)
        head2 = head[:i].rstrip()
        if head2.endswith(","):
            head2 = head2[:-1]
        try:
            d2 = json.loads(head2 + "\n}\n")
        except json.JSONDecodeError as e:
            raise ValueError("cannot isolate the earlier draft block — %s" % e)
        if any(k in d2 for k in FIELDS + (MARK,)):
            raise ValueError("a spec field sits outside the extractor's block — hand-edited; refusing")
        head = head2
    return head.rstrip(), tail


def render_block(block):
    lines = []
    for k in FIELDS + (MARK,):
        body = json.dumps(block[k], indent=2, ensure_ascii=False)
        body = "\n".join(("  " + ln if ln else ln) for ln in body.split("\n"))
        lines.append('  "%s": %s' % (k, body.lstrip()))
    return ",\n".join(lines)


def write_meta(meta_path, block):
    raw = open(meta_path, encoding="utf-8").read()
    before = json.loads(raw)
    head, tail = split_block(raw)
    sep = "," if not head.rstrip().endswith(("{", ",")) else ""
    new = head + sep + "\n" + render_block(block) + "\n}" + ("\n" if tail.endswith("\n") else "")
    after = json.loads(new)
    for k, v in before.items():
        if k in FIELDS or k == MARK:
            continue
        if after.get(k) != v:
            raise ValueError("pre-existing field %r would change — refusing" % k)
    for k in FIELDS + (MARK,):
        if after[k] != block[k]:
            raise ValueError("written %r does not read back equal" % k)
    if new != raw:
        with open(meta_path, "w", encoding="utf-8") as f:
            f.write(new)
        return True
    return False


# ─────────────────────────────── report ───────────────────────────────
def coverage_of_meta(meta_path):
    """Re-check a meta ON DISK: full | partial(reasons) | undrafted | fenced."""
    meta = json.load(open(meta_path, encoding="utf-8"))
    meta_id = os.path.basename(meta_path)[:-len(".meta.json")]
    if meta.get("aliasOf"):
        return "fenced", []
    present = [k for k in FIELDS if k in meta]
    if not present:
        return "undrafted", []
    reasons = [k + " missing" for k in FIELDS if k not in meta]
    if MARK not in meta:
        reasons.append("$extracted missing")
    snip = snippet_for(meta, meta_id)
    if not snip:
        reasons.append("no snippet")
    else:
        body = parse_body(open(snip, encoding="utf-8").read())
        if isinstance(meta.get("anatomy"), dict):
            bad = [n.get("part") for n in _walk_tree(meta["anatomy"]) if not n.get("$sel") or resolve_sel(body, n["$sel"]) is None]
            if bad:
                reasons.append("%d part(s) unresolved: %s" % (len(bad), ", ".join(map(str, bad[:6]))))
    for var, ref in (meta.get("bindings") or {}).items():
        if var.startswith("$"):
            continue
        path = ref.strip("{}").replace(".", "/")
        if not resolve_token(path):
            reasons.append("%s → %s unresolved" % (var, path))
    return ("full" if not reasons else "partial"), reasons


def report(components_dir=HERE, quiet=False):
    paths = sorted(glob.glob(os.path.join(components_dir, "*.meta.json")))
    tally = {"full": [], "partial": [], "undrafted": [], "fenced": [], "exempt": []}
    for p in paths:
        if os.path.basename(p) in EXEMPT:
            tally["exempt"].append((os.path.basename(p)[:-len(".meta.json")], ["declared exempt (the template example)"]))
            continue
        kind, reasons = coverage_of_meta(p)
        tally[kind].append((os.path.basename(p)[:-len(".meta.json")], reasons))
    n = len(paths)
    if not quiet:
        for mid, reasons in tally["partial"]:
            print("  ⛔ %s — %s" % (mid, "; ".join(reasons)))
        print("full coverage: " + (", ".join(m for m, _ in tally["full"]) or "none"))
        print("fenced (aliasOf): " + (", ".join(m for m, _ in tally["fenced"]) or "none"))
        print("undrafted: %d" % len(tally["undrafted"]))
    print("COUNTS: %d of %d at full coverage · %d refused by name · %d undrafted · %d fenced (aliasOf) · %d exempt (%s)"
          % (len(tally["full"]), n, len(tally["partial"]), len(tally["undrafted"]), len(tally["fenced"]),
             len(tally["exempt"]), ", ".join(m for m, _ in tally["exempt"]) or "-"))
    return tally


# ─────────────────────────────── selftest ───────────────────────────────
def selftest():
    import jsonschema
    schema = json.load(open(SCHEMA, encoding="utf-8"))
    validator = jsonschema.Draft7Validator(schema)
    tmp = tempfile.mkdtemp(prefix="extract_spec_")
    ok = True

    def check(label, cond):
        nonlocal ok
        print(("  ✅ " if cond else "  ⛔ ") + label)
        ok = ok and cond

    try:
        for mid in ("button", "tabs"):
            src = os.path.join(HERE, mid + ".meta.json")
            dst = os.path.join(tmp, mid + ".meta.json")
            shutil.copy(src, dst)
            raw0 = open(dst, encoding="utf-8").read()
            block, cov = draft(src, date="2026-10-01")
            check("%s: drafted at full coverage (%s)" % (mid, cov["refusals"] or "no refusals"), block is not None and not cov["refusals"])
            write_meta(dst, block)
            raw1 = open(dst, encoding="utf-8").read()
            errs = list(validator.iter_errors(json.loads(raw1)))
            check("%s: written meta validates against meta.schema.json (%d findings)" % (mid, len(errs)), not errs)
            before, after = json.loads(raw0), json.loads(raw1)
            check("%s: every pre-existing field reads back equal" % mid, all(after.get(k) == v for k, v in before.items()))
            check("%s: the original text is a prefix-preserved head of the new file" % mid,
                  raw1.startswith(raw0.rstrip()[:-1].rstrip()))
            write_meta(dst, block)
            raw2 = open(dst, encoding="utf-8").read()
            check("%s: second write is byte-identical" % mid, raw1 == raw2)
            kind, reasons = coverage_of_meta(dst)
            check("%s: on-disk coverage reads full (%s)" % (mid, reasons or "-"), kind == "full")
            # plant: a binding that does not resolve → the coverage reader goes red
            d = json.loads(raw1)
            d["bindings"]["--planted"] = "{no.such.token}"
            open(dst, "w", encoding="utf-8").write(json.dumps(d, indent=2, ensure_ascii=False) + "\n")
            kind, reasons = coverage_of_meta(dst)
            check("%s: planted unresolvable binding is REFUSED by name (%s)" % (mid, reasons[:1]), kind == "partial" and any("--planted" in r for r in reasons))
            # plant: a part whose $sel resolves to nothing
            d = json.loads(raw1)
            d["anatomy"]["$sel"] = "body > div.no-such-root"
            open(dst, "w", encoding="utf-8").write(json.dumps(d, indent=2, ensure_ascii=False) + "\n")
            kind, reasons = coverage_of_meta(dst)
            check("%s: planted unresolvable part is REFUSED by name" % mid, kind == "partial" and any("unresolved" in r for r in reasons))
            # the alias fence
        alias = next((p for p in glob.glob(os.path.join(HERE, "*.meta.json")) if json.load(open(p)).get("aliasOf")), None)
        if alias:
            block, cov = draft(alias)
            check("alias meta %s refused (%s)" % (os.path.basename(alias), cov["refusals"][:1]), block is None)
        # a hand-edited meta (a spec key outside the block) refuses the write
        src = os.path.join(HERE, "button.meta.json")
        dst = os.path.join(tmp, "hand.meta.json")
        raw = open(src, encoding="utf-8").read()
        d = json.loads(raw)
        d2 = {"emits": []}
        d2.update(d)
        open(dst, "w", encoding="utf-8").write(json.dumps(d2, indent=2, ensure_ascii=False) + "\n")
        block, _ = draft(src, date="2026-10-01")
        try:
            write_meta(dst, block)
            check("hand-placed spec key refuses the write", False)
        except ValueError as e:
            check("hand-placed spec key refuses the write (%s)" % str(e)[:60], True)
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
    print(("✅ extract_spec selftest PASS" if ok else "⛔ extract_spec selftest FAIL"))
    return 0 if ok else 1


# ─────────────────────────────── main ───────────────────────────────
def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[1], add_help=True)
    ap.add_argument("--only", nargs="+", metavar="ID", help="meta ids to draft (cohort one list)")
    ap.add_argument("--write", action="store_true", help="write the drafts (default: dry run)")
    ap.add_argument("--force", action="store_true", help="overwrite a meta whose $extracted.reviewed is true")
    ap.add_argument("--json", action="store_true", help="print each draft block as JSON")
    ap.add_argument("--date", default=None, help="date for $extracted (default today; an earlier draft's date is kept)")
    ap.add_argument("--sha", default=None, help="the committed sha the snippet was read at, stamped into $extracted.sha")
    ap.add_argument("--report", action="store_true", help="coverage count over every meta on disk")
    ap.add_argument("--selftest", action="store_true")
    ap.add_argument("--quiet", action="store_true")
    a = ap.parse_args(argv)
    if a.selftest:
        return selftest()
    if a.report:
        report(quiet=a.quiet)
        return 0
    if not a.only:
        ap.print_usage()
        print("extract_spec: name the metas with --only, or ask for --report / --selftest", file=sys.stderr)
        return 2
    rc, full = 0, []
    for mid in a.only:
        path = os.path.join(HERE, mid + ".meta.json")
        if not os.path.exists(path):
            print("⛔ %s: no such meta" % mid)
            rc = 1
            continue
        block, cov = draft(path, date=a.date, sha=a.sha)
        f = cov["found"]
        if cov["refusals"]:
            print("⛔ %s REFUSED — %s" % (mid, " · ".join(cov["refusals"])))
            rc = 1
        else:
            full.append(mid)
            print("✅ %s — root %s · nodes %d (%d repeats collapsed) · states %d · transitions %d · keys %d · "
                  "listeners %d · emits %d · bindings %d resolved"
                  % (mid, f["root"], f["nodes"], f["repeats-collapsed"], f["states"], f["transitions"],
                     f["keys"], f["listeners"], f["emits"], f["bindings"]))
        if a.json and block:
            print(json.dumps(block, indent=2, ensure_ascii=False))
        if a.write and block and not cov["refusals"]:
            meta = json.load(open(path, encoding="utf-8"))
            ex = meta.get(MARK)
            if isinstance(ex, dict) and ex.get("reviewed") is True and not a.force:
                print("   ⛔ %s: $extracted.reviewed is true — not overwritten without --force" % mid)
                rc = 1
                continue
            try:
                changed = write_meta(path, block)
                print("   wrote %s" % os.path.relpath(path, ROOT) if changed else "   unchanged (byte-identical)")
            except ValueError as e:
                print("   ⛔ %s: %s" % (mid, e))
                rc = 1
    print("COUNTS: %d of %d named at full coverage%s" % (len(full), len(a.only), "" if a.write else " (dry run — nothing written)"))
    return rc


if __name__ == "__main__":
    sys.exit(main())
