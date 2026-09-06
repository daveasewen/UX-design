#!/usr/bin/env python3
"""ADVERSARIAL probe of code_only() — verifier seat, #250. Reads the LIVE gate."""
import sys, os
sys.path.insert(0, "/sessions/epic-trusting-goldberg/mnt/UX-design/knowledge")
os.environ["HELPGATE_OK"] = "1"
sys.argv = ["_validate_behaviour.py", "--selftest"]   # keep help_gate quiet
import importlib.util
spec = importlib.util.spec_from_file_location(
    "vb", "/sessions/epic-trusting-goldberg/mnt/UX-design/knowledge/_validate_behaviour.py")
vb = importlib.util.module_from_spec(spec)
spec.loader.exec_module(vb)
code_only = vb.code_only

CASES = [
    # (name, source, expected code_only substring/ properties)
    ("A1 // inside a double-quoted string",
     'var u = "a//b";\n', 'var u = "a//b";'),
    ("A2 http:// URL in code",
     'var u = "http://example.com/x";\n', 'var u = "http://example.com/x";'),
    ("A3 /* inside a regex literal  /\\/*foo/",
     'var r = /\\/*foo/;\n', 'var r = /\\/*foo/;'),
    ("A4 template literal with ${} containing //",
     'var t = `a${b//c\n}d`;\n', 'TEMPLATE'),
    ("A5 block comment containing */ inside a string",
     'var s = "/* x */";\nvar y=1;\n', 'both lines survive'),
    ("A6 division then line comment: a / b // comment",
     'var z = a / b; // comment\n', 'var z = a / b;'),
    ("A7 regex after return",
     'function f(s){ return /x/.test(s); }\n', 'regex kept'),
    ("A8 6/2/1 chained division",
     'var q = 6/2/1;\n', 'var q = 6/2/1;'),
    ("A9 NESTED template literal `a${`b`}c`",
     'var t = `a${`b`}c`;\nvar after = 1;\n', 'NESTED'),
    ("A10 regex immediately after )  if(x) /re/.test(y)",
     'if (x) /re/.test(y);\nvar after = 1;\n', 'PAREN-REGEX'),
    ("A11 unterminated-looking: division after ] then //",
     'var v = arr[0] / 2; // tail\n', 'var v = arr[0] / 2;'),
    ("A12 string with escaped quote then //",
     'var s = "he said \\"hi\\" // not a comment";\nvar after=1;\n', 'ESCQ'),
    ("A13 keyword-suffix identifier: x.of / 2",
     'var w = x.of / 2;\nvar after=1;\n', 'KWSUFFIX'),
    ("A14 block comment spanning lines w/ code after on same line",
     'var a=1; /* c\nc */ var b=2;\n', 'BLOCKTAIL'),
    ("A15 regex with // inside char class",
     'var r = /[//]/;\nvar after=1;\n', 'CLASSSLASH'),
]
print("%-52s | %s" % ("CASE", "code_only() OUTPUT (repr)"))
print("-" * 120)
for name, src, note in CASES:
    try:
        out = code_only(src)
    except Exception as e:
        out = "EXCEPTION: %r" % e
    print("%-52s | %r" % (name, out))
