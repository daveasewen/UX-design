#!/usr/bin/env python3
"""#313 lane D4 — s308-D20's one name on the metas: every `edges.obeys[]` entry's `$why` becomes `why`.

Text edit inside each meta's `edges.obeys` array only (every other byte kept, the `$why` an `$extracted` block
carries is not an edge reason and is untouched), then proven: the parsed meta equals the original with exactly
that key renamed. Idempotent. `--check` writes nothing. Run from the repo root.
"""
import glob, json, sys

def rename(d):
    ob = ((d.get('edges') or {}).get('obeys'))
    if isinstance(ob, list):
        for i, e in enumerate(ob):
            if isinstance(e, dict) and '$why' in e:
                ob[i] = {('why' if k == '$why' else k): v for k, v in e.items()}
    return d

def main(argv):
    total = files = 0
    for p in sorted(glob.glob('knowledge/components/*.meta.json')):
        raw = open(p, encoding='utf-8').read()
        d = json.loads(raw)
        want = rename(json.loads(raw))
        if want == d:
            continue
        lines = raw.split('\n')
        i = next(n for n, ln in enumerate(lines) if ln.strip().startswith('"obeys": ['))
        ind = len(lines[i]) - len(lines[i].lstrip())
        j = next(n for n in range(i + 1, len(lines)) if lines[n].startswith(' ' * ind + ']'))
        n = 0
        for k in range(i, j):
            if lines[k].lstrip().startswith('"$why":'):
                lines[k] = lines[k].replace('"$why":', '"why":', 1); n += 1
        new = '\n'.join(lines)
        if json.loads(new) != want:
            print('REFUSED', p, 'the text edit does not equal the rename'); return 1
        print(f'{p}: {n} obeys reason(s) $why → why')
        total += n; files += 1
        if '--check' not in argv:
            open(p, 'w', encoding='utf-8').write(new)
    print(f'COUNTS: metas {files} · reasons renamed {total}' + (' (check only)' if '--check' in argv else ''))
    return 0

if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
