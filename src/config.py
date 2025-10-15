from pathlib import Path
UNKNOWN_TEMPLATE_CONF_THRESHOLD = 0.85
LOW_ROW_CONFIDENCE = 0.70
CANDIDATE_DIR = Path("feedback/candidates")
CANDIDATE_DIR.mkdir(parents=True, exist_ok=True)
ENABLE_TEMPLATE_RERUN = True
MAX_RERUNS = 1

REGISTRY_DIR = Path("templates/registry")
REGISTRY_DIR.mkdir(parents=True, exist_ok=True)
REGISTRY_MATCH_THRESHOLD = 0.75
