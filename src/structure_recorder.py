from dataclasses import dataclass, asdict
from typing import List, Dict, Any, Optional
from datetime import datetime
from pathlib import Path
import yaml
from .config import CANDIDATE_DIR

@dataclass
class CandidateStructure:
    bank_guess: Optional[str]
    template_guess: Optional[str]
    overall_confidence: float
    header_fields: List[str]
    sample_rows: List[Dict[str, Any]]
    low_confidence_rows: List[int]
    llm_report_excerpt: str
    source_pdf: str
    created_at: str

def save_candidate(struct: CandidateStructure):
    stamp = datetime.utcnow().strftime("%Y%m%dT%H%M%SZ")
    fname = f"{stamp}.yaml"
    path = CANDIDATE_DIR / fname
    with path.open("w", encoding="utf-8") as f:
        yaml.safe_dump(asdict(struct), f, allow_unicode=True, sort_keys=False)
    return path
