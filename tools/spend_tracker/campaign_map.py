"""Campaign -> market, region, type. Rules read the location code in the campaign name ("Geo:XX" or a prefix)."""
import re

# location code (as written in campaign names) -> (market, region)
GEO = {
    'EMEA': ('EMEA – multi-country', 'EMEA'), 'GLOBAL EMEA': ('EMEA – multi-country', 'EMEA'),
    'WESTERN-EUROPE': ('Western Europe – multi-country', 'EMEA'),
    'MIDDLE-EAST': ('Middle East', 'EMEA'), 'SA': ('Middle East', 'EMEA'),
    'UK': ('UK', 'EMEA'), 'FR': ('France', 'EMEA'), 'IT': ('Italy', 'EMEA'),
    'US': ('US – national', 'Americas'), 'GLOBAL US': ('US – national', 'Americas'),
    'USCA': ('US & Canada', 'Americas'), 'NA': ('US & Canada', 'Americas'),
    'CALIFORNIA': ('California', 'Americas'), 'US-CALIFORNIA': ('California', 'Americas'), 'US-CA': ('California', 'Americas'),
    'US-SV': ('California', 'Americas'),
    'US-EASTCOAST': ('US East Coast', 'Americas'), 'US-EAST-COAST': ('US East Coast', 'Americas'),
    'US-MIDDLE-SOUTH': ('US South & Central', 'Americas'), 'US-SOUTH-CENTRAL': ('US South & Central', 'Americas'),
    'NEW YORK': ('New York', 'Americas'), 'NEW JERSEY': ('New Jersey', 'Americas'), 'FLORIDA': ('Florida', 'Americas'),
    'FL': ('Florida', 'Americas'), 'TEXAS': ('Texas', 'Americas'), 'TX': ('Texas', 'Americas'), 'ARIZONA': ('Arizona', 'Americas'),
    'WW': ('Worldwide', 'Global'), 'ALL': ('Worldwide', 'Global'), 'US-UK-FR-IT': ('Worldwide', 'Global'),
}
# campaigns whose location is not written as a code
OVERRIDE = {
    'CFA | Amazon US batch 1': ('US – national', 'Americas'),
    'YT | PSS | US | Pepsi Campaign': ('US – national', 'Americas'),
    'Test 1': ('Not specified', 'Not specified'),
}


def location(name):
    if name in OVERRIDE:
        return OVERRIDE[name]
    m = re.match(r'Geo:([^_]+)', name)
    code = m.group(1) if m else re.split(r'[_|]', name)[0].strip()
    if code.upper().startswith('PNP'):
        code = name.split('_')[1]
    return GEO.get(code.upper(), ('Not specified', 'Not specified'))


def ctype(channel, name):
    n = name.lower()
    if channel == 'Meta':
        if 'retargeting' in n:
            return 'Meta – lead ads, retargeting'
        if 'objective:lead' in n:
            return 'Meta – lead ads, prospecting'
        if 'traffic' in n or 'alibaba' in n:
            return 'Meta – traffic'
        return 'Meta – other'
    if channel == 'Google Ads':
        if 'pmax' in n:
            return 'Google – Performance Max'
        if 'demandgen' in n or n.startswith(('global', 'yt |')) or 'universities' in n:
            return 'Google – Demand Gen / YouTube reach'
        if 'youtube' in n:
            return 'Google – YouTube video'
        if 'brand' in n and 'non-brand' not in n:
            return 'Google – Search, brand'
        if 'coworking' in n:
            return 'Google – Search, coworking'
        if 'search' in n:
            return 'Google – Search, non-brand'
        return 'Google – other'
    if channel == 'ChatGPT Ads':
        return 'ChatGPT – test'
    return channel + ' – other'
