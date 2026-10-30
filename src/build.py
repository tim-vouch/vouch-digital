"""Builds the static site into public/. Run: python3 src/build.py

Shared header, footer and SEO tags live here so every page stays consistent.
Business facts come from site_data.py; never hard-code them in page content.
"""
import json
from pathlib import Path

from icons import icon
from site_data import SITE, REVIEWS, FAQ_HOME
import pages
import pages_more

ROOT = Path(__file__).resolve().parent.parent

# Meta pixel base code, exactly as Meta provides it, plus Meta's consent call: the pixel stays paused
# (no cookies, no events sent) until the visitor clicks Accept, which calls fbq('consent','grant') in site.js.
# The <noscript> image is deliberately left out: it would track visitors who can't see the cookie banner.
PIXEL_HEAD = """<!-- Meta Pixel Code -->
<script>
!function(f,b,e,v,n,t,s)
{if(f.fbq)return;n=f.fbq=function(){n.callMethod?
n.callMethod.apply(n,arguments):n.queue.push(arguments)};
if(!f._fbq)f._fbq=n;n.push=n;n.loaded=!0;n.version='2.0';
n.queue=[];t=b.createElement(e);t.async=!0;
t.src=v;s=b.getElementsByTagName(e)[0];
s.parentNode.insertBefore(t,s)}(window, document,'script',
'https://connect.facebook.net/en_US/fbevents.js');
fbq('consent', 'revoke');
fbq('init', '""" + SITE["meta_pixel_id"] + """');
</script>
<!-- End Meta Pixel Code -->"""
OUT = ROOT / "public"


def head(title, desc, path, noindex=False):
    url = SITE["domain"] + path
    org = {
        "@context": "https://schema.org",
        "@type": "ProfessionalService",
        "name": SITE["brand"],
        "legalName": SITE["legal_name"],
        "url": SITE["domain"],
        "telephone": SITE["phone_intl"],
        "logo": SITE["domain"] + "/assets/img/logo.png",
        "email": SITE["email"],
        "areaServed": "GB",
        "address": {
            "@type": "PostalAddress",
            "streetAddress": "167–169 Great Portland Street, 5th Floor",
            "addressLocality": "London",
            "postalCode": "W1W 5PF",
            "addressCountry": "GB",
        },
    }
    robots = '<meta name="robots" content="noindex, nofollow">' if (SITE["noindex"] or noindex) else ""
    return f"""<!doctype html>
<html lang="en-GB">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="canonical" href="{url}">
{robots}
<meta property="og:type" content="website">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="{url}">
<meta name="theme-color" content="#04201b">
<meta name="facebook-domain-verification" content="3t84q3i49854mqyiuc8ebzmlia4rfv" />
<meta name="meta-pixel-id" content="{SITE['meta_pixel_id']}">
{PIXEL_HEAD}
<meta property="og:image" content="{SITE['domain']}/assets/img/icon-512.png">
<link rel="icon" href="/favicon.ico" sizes="any">
<link rel="icon" type="image/png" sizes="32x32" href="/favicon-32.png">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Outfit:wght@600;700;800&display=swap" rel="stylesheet">
<link rel="stylesheet" href="/assets/site.css?v={ASSET_V}">
<script type="application/ld+json">{json.dumps(org, ensure_ascii=False)}</script>
</head>
<body>"""


import hashlib as _h
_root = Path(__file__).resolve().parent.parent / "public" / "assets"
# Cache-busting: changes whenever site.css or site.js changes, so browsers fetch the new files.
ASSET_V = _h.md5((_root / "site.css").read_bytes() + (_root / "site.js").read_bytes()).hexdigest()[:8]

NAV = [("Services", "/services"), ("Pricing", "/pricing"),
       ("About", "/about"), ("FAQ", "/faq"), ("Contact", "/contact")]


# Ad landing pages: one action only (Hormozi). The header and footer stay for looks and the legal details, but
# nothing navigates away: no menu, no phone, logo not linked, every button opens the quiz, legal pages open in a new tab.
FUNNEL = {"/book-form", "/book-call"}
QUIZ_CTA = 'Click to see how it works'


def funnel_cta(path):
    if path == "/book-call":  # already past the quiz: the one action is picking a time
        return f'<a class="btn btn-mint" href="#calendar">Pick a time {icon("arrow")}</a>'
    return f'<a class="btn btn-mint" href="/book-call" data-quiz-open>{QUIZ_CTA} {icon("arrow")}</a>'


def header(path):
    if path in FUNNEL:
        return f"""
<header class="site-head funnel-head">
  <div class="wrap">
    <span class="logo"><img src="/assets/img/logo.webp" alt="Vouch Digital" width="112" height="48"></span>
    <div class="head-cta">{funnel_cta(path)}</div>
  </div>
</header>"""
    links = "".join(
        f'<a href="{href}"{" aria-current=page" if href == path or path.startswith(href + "/") else ""}>{name}</a>'
        for name, href in NAV)
    return f"""
<header class="site-head">
  <div class="wrap">
    <a class="logo" href="/"><img src="/assets/img/logo.webp" alt="Vouch Digital" width="112" height="48"></a>
    <nav class="nav" id="nav">{links}</nav>
    <div class="head-cta">
      <a class="head-phone" href="tel:{SITE['phone_intl']}" aria-label="Call {SITE['phone']}">{icon('phone')} <span>{SITE['phone']}</span></a>
      <a class="btn btn-mint" href="/book-form" target="_blank" rel="noopener">Book a call {icon('arrow')}</a>
      <button class="menu-btn" aria-label="Menu" aria-controls="nav" aria-expanded="false">{icon('menu')}</button>
    </div>
  </div>
</header>"""


def footer(path=""):
    funnel = path in FUNNEL
    if funnel:
        logo = '<span class="logo"><img src="/assets/img/logo.webp" alt="Vouch Digital" width="112" height="48" loading="lazy"></span>'
        nav = ""
        cta = funnel_cta(path)
        contact = f'<a href="mailto:{SITE["email"]}">{SITE["email"]}</a>'
        nt = ' target="_blank" rel="noopener"'
    else:
        logo = '<a class="logo" href="/"><img src="/assets/img/logo.webp" alt="Vouch Digital" width="112" height="48" loading="lazy"></a>'
        nav = '<nav class="foot-nav">' + "".join(f'<a href="{h}">{n}</a>' for n, h in NAV) + '</nav>'
        cta = f'<a class="btn btn-mint" href="/book-form" target="_blank" rel="noopener">Book a call {icon("arrow")}</a>'
        contact = f'<a href="tel:{SITE["phone_intl"]}">{SITE["phone"]}</a> · <a href="mailto:{SITE["email"]}">{SITE["email"]}</a>'
        nt = ""
    return f"""
<footer class="site-foot">
  <div class="wrap">
    <div class="foot-top">
      {logo}
      {nav}
      {cta}
    </div>
    <div class="foot-legal">
      <p>Vouch Digital is a trading name of {SITE['legal_name']}. Registered in England and Wales, company number {SITE['company_no']}.<br>
      Registered office: {SITE['address']}. ICO registration: {SITE['ico']}.<br>
      {contact}</p>
      <p>© 2026 {SITE['legal_name']}. <a href="/privacy"{nt}>Privacy Policy</a> · <a href="/terms"{nt}>Terms</a> · <button type="button" class="link-btn" data-cookie-settings>Cookie settings</button></p>
    </div>
  </div>
</footer>
<script src="/assets/site.js?v={ASSET_V}" defer></script>
</body></html>"""


def render(path, title, desc, body, noindex=False):
    return head(title, desc, path, noindex) + header(path) + body + footer(path)


def write(path, html):
    target = OUT / ("index.html" if path == "/" else path.strip("/") + "/index.html")
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(html, encoding="utf-8")
    print("built", path)


def main():
    all_pages = pages.ALL + pages_more.ALL_MORE
    for p in all_pages:
        write(p["path"], render(p["path"], p["title"], p["desc"], p["body"](), p.get("noindex", False)))

    # sitemap.xml and robots.txt (indexable pages only)
    urls = "".join(f"<url><loc>{SITE['domain']}{p['path']}</loc></url>"
                   for p in all_pages if not p.get("noindex"))
    (OUT / "sitemap.xml").write_text(
        '<?xml version="1.0" encoding="UTF-8"?>'
        f'<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">{urls}</urlset>\n', encoding="utf-8")
    (OUT / "robots.txt").write_text(
        "User-agent: *\nAllow: /\nDisallow: /book-form\nDisallow: /book-call\n\n" f"Sitemap: {SITE['domain']}/sitemap.xml\n", encoding="utf-8")
    print("built sitemap.xml, robots.txt")


if __name__ == "__main__":
    main()
