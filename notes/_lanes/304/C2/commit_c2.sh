# #304 C2 commit seat - wave two door run. Paths in paths-c2.txt, each checked changed-or-untracked first (C1's lock trap).
cd "$(dirname "$0")/../../../.." || exit 1
LOG=${1:-notes/_lanes/304/C2/_gitcommit-C2.log}
mapfile -t P < notes/_lanes/304/C2/paths-c2.txt
SESSION_N=304 bash knowledge/_git_commit.sh --reconciled --quiet=$LOG notes/_lanes/304/C2/_msg-C2.txt "${P[@]}"
echo "EXIT=$?"
