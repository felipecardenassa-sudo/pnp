"""Read a platform export the way Google Sheets shows it after File > Import (numbers and dates converted,
nothing dropped, nothing re-ordered), so the export tabs in the workbook look exactly like a real weekly import.

Meta Ads Manager: 'Export table data' CSV (UTF-8, comma separated).
Google Ads report editor: '.csv' (UTF-8) or 'Excel .csv' (UTF-16, tab separated), with its title lines on top.
"""
import csv, io, re, datetime

_DATE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
_NUM = re.compile(r"^-?\d{1,3}(,\d{3})+(\.\d+)?$|^-?\d+(\.\d+)?$")


def _cell(v):
    s = v.strip()
    if s == "":
        return None
    if _DATE.match(s):
        return datetime.date.fromisoformat(s)
    if _NUM.match(s):
        f = float(s.replace(",", ""))
        return int(f) if f.is_integer() and "." not in s else f
    return s


def read(path):
    raw = open(path, "rb").read()
    if raw[:2] in (b"\xff\xfe", b"\xfe\xff"):
        txt = raw.decode("utf-16")
    else:
        txt = raw.decode("utf-8-sig")
    lines = txt.splitlines()
    head = "\n".join(lines[:10])
    delim = "\t" if head.count("\t") > head.count(",") else ","
    rows = [[_cell(v) for v in r] for r in csv.reader(io.StringIO("\n".join(lines)), delimiter=delim)]
    while rows and not any(v is not None for v in rows[-1]):
        rows.pop()
    return rows
