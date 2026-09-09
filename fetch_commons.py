#!/usr/bin/env python3
"""Search Wikimedia Commons for candidate photos per subject, cache to commons.json."""
import json, urllib.request, urllib.parse, re, time

API = 'https://commons.wikimedia.org/w/api.php'

def search(term, limit=8):
    q = {
        'action': 'query', 'format': 'json', 'generator': 'search',
        'gsrsearch': term, 'gsrnamespace': 6, 'gsrlimit': limit,
        'prop': 'imageinfo', 'iiprop': 'url|size|extmetadata',
        'iiurlwidth': 960,
    }
    url = API + '?' + urllib.parse.urlencode(q)
    req = urllib.request.Request(url, headers={'User-Agent': 'tokyo-liberta-day/1.0 (research)'})
    with urllib.request.urlopen(req, timeout=20) as r:
        data = json.load(r)
    out = []
    pages = data.get('query', {}).get('pages', {})
    for p in pages.values():
        ii = (p.get('imageinfo') or [None])[0]
        if not ii:
            continue
        meta = ii.get('extmetadata', {})
        lic = meta.get('LicenseShortName', {}).get('value', '?')
        by = meta.get('Artist', {}).get('value', '')
        by = re.sub('<[^>]+>', '', by)[:120]
        thumb = ii.get('thumburl') or ii.get('url')
        out.append({
            't': p.get('title'), 'thumb': thumb,
            'w': ii.get('thumbwidth', ii.get('width')), 'h': ii.get('thumbheight', ii.get('height')),
            'lic': lic, 'by': by,
        })
    return out

TERMS = {
    'tokyo_station_platform': 'Tokyo Station Shinkansen platform',
    'ginza_street': 'Ginza street Tokyo',
    'printing_workshop': 'letterpress printing workshop',
    'silkscreen_printing': 'silkscreen printing workshop',
    'kappabashi': 'Kappabashi Tokyo',
    'kappabashi_knife': 'Kappabashi knife shop',
    'food_samples': 'plastic food samples Japan',
    'yanaka_ginza': 'Yanaka Ginza',
    'yanaka_street': 'Yanaka Tokyo',
    'sunshine_city': 'Sunshine City Ikebukuro',
    'soba_noodles': 'zaru soba',
    'unagi_don': 'unadon eel rice bowl',
    'omurice': 'omurice Japan',
}

if __name__ == '__main__':
    out = {}
    for key, term in TERMS.items():
        try:
            out[key] = search(term)
            print(key, len(out[key]))
        except Exception as e:
            print(key, 'FAILED', e)
            out[key] = []
        time.sleep(0.3)
    json.dump(out, open('commons.json', 'w'), ensure_ascii=False, indent=1)
    print('written commons.json')
