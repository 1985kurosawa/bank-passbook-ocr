from __future__ import annotations
from dataclasses import dataclass
from pathlib import Path
from typing import List, Tuple, Optional, Dict
from difflib import SequenceMatcher
import re, yaml
from .config import REGISTRY_DIR, REGISTRY_MATCH_THRESHOLD

@dataclass
class TemplateSpec:
    bank: str
    template: str
    version: str
    headers: List[str]
    header_synonyms: List[str]
    keywords: List[str]

def _sim(a: str, b: str) -> float:
    return SequenceMatcher(None, (a or "").lower(), (b or "").lower()).ratio()

def _load_all() -> List[TemplateSpec]:
    specs: List[TemplateSpec] = []
    if not REGISTRY_DIR.exists():
        return specs
    for y in list(REGISTRY_DIR.rglob("*.yaml")) + list(REGISTRY_DIR.rglob("*.yml")):
        with y.open("r", encoding="utf-8") as f:
            d = yaml.safe_load(f) or {}
        specs.append(TemplateSpec(
            bank=d.get("bank",""),
            template=d.get("template",""),
            version=str(d.get("version","1.0.0")),
            headers=list(d.get("headers") or []),
            header_synonyms=list(d.get("header_synonyms") or []),
            keywords=list(d.get("detect", {}).get("keywords") or [])
        ))
    return specs

def match(detected_headers: List[str], report_text: str) -> Tuple[Optional[str], Optional[str], float, List[str]]:
    specs = _load_all()
    best = (None, None, 0.0, [])
    for s in specs:
        direct = sum(1 for h in detected_headers if h in s.headers) / max(1, len(s.headers))
        syn_score = 0.0
        for h in detected_headers:
            syn_score = max(syn_score, max((_sim(h, syn) for syn in s.header_synonyms), default=0.0))
        fuzzy = 0.0
        if s.headers:
            fuzzy = sum(max((_sim(h, e) for h in detected_headers), default=0.0) for e in s.headers) / len(s.headers)
        hint = 0.0
        if s.keywords:
            hint = max((1.0 if re.search(re.escape(k), report_text or "", re.I) else 0.0) for k in s.keywords)
            hint *= 0.1
        score = 0.5*direct + 0.3*fuzzy + 0.1*syn_score + hint
        if score > best[2]:
            best = (s.bank, s.template, score, [f"direct={direct:.2f}", f"fuzzy={fuzzy:.2f}", f"syn={syn_score:.2f}", f"hint={hint:.2f}"])
    return best

def register_from_candidate(candidate_yaml: str, bank: str, template: str, version: str="1.0.0") -> Path:
    p = Path(candidate_yaml)
    data = yaml.safe_load(p.read_text(encoding="utf-8")) or {}
    headers = list(data.get("header_fields") or [])
    synonyms = sorted(set(headers + ["日付","取引日","ご利用日","摘要","内容","出金","お支払","入金","お預り","差引残高","残高"]))
    spec = {
        "bank": bank,
        "template": template,
        "version": version,
        "headers": headers,
        "header_synonyms": synonyms,
        "detect": {"keywords": [bank, template]}
    }
    outdir = REGISTRY_DIR / bank
    outdir.mkdir(parents=True, exist_ok=True)
    out = outdir / f"{template}.yaml"
    with out.open("w", encoding="utf-8") as f:
        yaml.safe_dump(spec, f, allow_unicode=True, sort_keys=False)
    return out
