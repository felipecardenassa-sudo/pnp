"""Weekly agency figures (as written in Notion, via the Claude in Chrome extraction) + flags + notes."""
import json, re, datetime, os
HERE = os.path.dirname(os.path.abspath(__file__))
rows = json.load(open(os.path.join(HERE, 'agency_rows.json'), encoding='utf-8'))
notes = json.load(open(os.path.join(HERE, 'agency_notes.json'), encoding='utf-8'))
for k in notes:
    notes[k] = notes[k].replace('PnP Paid Media – Agency Weekly Reports Extraction (Jan–Oct 2026)', '').strip()


def num(s):
    s = (s or '').replace('$', '').replace('€', '').replace(',', '').strip()
    m = re.match(r'^-?\d+(\.\d+)?', s)
    return float(m.group(0)) if m else None


def clean(s):
    return re.sub(r'\s+', ' ', (s or '').replace('\x0c', ' ').replace('PnP Paid Media – Agency Weekly Reports Extraction (Jan–Oct 2026)', '')).strip()


FLAGS = {
    '2026-02-09': 'Meta spend only given as "$7k" in the text.',
    '2026-03-02': 'Own report has no spend; figures as restated in the W/C 23 Mar report.',
    '2026-03-09': 'Own report has no spend; figures as restated in the W/C 23 Mar report.',
    '2026-03-16': 'Own report has no spend. Google restated twice: $2,696.09 / 25 leads (W/C 23 Mar report) and $4,681.38 / 50.57 (W/C 6 Apr report).',
    '2026-04-06': 'Google looks doubled: the W/C 13 Apr report shows $1,923.09 for this week.',
    '2026-04-20': 'Report is labelled 21 Apr (a Tuesday); exact window unclear.',
    '2026-05-11': 'Google spend, impressions and clicks look doubled (about 2× what later reports show). No currency symbol shown.',
    '2026-05-25': 'Google spend, impressions and clicks look doubled (about 2× what later reports show).',
    '2026-07-06': 'Google split in the report: Search/Other $1,985.63 + YouTube $517.43.',
    '2026-07-20': 'Report says its figures are USD converted from EUR at ≈1.14. Welcome event not recording: leads unreliable.',
    '2026-07-27': 'Google figure restated in later reports ($2,951.33 / $2,951).',
    '2026-08-10': 'Google figure restated in a later report ($2,151.76).',
    '2026-09-07': 'Meta figure excludes FR_Alibaba (run by PnP\'s internal team).',
    '2026-09-14': 'Meta excludes FR_Alibaba. Later reports show the Google figure as €1,907.',
    '2026-09-21': 'Meta excludes FR_Alibaba. Google now explicitly in € (account currency).',
    '2026-09-28': 'Meta excludes FR_Alibaba.',
    '2026-10-05': 'Meta excludes FR_Alibaba.',
}
CHART_ONLY = {'2025-12-29', '2026-01-05', '2026-01-12', '2026-01-19'}


def pick(week, prefix, prefer_restated=False):
    if week == '2026-04-20':
        week = '2026-04-21'
    own = [r for r in rows if r['week_start'] == week and clean(r['channel']).startswith(prefix)
           and r['period_type'].startswith('weekly') and 'restated' not in r['period_type'] and 'chart' not in r['period_type']
           and 'EMEA' not in r['channel'] and 'USCA' not in r['channel'] and 'HubSpot' not in r['channel']
           and 'total (summary' not in r['channel']]
    rest = [r for r in rows if r['week_start'] == week and clean(r['channel']).startswith(prefix) and 'restated in W/C 23/03' in r['period_type']]
    if prefer_restated and rest:
        return rest
    return own


def weeks():
    out = []
    d = datetime.date(2025, 12, 29)
    while d <= datetime.date(2026, 10, 5):
        k = d.isoformat()
        restated = k in ('2026-03-02', '2026-03-09', '2026-03-16')
        meta = pick(k, 'Meta', restated)
        goog = pick(k, 'Google Ads', restated)
        w = dict(start=d, end=d + datetime.timedelta(days=6), notes=notes.get(k) or notes.get('2026-04-21' if k == '2026-04-20' else ''),
                 flags=FLAGS.get(k, ''))
        if k in CHART_ONLY:
            w['flags'] = 'Numbers only in chart images (CPL readable, spend not).'
        if meta:
            r = meta[0]
            w.update(meta_spend=7000.0 if clean(r['spend']) == '$7k' else num(r['spend']), meta_spend_txt=clean(r['spend']), meta_leads=num(r['leads']),
                     meta_def=clean(r['lead_metric_name']), meta_cpl=clean(r['cpl']), meta_channel=clean(r['channel']))
        if goog:
            if k == '2026-07-06':
                tot = sum(num(r['spend']) or 0 for r in goog if 'Search/Other' in r['channel'] or 'YouTube' in r['channel'])
                w.update(google_spend=round(tot, 2), google_spend_txt='$1,985.63 + $517.43', google_cur='$',
                         google_leads=15.0, google_def='Leads', google_cpl='$166.87 (summary text)')
            else:
                r = goog[0]
                cur = clean(r['currency'])
                cur = '$' if cur.startswith('$') else ('€' if cur.startswith('€') else ('none shown' if 'none' in cur else cur))
                w.update(google_spend=num(r['spend']), google_spend_txt=clean(r['spend']), google_cur=cur,
                         google_leads=num(r['leads']), google_def=clean(r['lead_metric_name']), google_cpl=clean(r['cpl']))
        out.append(w)
        d += datetime.timedelta(days=7)
    return out


if __name__ == '__main__':
    for w in weeks():
        print(w['start'], '| M', w.get('meta_spend'), w.get('meta_leads'), (w.get('meta_def') or '')[:22], '| G', w.get('google_spend'), w.get('google_cur'), w.get('google_leads'), '|', w['flags'][:50])
