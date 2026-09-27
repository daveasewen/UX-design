#!/bin/bash
# usage: run13.sh <label> <ledger_n|orig> <code: fixed|old> [tmpdir]
cd $HOME/clone304w3c
export TMPDIR=${4:-/dev/shm}
L=notes/_BUILD-VERDICT-LOG.jsonl
cp $HOME/w3c/ledger.orig $L
if [ "$2" != orig ]; then python3 - "$2" <<'PY'
import json,sys,subprocess
n=int(sys.argv[1]); sha=subprocess.run(["git","rev-parse","--short","HEAD"],capture_output=True,text=True).stdout.strip()
r={"at":"2026-09-27T00:00:00","sha":sha,"dirty":False,"steps_on_disk":n,"range":None,"timeout":60,"include_mutating":False,"tool":"_build_survey.py","passed":list(range(1,n+1)),"failed":[],"refused":[],"errored":[],"skipped":[]}
open("notes/_BUILD-VERDICT-LOG.jsonl","a").write(json.dumps(r,sort_keys=True)+"\n")
PY
fi
[ "$3" = old ] && git show aaf3bb7e:knowledge/_gen_chain.py > knowledge/_gen_chain.py
s=$(date +%s); python3 knowledge/_capture_gate.py --selftest > $HOME/w3c/r13_$1.txt 2>&1; rc=$?
echo "$1 ledger=$2 code=$3 tmp=$TMPDIR rc=$rc t=$(( $(date +%s)-s ))" | tee -a $HOME/w3c/r13_results.txt
cp $HOME/w3c/ledger.orig $L; git checkout -q -- knowledge/_gen_chain.py
