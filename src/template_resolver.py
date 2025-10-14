
from typing import Dict, List, Optional, Tuple
from difflib import SequenceMatcher
from pathlib import Path
import re, yaml

class TemplateGuess:
    def __init__(self, bank: Optional[str], template: Optional[str], score: float, reasons: list):
        self.bank, self.template, self.score, self.reasons = bank, template, score, reasons

def _sim(a: str, b: str) -> float:
    return SequenceMatcher(None, (a or "").lower(), (b or "").lower()).ratio()

def _load_banks(path: str = "templates/banks.yaml") -> Dict:
    p = Path(path)
    if not p.exists():
        return {}
    with p.open("r", encoding="utf-8") as f:
        return yaml.safe_load(f) or {}

def infer_template(report_text: str, detected_headers: List[str], banks: Optional[Dict]=None) -> TemplateGuess:
    banks = banks or _load_banks()
    best: Tuple[Optional[str], Optional[str], float, List[str]] = (None, None, 0.0, [])
    for bank, meta in banks.items():
        tpls = (meta or {}).get("templates", {})
        synonyms = (meta or {}).get("header_synonyms", [])
        hint = 0.1 if re.search(re.escape(bank), report_text or "", flags=re.I) else 0.0
        for tpl_name, tpl_def in tpls.items():
            expected = (tpl_def or {}).get("headers", [])
            direct = sum(1 for h in detected_headers if h in expected) / max(1, len(expected))
            syn_score = 0.0
            for h in detected_headers:
                syn_score = max(syn_score, max((_sim(h, s) for s in synonyms), default=0.0))
            fuzzy = 0.0
            if expected:
                fuzzy = sum(max((_sim(h, e) for h in detected_headers), default=0.0) for e in expected) / len(expected)
            score = 0.5*direct + 0.3*fuzzy + 0.1*syn_score + hint
            if score > best[2]:
                best = (bank, tpl_name, score, [
                    f"direct={direct:.2f}", f"fuzzy={fuzzy:.2f}", f"syn={syn_score:.2f}", f"hint={hint:.2f}"
                ])
    return TemplateGuess(*best)
