import argparse
from src.processor import process_pdf

def parse_args():
    p = argparse.ArgumentParser()
    p.add_argument("--dry-run", action="store_true")
    p.add_argument("--customer", default="Sample")
    p.add_argument("--workers", type=int, default=1)
    p.add_argument("--log-level", default="INFO")
    return p.parse_args()

def main():
    args = parse_args()
    pdf_path = "input/sample.pdf"
    out_xlsx = "output/sample.xlsx"
    res = process_pdf(pdf_path, out_xlsx, dry_run=args.dry_run)
    print("RESULT:", res)

if __name__ == "__main__":
    main()
