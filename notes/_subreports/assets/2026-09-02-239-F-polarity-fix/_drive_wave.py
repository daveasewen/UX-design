#!/usr/bin/env python3
"""#239-F driver: runs V's wave scripts BYTE-IDENTICAL. The only re-seating beyond _v_attack.py's two
constants is the dump() target the waves hardcode to V's seat (V pitfall 2 under-counted it)."""
import runpy, sys, os
F = "/sessions/keen-serene-johnson/mnt/outputs/f239"
sys.path.insert(0, F)
import _v_attack  # noqa: E402
_orig = _v_attack.dump
_v_attack.dump = lambda path: _orig(path.replace("/sessions/wonderful-adoring-euler/mnt/outputs/v238", F))
runpy.run_path(os.path.join(F, sys.argv[1]), run_name="__main__")
