#!/usr/bin/env python3
"""Numbered contact sheet of every Commons candidate considered, grouped by search category."""
import json, html

m = json.load(open('manifest.json'))
picked = {4, 110, 39, 63, 188, 53, 76, 89, 100, 189, 190, 191}

by_cat = {}
for x in m:
    by_cat.setdefault(x['cat'], []).append(x)

sections = []
for cat, items in by_cat.items():
    cards = ''
    for x in items:
        star = ' class="pick"' if x['n'] in picked else ''
        badge = '<span class="badge">SELECTED</span>' if x['n'] in picked else ''
        cards += f'''<figure{star}><img src="{x['file']}" loading="lazy">
<figcaption><b>#{x['n']}</b> {badge}<br>{html.escape(x['title'])}<br><i>{html.escape(x['lic'])}</i></figcaption></figure>'''
    sections.append(f'<section><h2>{html.escape(cat)}</h2><div class="grid">{cards}</div></section>')

page = f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><title>Contact sheet — tokyo-liberta-day</title>
<style>
body{{font-family:-apple-system,sans-serif;background:#faf8f2;margin:0;padding:24px;color:#111}}
h1{{margin:0 0 4px}} .sub{{color:#666;margin:0 0 24px;font-size:14px}}
h2{{font-size:14px;text-transform:uppercase;letter-spacing:.08em;color:#1a5c3a;border-top:1px solid #eae4d6;padding-top:18px;margin-top:28px}}
.grid{{display:grid;grid-template-columns:repeat(auto-fill,minmax(160px,1fr));gap:12px}}
figure{{margin:0;background:#fff;border:1px solid #eae4d6;border-radius:8px;overflow:hidden}}
figure.pick{{border:2px solid #1a5c3a;box-shadow:0 4px 14px rgba(26,92,58,.25)}}
figure img{{display:block;width:100%;aspect-ratio:4/3;object-fit:cover;background:#eee}}
figcaption{{padding:6px 8px;font-size:11px;line-height:1.4;color:#444}}
figcaption b{{color:#111}}
.badge{{background:#1a5c3a;color:#fff;font-size:9px;font-weight:700;letter-spacing:.06em;padding:1px 5px;border-radius:3px}}
</style></head><body>
<h1>Contact sheet — tokyo-liberta-day</h1>
<p class="sub">Every Wikimedia Commons candidate pulled for this page, by search category. Green border + SELECTED badge = used in the built page. Swap by editing photos.json.</p>
{''.join(sections)}
</body></html>'''
open('contact-sheet.html', 'w').write(page)
print('written contact-sheet.html', len(page))
