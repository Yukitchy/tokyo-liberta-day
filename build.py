#!/usr/bin/env python3
"""Brian & Dashiell (9/11) 到着日1本コースページ。 python3 build.py -> index.html"""
import json, html

# 写真は「ワクワク採点」で選ぶ。建物の外観でなく、そこで人が楽しんでいる絵を最優先。
# 採点と選定理由は photos.json の score / note、候補一覧は contact-sheet.html を見る。
PH = json.load(open('photos.json'))
gm = lambda q: 'https://www.google.com/maps/search/?api=1&query=' + q.replace(' ', '+')
def route_emb(stops):
    s = [x.replace(' ', '+') for x in stops]
    return 'https://maps.google.com/maps?saddr=' + s[0] + '&daddr=' + '+to:'.join(s[1:]) + '&output=embed'
def route_link(stops):
    s = [x.replace(' ', '+') for x in stops]
    return ('https://www.google.com/maps/dir/?api=1&origin=' + s[0] + '&destination=' + s[-1]
            + ('&waypoints=' + '%7C'.join(s[1:-1]) if len(s) > 2 else '') + '&travelmode=transit')

DAY = dict(
 kicker='Tokyo · Friday, September 11, 2026',
 title_pre='A day made ', title_nb='to order.',
 lead=("A full day in Tokyo, about six hours door to door: your Hikari gets in at Tokyo Station, then it's a print "
       "workshop in Ginza, the kitchenware wholesalers of Kappabashi, and the old backstreets of Yanesen. "
       "You're checked in at your hotel by 16:30, bags already there."),
 guide='Yuuki', time='10:42–16:30', group='Brian and Dashiell', route='Tokyo Station → your hotel',
 steps=[('9:41', 'Depart Shizuoka Station',
         'Hikari 640, ordinary car 13, seats 1D and 1E. About an hour to Tokyo.'),
        ('10:42', 'Arrive Tokyo Station',
         'I&rsquo;ll be waiting on the platform, right at the door closest to your seats. Message me on WhatsApp if '
         'anything changes.'),
        ('11:30', 'FLAT LABO, Ginza',
         'A showroom for museum-quality digital art printing: the craftsmanship and technology behind fine art prints, '
         'plus a live printing demonstration up close. 2-16-7 Ginza, Shochiku Building, Chuo-ku &middot; 03-6264-7718. '
         'About an hour, with me interpreting.'),
        ('Optional', 'Frames at K.Itoya',
         'If you want to see frames for the print before lunch, K.Itoya&rsquo;s frame corner is a 6-minute walk from FLAT '
         'LABO &mdash; about 1,500 frame samples and 500 mat samples, B1 floor. '
         f'<a href="{gm("Ito-ya K.Itoya Ginza 2-7-15")}" target="_blank" rel="noopener">Google Maps ↗</a>'),
        ('Midday', 'Lunch',
         'One of the five picks below, decided on the day.'),
        ('Afternoon', 'Kappabashi Kitchenware Street',
         'A shopping street for professional-grade kitchen tools and restaurant supplies &mdash; Japanese knives, ceramics, '
         'and the realistic food replicas restaurants use. Popular with chefs and food enthusiasts alike.'),
        ('Late afternoon', 'Yanesen',
         'Yanaka, Nezu and Sendagi: quiet lanes of old wooden houses, local shops and artisan boutiques, and Yanaka Ginza, '
         'lively with street food and small eateries. A glimpse of old Tokyo.'),
        ('16:30', 'Arrive Sunshine City Prince Hotel',
         'I&rsquo;ll help with check-in, and that&rsquo;s where the guided day ends. The suitcase sent ahead from Shizuoka '
         'will be waiting for you. Evening free, dinner on your own.')],
 stops=['Tokyo Station', 'Ginza 2-16-7 Tokyo', 'Kappabashi Dougu Street', 'Yanaka Ginza', 'Sunshine City Prince Hotel'],
 moves=('Tokyo Station &rarr; Ginza about 15 minutes by train, one IC card tap. Ginza &rarr; Kappabashi about 40 minutes by train. '
        'Kappabashi &rarr; Yanesen about 20 minutes by train. Yanesen &rarr; Sunshine City Prince Hotel about 30 minutes by train.'),
 food=[('Rengatei', 'Ginza · western food since 1895',
        'The Ginza restaurant that invented the pork cutlet and the rice omelette &mdash; Japan&rsquo;s own take on Western food, not the diner version you know.',
        'Rengatei Ginza Tokyo'),
       ('Ginza Tenkuni', 'Ginza · tempura since 1885',
        'Tendon, a tempura rice bowl fried to order, in a shop that has been doing exactly this since the Meiji era.',
        'Ginza Tenkuni Tempura'),
       ('Tsukiji Yamacho', 'Tsukiji · tamagoyaki since 1949',
        'A thick, sweet-savory rolled omelette grilled fresh and handed over on a stick &mdash; street food, not scrambled eggs.',
        'Tsukiji Yamacho Tamagoyaki'),
       ('Tsukiji Unagi Shokudo', 'Tsukiji · eel',
        'Freshwater eel, grilled over charcoal and glazed, served on rice &mdash; richer and smokier than anything called &ldquo;eel&rdquo; back home.',
        'Tsukiji Unagi Shokudo'),
       ('Uni LABO Marushu', 'Tsukiji · sea urchin',
        'A bowl piled high with uni over rice &mdash; more of it, and fresher, than sea urchin ever gets served in the US.',
        'Uni LABO Marushu Tsukiji')],
 costs=[('FLAT LABO additional work', 'JPY 65,780 (tax included)',
         'Paid on site by credit card via a payment link. Data preparation fee JPY 20,000 &times; 2, UV layered printing fee JPY 9,900 &times; 2.'),
        ('Lunch and dinner', 'On your own', ''),
        ('Same-day luggage delivery', 'Optional, paid on site', 'Worth it if you&rsquo;re carrying a lot.'),
        ('Local transport', 'Your own IC card', '')],
 good='Kappabashi and Yanesen are both made for browsing and street food — bring an appetite and a little cash for small shops.',
 mind='Tokyo is still warm in September, so bring water and comfortable walking shoes. Please send FLAT LABO your image files ahead of time for the live printing demonstration.',
 links=[('FLAT LABO (official)', 'https://flatlabo.com/'),
        ('Kappabashi Dougu Street (official)', 'https://www.kappabashi.or.jp/'),
        ('Yanaka Ginza (official)', 'https://www.yanakaginza.com/')],
)
DATE_LABEL = DAY['kicker'].split('· ')[1].rsplit(',', 1)[0]  # "Friday, September 11"

# Optional extra day, not part of Friday's plan — a private Akihabara anime tour, offered as a low-key add-on.
EXTRA = dict(
 items=["Built around whatever series you're into, not a fixed script",
        "The real streets a favorite scene was drawn from",
        "Floors for retro games, figures and doujin, with the culture explained along the way",
        "Secondhand shops for figures and games, where I can also tell you if a price is fair",
        "A route we work out together once I know what you love"],
 dashiell=("For Dashiell: <i>To Your Eternity</i>, <i>Ruri Rocks</i>, <i>The Girl From the Other Side</i> and "
           "<i>Frieren</i> share a certain feel &mdash; quiet, strange, beautifully drawn, more about the world than the fight. "
           "Akihabara has secondhand shops trading in old manga, art books and cel art, worth a look for series like these. "
           "And since <i>Ruri Rocks</i> is about minerals, Tokyo Science, a fossil and mineral specimen shop on the 1st floor "
           "of Kinokuniya&rsquo;s Shinjuku main store &mdash; ammonites, trilobites, mineral clusters, open daily &mdash; is "
           "worth a stop if that appeals."),
 photos=[('img/akiba-figure-hunt.jpg', 'A teenager picking out a figure from a secondhand shop shelf'),
         ('img/akiba-street-friends.jpg', 'Three friends laughing together on an Akihabara street'),
         ('img/akiba-tote.jpg', 'A guest showing off a tote bag she just bought'),
         ('img/akiba-cheers.jpg', 'Two guests raising a toast at a table'),
         ('img/akiba-cafe.jpg', 'A maid cafe drink being poured at the table')],
 ig='https://www.instagram.com/yukianimesensei/',
 ig_handle='@yukianimesensei', ig_name='Yuuki_AnimeSensei_JAPANTourguide',
 ig_posts='934 posts', ig_followers='7,188 followers',
 ig_bio='Akihabara anime tour guide | 2,000+ guests',
 ig_grid=[f'img/ig/{n:02d}.jpg' for n in range(1, 10)],
)

def eats_block(food, food_photos):
    return ''.join(
        f'<a class="eat" href="{gm(q)}" target="_blank" rel="noopener">'
        f'<img src="{im["thumb"]}" alt="{html.escape(im["title"])}" loading="lazy">'
        f'<span class="eb"><strong>{html.escape(n)}</strong><em>{html.escape(a)}</em><span>{d}</span>'
        f'<i>Open in Google Maps ↗</i></span></a>'
        for (n, a, d, q), im in zip(food, food_photos))

def links_block(links):
    return ' '.join(f'<a href="{u}" target="_blank" rel="noopener">{html.escape(t)} ↗</a>' for t, u in links)

def costs_block(costs):
    return ''.join(
        f'<li><b>{html.escape(label)}</b><strong>{html.escape(amount)}</strong>' + (f'<span>{detail}</span>' if detail else '') + '</li>'
        for label, amount, detail in costs)

NAV_CSS = """
[id]{scroll-margin-top:64px}
.topbar{position:sticky;top:0;z-index:20;background:rgba(255,253,246,.9);backdrop-filter:blur(8px);-webkit-backdrop-filter:blur(8px);border-bottom:1px solid var(--line)}
.tb-in{display:flex;align-items:center;justify-content:space-between;padding:10px 20px}
.tb-id{display:flex;align-items:center;gap:10px;min-width:0}
.av{width:32px;height:32px;border-radius:50%;background:var(--acc);color:#fff;display:flex;align-items:center;justify-content:center;font-weight:700;font-size:13px;flex:none}
.tb-id b{display:block;font-size:13.5px;font-weight:600;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
.tb-id b em{font-style:normal;font-weight:400;color:var(--mute)}
.tb-id .tbdate{display:block;font-size:11px;color:var(--mute)}
.menu{position:relative;flex:none;margin-left:12px}
.menu summary{list-style:none;cursor:pointer;font-size:18px;line-height:1;padding:6px 10px;border-radius:6px;color:var(--ink)}
.menu summary::-webkit-details-marker{display:none}
.menu[open] summary{background:var(--line)}
.menu-list{position:absolute;right:0;top:calc(100% + 8px);background:var(--card);border:1px solid var(--line);border-radius:8px;box-shadow:0 8px 24px rgba(0,0,0,.1);padding:6px;display:flex;flex-direction:column;min-width:190px}
.menu-list a{padding:9px 12px;border-radius:6px;font-size:14px;color:var(--ink);text-decoration:none}
.menu-list a:hover{background:var(--bg)}
.fold{border:1px solid var(--line);border-radius:8px;background:var(--card);margin:0 0 14px}
.fold>summary{cursor:pointer;list-style:none;display:flex;align-items:center;justify-content:space-between;gap:10px;padding:14px 18px;font-weight:600;font-size:15px}
.fold>summary::-webkit-details-marker{display:none}
.fold>summary::after{content:"+";font-weight:400;font-size:19px;color:var(--mute)}
.fold[open]>summary{border-bottom:1px solid var(--line)}
.fold[open]>summary::after{content:"\\2212"}
.fold-body{padding:18px}
.fold-body>.photos{margin-bottom:14px}
"""
CHAT_CSS = """
.thread{max-width:640px;margin:0 auto;padding:18px 18px 30px}
.row{display:flex;margin-bottom:12px}
.row.me{justify-content:flex-end}
.bub{max-width:82%;padding:11px 14px;border-radius:16px;font-size:15px}
.row:not(.me) .bub{background:var(--card);border:1px solid var(--line);border-bottom-left-radius:4px}
.row.me .bub{background:var(--acc);color:#fff;border-bottom-right-radius:4px}
.bub a{color:inherit}
.bub .tm{display:block;font-size:10.5px;color:var(--mute);margin-top:6px}
.row.me .bub .tm{color:#cfe6da}
.bub img.att{display:block;width:100%;max-width:260px;border-radius:10px;margin-top:8px;object-fit:cover;aspect-ratio:4/3}
.bub .mt{display:block;font-size:11px;font-weight:700;letter-spacing:.07em;text-transform:uppercase;color:var(--acc);margin-bottom:3px}
.bub h4{margin:0 0 3px;font-size:16px;font-weight:700;letter-spacing:-.01em}
.bub.card{max-width:100%;padding:14px}
.facts{display:grid;grid-template-columns:auto 1fr;gap:4px 12px;margin:8px 0 0;padding:0;list-style:none;font-size:13.5px;color:var(--mute)}
.facts li{display:contents} .facts b{color:var(--ink);font-weight:600;white-space:nowrap}
.photos{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:8px;margin:10px 0 0}
.photos img{display:block;width:100%;aspect-ratio:4/3;object-fit:cover;border-radius:8px;background:#f0ebe0}
.mapbox{border-radius:8px;overflow:hidden;background:#f0ebe0;margin-top:6px} .mapbox iframe{display:block;width:100%;height:220px;border:0}
.moves{font-size:13.5px;color:var(--mute);margin:10px 0 0} .moves a{color:var(--ink);text-decoration:underline;text-underline-offset:3px}
.eats{display:flex;overflow-x:auto;gap:10px;margin-top:8px;padding-bottom:4px;scroll-snap-type:x mandatory;-webkit-overflow-scrolling:touch}
.eat{flex:0 0 78%;scroll-snap-align:start;display:flex;flex-direction:column;text-decoration:none;color:inherit;background:var(--bg);border:1px solid var(--line);border-radius:8px;overflow:hidden}
.eat>img{display:block;width:100%;aspect-ratio:16/9;object-fit:cover;background:#f0ebe0}
.eb{display:flex;flex-direction:column;flex:1;padding:12px 14px 14px}
.eat strong{display:block;font-weight:700;font-size:16.5px;line-height:1.2;letter-spacing:-.01em}
.eat em{display:block;font-style:normal;font-size:11px;color:var(--acc);font-weight:600;letter-spacing:.07em;text-transform:uppercase;margin:5px 0 8px}
.eb>span{display:block;font-size:13.5px;color:var(--mute)} .eat i{display:block;font-style:normal;font-size:12px;margin-top:auto;padding-top:9px;text-decoration:underline;text-underline-offset:3px}
.notes{display:flex;flex-direction:column;gap:10px;margin-top:8px;font-size:13.5px}
.notes p{margin:0;padding:12px 14px;background:var(--bg);border:1px solid var(--line);border-radius:8px}
.notes b{display:block;font-weight:600;margin-bottom:3px}
.costs{list-style:none;margin:8px 0 0;padding:0}
.costs li{padding:10px 0;border-bottom:1px solid var(--line)} .costs li:last-child{border-bottom:0}
.costs b{display:block;font-weight:600;font-size:14.5px} .costs strong{display:block;font-weight:700;font-size:14.5px;color:var(--acc)}
.costs span{display:block;color:var(--mute);font-size:13px;margin-top:2px}
.links a{color:var(--ink);text-decoration:underline;text-underline-offset:3px}
.igcard{display:block;background:var(--bg);border:1px solid var(--line);border-radius:8px;padding:14px;text-decoration:none;color:inherit;margin-top:4px;transition:border-color .15s ease}
.igcard:hover{border-color:var(--ink)}
.ighead{display:flex;align-items:center;gap:12px;margin-bottom:12px}
.igavatar{width:44px;height:44px;border-radius:50%;background:var(--card);border:1px solid var(--line);flex:none;display:flex;align-items:center;justify-content:center;font-weight:700;color:var(--acc);font-size:16px}
.ighandle{display:block;font-weight:700;font-size:14.5px}
.igname{display:block;font-size:12px;color:var(--mute)}
.igstats{display:flex;gap:14px;font-size:12.5px;color:var(--mute);margin-bottom:8px} .igstats b{color:var(--ink)}
.igbio{font-size:13px;color:var(--mute);margin:0 0 12px}
.iggrid{display:grid;grid-template-columns:repeat(3,1fr);gap:3px}
.iggrid img{display:block;width:100%;aspect-ratio:1/1;object-fit:cover;border-radius:3px;background:#f0ebe0}
.foot{max-width:640px;margin:0 auto;padding:16px 18px 0;font-size:12.5px;color:var(--mute);border-top:1px solid var(--line)}
.foot p{margin:0 0 6px}
.cred summary{cursor:pointer;font-size:12px;color:var(--mute);opacity:.75;list-style:none;display:inline-block;text-decoration:underline;text-underline-offset:3px}
.cred summary::-webkit-details-marker{display:none} .cred p{margin:8px 0 0;font-size:11.5px;line-height:1.6;opacity:.8}
.pinbar{position:fixed;left:0;right:0;bottom:0;z-index:20;background:rgba(255,253,246,.94);backdrop-filter:blur(8px);-webkit-backdrop-filter:blur(8px);border-top:1px solid var(--line);padding:9px 10px calc(12px + env(safe-area-inset-bottom));display:flex;gap:6px;max-width:640px;margin:0 auto}
.pin{flex:1;min-width:0;display:block;background:var(--card);border:1px solid var(--line);border-radius:10px;padding:8px 4px;font-size:10px;text-align:center;color:var(--ink);text-decoration:none}
.pin b{display:block;font-size:12.5px;white-space:nowrap;font-weight:700;color:var(--acc)}
body{padding-bottom:72px}
@media(max-width:480px){
 .eat{flex-basis:82%}
}
"""

# clock for message timestamps — a small self-paced conversation starting 7:00am
_clock = [7 * 60]
def stamp(step=1):
    v = _clock[0]
    _clock[0] += step
    return f'{v // 60}:{v % 60:02d}'

def gmsg(body='', img=None, id_=None, card=False, extra=''):
    idattr = f' id="{id_}"' if id_ else ''
    att = f'<img class="att" src="{img[0]}" alt="{html.escape(img[1])}" loading="lazy">' if img else ''
    return f'<div class="row"{idattr}><div class="bub{" card" if card else ""}">{body}{att}{extra}</div></div>'

def umsg(body):
    return f'<div class="row me"><div class="bub">{body}</div></div>'

def step_body(t, h, d):
    return f'<span class="mt">{t}</span><h4>{h}</h4>{d}'

credits = '; '.join(html.escape(x['title'].replace('File:', '')) + ' (' + x['lic'] + ')'
                     for group in ('hero', 'steps', 'food') for x in PH[group])
S = DAY['steps']  # 0 depart, 1 arrive Tokyo, 2 FLAT LABO, 3 K.Itoya, 4 lunch, 5 Kappabashi, 6 Yanesen, 7 hotel
H, T = PH['hero'], PH['steps']  # hero: Tokyo/Ginza/Kappabashi/Yanaka Ginza; steps: Mokuhankan/plastic food/Sunshine walkway

thread = ''.join([
    gmsg('A quick recap of Friday, so you have it in one place.'),
    gmsg(DAY['lead'], extra=(
        f'<ul class="facts"><li><b>Guide</b> {DAY["guide"]}</li><li><b>Time</b> {DAY["time"]}</li>'
        f'<li><b>Group</b> {DAY["group"]}</li><li><b>Start and end</b> {DAY["route"]}</li></ul>')),
    gmsg(step_body(*S[0])),
    gmsg(step_body(*S[1]), img=(H[0]['thumb'], H[0]['label']), id_='day'),
    gmsg(step_body(*S[2]), img=(T[0]['thumb'], 'Print workshop demonstration')),
    gmsg(step_body(*S[3])),
    umsg('How do we decide where to eat?'),
    gmsg('Good question — here are five picks, we&rsquo;ll decide on the day.', card=True, id_='eat',
         extra=f'<div class="eats">{eats_block(DAY["food"], PH["food"])}</div>'),
    gmsg(step_body(*S[5]), img=(T[1]['thumb'], 'Plastic food replicas for restaurants')),
    gmsg(step_body(*S[6]), img=(H[3]['thumb'], H[3]['label'])),
    gmsg(step_body(*S[7]), img=(T[2]['thumb'], 'Walkway to Sunshine City'), id_='hotel'),
    gmsg('Getting between stops, all by train:', card=True,
         extra=(f'<div class="mapbox"><iframe src="{route_emb(DAY["stops"])}" loading="lazy" title="Route for the day" '
                f'referrerpolicy="no-referrer-when-downgrade"></iframe></div>'
                f'<p class="moves">{DAY["moves"]} <a href="{route_link(DAY["stops"])}" target="_blank" rel="noopener">'
                f'Open the route in Google Maps ↗</a></p>')),
    umsg('And what do we owe today?'),
    gmsg('Just the one thing:', card=True, id_='pay', extra=f'<ul class="costs">{costs_block(DAY["costs"])}</ul>'),
    gmsg('A couple of notes:', card=True, extra=(
        f'<div class="notes"><p><b>Good for</b> {html.escape(DAY["good"])}</p>'
        f'<p><b>Keep in mind</b> {html.escape(DAY["mind"])}</p></div>')),
    gmsg(f'Official sites, if useful: <span class="links">{links_block(DAY["links"])}</span>'),
    gmsg('That&rsquo;s the whole day &mdash; message me if anything needs to move.'),
])

akiba = f'''<details class="fold" id="akiba"><summary>More: an Akihabara anime day</summary><div class="fold-body">
<p><strong>Not part of Friday.</strong> A separate day, only if it interests you &mdash; a private half-day anime tour around Akihabara, Tokyo&rsquo;s anime and electronics district.</p>
<ul style="margin:0 0 16px 20px;padding:0;font-size:14.5px;color:var(--mute)">{''.join(f'<li style="margin-bottom:6px">{x}</li>' for x in EXTRA['items'])}</ul>
<p style="font-size:14.5px">{EXTRA['dashiell']}</p>
<div class="photos">{''.join(f'<img src="{src}" alt="{html.escape(alt)}" loading="lazy">' for src, alt in EXTRA['photos'])}</div>
<p class="iginvite" style="font-size:13.5px;color:var(--mute);margin:12px 0 6px">More of these days on Instagram.</p>
<a class="igcard" href="{EXTRA['ig']}" target="_blank" rel="noopener">
<div class="ighead"><div class="igavatar">Y</div><div><span class="ighandle">{EXTRA['ig_handle']}</span><span class="igname">{html.escape(EXTRA['ig_name'])}</span></div></div>
<div class="igstats"><span><b>{EXTRA['ig_posts']}</b></span><span><b>{EXTRA['ig_followers']}</b></span></div>
<p class="igbio">{html.escape(EXTRA['ig_bio'])}</p>
<div class="iggrid">{''.join(f'<img src="{src}" alt="Tour guest photo {i+1} from an Akihabara anime tour" loading="lazy">' for i, src in enumerate(EXTRA['ig_grid']))}</div>
</a>
<p style="font-size:14.5px">Interested, or just curious? Yuuki Ichihara, +81 (0)90-4494-1989, WhatsApp works too &mdash; same guide, same number as Friday.</p>
</div></details>'''

page = f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Tokyo, September 11: Brian and Dashiell</title><meta name="robots" content="noindex">
<link rel="preconnect" href="https://fonts.googleapis.com"><link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet">
<style>
:root{{--bg:#fffdf6;--card:#fff;--ink:#111;--mute:#767065;--line:#eae4d6;--acc:#1a5c3a;--r:10px}}
*{{box-sizing:border-box;min-width:0}} html{{overflow-x:hidden;max-width:100%}} body{{max-width:100%}} img{{max-width:100%}}
body{{margin:0;font-family:Inter,-apple-system,"Hiragino Sans",sans-serif;color:var(--ink);background:var(--bg);line-height:1.5}}
.wrap{{max-width:1080px;margin:0 auto;padding:0 20px}}
{NAV_CSS}
{CHAT_CSS}
</style></head><body>
<nav class="topbar"><div class="wrap tb-in">
<div class="tb-id"><div class="av">Y</div><div><b>Yuuki <em>&middot; your guide</em></b><span class="tbdate">{DATE_LABEL}</span></div></div>
<details class="menu"><summary aria-label="Menu">&#9776;</summary>
<div class="menu-list">
<a href="#day">The day</a>
<a href="#pay">What you&rsquo;ll pay</a>
<a href="#eat">Where we eat</a>
<a href="#akiba">Akihabara</a>
</div></details>
</div></nav>
<div class="thread">
{thread}
{akiba}
</div>
<div class="foot"><p>Times are approximate and can move earlier or later on the day.</p>
<details class="cred"><summary>Photo credits</summary><p>{credits}, via Wikimedia Commons.</p></details></div>
<div class="pinbar">
<a class="pin" href="#day"><b>10:42</b>Tokyo Sta.</a>
<a class="pin" href="#eat"><b>Lunch</b>5 picks</a>
<a class="pin" href="#pay"><b>&yen;65,780</b>today</a>
<a class="pin" href="#hotel"><b>16:30</b>Hotel</a>
</div>
{{DEVBAR}}</body></html>'''
open('index.html', 'w').write(page.replace('{DEVBAR}', ''))
open('preview.html', 'w').write(page.replace(
    '{DEVBAR}',
    '<script>window.DEVBAR_FORCE=1</script><script src="devbar.js?v=3"></script>'))
print('written', len(page), '-> index.html + preview.html')
