# #304 C4 commit seat - wave four door run. Paths in paths-c4.txt, each checked changed-or-untracked first (C1's lock trap).
cd "$(dirname "$0")/../../../.." || exit 1
LOG=${1:-notes/_lanes/304/C4/_gitcommit-C4.log}
mapfile -t P < notes/_lanes/304/C4/paths-c4.txt
SESSION_N=304 bash knowledge/_git_commit.sh --reconciled --quiet=$LOG notes/_lanes/304/C4/_msg-C4.txt "${P[@]}"
echo "EXIT=$?"
