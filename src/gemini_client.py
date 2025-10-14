
import os, json, tempfile
from typing import Optional
import google.generativeai as genai

MODEL_NAME = "gemini-1.5-pro"

_STUB = {
    "data": [{"日付":"2025-01-01","摘要":"テスト","出金":0,"入金":1000,"残高":1000}],
    "report": "stub report",
    "headers": ["日付","摘要","出金","入金","残高"],
    "row_confidences": [0.95],
}

PROMPT = """あなたは日本の銀行通帳明細の抽出器です。PDF/画像から明細表だけを読み取り、
次のJSONスキーマで厳密に出力します。説明文は返さず、JSONのみ返してください。

- headers: 明細表の列名（例: ["日付","摘要","出金","入金","残高"]）
- data: 各行のオブジェクト配列。金額は数値、日付は YYYY-MM-DD。欠損は null。
- report: 変換・判断の要点（マッピング根拠/曖昧箇所/補正の説明など）
- row_confidences: 各行の信頼度 0.0–1.0（長さは data と同じ）

同義語例: 日付=取引日/ご利用日, 摘要=内容/取引内容, 出金=出金額/お支払, 入金=入金額/お預り, 残高=差引残高/残高
厳守: 出金/入金/残高は数値（記号除去）。空は null。response は JSON のみ。
"""

SCHEMA = {
    "type": "object",
    "properties": {
        "headers": {"type": "array", "items": {"type": "string"}},
        "data":    {"type": "array", "items": {"type": "object"}},
        "report":  {"type": "string"},
        "row_confidences": {"type": "array", "items": {"type": "number"}}
    },
    "required": ["headers","data","report","row_confidences"],
    "additionalProperties": True
}

def _ensure_defaults(payload: dict) -> dict:
    headers = payload.get("headers") or []
    rows = payload.get("data") or []
    confs = payload.get("row_confidences") or []
    if not headers and rows:
        headers = list(rows[0].keys())
    if len(confs) != len(rows):
        confs = [0.9]*len(rows)
    return {
        "headers": headers,
        "data": rows,
        "report": payload.get("report", ""),
        "row_confidences": confs
    }

def extract_table_with_report(image_or_pdf_bytes: bytes, template_hint: Optional[str]=None) -> dict:
    # ドライラン（空バイト）はスタブ返却
    if not image_or_pdf_bytes:
        return dict(_STUB)

    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise RuntimeError("環境変数 GEMINI_API_KEY が未設定です。")

    genai.configure(api_key=api_key)
    model = genai.GenerativeModel(MODEL_NAME)

    hint = f"\\nテンプレートヒント: {template_hint}\\n" if template_hint else ""
    full_prompt = PROMPT + hint

    with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as f:
        f.write(image_or_pdf_bytes)
        f.flush()
        temp_path = f.name

    file = genai.upload_file(path=temp_path)
    try:
        resp = model.generate_content(
            [full_prompt, file],
            generation_config={
                "temperature": 0.2,
                "response_mime_type": "application/json",
                "response_schema": SCHEMA,
            },
        )
        text = getattr(resp, "text", "") or ""
        payload = json.loads(text) if text.strip() else {}
        return _ensure_defaults(payload)
    finally:
        try:
            genai.delete_file(file.name)
        except Exception:
            pass
        try:
            os.remove(temp_path)
        except Exception:
            pass
