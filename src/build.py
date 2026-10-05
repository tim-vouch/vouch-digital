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
        "areaServed": SITE["area"],
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
<meta property="og:image" content="{SITE['domain']}/assets/img/icon-512.png">
<link rel="icon" href="/favicon.ico" sizes="any">
<link rel="icon" type="image/png" sizes="32x32" href="/favicon-32.png">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Outfit:wght@600;700;800&display=swap" rel="stylesheet">
<link rel="stylesheet" href="/assets/site.css">
<script type="application/ld+json">{json.dumps(org, ensure_ascii=False)}</script>
</head>
<body>"""


# Lean launch: only link to sections that exist. Restore page links as each page is built.
NAV = [("Services", "/#services"), ("How it works", "/#how"), ("Reviews", "/#reviews"),
       ("FAQ", "/#faq")]


def header(path):
    links = "".join(
        f'<a href="{href}"{" aria-current=page" if href == path else ""}>{name}</a>'
        for name, href in NAV)
    return f"""
<header class="site-head">
  <div class="wrap">
    <a class="logo" href="/"><img src="/assets/img/logo.webp" alt="Vouch Digital" width="112" height="48"></a>
    <nav class="nav" id="nav">{links}</nav>
    <div class="head-cta">
      <a class="head-phone" href="tel:{SITE['phone_intl']}">{icon('phone')} {SITE['phone']}</a>
      <a class="btn btn-mint" href="/#audit">Find My Missed Jobs {icon('arrow')}</a>
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
      <a class="logo" href="/"><img src="/assets/img/logo.webp" alt="Vouch Digital" width="112" height="48" loading="lazy"></a>
      <nav class="foot-nav">{links}</nav>
      <a class="btn btn-mint" href="/#audit">Find My Missed Jobs {icon('arrow')}</a>
    </div>
    <div class="foot-legal">
      <p>Vouch Digital is a trading name of {SITE['legal_name']}. Registered in England and Wales, company number {SITE['company_no']}.<br>
      Registered office: {SITE['address']}. ICO registration: {SITE['ico']}.<br>
      <a href="tel:{SITE['phone_intl']}">{SITE['phone']}</a> · <a href="mailto:{SITE['email']}">{SITE['email']}</a></p>
      <p>© 2026 {SITE['legal_name']}. <a href="/privacy">Privacy Policy</a> · <a href="/terms">Terms</a></p>
    </div>
  </div>
</footer>
<div class="mbar"><a class="btn btn-ghost" href="tel:{SITE['phone_intl']}">{icon('phone')} Call</a><a class="btn btn-mint" href="/#audit">Missed Jobs Check</a></div>
<script src="/assets/site.js" defer></script>
</body></html>"""


def render(path, title, desc, body, noindex=False):
    return head(title, desc, path, noindex) + header(path) + body + footer()


def write(path, html):
    target = OUT / ("index.html" if path == "/" else path.strip("/") + "/index.html")
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(html, encoding="utf-8")
    print("built", path)


def main():
    for p in pages.ALL:
        write(p["path"], render(p["path"], p["title"], p["desc"], p["body"](), p.get("noindex", False)))


if __name__ == "__main__":
    main()
