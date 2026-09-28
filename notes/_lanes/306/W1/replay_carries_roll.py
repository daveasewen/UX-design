# #306 W1 - replay #305's carry roll with _wrap_carries.roll_text on the tree BEFORE the #305 wrap commit
# (cd16f7ec = 81bce363^), and compare with what the #305 wrap seat's carries_306.py wrote (81bce363),
# its twelve strikes (the #305 append form) removed. Read-only: git show only.
import re, subprocess, sys
sys.path.insert(0, 'knowledge')
import _wrap_carries as wc
def show(sha): return subprocess.run(['git','--no-optional-locks','show',f'{sha}:_CARRIES.md'],capture_output=True).stdout.decode()
before, after = show('81bce363^'), show('81bce363')
_, actual = wc.list_line(after.split('\n'), 306)
segs = re.sub(r'^> \*\*residual → #306:\*\*', '', actual).split(' · ')
new = [s.strip() for s in segs if wc.NEW_RE.search(s)][:15]
assert len(new) == 15, len(new)
rolled, rec = wc.roll_text(before, 305, 306, new)
_, mine = wc.list_line(rolled.split('\n'), 306)
stripped = re.sub(r' ⛔ \*\*STRUCK AT THE #305 WRAP, BY ADDITION.*?\*\* ', '', actual)
norm = lambda s: re.sub(r'\s*·\s*', ' · ', ' '.join(s.split()))
print('roll receipt', rec)
print('strikes removed from the actual line:', len(re.findall(r' ⛔ \*\*STRUCK AT THE #305 WRAP, BY ADDITION', actual)))
print('mine == actual (strikes removed, whitespace normalised):', norm(mine) == norm(stripped))
if norm(mine) != norm(stripped):
    a, b = norm(mine), norm(stripped); i = next(i for i in range(min(len(a),len(b))) if a[i]!=b[i]); print(i, a[i-80:i+80]); print(b[i-80:i+80])
print('count at 81bce363 by the tool:', wc.count_text(after, 306)['items'])
