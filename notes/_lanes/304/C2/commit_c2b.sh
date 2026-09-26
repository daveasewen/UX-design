# #304 C2 commit seat - the stamps commit (s245-D10, s277-D12 enacted).
cd "$(dirname "$0")/../../../.." || exit 1
LOG=${1:-notes/_lanes/304/C2/_gitcommit-C2b.log}
SESSION_N=304 bash knowledge/_git_commit.sh --reconciled --quiet=$LOG notes/_lanes/304/C2/_msg-C2b.txt \
 knowledge/_rulings.json notes/_RULINGS.html \
 notes/_lanes/304/C2/_gitcommit-C2.log notes/_lanes/304/C2/_gitcommit-C2.term \
 notes/_lanes/304/C2/step5-stamps.log notes/_lanes/304/C2/step5-regen.log \
 notes/_lanes/304/C2/_msg-C2b.txt notes/_lanes/304/C2/commit_c2b.sh notes/_lanes/304/C2/_msg-C2.txt.t3-rendered
echo "EXIT=$?"
