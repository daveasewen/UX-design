#!/usr/bin/env python3
"""#304 Run 2a — STAMP the ENACTED verdicts through the sanctioned writer ONLY
(`knowledge/_inscribe_ruling.set_status`, the same function `--set-status` calls; S1–S6 + R5/R6 run on
every call, the reconstruction proof included). Never hand-edits _rulings.json.

  python3 stamp.py --dry-run     # every stamp composed against the live file, nothing written
  python3 stamp.py --write       # stamp, one ruling per call, each logged to WRITES.log; resumable
                                  # (a ruling whose status already leads with 'ENACTED (back-stamped #304' is skipped)
Pre-checks per stamp: the sha resolves to a commit in this repo (git rev-parse), and the commit date is
not before the ruling's date."""
import json, os, subprocess, sys, datetime
sys.path.insert(0, 'knowledge')
import _inscribe_ruling as IR

MARK = 'ENACTED (back-stamped #304 2026-09-26, Run 2 audit)'
LOG = 'notes/_lanes/304/R2/WRITES.log'
write = '--write' in sys.argv
D = [d for d in json.load(open('notes/_lanes/304/R2/decisions.json')) if d['verdict'] == 'ENACTED']

def status_for(d, old):
    basis = {'S-A': 'commit body names it with an enactment verb and touches a governed file',
             'S-B': 'a governed file carries its id, introduced by a commit that names it',
             'MANUAL': 'hand-read receipt'}[d['basis']]
    return (f"{MARK} in commit {d['sha']} — basis {d['basis']} ({basis}). Receipt: {d['receipt']} "
            f"· Was: {old!r}. Audit record: notes/_lanes/304/R2/decisions.json")

ok = fail = skip = 0
for d in D:
    rid, sha = d['id'], d['sha']
    cur = {r['id']: r for r in json.load(open(IR.RULINGS))['rulings']}[rid]
    if cur['status'].startswith(MARK):
        skip += 1; continue
    full = subprocess.run(['git', '--no-optional-locks', 'rev-parse', '--verify', '-q', sha + '^{commit}'],
                          capture_output=True, text=True).stdout.strip()
    cdate = subprocess.run(['git', '--no-optional-locks', 'show', '-s', '--format=%ad', '--date=short', sha],
                           capture_output=True, text=True).stdout.strip() if full else ''
    if not full:
        print(f'⛔ {rid}: sha {sha} does not resolve'); fail += 1; continue
    if d['date'] and cdate < d['date']:
        print(f'⛔ {rid}: commit {sha} {cdate} is before the ruling date {d["date"]}'); fail += 1; continue
    new = status_for(d, cur['status'])
    try:
        rep = IR.set_status(rid, new, sha, IR.RULINGS, write=write)
    except IR.InscriptionRefused as ex:
        print(f'⛔ {rid}: REFUSED {str(ex)[:300]}'); fail += 1; continue
    ok += 1
    if write:
        with open(LOG, 'a') as fh:
            fh.write(json.dumps({'at': datetime.datetime.utcnow().isoformat() + 'Z', 'op': 'set_status', 'id': rid,
                                 'sha': sha, 'commit_full': full, 'commit_date': cdate,
                                 'status_before': rep['status_before'][:200], 'evidence_before': rep['evidence_before'],
                                 'evidence_after': rep['evidence_after'], 'bytes': [rep['file_bytes_before'], rep['file_bytes_after']]},
                                ensure_ascii=False) + '\n')
print(f"{'WRITE' if write else 'DRY-RUN'}: ok {ok} · refused/failed {fail} · already stamped {skip} · of {len(D)} ENACTED verdicts")
