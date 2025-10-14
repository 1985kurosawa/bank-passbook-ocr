def extract_table_with_report(image_or_pdf_bytes: bytes, template_hint: str | None = None) -> dict:
    return {
        "data": [{"日付":"2025-01-01","摘要":"テスト","出金":0,"入金":1000,"残高":1000}],
        "report": "stub report",
        "headers": ["日付","摘要","出金","入金","残高"],
        "row_confidences": [0.95]
    }
