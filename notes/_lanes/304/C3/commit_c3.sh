# #304 C3 commit seat - wave three door run. Paths in paths-c3.txt, each checked changed-or-untracked first (C1's lock trap).
cd "$(dirname "$0")/../../../.." || exit 1
LOG=${1:-notes/_lanes/304/C3/_gitcommit-C3.log}
mapfile -t P < notes/_lanes/304/C3/paths-c3.txt
SESSION_N=304 bash knowledge/_git_commit.sh --reconciled --quiet=$LOG notes/_lanes/304/C3/_msg-C3.txt "${P[@]}"
echo "EXIT=$?"
