cd "$(dirname "$0")/../../../../.." || exit 1
SESSION_N=305 bash knowledge/_git_commit.sh --reconciled --quiet=notes/_lanes/305/W/_gitcommit-W1.log notes/_lanes/305/W/_msg-W1.txt \
 $(cat notes/_lanes/305/W/_work/paths_w1.txt | tr '\n' ' ')
echo "EXIT=$?"
