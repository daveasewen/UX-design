#!/usr/bin/env python3
"""#311 lane P — assemble the Thursday burn plan page from the #311-B review shell + body.html."""
import re, pathlib
ROOT = pathlib.Path(__file__).resolve().parents[4]
shell = (ROOT/'notes/_REVIEW-311-B-icons-and-supercharge-page-2026-09-30-v1.html').read_text()
body = (pathlib.Path(__file__).parent/'body.html').read_text()
head = shell.split('</head>')[0] + '</head>\n<body>\n'
head = head.replace('<title>Icons, Supercharge page</title>', '<title>Thursday burn plan</title>')
script = shell.split('<script>')[1].split('</script>')[0]
script = script.replace("review-311-B-icons-and-supercharge-page-v1", "plan-311-thursday-burn-v1")
script = script.replace("notes/_REVIEW-311-B-icons-and-supercharge-page-2026-09-30-v1.html", "notes/_PLAN-311-thursday-burn-2026-10-01-v1.html")
script = script.replace("Session 311 · The icons and Supercharge\\'s dark page, built · comments", "Session 311 · The Thursday burn plan · your calls")
script = script.replace("L.push('3. Note on the page: '", "L.push('Note on the page: '")
script = script.replace("review-311-B-icons-and-supercharge-page.txt", "plan-311-thursday-burn.txt")
bar = '''
<div class="bar" role="region" aria-label="Your decisions"><div class="in">
  <b>Your calls</b><span id="count">0 of 10 answered</span><span class="msg" id="msg">Saves in this browser as you go</span>
  <button type="button" class="pri" id="copy">Copy as text</button><button type="button" id="export">Export</button><button type="button" id="clear">Clear</button>
</div></div>
'''
out = head + body + bar + '<script>' + script + '</script>\n</body></html>\n'
p = ROOT/'notes/_PLAN-311-thursday-burn-2026-10-01-v1.html'
p.write_text(out)
print(p, len(out))
