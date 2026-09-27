"""305 B2 — read the baked data out of a built explorer page (the <script id="kg"> JSON)."""
import json, re, sys, html as H
def load(path):
    h = open(path, encoding="utf-8").read()
    m = re.search(r'<script[^>]*id="kg"[^>]*>(.*?)</script>', h, re.S)
    return json.loads(m.group(1))
