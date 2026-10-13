import re, csv, io, json, sys
raw = open('raw.txt', encoding='utf-8').read()
sec = raw.split('\nweekly_by_channel\n', 1)[1].split('\nweekly_by_market\n', 1)[0]
lines = [l for l in sec.split('\n') if l.strip() and not l.startswith('PnP Paid Media – Agency') and not re.match(r'^Page \d+ of 42$', l)]
text = ' '.join(lines)
start = text.index('2025-12-29,')
recs = re.split(r' (?=\d{4}-\d{2}-\d{2},\d{4}-\d{2}-?\d{2},)', text[start:])
rows = []
for r in recs:
    try:
        f = next(csv.reader(io.StringIO(r)))
    except Exception as e:
        print('ERR', r[:80]); continue
    if len(f) < 17:
        print('SHORT', len(f), r[:120]); continue
    keys = ['week_start','week_end','period_type','channel','spend','currency','impressions','clicks','ctr','cpc','leads','lead_metric_name','cpl','mqls','sqls','budget_or_plan']
    d = dict(zip(keys, [x.strip() for x in f[:16]]))
    rows.append(d)
json.dump(rows, open('agency_rows.json','w'), indent=1, ensure_ascii=False)
print(len(rows), 'rows')
import collections
c = collections.Counter(r['channel'] for r in rows)
print(c.most_common())
