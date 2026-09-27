# #304 C5 commit seat - wave five door run. Paths in paths-c5.txt, each checked changed-or-untracked first (C1's lock trap).
cd "$(dirname "$0")/../../../.." || exit 1
LOG=${1:-notes/_lanes/304/C5/_gitcommit-C5.log}
mapfile -t P < notes/_lanes/304/C5/paths-c5.txt
SESSION_N=304 bash knowledge/_git_commit.sh --reconciled --quiet=$LOG notes/_lanes/304/C5/_msg-C5.txt "${P[@]}"
echo "EXIT=$?"
