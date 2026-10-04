"""Builds the static site into public/. Run: python3 src/build.py

Shared header, footer and SEO tags live here so every page stays consistent.
Business facts come from site_data.py; never hard-code them in page content.
"""
import json
from pathlib import Path

from icons import icon
from site_data import SITE, REVIEWS, FAQ_HOME
import pages

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "public"


def head(title, desc, path):
    url = SITE["domain"] + path
    org = {
        "@context": "https://schema.org",
        "@type": "ProfessionalService",
        "name": SITE["brand"],
        "legalName": SITE["legal_name"],
        "url": SITE["domain"],
        "telephone": SITE["phone_intl"],
        "email": SITE["email"],
        "areaServed": SITE["area"],
        "address": {
            "@type": "PostalAddress",
            "streetAddress": "167–169 Great Portland Street, 5th Floor",
            "addressLocality": "London",
            "postalCode": "W1W 5PF",
            "addressCountry": "GB",
        },
    }
    robots = '<meta name="robots" content="noindex, nofollow">' if SITE["noindex"] else ""
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
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Outfit:wght@600;700;800&display=swap" rel="stylesheet">
<link rel="stylesheet" href="/assets/site.css">
<script type="application/ld+json">{json.dumps(org, ensure_ascii=False)}</script>
</head>
<body>"""


NAV = [("Home", "/"), ("Services", "/services"), ("Plumbers", "/plumbers"),
       ("Electricians", "/electricians"), ("About", "/about"), ("Contact", "/contact")]


def header(path):
    links = "".join(
        f'<a href="{href}"{" aria-current=page" if href == path else ""}>{name}</a>'
        for name, href in NAV)
    return f"""
<header class="site-head">
  <div class="wrap">
    <a class="logo" href="/" aria-label="Vouch Digital home"><b>Vouch</b><span>DIGITAL</span></a>
    <nav class="nav" id="nav">{links}</nav>
    <div class="head-cta">
      <a class="head-phone" href="tel:{SITE['phone_intl']}">{icon('phone')} {SITE['phone']}</a>
      <a class="btn btn-mint" href="/#audit">Get a Free Audit {icon('arrow')}</a>
      <button class="menu-btn" aria-label="Menu" aria-controls="nav" aria-expanded="false">{icon('menu')}</button>
    </div>
  </div>
</header>"""


def footer():
    links = "".join(f'<a href="{h}">{n}</a>' for n, h in NAV)
    return f"""
<footer class="site-foot">
  <div class="wrap">
    <div class="foot-top">
      <a class="logo" href="/"><b>Vouch</b><span>DIGITAL</span></a>
      <nav class="foot-nav">{links}<a href="/faq">FAQ</a></nav>
      <a class="btn btn-mint" href="/#audit">Get a Free Audit {icon('arrow')}</a>
    </div>
    <div class="foot-legal">
      <p>Vouch Digital is a trading name of {SITE['legal_name']}. Registered in England and Wales, company number {SITE['company_no']}.<br>
      Registered office: {SITE['address']}. ICO registration: {SITE['ico']}.<br>
      <a href="tel:{SITE['phone_intl']}">{SITE['phone']}</a> · <a href="mailto:{SITE['email']}">{SITE['email']}</a></p>
      <p>© 2026 {SITE['legal_name']}. <a href="/privacy">Privacy Policy</a> · <a href="/terms">Terms</a></p>
    </div>
  </div>
</footer>
<div class="mbar"><a class="btn btn-ghost" href="tel:{SITE['phone_intl']}">{icon('phone')} Call</a><a class="btn btn-mint" href="/#audit">Free Audit</a></div>
<script src="/assets/site.js" defer></script>
</body></html>"""


def render(path, title, desc, body):
    return head(title, desc, path) + header(path) + body + footer()


def write(path, html):
    target = OUT / ("index.html" if path == "/" else path.strip("/") + "/index.html")
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(html, encoding="utf-8")
    print("built", path)


def main():
    for p in pages.ALL:
        write(p["path"], render(p["path"], p["title"], p["desc"], p["body"]()))


if __name__ == "__main__":
    main()
