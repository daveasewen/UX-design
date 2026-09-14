# #271 — the plain-prose wrap summary (`s250`)

Session #271 did three unrelated things and finished all of them, which is unusual here.

It opened with a single word. #270 had built the generator that puts roles, intents and data
shapes into the knowledge graph, dry-run it, proved that it refuses to land without a recorded
ruling id, and then deliberately stopped — because adding an edge type changes a vocabulary that
was closed at #75, and that is yours. You said "ratify". `s270-D2` went into the store and 115
edges across 45 new nodes and 26 component files landed at `23f7d16`: the graph now knows which
components provide which roles, which questions they answer, what shape of data they take and
what yields to what. It is the first extension of that vocabulary since it was closed. The one
thing the landing did not do is fix the drift it found on the way — `roles.json` claims 108
memberships against 24 component files that actually declare what they provide — because putting
a repair inside a landing commit makes two changes look like one. It is written down and it is
carried.

The middle of the day was the harvest. Three parallel lanes read the whole component library
against thirteen external design systems and came back with 132 components, 485 quotations each
under fifteen words, and a result that splits into 69 rows where the systems disagree, 15 where
they all agree, and 31 where nobody has a source at all and the number in our files is a guess we
have now labelled as one. The verifier that checked this work went red before it went green: it
found over-long quotations, mismatched receipts, and one sentence attributed to you that you never
said. A repair lane fixed all of it, and the record says "green by addition" rather than "green",
because the difference matters. The finding worth keeping is that these systems agree almost
perfectly on what to measure and almost never on where to cut: navigation breaks at five items or
seven, a toast dismisses at four seconds or ten, a pie chart caps at five slices or six. That is
exactly why the 69 are yours and not a lane's — averaging thirteen opinions produces a number
nobody holds.

Then you asked, mid-turn, for the review page to be something you could actually work in rather
than read. That produced the v2 decision sheet: every row now has a real control and a notes
field, there is a side nav that counts how many you have decided per role, filters for status and
contested-ness, and an export button. The export is the point — its JSON is the input to the next
session, where a lane cuts one ruling per row you decided, using your notes as the words. It is
the first review artefact in this project with a machine-readable return path.

Dream pass 12 closed the same day it was ruled, which has not happened before. The stop line is
one number now — 180,000 — and you explained why, which retired the old 150,929 as a figure from
before we started delegating wraps rather than overruling it. A new warning arm watches the fill
figure a wrap declares; whether it ever blocks was not asked, so it does not. The demo dates are
recorded as undecided, with your own hedge — "a guess" — kept in the record so nothing prints a
date you did not give. And the fourth proposal, the one you said you did not understand, was
re-explained and answered "A. re-check": from now on an open item written into memory before you
have answered is recorded as a question put to you, and the wrap's last act is to read that list
back against the rulings and strike whatever the session itself closed. Its first live run caught
the previous session's hook still claiming the edge types were open, five hours after you had
ratified them.

What went wrong is the fill. The handoff was written at about 195,000 and this wrap seat measured
206,466 — past the stop line ruled that same morning, and over the 200,000 working ceiling. Both
are written down rather than smoothed, on your "no panic until we get to 256". Boot is 80,474, a
seventh consecutive breach of a number that may only ever shrink. And the memory store was
read-only from the wrap seat again, so the hook exists as a complete draft for the conductor to
copy rather than as an entry.

Everything else is yours: the 69 decisions, the 15 to bulk-ratify, whether either new gate arm
should block, three colours that shipped only so new nodes would render, and the sentence about
256 — which is ruling-shaped and was deliberately not turned into a ruling by a wrap.
