from datetime import datetime
from .gemini_client import extract_table_with_report
from .template_resolver import infer_template
from .structure_recorder import CandidateStructure, save_candidate
from .config import (UNKNOWN_TEMPLATE_CONF_THRESHOLD, LOW_ROW_CONFIDENCE,
                     ENABLE_TEMPLATE_RERUN, MAX_RERUNS)

def process_pdf(pdf_path: str, out_xlsx: str, dry_run: bool=False):
    r1 = extract_table_with_report(b"", template_hint=None)
    guess = infer_template(r1["report"], r1["headers"])
    low_idx = [i for i,c in enumerate(r1["row_confidences"]) if c < LOW_ROW_CONFIDENCE]

    result = r1
    reruns = 0
    if ENABLE_TEMPLATE_RERUN and guess.score >= UNKNOWN_TEMPLATE_CONF_THRESHOLD and MAX_RERUNS > 0:
        result = extract_table_with_report(b"", template_hint="dummy")
        reruns = 1

    if guess.score < UNKNOWN_TEMPLATE_CONF_THRESHOLD or low_idx:
        cand = CandidateStructure(
            bank_guess=guess.bank, template_guess=guess.template,
            overall_confidence=float(guess.score),
            header_fields=list(result["headers"]),
            sample_rows=list(result["data"][:5]),
            low_confidence_rows=low_idx,
            llm_report_excerpt=str(result["report"])[:2000],
            source_pdf=pdf_path, created_at=datetime.utcnow().isoformat()
        )
        save_candidate(cand)

    if not dry_run:
        from .excel_generator_v2 import generate_simple_to_file
        generate_simple_to_file(result["data"], result["headers"], out_xlsx)

    return {"reruns": reruns, "guess_score": float(guess.score), "low_rows": len(low_idx)}
