# usage: gate.sh <tree> <outjson>
T=$1; OUT=$2
cd "$HOME/mnt/Projects--UX-design"
F=""
for p in bar boxplot bullet butterfly-h butterfly-v candlestick combo donut histogram line scatter sparkline stacked-area; do F="$F $T/knowledge/_tests/chart-engine/$p.html"; done
for s in bar boxplot bullet butterfly-h butterfly-v candlestick combo donut histogram line pie scatter sparkline stacked-area; do F="$F $T/knowledge/snippets/Chart-$s.reference.html"; done
F="$F $T/knowledge/snippets/Template-dashboard-bento.reference.html $T/knowledge/snippets/Legend.reference.html"
python3 knowledge/_validate_geometry.py $F --widths 1440 --json $OUT > ${OUT%.json}.txt 2>&1; echo rc=$?
