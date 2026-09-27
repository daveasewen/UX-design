cd "$(dirname "$0")/../../../../.." || exit 1
SESSION_N=304 bash knowledge/_git_commit.sh --reconciled --quiet=notes/_lanes/304/W/_gitcommit-W5b.log notes/_lanes/304/W/_msg-W5b.txt \
 _LIVE-STATE.md _CHAIN.md knowledge/_memento-index.json reviews/MEMENTO-SCHEMATIC-2026-08-07-v2.html \
 _HANDOFF-155-the-weekend-runs-landed-and-the-review-moved-to-an-artifact.md \
 notes/_lanes/304/WRAP-MEMORY-HOOK.md \
 notes/_subreports/2026-09-27-304-W-wrap.md \
 notes/_lanes/304/W
echo "EXIT=$?"
