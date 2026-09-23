cd "$(dirname "$0")/../../../../.." || exit 1
SESSION_N=300 bash knowledge/_git_commit.sh --reconciled --quiet=notes/_lanes/300/W/_gitcommit-W5b.log notes/_lanes/300/W/_msg-W5b.txt \
 _LIVE-STATE.md _CHAIN.md knowledge/_memento-index.json notes/_REHEARSAL-LOG.jsonl \
 _HANDOFF-151-the-boot-was-measured-and-the-reading-stays.md \
 notes/_lanes/300/WRAP-MEMORY-HOOK.md notes/_lanes/299/WRAP-MEMORY-HOOK.md \
 notes/_subreports/2026-09-23-300-W-wrap.md \
 notes/_lanes/300/W/_work notes/_lanes/300/W/_ops-300W-5b.json \
 notes/_lanes/300/W/_msg-W1.txt notes/_lanes/300/W/_msg-W1.txt.t3-rendered \
 notes/_lanes/300/W/_gitcommit-W1.log notes/_lanes/300/W/_gitcommit-W1.term \
 notes/_lanes/300/W/_gitcommit-W1-refused-stalechain.log notes/_lanes/300/W/_gitcommit-W1-refused-stalechain.term \
 notes/_lanes/300/W/_push-W1-plain.log notes/_lanes/300/W/_ci-gates-W.log
echo "EXIT=$?"
