# Generador de las 3 variantes (stripe / uber / airbnb) del DMC v3 — mismo copy y estructura.
# Uso: python variants/build.py  (escribe variants/<v>/index.html). Copy = acta cmo 08-nov §3
# con los cambios del CEO 08-nov: sin Cairo/Albacete/Arabic; Trekko = «our sister brand, the bed bank».
import os
HERE = os.path.dirname(os.path.abspath(__file__))
TK = "https://trekko.co/signup?from=en&amp;utm_source=dmc&amp;utm_medium=referral&amp;utm_campaign=dmc-v3-{v}"
FONT = '-apple-system,BlinkMacSystemFont,"SF Pro Display","SF Pro Text",Inter,"Helvetica Neue",Arial,sans-serif'
ARROW = '<svg class="ico" viewBox="0 0 24 24" aria-hidden="true"><path d="M5 12h14M13 6l6 6-6 6"/></svg>'
ICONS = {
 'group': '<svg class="ico" viewBox="0 0 24 24" aria-hidden="true"><circle cx="9" cy="8" r="3"/><path d="M3 20c0-3.3 2.7-6 6-6s6 2.7 6 6"/><circle cx="17" cy="9" r="2.5"/><path d="M16 14.2c2.8.4 5 2.8 5 5.8"/></svg>',
 'route': '<svg class="ico" viewBox="0 0 24 24" aria-hidden="true"><circle cx="6" cy="18" r="2"/><circle cx="18" cy="6" r="2"/><path d="M8 18h6a4 4 0 0 0 0-8h-4a4 4 0 0 1 0-8h6"/></svg>',
 'heart': '<svg class="ico" viewBox="0 0 24 24" aria-hidden="true"><path d="M12 20s-7-4.4-7-10a4 4 0 0 1 7-2.6A4 4 0 0 1 19 10c0 5.6-7 10-7 10z"/></svg>',
 'school': '<svg class="ico" viewBox="0 0 24 24" aria-hidden="true"><path d="M2 9l10-5 10 5-10 5z"/><path d="M6 11v5c0 1.7 2.7 3 6 3s6-1.3 6-3v-5"/></svg>',
 'brief': '<svg class="ico" viewBox="0 0 24 24" aria-hidden="true"><rect x="3" y="7" width="18" height="13" rx="2"/><path d="M8 7V5a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2M3 12h18"/></svg>',
}
SERVICES = [
 ('group', 'Groups', '"Groups? Please fill in this 6-page form."', 'Tell us the dates and the headcount. We bring coaches, guides, hotels and tickets in one programme.', 'Group'),
 ('route', 'Multi-country tours', '"Three countries, three suppliers, three invoices."', 'One itinerary. One quote. One team, from Italy to the Adriatic to Spain.', 'Multi-destination package'),
 ('heart', 'Honeymoons &amp; luxury', '"Romantic package: rose petals included."', 'Private itineraries with hand-picked hotels, chauffeurs and experiences. No petals unless you ask.', 'Honeymoon or luxury'),
]
SEGMENTS = [
 ('school', 'School &amp; university groups', '"Students: the word that makes suppliers go quiet."', 'Educational and sports trips with coaches, guides, tickets and logistics students and teachers can rely on.', 'School or university', 'Plan a group trip'),
 ('brief', 'Corporate &amp; MICE', '"Forty emails to move one delegation."', 'One brief, one proposal, one team on the ground.', 'Event or MICE', 'Plan an event'),
]
PILLS = ['Travel agencies', 'Tour operators', 'Corporate &amp; MICE', 'School &amp; university groups', 'Senior groups', 'Honeymoons &amp; luxury', 'Families']

def page(v, css, hero_media, labels):
    tk = TK.format(v=v)
    svc = ''.join(f'''
      <a class="card svc" href="#proposal" data-trip="{t}">
        <div class="slot" aria-hidden="true"></div>
        <div class="body">{ICONS[i] if labels['icons'] else ''}<h3>{h}</h3><p class="q">{q}</p><p>{a}</p><span class="go">Get a proposal {ARROW}</span></div>
      </a>''' for i, h, q, a, t in SERVICES)
    seg = ''.join(f'''
      <a class="card seg" href="#proposal" data-trip="{t}">
        <div class="slot" aria-hidden="true"></div>
        <div class="body">{ICONS[i] if labels['icons'] else ''}<h3>{h}</h3><p class="q">{q}</p><p>{a}</p><span class="go">{cta} {ARROW}</span></div>
      </a>''' for i, h, q, a, t, cta in SEGMENTS)
    pills = ''.join(f'<li><a href="#segments"{" aria-current=\"true\"" if k == 0 else ""}>{x}</a></li>' for k, x in enumerate(PILLS))
    return f'''<!doctype html>
<html lang="en" dir="ltr" data-dmc-design="v3-{v}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>StayTick DMC — proposal {labels['name']}</title>
<meta name="robots" content="noindex, nofollow">
<link rel="icon" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 64 64'%3E%3Crect width='64' height='64' rx='12' fill='%23FFFFFF'/%3E%3Ctext x='32' y='43' font-family='Helvetica,Arial,sans-serif' font-weight='700' font-size='34' fill='%23F60C75' text-anchor='middle'%3ES%3C/text%3E%3C/svg%3E">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&amp;display=swap">
<style>
:root{{--font:{FONT};--magenta:#DB0A69;--brand:#F60C75;--gutter:16px;--maxw:1240px;--header-h:72px}}
@media (min-width:640px){{:root{{--gutter:clamp(24px,4vw,48px);--header-h:76px}}}}
*,*::before,*::after{{box-sizing:border-box}}
html{{scroll-behavior:smooth;scroll-padding-top:calc(var(--header-h) + 8px);-webkit-text-size-adjust:100%}}
body{{margin:0;font-family:var(--font);font-size:1rem;line-height:1.55;-webkit-font-smoothing:antialiased;overflow-x:clip}}
em,i{{font-style:normal}} button,input{{font-family:inherit}}
img{{display:block;max-width:100%;height:auto}} a{{color:inherit}} p{{margin:0}}
h1,h2,h3{{margin:0;text-wrap:balance}}
.wrap{{max-width:var(--maxw);margin-inline:auto;padding-inline:var(--gutter)}}
.sr-only{{position:absolute!important;width:1px;height:1px;overflow:hidden;clip:rect(0 0 0 0);white-space:nowrap}}
.skip{{position:absolute;inset-inline-start:var(--gutter);inset-block-start:-100px;z-index:100;background:#000;color:#fff;padding:.7rem 1rem}}
.skip:focus{{inset-block-start:8px}}
.ico{{width:26px;height:26px;flex:none;stroke:currentColor;fill:none;stroke-width:1.6;stroke-linecap:round;stroke-linejoin:round}}
.go .ico{{width:18px;height:18px;transition:transform .2s}}
.card:hover .go .ico{{transform:translateX(3px)}}
[dir="rtl"] .go .ico{{transform:scaleX(-1)}}
.btn{{display:inline-flex;align-items:center;justify-content:center;gap:.5rem;min-height:52px;padding:.85rem 1.5rem;border:0;font-weight:600;font-size:1rem;line-height:1.2;text-decoration:none;cursor:pointer;transition:background .2s,transform .2s,box-shadow .2s}}
.btn:active{{transform:scale(.98)}}
.hdr{{position:sticky;inset-block-start:0;z-index:60}}
.hdr .wrap{{display:flex;align-items:center;gap:1rem;height:var(--header-h)}}
.brand{{display:flex;flex:none}} .brand img{{height:36px;width:auto}}
.nav-main{{display:none;margin-inline-start:auto}}
.nav-main ul{{display:flex;gap:.25rem;list-style:none;margin:0;padding:0}}
.nav-main a{{display:block;padding:.55rem .8rem;font-size:.95rem;font-weight:500;text-decoration:none;white-space:nowrap}}
.hdr-ctas{{display:flex;align-items:center;gap:.5rem;margin-inline-start:auto}}
.hdr-ctas .btn{{min-height:44px;padding:.5rem 1.1rem;font-size:1rem;white-space:nowrap}}
.hdr-rfp,.full{{display:none}}
.burger{{display:inline-grid;place-items:center;width:44px;height:44px;border:0;background:transparent;color:inherit;cursor:pointer}}
.burger span{{display:block;width:20px;height:2px;background:currentColor;position:relative}}
.burger span::before,.burger span::after{{content:"";position:absolute;inset-inline-start:0;width:20px;height:2px;background:currentColor}}
.burger span::before{{top:-6px}} .burger span::after{{top:6px}}
.mnav{{position:fixed;inset:var(--header-h) 0 0 0;z-index:55;overflow-y:auto;padding:1rem var(--gutter) 2rem;display:flex;flex-direction:column;gap:.9rem}}
.mnav[hidden]{{display:none}}
.mnav ul{{list-style:none;margin:0;padding:0}}
.mnav li a{{display:block;padding:.9rem 0;font-size:1.35rem;font-weight:600;text-decoration:none}}
.mnav .btn{{width:100%}}
body.menu-open{{overflow:hidden}}
@media (min-width:720px){{.hdr-rfp{{display:inline-flex}}.full{{display:inline}}.short{{display:none}}}}
@media (min-width:1100px){{.nav-main{{display:block}}.hdr-ctas{{margin-inline-start:.5rem}}.burger{{display:none}}.mnav{{display:none!important}}}}
.hero-ctas{{display:flex;flex-wrap:wrap;gap:.75rem}}
@media (max-width:639px){{.hero-ctas .btn{{width:100%}}}}
.slot{{position:relative;overflow:hidden}}
.slot-tag{{position:absolute;inset-block-start:12px;inset-inline-start:12px;max-width:calc(100% - 24px);font-size:.72rem;font-weight:600;line-height:1.35;padding:.3rem .6rem}}
.cards{{display:grid;gap:1.25rem}}
.card{{display:flex;flex-direction:column;text-decoration:none;color:inherit;overflow:hidden}}
.card .body{{display:flex;flex-direction:column;gap:.55rem;flex:1}}
.go{{margin-block-start:auto;display:inline-flex;align-items:center;gap:.4rem;font-weight:600;font-size:.95rem;padding-block-start:.4rem}}
.pills{{display:flex;gap:.5rem;list-style:none;margin:0;padding:0;overflow-x:auto;scrollbar-width:none}}
.card .q{{color:#717171!important;font-size:.95rem}}
.honest{{list-style:none;margin:0 0 1.6rem;padding:0;display:grid;gap:.9rem}}
.honest li{{font-size:clamp(1.2rem,1rem + .8vw,1.6rem);font-weight:600;letter-spacing:-.015em;line-height:1.3}}
.banner-ctas{{display:flex;flex-wrap:wrap;gap:1rem 1.5rem;align-items:center}}
.blink{{font-weight:600;text-decoration:underline;text-underline-offset:3px}}
.note a{{text-decoration:underline;text-underline-offset:3px}}
.pills::-webkit-scrollbar{{display:none}} .pills li{{flex:none}}
.pills a{{display:inline-flex;align-items:center;min-height:42px;padding:.5rem 1rem;font-size:.92rem;font-weight:500;text-decoration:none;white-space:nowrap}}
{css}
</style>
</head>
<body class="v-{v}">
<a class="skip" href="#main">Skip to content</a>
<header class="hdr">
  <div class="wrap">
    <a class="brand" href="#top" aria-label="StayTick DMC — home"><img src="/img/staytick-logo.png" alt="StayTick DMC" width="620" height="211"></a>
    <nav class="nav-main" aria-label="Main"><ul><li><a href="#services">Services</a></li><li><a href="#segments">Who we serve</a></li><li><a href="#what">How it works</a></li><li><a href="#trekko">Trekko</a></li></ul></nav>
    <div class="hdr-ctas">
      <a class="btn b1 hdr-rfp" href="#proposal">Get a proposal</a>
      <a class="btn b2" href="{tk}" rel="noopener">Join Trekko</a>
      <button class="burger" id="burger" type="button" aria-expanded="false" aria-controls="mnav"><span aria-hidden="true"></span><span class="sr-only">Menu</span></button>
    </div>
  </div>
</header>
<nav class="mnav" id="mnav" aria-label="Mobile" hidden>
  <ul><li><a href="#services">Services</a></li><li><a href="#segments">Who we serve</a></li><li><a href="#what">How it works</a></li><li><a href="#trekko">Trekko</a></li><li><a href="#proposal">Contact</a></li></ul>
  <a class="btn b1" href="#proposal">Get a proposal</a>
  <a class="btn b2" href="{tk}" rel="noopener">Join Trekko</a>
</nav>
<main id="main">
<section class="hero" id="top" aria-labelledby="h1">
  <div class="wrap hero-grid">
    <div class="hero-copy">
      <span class="kicker">StayTick DMC · Spain · Italy · Europe · USA · Japan</span>
      <h1 id="h1">The trips booking engines can't handle.</h1>
      <p class="lead">Groups, events, honeymoons, multi-country tours, villas and VIP arrivals. You send the brief. We design it, price it and run it.</p>
      <div class="hero-ctas"><a class="btn b1" href="#proposal">Get a proposal</a><a class="btn b2" href="{tk}" rel="noopener">Join Trekko</a></div>
      <p class="note"><a href="{tk}" rel="noopener">Just need a hotel, fast? Book it on Trekko →</a></p>
    </div>
    {hero_media}
  </div>
</section>

<section class="sec what" id="what" aria-labelledby="h-what">
  <div class="wrap what-grid">
    <div><span class="kicker">Let's be honest</span><h2 id="h-what">Some trips don't fit in a search box.</h2></div>
    <div>
      <ul class="honest"><li>Forty students, three countries, one teacher who wants a vegetarian menu.</li><li>A board meeting in Madrid that becomes a dinner for eighty.</li><li>A honeymoon where "standard room" is not an option.</li></ul>
      <p class="lead">The sector's answer is usually "on request". Ours is a proposal.</p>
      <p class="pull">Clickable? Book it on Trekko. Not clickable? That's our job.</p>
    </div>
  </div>
</section>

<section class="sec services" id="services" aria-labelledby="h-svc">
  <div class="wrap">
    <div class="head"><span class="kicker">What we do</span><h2 id="h-svc">One team. Every piece of the trip.</h2><p class="lead">Package or service by service. Net pricing for the trade.</p></div>
    <div class="cards c3">{svc}
    </div>
  </div>
</section>

<section class="sec segments" id="segments" aria-labelledby="h-seg">
  <div class="wrap">
    <div class="head"><span class="kicker">Who we serve</span><h2 id="h-seg">Built for people who sell travel.</h2></div>
    {'<ul class="pills" aria-label="Who we serve">' + pills + '</ul>' if labels['pills'] else ''}
    <div class="cards c2">{seg}
    </div>
  </div>
</section>

<section class="banner" id="trekko" aria-labelledby="h-tk">
  <div class="wrap banner-grid">
    <div>
      <span class="kicker">Two ways to book</span>
      <h2 id="h-tk">Tailor-made, or right now?</h2>
      <p>Trekko is our sister brand: a bed bank for travel agencies. Over 3 million hotels, plus transfers, chauffeurs and car rental, at net rates with instant confirmation.</p>
    </div>
    <div class="banner-ctas"><a class="btn b-banner" href="{tk}" rel="noopener">Join Trekko {ARROW}</a><a class="blink" href="#proposal">Or get a proposal from us</a></div>
  </div>
</section>
</main>

<footer class="ftr" id="proposal">
  <div class="wrap ftr-grid">
    <div><img class="flogo" src="/img/staytick-logo.png" alt="StayTick DMC" width="620" height="211" loading="lazy"><p>Tailor-made travel for the trade. Based in Madrid, with offices across Europe.</p></div>
    <div><b>Get a proposal</b><p><a href="tel:+34643195384">+34 643 19 53 84</a></p><p>Every day, 9:00–22:00 CET. Yes, Sundays too.</p></div>
    <div><b>Trekko</b><p><a href="{tk}" rel="noopener">Join Trekko</a></p><p class="langs"><a href="/" lang="en">English</a> · <a href="/es/" lang="es" hreflang="es">Español</a></p></div>
  </div>
  <div class="wrap fine">© <span id="yr">2026</span> StayTick DMC · Trekko is our sister brand · Proposal {labels['name']}, not published</div>
</footer>
<script>
(function(){{var d=document;d.getElementById('yr').textContent=new Date().getFullYear();
var b=d.getElementById('burger'),m=d.getElementById('mnav');
function s(o){{b.setAttribute('aria-expanded',o?'true':'false');m.hidden=!o;d.body.classList.toggle('menu-open',o);}}
b.addEventListener('click',function(){{s(b.getAttribute('aria-expanded')!=='true');}});
m.addEventListener('click',function(e){{if(e.target.closest('a'))s(false);}});
d.addEventListener('keydown',function(e){{if(e.key==='Escape'&&b.getAttribute('aria-expanded')==='true'){{s(false);b.focus();}}}});}})();
</script>
</body>
</html>
'''

STRIPE = '''
body{background:#fff;color:#0A2540}
.hdr{background:rgba(255,255,255,.9);backdrop-filter:blur(14px);-webkit-backdrop-filter:blur(14px);border-block-end:1px solid #E6EBF1}
.nav-main a{color:#425466;border-radius:8px}.nav-main a:hover{color:#0A2540;background:#F6F9FC}
.btn{border-radius:999px}
.b1{background:#0A2540;color:#fff}.b1:hover{background:#1A3A5C}
.b2{background:var(--magenta);color:#fff}.b2:hover{background:#BE085B}
.mnav{background:#fff}.mnav li a{border-block-end:1px solid #E6EBF1}
.hero{position:relative;isolation:isolate;overflow:hidden;padding-block:clamp(3.5rem,2rem + 6vw,8rem) clamp(4rem,2rem + 6vw,8rem)}
.hero::before{content:"";position:absolute;inset:-30% -10% auto -10%;height:120%;z-index:-1;transform:skewY(-8deg);transform-origin:0 0;
 background:radial-gradient(40% 60% at 15% 35%,#A960EE 0%,rgba(169,96,238,0) 70%),radial-gradient(45% 55% at 55% 20%,#F60C75 0%,rgba(246,12,117,0) 70%),radial-gradient(45% 60% at 90% 40%,#90E0FF 0%,rgba(144,224,255,0) 70%),radial-gradient(50% 60% at 70% 75%,#635BFF 0%,rgba(99,91,255,0) 70%);opacity:.55;filter:blur(10px)}
.hero::after{content:"";position:absolute;inset:auto 0 0 0;height:45%;z-index:-1;background:linear-gradient(180deg,rgba(255,255,255,0),#fff)}
.hero-grid{display:grid;gap:3rem;align-items:center}
@media(min-width:1000px){.hero-grid{grid-template-columns:1.15fr .85fr}}
.kicker{display:inline-block;font-size:.9rem;font-weight:600;color:#635BFF;margin-block-end:1rem}
h1{font-size:clamp(2.75rem,1.4rem + 5vw,5rem);font-weight:700;letter-spacing:-.035em;line-height:1.02}
h2{font-size:clamp(2rem,1.3rem + 2.6vw,3.25rem);font-weight:700;letter-spacing:-.025em;line-height:1.08}
h3{font-size:1.2rem;font-weight:600;letter-spacing:-.01em}
.lead{font-size:clamp(1.06rem,1rem + .35vw,1.25rem);color:#425466;max-width:58ch;margin-block-start:1.2rem}
.hero-ctas{margin-block-start:2rem}
.note{margin-block-start:1rem;color:#425466;font-size:.92rem}
.hero-card{background:rgba(255,255,255,.75);backdrop-filter:blur(10px);border:1px solid rgba(255,255,255,.8);border-radius:16px;box-shadow:0 30px 60px -12px rgba(50,50,93,.25),0 18px 36px -18px rgba(0,0,0,.3);padding:1.5rem;display:grid;gap:.9rem}
.hero-card .row{display:flex;gap:.8rem;align-items:center;padding:.8rem;border-radius:10px;background:#F6F9FC;font-weight:600;font-size:.95rem}
.hero-card .row .ico{color:#635BFF}
.hero-card small{color:#425466;font-weight:500}
.sec{padding-block:clamp(4rem,2.5rem + 5vw,7rem)}
.what{background:#F6F9FC}
.what-grid{display:grid;gap:2rem}@media(min-width:1000px){.what-grid{grid-template-columns:1fr 1fr;gap:4rem}}
.what .lead{margin:0}
.pull{margin-block-start:1.6rem;font-size:1.35rem;font-weight:600;letter-spacing:-.01em;background:linear-gradient(90deg,#635BFF,#F60C75);-webkit-background-clip:text;background-clip:text;color:transparent}
.head{margin-block-end:2.5rem;max-width:720px}
.cards.c3{grid-template-columns:1fr}@media(min-width:760px){.cards.c3{grid-template-columns:repeat(3,1fr)}}
.cards.c2{grid-template-columns:1fr}@media(min-width:760px){.cards.c2{grid-template-columns:repeat(2,1fr)}}
.card{background:#fff;border:1px solid #E6EBF1;border-radius:12px;box-shadow:0 2px 5px -1px rgba(50,50,93,.08),0 1px 3px -1px rgba(0,0,0,.1);transition:box-shadow .25s,transform .25s}
.card:hover{transform:translateY(-3px);box-shadow:0 13px 27px -5px rgba(50,50,93,.2),0 8px 16px -8px rgba(0,0,0,.25)}
.card .slot{aspect-ratio:16/10;background:radial-gradient(70% 90% at 20% 20%,#C8B6FF,transparent),radial-gradient(70% 90% at 90% 80%,#FFB3D6,transparent),linear-gradient(135deg,#E0E7FF,#F6F9FC)}
.seg .slot{background:radial-gradient(70% 90% at 80% 20%,#A5E8FF,transparent),radial-gradient(70% 90% at 10% 90%,#C8B6FF,transparent),linear-gradient(135deg,#EEF2FF,#F6F9FC)}
.slot-tag{background:rgba(255,255,255,.85);color:#425466;border-radius:6px}
.card .body{padding:1.4rem}
.card .body>.ico{color:#635BFF}
.card p{color:#425466;font-size:.97rem}
.go{color:#635BFF}
.segments .pills{display:none}
.banner{padding-block:clamp(2.5rem,2rem + 2vw,4rem);background:#0A2540;color:#fff;position:relative;overflow:hidden;isolation:isolate}
.banner::before{content:"";position:absolute;inset:0;z-index:-1;background:radial-gradient(40% 120% at 85% 50%,rgba(246,12,117,.55),transparent),radial-gradient(40% 120% at 60% 0%,rgba(99,91,255,.6),transparent)}
.banner-grid{display:grid;gap:1.5rem;align-items:center}@media(min-width:900px){.banner-grid{grid-template-columns:1fr auto}}
.banner .kicker{color:#A5B4FF}
.banner p{color:#ADBDCC;margin-block-start:.6rem}
.b-banner{background:#fff;color:#0A2540}.b-banner:hover{background:#F6F9FC}
.ftr{padding-block:3rem 2rem;border-block-start:1px solid #E6EBF1;color:#425466;font-size:.92rem}
.ftr-grid{display:grid;gap:1.5rem}@media(min-width:900px){.ftr-grid{grid-template-columns:repeat(3,1fr)}}
.ftr b{display:block;color:#0A2540;margin-block-end:.4rem}.ftr p{margin-block-end:.3rem}
.flogo{height:32px;width:auto;margin-block-end:.6rem}
.fine{margin-block-start:2rem;font-size:.8rem}
.ph{border:1px dashed #A3ACB9;padding:0 .3rem;border-radius:4px;font-size:.85em}
:focus-visible{outline:2px solid #635BFF;outline-offset:3px;border-radius:6px}
'''

UBER = '''
body{background:#fff;color:#000}
.hdr{background:#000;color:#fff}
.brand{background:#fff;padding:.35rem .6rem;border-radius:4px}.brand img{height:28px}
.nav-main a{color:#fff;border-radius:999px}.nav-main a:hover{background:#333}
.btn{border-radius:8px}
.b1{background:#000;color:#fff}.b1:hover{background:#333}
.hdr .b1,.mnav .b1{background:#fff;color:#000}.hdr .b1:hover{background:#E2E2E2}
.b2{background:var(--magenta);color:#fff}.b2:hover{background:#BE085B}
.mnav{background:#000;color:#fff}.mnav li a{border-block-end:1px solid #333}
.hero{background:#000;color:#fff;padding-block:clamp(3rem,2rem + 5vw,7rem)}
.hero-grid{display:grid;gap:2.5rem;align-items:end}
@media(min-width:1000px){.hero-grid{grid-template-columns:1.2fr .8fr}}
.hero .b1{background:#fff;color:#000}.hero .b1:hover{background:#E2E2E2}
.kicker{display:block;font-size:.85rem;font-weight:600;letter-spacing:.02em;margin-block-end:1.2rem;opacity:.8}
h1{font-size:clamp(3rem,1.4rem + 6vw,5.5rem);font-weight:700;letter-spacing:-.04em;line-height:.98}
h2{font-size:clamp(2.2rem,1.3rem + 3.4vw,4rem);font-weight:700;letter-spacing:-.035em;line-height:1.02}
h3{font-size:1.4rem;font-weight:700;letter-spacing:-.02em}
.lead{font-size:clamp(1.06rem,1rem + .4vw,1.3rem);max-width:56ch;margin-block-start:1.4rem;opacity:.85}
.hero-ctas{margin-block-start:2.2rem}
.note{margin-block-start:1rem;font-size:.92rem;opacity:.7}
.hero-media{aspect-ratio:1/1;background:linear-gradient(180deg,#3A3A3A,#0D0D0D);border-radius:0}
.slot-tag{background:#fff;color:#000;border-radius:0}
.sec{padding-block:clamp(4rem,2.5rem + 5vw,8rem)}
.what{background:#fff}
.what-grid{display:grid;gap:2rem}@media(min-width:1000px){.what-grid{grid-template-columns:1fr 1fr;gap:5rem}}
.what .lead{margin:0;opacity:1;color:#333}
.pull{margin-block-start:2rem;padding-block-start:1.5rem;border-block-start:4px solid #000;font-size:clamp(1.4rem,1.1rem + 1vw,2rem);font-weight:700;letter-spacing:-.02em;line-height:1.15}
.services{background:#F3F3F3}
.head{margin-block-end:2.5rem;max-width:760px}.head .lead{color:#333;opacity:1}
.cards{gap:0;border:2px solid #000}
.cards.c3{grid-template-columns:1fr}@media(min-width:760px){.cards.c3{grid-template-columns:repeat(3,1fr)}}
.cards.c2{grid-template-columns:1fr}@media(min-width:760px){.cards.c2{grid-template-columns:repeat(2,1fr)}}
.card{background:#fff;border:2px solid #000;margin:-1px;transition:background .2s}
.card:hover{background:#F6F6F6}
.card .slot{aspect-ratio:4/3;background:linear-gradient(160deg,#5A5A5A 0%,#111 100%)}
.card .body{padding:1.5rem 1.4rem 1.7rem}
.card p{color:#333}
.segments{background:#000;color:#fff}.segments .head .lead{color:#ccc}
.segments .pills{margin-block-end:1.8rem}
.segments .pills a{background:#222;color:#fff;border-radius:999px}.segments .pills a[aria-current]{background:#fff;color:#000}
.segments .cards{border-color:#fff}.segments .card{background:#000;border-color:#fff}.segments .card:hover{background:#111}.segments .card p{color:#ccc}
.segments .card .slot{background:linear-gradient(160deg,#777 0%,#222 100%)}
.banner{background:var(--magenta);color:#fff;padding-block:clamp(2.5rem,2rem + 3vw,5rem)}
.banner-grid{display:grid;gap:1.5rem;align-items:center}@media(min-width:900px){.banner-grid{grid-template-columns:1fr auto}}
.banner .kicker{opacity:.9}.banner p{margin-block-start:.6rem;opacity:.9}
.b-banner{background:#000;color:#fff;min-height:60px;padding-inline:2rem;font-size:1.05rem}.b-banner:hover{background:#222}
.ftr{background:#000;color:#ccc;padding-block:3rem 2rem;font-size:.92rem}
.ftr-grid{display:grid;gap:1.5rem}@media(min-width:900px){.ftr-grid{grid-template-columns:repeat(3,1fr)}}
.ftr b{display:block;color:#fff;margin-block-end:.4rem}.ftr p{margin-block-end:.3rem}
.flogo{height:30px;width:auto;margin-block-end:.6rem;background:#fff;padding:.3rem .5rem}
.fine{margin-block-start:2rem;font-size:.8rem;color:#999}
.ph{border:1px dashed #888;padding:0 .3rem;font-size:.85em}
:focus-visible{outline:3px solid var(--magenta);outline-offset:3px}
'''

AIRBNB = '''
body{background:#fff;color:#222}
.hdr{background:#fff;border-block-end:1px solid #EBEBEB}
.nav-main a{color:#222;border-radius:999px}.nav-main a:hover{background:#F7F7F7}
.btn{border-radius:12px}
.b1{background:var(--magenta);color:#fff}.b1:hover{background:#BE085B}
.b2{background:#222;color:#fff}.b2:hover{background:#000}
.mnav{background:#fff}.mnav li a{border-block-end:1px solid #EBEBEB}
.hero{padding-block:clamp(2rem,1.5rem + 3vw,4.5rem) clamp(3rem,2rem + 3vw,5rem)}
.hero-grid{display:grid;gap:2.2rem;align-items:center}
@media(min-width:1000px){.hero-grid{grid-template-columns:1fr 1fr;gap:3.5rem}}
.kicker{display:inline-block;font-size:.88rem;font-weight:600;color:#6A6A6A;margin-block-end:1rem}
h1{font-size:clamp(2.6rem,1.4rem + 4.6vw,4.6rem);font-weight:700;letter-spacing:-.03em;line-height:1.04}
h2{font-size:clamp(1.9rem,1.3rem + 2.2vw,3rem);font-weight:700;letter-spacing:-.022em;line-height:1.1}
h3{font-size:1.15rem;font-weight:600;letter-spacing:-.01em}
.lead{font-size:clamp(1.05rem,1rem + .3vw,1.2rem);color:#6A6A6A;max-width:56ch;margin-block-start:1.2rem}
.hero-ctas{margin-block-start:2rem}
.note{margin-block-start:1rem;color:#6A6A6A;font-size:.92rem}
.hero-media{aspect-ratio:4/5;border-radius:24px;background:linear-gradient(160deg,#F3E7DF 0%,#D9C2B3 100%);box-shadow:0 6px 24px rgba(0,0,0,.08)}
@media(max-width:999px){.hero-media{aspect-ratio:4/3}}
.slot-tag{background:#fff;color:#222;border-radius:999px;box-shadow:0 1px 4px rgba(0,0,0,.12)}
.sec{padding-block:clamp(3.5rem,2.5rem + 4vw,6.5rem)}
.what{background:#F7F7F7}
.what-grid{display:grid;gap:1.8rem}@media(min-width:1000px){.what-grid{grid-template-columns:1fr 1.1fr;gap:4rem}}
.what .lead{margin:0}
.pull{margin-block-start:1.6rem;display:inline-block;background:#fff;border-radius:16px;padding:1rem 1.2rem;box-shadow:0 2px 12px rgba(0,0,0,.06);font-weight:600;font-size:1.15rem}
.head{margin-block-end:2rem;max-width:720px}
.cards.c3{grid-template-columns:1fr}@media(min-width:760px){.cards.c3{grid-template-columns:repeat(3,1fr)}}
.cards.c2{grid-template-columns:1fr}@media(min-width:760px){.cards.c2{grid-template-columns:repeat(2,1fr)}}
.card{gap:.9rem;transition:transform .25s}
.card:hover{transform:translateY(-2px)}
.card .slot{aspect-ratio:1/1;border-radius:20px;background:linear-gradient(160deg,#EFE3DA 0%,#CDB6A6 100%)}
.card.seg .slot{aspect-ratio:3/2;background:linear-gradient(160deg,#E7E3EE 0%,#BFB6CF 100%)}
.card:hover .slot{box-shadow:0 8px 28px rgba(0,0,0,.14)}
.card .body{padding:0 .2rem}
.card .body>.ico{display:none}
.card p{color:#6A6A6A;font-size:.96rem}
.go{color:#222;text-decoration:underline;text-underline-offset:3px}
.segments .pills{margin-block-end:1.8rem;border-block-end:1px solid #EBEBEB;padding-block-end:1rem}
.segments .pills a{border:1px solid #DDDDDD;border-radius:999px;background:#fff;color:#222}
.segments .pills a:hover{border-color:#222}
.segments .pills a[aria-current]{background:#222;color:#fff;border-color:#222}
.banner{padding-block:clamp(1.5rem,1rem + 2vw,3rem)}
.banner-grid{display:grid;gap:1.4rem;align-items:center;background:#222;color:#fff;border-radius:24px;padding:clamp(1.6rem,1.2rem + 2vw,3rem)}
@media(min-width:900px){.banner-grid{grid-template-columns:1fr auto}}
.banner .kicker{color:#FF8FBF}.banner p{color:#ccc;margin-block-start:.6rem}
.b-banner{background:var(--magenta);color:#fff}.b-banner:hover{background:#BE085B}
.ftr{background:#F7F7F7;border-block-start:1px solid #EBEBEB;padding-block:3rem 2rem;color:#6A6A6A;font-size:.92rem}
.ftr-grid{display:grid;gap:1.5rem}@media(min-width:900px){.ftr-grid{grid-template-columns:repeat(3,1fr)}}
.ftr b{display:block;color:#222;margin-block-end:.4rem}.ftr p{margin-block-end:.3rem}
.flogo{height:32px;width:auto;margin-block-end:.6rem}
.fine{margin-block-start:2rem;font-size:.8rem}
.ph{border:1px dashed #B0B0B0;padding:0 .3rem;border-radius:6px;font-size:.85em}
:focus-visible{outline:2px solid #222;outline-offset:3px;border-radius:8px}
'''

STRIPE_MEDIA = ('<div class="hero-card" aria-label="Two ways to work with us">'
  '<div class="row">' + ICONS['route'] + '<div>We design it<br><small>Groups, events, multi-destination programmes</small></div></div>'
  '<div class="row">' + ICONS['brief'] + '<div>You book it online<br><small>Hotels, transfers, chauffeurs, car rental on Trekko</small></div></div>'
  '<div class="row">' + ICONS['heart'] + '<div>One contact<br><small>Every day, 9:00–22:00 CET</small></div></div></div>')
MEDIA = '<div class="hero-media slot" aria-hidden="true"></div>'

for v, css, media, labels in [
    ('stripe', STRIPE, STRIPE_MEDIA, {'name': 'Stripe style', 'icons': True, 'pills': False}),
    ('uber', UBER, MEDIA, {'name': 'Uber style', 'icons': False, 'pills': True}),
    ('airbnb', AIRBNB, MEDIA, {'name': 'Airbnb style', 'icons': False, 'pills': True}),
]:
    os.makedirs(os.path.join(HERE, v), exist_ok=True)
    with open(os.path.join(HERE, v, 'index.html'), 'w', encoding='utf-8', newline='\n') as f:
        f.write(page(v, css, media, labels))
print('ok')
