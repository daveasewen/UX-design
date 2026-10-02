"""Read-only parsers for the #315 LA library audit. No writes to the library."""
import re, os, glob, json
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../..'))
K = os.path.join(ROOT, 'knowledge')

def rel(p): return os.path.relpath(p, ROOT)

def line_of(text, off): return text.count('\n', 0, off) + 1

def style_blocks(html):
    for m in re.finditer(r'<style[^>]*>(.*?)</style>', html, re.S | re.I):
        yield m.start(1), m.group(1)

def parse_css(css, base_off=0, full=None):
    """Yield dicts {sel, decls(str), media, line} for every style rule. Comments blanked (offsets kept)."""
    clean = re.sub(r'/\*.*?\*/', lambda m: re.sub(r'[^\n]', ' ', m.group(0)), css, flags=re.S)
    out = []
    def walk(s, start, end, media):
        i = start
        while i < end:
            j = s.find('{', i, end)
            if j < 0: break
            head = s[i:j].strip()
            # find matching brace
            depth, k = 1, j + 1
            while k < end and depth:
                if s[k] == '{': depth += 1
                elif s[k] == '}': depth -= 1
                k += 1
            body_s, body_e = j + 1, k - 1
            # head may contain trailing decls/semicolons from previous; keep after last ';' or '}'
            head_start = i + max(s[i:j].rfind(';'), s[i:j].rfind('}')) + 1
            head = s[head_start:j].strip()
            if head.startswith('@'):
                if re.match(r'@(media|supports|container|layer)', head):
                    walk(s, body_s, body_e, (media + ' ' + head).strip())
                # @keyframes, @font-face etc skipped
            else:
                off = base_off + head_start + (len(s[head_start:j]) - len(s[head_start:j].lstrip()))
                out.append({'sel': ' '.join(head.split()), 'decls': s[body_s:body_e], 'media': media,
                            'off': off, 'line': line_of(full, off) if full is not None else None})
            i = k
    walk(clean, 0, len(clean), '')
    return out

def snippet_rules(path):
    html = open(path, encoding='utf-8').read()
    rules = []
    for off, css in style_blocks(html):
        rules += parse_css(css, off, html)
    return html, rules

def decl(decls, prop):
    """last value of prop in a declaration string, or None"""
    vals = re.findall(r'(?:^|;|\s)' + re.escape(prop) + r'\s*:\s*([^;]+)', decls)
    return vals[-1].strip() if vals else None

def parts():
    metas = {os.path.basename(f)[:-10]: f for f in glob.glob(os.path.join(K, 'components', '*.meta.json'))}
    snips = {os.path.basename(f)[:-15]: f for f in glob.glob(os.path.join(K, 'snippets', '*.reference.html'))}
    sl = {k.lower(): v for k, v in snips.items()}
    out = []
    for slug, mf in sorted(metas.items()):
        out.append({'slug': slug, 'meta': mf, 'snippet': sl.get(slug.lower())})
    return out

def visible_text(html):
    h = re.sub(r'<(script|style)[^>]*>.*?</\1>', ' ', html, flags=re.S | re.I)
    h = re.sub(r'<!--.*?-->', ' ', h, flags=re.S)
    return h

FENCE = re.compile(r"/\* ===== APOLLO-DEMO[^\n]*?START.*?APOLLO-DEMO[^\n]*?END ===== \*/", re.S)
DROP_FIRST = ("body", "html", "*", ".demo-controls", ".cap", ".stateLabel")
ROOT_ANCESTOR = re.compile(r'^((?::root|html)(?:\[[^\]]*\])*|\[[^\]]*\])\s+(.+)$')
def is_harness(sel):
    """mirror of knowledge/canon/gen_canon_components.py is_harness (read, not imported)"""
    first = sel.split(",")[0].strip()
    if first == ":root": return True
    m = ROOT_ANCESTOR.match(first)
    if m: return is_harness(m.group(2))
    if first.startswith("[data-theme"): return True
    fs = first.split()[0] if first.split() else first
    for d in DROP_FIRST:
        if fs == d or fs.startswith(d): return True
    return False

def fenced_spans(html):
    return [(m.start(), m.end()) for m in FENCE.finditer(html)] + \
           [(m.start(), m.end()) for m in re.finditer(r"<!-- ===== APOLLO-DEMO.*?END ===== -->", html, re.S)]

def part_rules(path):
    html, rules = snippet_rules(path)
    spans = fenced_spans(html)
    keep = [r for r in rules if not is_harness(r['sel']) and not any(a <= r['off'] < b for a, b in spans)]
    return html, keep

def manifest(html):
    m = re.search(r'<script type="application/json" id="token-manifest">(.*?)</script>', html, re.S)
    if not m: return {}
    try: return json.loads(m.group(1))
    except Exception: return {'$unparsed': True}

def theme_vals(html, theme_sel):
    """custom-property values declared in harness blocks like :root{..} or [data-theme="dark"]{..}"""
    out = {}
    for off, css in style_blocks(html):
        for r in parse_css(css, off, html):
            if r['sel'] == theme_sel:
                for k, v in re.findall(r'(--[\w-]+)\s*:\s*([^;]+)', r['decls']): out[k] = v.strip()
    return out
