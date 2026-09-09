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
         'I&rsquo;ll be waiting on the platform, right at the door closest to your seats &mdash; Yuuki Ichihara, '
         '+81 (0)90-4494-1989, WhatsApp works too.'),
        ('11:30', 'FLAT LABO, Ginza',
         'A showroom for museum-quality digital art printing: the craftsmanship and technology behind fine art prints, '
         'plus a live printing demonstration up close. 2-16-7 Ginza, Shochiku Building, Chuo-ku &middot; 03-6264-7718. '
         'About an hour, with me interpreting.'),
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
           "Popular shows often get a collaboration cafe or pop-up somewhere in the neighborhood that month &mdash; we&rsquo;d "
           "check what&rsquo;s running when the day comes. And since <i>Ruri Rocks</i> is about minerals, there are also small "
           "shops around Tokyo that sell mineral and fossil specimens, worth a stop if that appeals."),
 photos=[('img/akiba-street.jpg', 'Standing in the middle of Akihabara on a tour day'),
         ('img/akiba-cafe.jpg', 'A maid cafe drink being poured at the table'),
         ('img/akiba-secondhand-shelf.jpg', 'Hunting through a shelf of secondhand boxes')],
 ig='https://www.instagram.com/yukianimesensei/',
)

def photos_block(items):
    return ''.join(f'<img src="{x["thumb"]}" alt="{html.escape(x.get("label", x["title"]))}" loading="lazy">' for x in items)

def steps_block(steps):
    return ''.join(f'<li><b>{t}</b><div><strong>{h}</strong><span>{d}</span></div></li>' for t, h, d in steps)

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

HERO_CSS = """
.hpic{position:relative;background:#111;color:#fff}
.slides{position:absolute;inset:0;overflow:hidden}
.slides img{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;opacity:0;transform:scale(1.06);transition:opacity 1.1s ease,transform 5s linear}
.slides img.on{opacity:1;transform:scale(1)}
.slides:after{content:"";position:absolute;inset:0;background:linear-gradient(180deg,rgba(0,0,0,.08) 30%,rgba(0,0,0,.74))}
.hcap{position:relative;z-index:1;min-height:40vh;max-height:390px;display:flex;flex-direction:column;justify-content:flex-end;padding-top:48px;padding-bottom:22px}
.hcap .kicker{color:#9ee3b8}
.hcap h1{color:#fff;margin:0 0 14px;text-shadow:0 2px 14px rgba(0,0,0,.3)}
.snav{display:flex;align-items:center;gap:10px}
.slabel{font:inherit;font-size:12.5px;font-weight:600;color:#fff;background:rgba(0,0,0,.38);border:1px solid rgba(255,255,255,.4);border-radius:999px;padding:7px 13px;backdrop-filter:blur(6px);-webkit-backdrop-filter:blur(6px);max-width:100%;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.dots{display:flex;gap:7px;margin-left:auto;flex:none}
.dots button{width:9px;height:9px;padding:0;border:none;border-radius:50%;background:rgba(255,255,255,.45);cursor:pointer}
.dots button.on{background:#fff}
.hbody{padding-top:22px;padding-bottom:26px}
@media(prefers-reduced-motion:reduce){.slides img{transition:none;transform:none}}
"""
NAV_CSS = """
[id]{scroll-margin-top:64px}
.topbar{position:sticky;top:0;z-index:20;background:rgba(255,253,246,.86);backdrop-filter:blur(8px);-webkit-backdrop-filter:blur(8px);border-bottom:1px solid var(--line)}
.tb-in{display:flex;align-items:center;justify-content:space-between;padding:12px 20px}
.tb-label{font-size:13px;font-weight:600;color:var(--ink);overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
.menu{position:relative;flex:none;margin-left:12px}
.menu summary{list-style:none;cursor:pointer;font-size:18px;line-height:1;padding:6px 10px;border-radius:6px;color:var(--ink)}
.menu summary::-webkit-details-marker{display:none}
.menu[open] summary{background:var(--line)}
.menu-list{position:absolute;right:0;top:calc(100% + 8px);background:var(--card);border:1px solid var(--line);border-radius:8px;box-shadow:0 8px 24px rgba(0,0,0,.1);padding:6px;display:flex;flex-direction:column;min-width:190px}
.menu-list a{padding:9px 12px;border-radius:6px;font-size:14px;color:var(--ink);text-decoration:none}
.menu-list a:hover{background:var(--bg)}
.fold{border:1px solid var(--line);border-radius:8px;background:var(--card);margin:0 0 26px}
.fold>summary{cursor:pointer;list-style:none;display:flex;align-items:center;justify-content:space-between;gap:10px;padding:14px 18px;font-weight:600;font-size:15px}
.fold>summary::-webkit-details-marker{display:none}
.fold>summary::after{content:"+";font-weight:400;font-size:19px;color:var(--mute)}
.fold[open]>summary{border-bottom:1px solid var(--line)}
.fold[open]>summary::after{content:"\\2212"}
.fold-body{padding:18px}
.fold-body>.eats,.fold-body>.photos{margin-bottom:0}
"""
HERO_JS = """
 (function(){
  var sl=[].slice.call(document.querySelectorAll('.slides img')),dots=[].slice.call(document.querySelectorAll('.dots button')),lab=document.querySelector('.slabel'),i=0,t;
  function show(n){i=n;sl.forEach(function(x,k){x.classList.toggle('on',k===n)});dots.forEach(function(x,k){x.classList.toggle('on',k===n)});
   lab.textContent=sl[n].dataset.name}
  function go(){clearInterval(t);if(!matchMedia('(prefers-reduced-motion: reduce)').matches)t=setInterval(function(){show((i+1)%sl.length)},4000)}
  dots.forEach(function(d,k){d.addEventListener('click',function(){show(k);go()})});
  show(0);go();
 })();
"""

credits = '; '.join(html.escape(x['title'].replace('File:', '')) + ' (' + x['lic'] + ')'
                     for group in ('hero', 'steps', 'food') for x in PH[group])
page = f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Tokyo, September 11: Brian and Dashiell</title><meta name="robots" content="noindex">
<link rel="preconnect" href="https://fonts.googleapis.com"><link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet">
<style>
:root{{--bg:#fffdf6;--card:#fff;--ink:#111;--mute:#767065;--line:#eae4d6;--acc:#1a5c3a;--r:10px}}
*{{box-sizing:border-box;min-width:0}} html{{overflow-x:hidden;max-width:100%}} body{{max-width:100%}} img{{max-width:100%}}
body{{margin:0;font-family:Inter,-apple-system,"Hiragino Sans",sans-serif;color:var(--ink);background:var(--bg);line-height:1.6}}
.wrap{{max-width:1080px;margin:0 auto;padding:0 20px}}
.kicker{{font-size:12px;font-weight:600;letter-spacing:.12em;text-transform:uppercase;color:var(--acc);margin:0 0 10px}}
h1,h2{{text-wrap:balance}} .nb{{white-space:nowrap}}
h1{{font-weight:800;font-size:clamp(34px,5.4vw,54px);line-height:1.06;letter-spacing:-.025em;margin:0 0 16px}}
h2{{font-weight:800;font-size:clamp(30px,4.2vw,42px);line-height:1.06;letter-spacing:-.025em;margin:0}}
h3{{font-size:12px;font-weight:600;letter-spacing:.12em;text-transform:uppercase;color:var(--acc);margin:0 0 12px}}
{HERO_CSS}
{NAV_CSS}
header p{{font-size:18px;color:var(--mute);margin:0;max-width:620px}}
.facts{{display:flex;flex-wrap:wrap;gap:6px 20px;margin:20px 0 0;padding:0;list-style:none;font-size:14px;color:var(--mute)}} .facts b{{color:var(--ink);font-weight:600}}
.sechead{{display:flex;align-items:baseline;gap:14px;padding:26px 0 16px;border-top:1px solid var(--line)}}
.sechead .n{{font-weight:800;font-size:26px;line-height:1;letter-spacing:-.02em;color:var(--acc)}}
.sechead b{{font-size:19px;font-weight:600}} .sechead span{{font-size:14px;color:var(--mute)}}
.photos{{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:10px;margin-bottom:26px}}
.photos img{{display:block;width:100%;aspect-ratio:4/3;object-fit:cover;border-radius:8px;background:#f0ebe0}}
.steps{{list-style:none;padding:0;margin:0 0 30px;border-top:1px solid var(--line);max-width:720px}}
.steps li{{display:grid;grid-template-columns:110px minmax(0,1fr);gap:16px;padding:14px 0;border-bottom:1px solid var(--line)}}
.steps b{{font-variant-numeric:tabular-nums;color:var(--acc);font-weight:600;font-size:14px}} .steps strong{{display:block;font-weight:600;font-size:17px;margin-bottom:2px}} .steps span{{color:var(--mute);font-size:14px}}
.mapbox{{border-radius:8px;overflow:hidden;background:#f0ebe0;max-width:720px}} .mapbox iframe{{display:block;width:100%;height:340px;border:0}}
.moves{{font-size:14px;color:var(--mute);margin:14px 0 0;max-width:720px}} .moves a{{color:var(--ink);text-decoration:underline;text-underline-offset:3px}}
.eats{{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:12px;margin-bottom:26px}}
.eat{{display:flex;flex-direction:column;text-decoration:none;color:inherit;background:var(--card);border:1px solid var(--line);border-radius:8px;overflow:hidden}}
.eat>img{{display:block;width:100%;aspect-ratio:3/2;object-fit:cover;background:#f0ebe0}}
.eb{{display:flex;flex-direction:column;flex:1;padding:14px 16px 16px}}
.eat:hover{{border-color:var(--ink)}}
.eat strong{{display:block;font-weight:700;font-size:18px;line-height:1.2;letter-spacing:-.015em}}
.eat em{{display:block;font-style:normal;font-size:11px;color:var(--acc);font-weight:600;letter-spacing:.08em;text-transform:uppercase;margin:5px 0 9px}}
.eb>span{{display:block;font-size:14px;color:var(--mute)}} .eat i{{display:block;font-style:normal;font-size:12px;margin-top:auto;padding-top:10px;text-decoration:underline;text-underline-offset:3px}}
.notes{{display:grid;grid-template-columns:1fr 1fr;gap:14px;margin-bottom:20px;font-size:14px;max-width:720px}} .notes p{{margin:0;padding:16px 18px;background:var(--card);border:1px solid var(--line);border-radius:8px}} .notes b{{display:block;font-weight:600;margin-bottom:3px}}
.costs{{list-style:none;margin:0 0 30px;padding:0;max-width:720px;border-top:1px solid var(--line)}}
.costs li{{display:grid;grid-template-columns:1fr auto;gap:2px 16px;padding:14px 0;border-bottom:1px solid var(--line);align-items:baseline}}
.costs b{{font-weight:600;font-size:15px}} .costs strong{{font-weight:700;font-size:15px;color:var(--acc);text-align:right;white-space:nowrap}}
.costs span{{grid-column:1/-1;color:var(--mute);font-size:13.5px}}
.links{{margin:0 0 30px;font-size:14px;display:flex;flex-wrap:wrap;gap:6px 18px}} .links a{{color:var(--ink);text-decoration:underline;text-underline-offset:3px}}
footer.wrap{{padding:26px 20px 60px;font-size:13px;color:var(--mute);border-top:1px solid var(--line)}} footer p{{margin:0 0 6px}}
.cred summary{{cursor:pointer;font-size:12px;color:var(--mute);opacity:.75;list-style:none;display:inline-block;text-decoration:underline;text-underline-offset:3px}}
.cred summary::-webkit-details-marker{{display:none}} .cred p{{margin:8px 0 0;font-size:11.5px;line-height:1.6;opacity:.8}}
@media(max-width:820px){{
 .photos,.eats,.notes{{grid-template-columns:1fr}}
 .mapbox iframe{{height:260px}}
}}
@media(max-width:560px){{
 .wrap{{padding:0 18px}}
 .hcap{{min-height:38vh;padding-bottom:18px}} .hbody{{padding-top:18px;padding-bottom:22px}} .kicker{{margin-bottom:12px}}
 h1{{font-size:33px;line-height:1.08;letter-spacing:-.03em;margin-bottom:14px}}
 header p{{font-size:16px;line-height:1.55;max-width:none}}
 .facts{{display:grid;grid-template-columns:auto 1fr;gap:3px 10px;margin-top:16px;font-size:13px;line-height:1.5}}
 .facts li{{display:contents}} .facts b{{white-space:nowrap}}
 .sechead{{display:block;padding:22px 0 12px}}
 .sechead .n{{font-size:20px;margin-right:8px;display:inline}}
 .sechead b{{font-size:17px}} .sechead span{{display:block;font-size:13px;line-height:1.5;margin-top:2px}}
 .photos{{gap:8px;margin-bottom:20px}}
 .steps li{{grid-template-columns:88px minmax(0,1fr);gap:10px;padding:11px 0}}
 .steps strong{{font-size:15.5px}} .steps span{{font-size:13.5px;line-height:1.5}}
 .mapbox iframe{{height:230px}}
 .eats{{gap:10px;margin-bottom:20px}} .eat>img{{aspect-ratio:16/9}} .eb{{padding:12px 14px 14px}}
 .notes{{gap:10px;margin-bottom:16px}} .notes p{{padding:14px 16px;font-size:13.5px}}
 .links{{font-size:13.5px;gap:4px 14px;margin-bottom:22px}}
 footer.wrap{{padding:20px 18px 44px;font-size:11.5px;line-height:1.55}}
}}
</style></head><body>
<nav class="topbar"><div class="wrap tb-in">
<span class="tb-label">Sep 11 &middot; {DAY['group']}</span>
<details class="menu"><summary aria-label="Menu">&#9776;</summary>
<div class="menu-list">
<a href="#day">The day</a>
<a href="#pay">What you&rsquo;ll pay</a>
<a href="#eat">Where we eat</a>
<a href="#akiba">Akihabara</a>
</div></details>
</div></nav>
<header class="hero">
<div class="hpic"><div class="slides">{''.join(f'<img src="{x["thumb"]}" alt="{html.escape(x["label"])}" data-name="{html.escape(x["label"])}">' for x in PH['hero'])}</div>
<div class="wrap hcap">
<p class="kicker">{DAY['kicker']}</p>
<h1>{DAY['title_pre']}<span class="nb">{DAY['title_nb']}</span></h1>
<div class="snav"><button class="slabel" type="button"></button><div class="dots">{''.join('<button type="button" aria-label="Show photo"></button>' for _ in PH['hero'])}</div></div>
</div></div>
<div class="wrap hbody">
<p>{DAY['lead']}</p>
<ul class="facts"><li><b>Guide</b> {DAY['guide']}</li><li><b>Time</b> {DAY['time']}</li><li><b>Group</b> {DAY['group']}</li><li><b>Start and end</b> {DAY['route']}</li></ul>
</div>
</header>
<div class="wrap">
<div class="sechead" id="day"><span class="n">1</span><div><b>The day</b> <span>Hour by hour, start to finish.</span></div></div>
<div class="photos">{photos_block(PH['steps'])}</div>
<ol class="steps">{steps_block(DAY['steps'])}</ol>
<details class="fold" id="eat"><summary>Five lunch ideas</summary><div class="fold-body">
<div class="eats">{eats_block(DAY['food'], PH['food'])}</div>
</div></details>
<div class="notes"><p><b>Good for</b> {html.escape(DAY['good'])}</p><p><b>Keep in mind</b> {html.escape(DAY['mind'])}</p></div>
<p class="links">{links_block(DAY['links'])}</p>
<div class="sechead" id="pay"><span class="n">2</span><div><b>What you&rsquo;ll pay today</b> <span>Everything else is already arranged.</span></div></div>
<ul class="costs">{costs_block(DAY['costs'])}</ul>
<div class="sechead"><span class="n">3</span><div><b>Getting around</b> <span>How the day connects, stop to stop.</span></div></div>
<div class="mapbox"><iframe src="{route_emb(DAY['stops'])}" loading="lazy" title="Route for the day" referrerpolicy="no-referrer-when-downgrade"></iframe></div>
<p class="moves">{DAY['moves']} <a href="{route_link(DAY['stops'])}" target="_blank" rel="noopener">Open the route in Google Maps ↗</a></p>
<details class="fold" id="akiba"><summary>More: an Akihabara anime day</summary><div class="fold-body">
<div class="sechead"><span class="n">4</span><div><b>Not part of Friday</b> <span>A separate day, only if it interests you.</span></div></div>
<p>Outside the plan above, I also run a private half-day anime tour around Akihabara, Tokyo&rsquo;s anime and electronics district. It isn&rsquo;t on Friday&rsquo;s schedule &mdash; just something worth knowing about if a second day in Tokyo ever fits your trip.</p>
<ul style="margin:0 0 16px 20px;padding:0;font-size:15px;color:var(--mute)">{''.join(f'<li style="margin-bottom:6px">{x}</li>' for x in EXTRA['items'])}</ul>
<p>{EXTRA['dashiell']}</p>
<div class="photos">{''.join(f'<img src="{src}" alt="{html.escape(alt)}" loading="lazy">' for src, alt in EXTRA['photos'])}</div>
<p class="links"><a href="{EXTRA['ig']}" target="_blank" rel="noopener">See recent tours on Instagram ↗</a></p>
<p>Interested, or just curious? Yuuki Ichihara, +81 (0)90-4494-1989, WhatsApp works too &mdash; same guide, same number as Friday.</p>
</div></details>
</div>
<footer class="wrap"><p>Times are approximate and can move earlier or later on the day.</p>
<details class="cred"><summary>Photo credits</summary><p>{credits}, via Wikimedia Commons.</p></details></footer>
<script>
{HERO_JS}
</script>
{{DEVBAR}}</body></html>'''
open('index.html', 'w').write(page.replace('{DEVBAR}', ''))
open('preview.html', 'w').write(page.replace(
    '{DEVBAR}',
    '<script>window.DEVBAR_FORCE=1</script><script src="devbar.js?v=3"></script>'))
print('written', len(page), '-> index.html + preview.html')
