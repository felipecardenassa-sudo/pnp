"""Load the daily platform exports exactly as exported (so the data tabs look like a straight paste).

Meta: Ads Manager CSV, campaign x day ('Reporting starts' = 'Reporting ends' = the day), 19 columns.
Google Ads: report editor download (UTF-16, tab-separated): two title lines, then Campaign, Day, Currency code, Cost, Impr., Clicks, Conversions.
Returns raw rows per tab (lists in export column order, all-zero rows dropped) and normalised rows for ordering lists.
"""
import csv, io, datetime

META_COLS = ["Reporting starts", "Reporting ends", "Campaign name", "Campaign delivery", "Attribution setting", "Results",
             "Result indicator", "Cost per results", "Ad set budget", "Ad set budget type", "Amount spent (USD)", "Impressions",
             "Reach", "Frequency", "Unique link clicks", "Website registrations completed", "Ends", "Results (initial)",
             "Results (initial) indicator"]
GOOGLE_COLS = ["Campaign", "Day", "Currency code", "Cost", "Impr.", "Clicks", "Conversions"]


def _num(x):
    if x is None:
        return None
    s = str(x).replace(",", "").strip()
    if s in ("", "--"):
        return None
    try:
        f = float(s)
        return int(f) if f.is_integer() and "." not in s else f
    except ValueError:
        return x


def _date(s):
    return datetime.date.fromisoformat(str(s).strip()[:10])


def meta(path):
    rd = list(csv.reader(open(path, encoding="utf-8-sig")))
    hdr = rd[0]
    assert hdr == META_COLS, f"Meta columns changed: {hdr}"
    raw, norm = [], []
    for r in rd[1:]:
        if not r or not r[2]:
            continue
        spend, impr = _num(r[10]) or 0, _num(r[11]) or 0
        if not spend and not impr:
            continue
        row = []
        for i, v in enumerate(r):
            if i in (0, 1):
                row.append(_date(v))
            elif i in (5, 7, 8, 10, 11, 12, 13, 14, 15, 17):
                row.append(_num(v))
            else:
                row.append(v if v != "" else None)
        raw.append(row)
        norm.append(dict(date=row[0], channel="Meta", campaign=r[2].strip(), spend=float(spend), impr=float(impr),
                         clicks=float(_num(r[14]) or 0), conv=float(_num(r[15]) or 0), rowtype=""))
    raw.sort(key=lambda x: (x[0], x[2]))
    return raw, norm


def google(path):
    txt = open(path, "rb").read().decode("utf-16")
    lines = txt.splitlines()
    i = next(k for k, l in enumerate(lines) if l.startswith("Campaign\t"))
    rd = list(csv.reader(io.StringIO("\n".join(lines[i:])), delimiter="\t"))
    assert rd[0] == GOOGLE_COLS, f"Google columns changed: {rd[0]}"
    raw, norm = [], []
    for r in rd[1:]:
        if len(r) < 7 or not r[1][:4].isdigit():
            continue
        cost, impr = _num(r[3]) or 0, _num(r[4]) or 0
        clicks, conv = _num(r[5]) or 0, _num(r[6]) or 0
        if not cost and not impr and not clicks and not conv:
            continue
        row = [r[0].strip(), _date(r[1]), r[2], float(cost), impr, clicks, conv]
        raw.append(row)
        norm.append(dict(date=row[1], channel="Google Ads", campaign=row[0], spend=float(cost), impr=float(impr),
                         clicks=float(clicks), conv=float(conv), rowtype=""))
    raw.sort(key=lambda x: (x[1], x[0]))
    return raw, norm
