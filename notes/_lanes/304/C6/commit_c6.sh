# #304 C6 - wave six door run. Paths in paths-c6.txt, each checked changed-or-untracked first.
cd "$(dirname "$0")/../../../.." || exit 1
LOG=${1:-notes/_lanes/304/C6/_gitcommit-C6.log}
mapfile -t P < notes/_lanes/304/C6/paths-c6.txt
SESSION_N=304 bash knowledge/_git_commit.sh --reconciled --quiet=$LOG notes/_lanes/304/C6/_msg-C6.txt "${P[@]}"
echo "EXIT=$?"
