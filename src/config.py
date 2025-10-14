from pathlib import Path
UNKNOWN_TEMPLATE_CONF_THRESHOLD = 0.85
LOW_ROW_CONFIDENCE = 0.70
CANDIDATE_DIR = Path("feedback/candidates")
CANDIDATE_DIR.mkdir(parents=True, exist_ok=True)
ENABLE_TEMPLATE_RERUN = True
MAX_RERUNS = 1
