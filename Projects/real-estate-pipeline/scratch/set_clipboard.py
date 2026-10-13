import win32clipboard
import win32con
import csv

csv_path = r"c:\Users\crypt\OneDrive\Desktop\Real-Estate-Lead-Gen\Traceflow_15_Qualified_SME_Prospects.csv"

rows = []
with open(csv_path, 'r', encoding='utf-8') as f:
    reader = csv.reader(f)
    for r in reader:
        # replace internal newlines in cells with space or slash so TSV row stays single line
        clean_row = [c.replace('\r\n', ' | ').replace('\n', ' | ').replace('\t', ' ') for c in r]
        rows.append('\t'.join(clean_row))

tsv_text = '\r\n'.join(rows)

win32clipboard.OpenClipboard()
win32clipboard.EmptyClipboard()
win32clipboard.SetClipboardData(win32con.CF_UNICODETEXT, tsv_text)
win32clipboard.CloseClipboard()

print(f"SUCCESS: Loaded {len(rows)} rows (headers + 15 records) onto Windows Clipboard!")
