from typing import Dict, List, Optional
from difflib import SequenceMatcher

class TemplateGuess:
    def __init__(self, bank: Optional[str], template: Optional[str], score: float, reasons: list):
        self.bank, self.template, self.score, self.reasons = bank, template, score, reasons

def _sim(a: str, b: str) -> float:
    return SequenceMatcher(None, a.lower(), b.lower()).ratio()

def infer_template(report_text: str, detected_headers: List[str], banks: Optional[Dict]=None) -> TemplateGuess:
    return TemplateGuess(None, None, 0.0, ["stub"])
