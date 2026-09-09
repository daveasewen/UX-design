#!/usr/bin/env python3
"""#261 Ft2 — HSBC product wording + a full-width pane on the footer review page.

Idempotent-ish one-shot: run once on the #261 Ft review page. Asserts every anchor it edits.
"""
import io, re

P = "/sessions/zen-funny-hawking/mnt/UX-design/notes/_lanes/261-Ft-footer-review.html"
s = io.open(P, encoding="utf-8").read()

# ---- 1. product wording (Apollo = design system, NOT the product) ----
n_prod = s.count("Apollo Console")
s = s.replace("Apollo Console", "HSBC Business banking")
s = s.replace("&copy; 2026 Apollo. All rights reserved.",
              "&copy; HSBC Group 2026. All rights reserved.")
s = s.replace("Apollo is the reference implementation of this design system.",
              "HSBC Business banking is the product this specimen ends.")
assert "Apollo is the reference implementation" not in s, "old-footer prose not replaced"

old_warn = ("shown inside an app-shell frame; switch theme and mode with the controls, "
            "which stay pinned as you scroll.</p>")
assert old_warn in s, "warn paragraph not found"
s = s.replace(old_warn, old_warn[:-len("</p>")] +
              "\n      <strong>Apollo</strong> is the design system these components come from; the "
              "product named in every specimen is <strong>HSBC Business banking</strong>.</p>", 1)

# ---- 2. full-width CSS ----
anchor_css = "/* the measurement table */"
FW_CSS = """/* ===================== FULL-WIDTH PANE (#261 Ft2) ===================== */
.fullbleed{width:100vw; margin-left:calc(50% - 50vw); margin-top:24px;}
.fw-case{display:flex; flex-direction:column; gap:8px; margin-bottom:32px;}
.fw-label{padding:0 24px;}
.fw-scroll{overflow-x:auto; border-top:1px solid var(--divider); border-bottom:1px solid var(--divider);}
.fw-frame{display:flex; flex-direction:column;}
.fw-frame .shell{border-left:0; border-right:0; border-top:0;}
.fw-1440{width:1440px;}
.fw-1920{width:1920px;}
.fw-375{width:375px; margin:0 auto; border-left:1px solid var(--divider);
  border-right:1px solid var(--divider);}

"""
assert anchor_css in s
s = s.replace(anchor_css, FW_CSS + anchor_css, 1)


def footer(sfx):
    return """          <footer class="ft spec" role="contentinfo" aria-label="Application footer"
                  data-env="prod" data-system="ok">
            <div class="ft-inner">
              <div class="ft-id">
                <span class="t-ed-body-small em">HSBC Business banking</span>
                <span class="ft-ver t-cm-legal">v4.2.1 &middot; build 8317</span>
                <span class="ft-env t-cm-legal env-label">Production</span>
                <span class="ft-status t-cm-legal" role="status">
                  <span class="ft-dot" aria-hidden="true"></span><span class="sys-label">All systems normal</span>
                </span>
              </div>
              <span class="ft-pip" aria-hidden="true"></span>
              <div class="ft-meta t-cm-legal">
                <span>Data as of <time datetime="2026-09-09T09:41:00+01:00">09:41</time> &middot; 3 minutes ago</span>
                <span class="ft-pip" aria-hidden="true"></span>
                <span>en-GB &middot; Europe/London (GMT+1)</span>
              </div>
              <nav class="ft-links" aria-label="Legal and support">
                <ul>
                  <li><a class="lnk t-cm-legal" href="#{s}a">Privacy</a></li>
                  <li><a class="lnk t-cm-legal" href="#{s}b">Terms</a></li>
                  <li><a class="lnk t-cm-legal" href="#{s}c">Accessibility</a></li>
                  <li><a class="lnk t-cm-legal" href="#{s}d">Support</a></li>
                </ul>
              </nav>
            </div>
          </footer>""".replace("{s}", sfx)


def case(cid, klass, tag, lead, note, rows=4):
    body = "\n".join(['            <div class="shell-row"></div>'] * rows)
    return """  <div class="fw-case" id="%s">
    <p class="t-ed-caption fw-label"><span class="tag t-cm-legal">%s</span> %s</p>
    <div class="fw-scroll">
      <div class="fw-frame %s">
        <div class="shell">
          <div class="shell-bar"><span class="t-cm-legal">Payments operations</span><span class="t-cm-legal">4,812 rows</span></div>
          <div class="shell-body">
%s
          </div>
%s
        </div>
      </div>
    </div>
    <p class="t-ed-caption caption fw-label">%s</p>
  </div>
""" % (cid, tag, lead, klass, body, footer(cid), note)


SECTION = """  <!-- ================= 2. FULL WIDTH (#261 Ft2) ================= -->
  <section class="stack-l">
    <div class="stack">
      <h2 class="t-ed-heading-4 rule">2 &middot; Full width &mdash; the footer edge to edge</h2>
      <p class="t-ed-body-small caption">Dave, verbatim: <strong>&ldquo;I need to see the full width
        version of this&rdquo;</strong>. Section&nbsp;1 shows the footer in a half-screen column, where
        the container query wraps it onto two rows. Here it is at its real widths, inside the app-shell
        frame and edge to edge &mdash; nothing is clipped to the review column. The theme, mode,
        environment and system controls above drive these three as well.</p>
    </div>
  </section>
"""

PANE = ('<div class="fullbleed">\n'
        + case("fw1440", "fw-1440", "1440px",
               "desktop default, inside the shell, edge to edge",
               "One 41px row. Identity and trust on the left in the order the question is asked; the "
               "regulator&rsquo;s row pinned right. The band is the width of the shell&rsquo;s content "
               "column, because the app footer has no inner rail of its own.")
        + case("fw1920", "fw-1920", "1920px",
               "wide desk &mdash; scroll this strip sideways if your screen is narrower",
               "Still one row at 1920. Only the gap between the two clusters stretches: there is no "
               "max-width and no centring, so the footer cannot drift away from the column it ends.")
        + case("fw0375", "fw-375", "375px",
               "handset, the stacked form",
               "The 375px container query stacks the clusters, drops the meta pips and gives the legal "
               "links their own row &mdash; 127px tall, 24px targets, 24px apart.", rows=6)
        + "</div>\n")

marker = "  <!-- ================= 2. VARIANTS ================= -->"
assert marker in s
s = s.replace(marker, SECTION + "\n" + PANE + "\n  <hr>\n\n"
              "  <!-- ================= 3. VARIANTS ================= -->", 1)

# ---- 3. renumber the sections that follow ----
renum = [("2 · The three variants", "3 · The three variants"),
         ("3 · The environment badge", "4 · The environment badge"),
         ("4 · What changed, measured", "5 · What changed, measured"),
         ("5 · Open, and yours", "6 · Open, and yours"),
         ("<!-- ================= 3. THE ENVIRONMENT BADGE ================= -->",
          "<!-- ================= 4. THE ENVIRONMENT BADGE ================= -->"),
         ("<!-- ================= 4. WHAT CHANGED, MEASURED ================= -->",
          "<!-- ================= 5. WHAT CHANGED, MEASURED ================= -->"),
         ("<!-- ================= 5. FOR DAVE ================= -->",
          "<!-- ================= 6. FOR DAVE ================= -->")]
for a, b in reversed(renum):
    assert a in s, "renumber anchor missing: " + a
    s = s.replace(a, b)

io.open(P, "w", encoding="utf-8").write(s)
print("product strings replaced:", n_prod)
print("Apollo left:", sorted(set(re.findall(r"Apollo[^<\n]{0,24}", s))))
