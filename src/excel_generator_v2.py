from openpyxl import Workbook
def generate_simple_to_file(rows, headers, outfile: str):
    from pathlib import Path
    Path(outfile).parent.mkdir(parents=True, exist_ok=True)
    wb = Workbook()
    ws = wb.active
    ws.title = "明細"
    ws.append(headers)
    for r in rows:
        ws.append([r.get(h, "") for h in headers])
    wb.save(outfile)
    return outfile
