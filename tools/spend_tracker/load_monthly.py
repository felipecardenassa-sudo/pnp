"""Load the platform exports we already have (campaign x month, Jan-Sep 2026) into normalised rows.
Rows: dict(date, channel, campaign, spend, impr, clicks, conv). Spend is in the billing currency."""
import csv, datetime, openpyxl

UP = '/root/.claude/uploads/f32fd57a-14dc-59dc-8790-b3491ef94cce/'
MONTHS = {m: i + 1 for i, m in enumerate(["January", "February", "March", "April", "May", "June", "July",
                                           "August", "September", "October", "November", "December"])}


def num(x):
    try:
        return float(str(x).replace(',', '')) if x not in (None, '', '--') else 0.0
    except ValueError:
        return 0.0


def meta_monthly():
    rows = []
    for x in csv.DictReader(open(UP + '47165e4d-Plug-and-Play-Tech-Center-Dollars-Campaigns-1-Jan-2026-30-Sep-2026.csv', encoding='utf-8-sig')):
        if not x['Campaign name']:
            continue
        rows.append(dict(date=datetime.date.fromisoformat(x['Reporting starts']), channel='Meta', campaign=x['Campaign name'].strip(),
                         spend=num(x['Amount spent (USD)']), impr=num(x['Impressions']), clicks=num(x['Unique link clicks']),
                         conv=num(x['Website registrations completed'])))
    return rows


def google_monthly():
    ws = openpyxl.load_workbook(UP + 'a648cefc-Campaign_report.xlsx', data_only=True).active
    it = list(ws.iter_rows(values_only=True))
    h = {k: i for i, k in enumerate(it[2])}
    rows = []
    for r in it[3:]:
        if not r[0] or r[0] == '--' or not r[h['Campaign']] or str(r[h['Campaign status']]).startswith('Total'):
            continue
        mname, yr = r[0].split()
        rows.append(dict(date=datetime.date(int(yr), MONTHS[mname], 1), channel='Google Ads', campaign=r[h['Campaign']].strip(),
                         spend=num(r[h['Cost']]), impr=num(r[h['Impr.']]), clicks=num(r[h['Clicks']]), conv=num(r[h['Conversions']])))
    return rows


def chatgpt():
    rows = []
    for x in csv.DictReader(open(UP + '5640ac9b-campaigns_1.csv', encoding='utf-8-sig')):
        if num(x['spend']) > 0:
            rows.append(dict(date=datetime.date.fromisoformat(x['start_time'][:10]), channel='ChatGPT Ads', campaign=x['campaign_name'].strip(),
                             spend=num(x['spend']), impr=num(x['impressions']), clicks=num(x['clicks']), conv=num(x['conversions'])))
    return rows


def all_rows():
    return [r for r in meta_monthly() + google_monthly() + chatgpt() if r['spend'] or r['impr'] or r['clicks'] or r['conv']]


if __name__ == '__main__':
    rs = all_rows()
    import collections
    t = collections.defaultdict(float)
    for r in rs:
        t[r['channel']] += r['spend']
    print(len(rs), {k: round(v, 2) for k, v in t.items()})
