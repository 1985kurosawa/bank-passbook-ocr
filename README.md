# 銀行通帳OCR（楽デジ互換 方針）
- 目的：通帳PDF → データ抽出 → Excel出力（未知テンプレは候補YAML保存）
- まずは動かす：`pip install -r requirements.txt` → `python3 main.py --dry-run`
- 詳細は /src を参照。閾値は `src/config.py`。
