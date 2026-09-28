# #306 T - stamp s306-D1..D3 enacted at the store-write commit (s295-D2), dry run then write.
cd "$(dirname "$0")/../../../.." || exit 1
SHA=${1:?sha}; MODE=${2:?--dry-run|--write}
S1="enacted #306 2026-09-28 - lane T: 24 rows parked -> done in knowledge/_state.json by addition, each body carrying the answering ruling ids and lane S's quote, closed_by naming this ruling (notes/_lanes/306/T/store_batch.write.json)"
S2="enacted #306 2026-09-28 - lane T: W-222 and W-272 parked -> done by addition under this ruling and s306-D1; W-305hr's body gains that he has said which way the two go, and it stays open on its kind-6 half"
S3="enacted #306 2026-09-28 - lane T: 78 rows parked -> open in knowledge/_state.json by addition, each with a dated paragraph (tick time, lane S's verdict); knowledge/_parked.json unchanged (no entries for these rows); W-305n5 and W-305b4 closed with receipts"
python3 knowledge/_inscribe_ruling.py --set-status s306-D1 "$S1" --evidence-sha "$SHA" $MODE; echo rc=$?
python3 knowledge/_inscribe_ruling.py --set-status s306-D2 "$S2" --evidence-sha "$SHA" $MODE; echo rc=$?
python3 knowledge/_inscribe_ruling.py --set-status s306-D3 "$S3" --evidence-sha "$SHA" $MODE; echo rc=$?
