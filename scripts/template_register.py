import argparse, glob, yaml
from datetime import datetime
from src.template_registry import register_from_candidate

ap = argparse.ArgumentParser()
ap.add_argument("--candidate", default=None)
ap.add_argument("--bank", default=None)
ap.add_argument("--template", default=None)
ap.add_argument("--version", default="1.0.0")
a = ap.parse_args()

cand = a.candidate or (sorted(glob.glob("feedback/candidates/*.yaml"))[-1])
data = yaml.safe_load(open(cand, "r", encoding="utf-8")) or {}
bank = a.bank or data.get("bank_guess") or "AutoBank"
template = a.template or data.get("template_guess") or "AutoTemplate_v1"

out = register_from_candidate(cand, bank, template, a.version)
print(f"REGISTERED: {out}")
