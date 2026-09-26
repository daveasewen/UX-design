cd "$(dirname "$0")/../../../../.." || exit 1
SESSION_N=303 bash knowledge/_git_commit.sh --reconciled --quiet=notes/_lanes/303/W/_gitcommit-W5b.log notes/_lanes/303/W/_msg-W5b.txt \
 _LIVE-STATE.md _CHAIN.md knowledge/_memento-index.json \
 _HANDOFF-154-the-deck-was-finished-for-friday-and-apollo-mcp-was-asked-for.md \
 notes/_lanes/303/WRAP-MEMORY-HOOK.md \
 notes/_subreports/2026-09-26-303-W-wrap.md \
 notes/_lanes/303/W/_work notes/_lanes/303/W/_ops-303W-5b.json \
 notes/_lanes/303/W/_msg-W1.txt notes/_lanes/303/W/_msg-W1.txt.t3-rendered \
 notes/_lanes/303/W/_gitcommit-W1.log notes/_lanes/303/W/_gitcommit-W1.term \
 notes/_lanes/303/W/_push-W1-plain.log notes/_lanes/303/W/_ci-gates-W.log notes/_lanes/303/W/_ci-runs-efe3bb47.txt
echo "EXIT=$?"
