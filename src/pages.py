"""Page bodies. Each entry in ALL becomes one page."""
from html import escape

from icons import icon
from services_data import SERVICE_PAGES, GROUPS
from site_data import SITE, REVIEWS, RATING, GOOGLE, FACEBOOK, TRUSTPILOT, FAQ_HOME, PLANS, EXTRAS, BILLING


TP_ICON = '<svg class="tp-ico" viewBox="0 0 48 48" aria-hidden="true"><path fill="#00B67A" d="M24 3l5.6 15.6H46L32.7 28.2 37.8 44 24 34.3 10.2 44l5.1-15.8L2 18.6h16.4z"/><path fill="#005128" d="M33.6 30.9l-1-2.7-8.6 6.1z"/></svg>'
FB_LOGO = '<svg class="fb-logo" viewBox="0 0 48 48" aria-hidden="true"><circle cx="24" cy="24" r="24" fill="#1877F2"/><path fill="#fff" d="M33.3 30.9l1.1-6.9h-6.6v-4.5c0-1.9.9-3.7 3.9-3.7h3v-5.9s-2.7-.5-5.4-.5c-5.5 0-9 3.3-9 9.2V24h-6.1v6.9h6.1V48c1.2.2 2.5.3 3.8.3s2.5-.1 3.8-.3V30.9h5.4z"/></svg>'
G_LOGO = '<svg class="g-logo" viewBox="0 0 48 48" aria-hidden="true"><path fill="#EA4335" d="M24 9.5c3.5 0 6.6 1.2 9.1 3.6l6.8-6.8C35.8 2.4 30.3 0 24 0 14.6 0 6.6 5.4 2.6 13.3l7.9 6.2C12.4 13.6 17.7 9.5 24 9.5z"/><path fill="#4285F4" d="M46.1 24.5c0-1.6-.1-3.1-.4-4.5H24v9h12.4c-.5 2.9-2.2 5.3-4.6 6.9l7.1 5.5c4.2-3.9 6.6-9.6 6.6-16.9z"/><path fill="#FBBC05" d="M10.5 28.6c-.5-1.4-.8-3-.8-4.6s.3-3.2.8-4.6l-7.9-6.2C.9 16.5 0 20.1 0 24s.9 7.5 2.6 10.8l7.9-6.2z"/><path fill="#34A853" d="M24 48c6.5 0 11.9-2.1 15.9-5.8l-7.1-5.5c-2.2 1.5-5 2.3-8.8 2.3-6.3 0-11.6-4.2-13.5-9.9l-7.9 6.2C6.6 42.6 14.6 48 24 48z"/></svg>'


def stars(n, total=5):
    return f'<span class="stars" aria-label="{n} out of 5 stars">{"★" * n}<span class="off">{"★" * (total - n)}</span></span>'


def mascot(cls="mascot", lazy=True):
    """The Vouch mascot (transparent webp). Original artwork supplied by Tim, Oct 2026."""
    lz = ' loading="lazy"' if lazy else ""
    return (f'<img class="{cls}" src="/assets/img/mascot.webp" srcset="/assets/img/mascot-sm.webp 320w, '
            f'/assets/img/mascot.webp 560w" sizes="(max-width:820px) 200px, 340px" width="560" height="755" '
            f'alt="Vouch Digital mascot: a plumber giving a thumbs up"{lz}>')


def process_steps(cls="dark process"):
    """'What working with us looks like': the 3-step journey shared by every page."""
    s = "".join(f"""<li><span class="j-num">{n}</span><h3>{t}</h3><p class="j-time">{tm}</p><p class="j-desc">{d}</p></li>"""
                for n, (t, tm, d) in enumerate([
                    ("Quick call", "15 mins",
                     "Yes, it's a sales call. But there's no pressure and no hard sell. We'll show you where "
                     "you're losing jobs online, answer your questions and see if we're a good fit."),
                    ("We build your system", "3–5 days",
                     "Fill in a short onboarding form with your business details. We get to work on your new "
                     "website and everything around it."),
                    ("Launch call", "25 mins",
                     "We walk you through your new website and system, answer any questions, and show you how it "
                     "all works. Then we keep it running while you're out on jobs."),
                ], 1))
    return f"""
<section class="{cls}" id="how">
  <div class="wrap">
    <div class="sec-head"><p class="eyebrow">How it works</p><h2>What working with us looks like</h2></div>
    <ol class="journey">{s}</ol>
  </div>
</section>"""


BOOK = "/book"



def book_buttons(second=("See pricing", "/pricing")):
    return (f'<div class="row"><a class="btn btn-mint" href="{BOOK}">Book a call {icon("arrow")}</a>'
            f'<a class="btn btn-ghost" href="{second[1]}">{second[0]}</a></div>')


def final_cta(h2="Be the plumber everyone vouches for.",
              text="Book a 15-minute call. We'll show you how it works and get your free website started."):
    return f"""
<section class="dark final has-mascot">
  <div class="wrap">
    <div class="final-copy">
    <p class="eyebrow">15 minutes, no hard sell</p>
    <h2>{h2}</h2>
    <p class="muted">{text}</p>
    <div class="row"><a class="btn btn-mint" href="{BOOK}">Book a call {icon('arrow')}</a>
    <a class="btn btn-ghost" href="tel:{SITE['phone_intl']}">{icon('phone')} Call {SITE['phone']}</a></div>
    </div>
    {mascot()}
  </div>
</section>"""


def pricing_section():
    """Single-plan card, centred list with dividers, with monthly/quarterly/annual toggle."""
    p = PLANS[0]
    free = "".join(f'<li class="free">{EXTRAS[k][1]} <b>FREE</b> <small>(save {EXTRAS[k][3]})</small></li>'
                   for k in p["extras"])
    # Included services listed by system, named and linked exactly like the service pages.
    items = ""
    for n, (title, _) in sorted(GROUPS.items(), reverse=True):  # System 2 first: seen as more valuable
        items += "".join(f'<li><a href="/services/{slug}">{d["name"]}</a></li>'
                         for slug, d in SERVICE_PAGES.items() if d["group"] == n and slug != "websites")
    tabs = ""
    for i, b in enumerate(BILLING):
        pill = f"<span>{b['pill']}</span>" if b["pill"] else ""
        selected = "true" if i == 0 else "false"
        tabs += (f'<button type="button" role="tab" id="bill-{b["id"]}" data-bill="{b["id"]}" '
                 f'aria-selected="{selected}">{b["label"]}{pill}</button>')
    data = "".join(
        f'<template data-bill-opt="{b["id"]}" data-per="{b["per_month"]}" data-billed="{b["billed"] or ""}" '
        f'data-save="{b["save"] or ""}"></template>' for b in BILLING)
    return f"""
<section class="tint pricing" id="pricing">
  <div class="wrap">
    <div class="sec-head"><p class="eyebrow">Pricing</p><h2>Our pricing</h2>
    <p>One plan, everything included. Pay monthly with no contract, or pay upfront and save.</p></div>
    <div class="bill-tabs" role="tablist" aria-label="Billing period">{tabs}</div>
    <div class="pk-stage"><img class="pk-lean" src="/assets/img/mascot-lean.webp" width="320" height="475" loading="lazy" alt="Vouch Digital mascot leaning on the pricing card, giving a thumbs up">
    <div class="pk" data-base="{p['price']}">{data}
      <p class="pk-label">Everything included</p>
      <h3>{p['name']}</h3>
      <p class="pk-price"><s class="pk-was" hidden>£{p['price']}</s><b class="pk-num">£{p['price']}</b><span>/month</span></p>
      <p class="pk-billed">Billed monthly.</p>
      <p class="pk-save is-note">No contract, cancel anytime</p>
      <ul>{free}{items}</ul>
      <a class="pk-btn" href="{BOOK}">Book a call</a>
    </div>
    </div>
    <p class="pr-foot">Want just the website? It's £1,499 as a one-off, yours to keep.</p>
  </div>
</section>"""


# One short benefit line per service card (homepage + services page). Groups, names and order
# come from SERVICE_PAGES in services_data.py.
PRODUCT_SHORT = {
    "missed-call-text-back": "Callers get a text back, so they don't ring the next plumber.",
    "lead-follow-up": "Every enquiry answered instantly and every quote chased for you.",
    "all-in-one-inbox": "Every enquiry in one place, so you save time and nothing gets forgotten.",
    "websites": "Free, live in 3–5 days, and built to turn visitors into enquiries.",
    "google-reviews": "Gives homeowners a reason to pick you over the plumber next door.",
    "marketing-campaigns": "Service reminders, offers and referrals sent to past customers automatically.",
    "google-business-profile": "Helps you show up when locals search \u201cplumber near me\u201d in Google and ChatGPT.",
}


def product_groups(current=None):
    """The two systems as side-by-side panels of linked service cards. current = slug of the page you're on."""
    groups = ""
    for n, (title, blurb) in GROUPS.items():
        cards = ""
        for slug, d in SERVICE_PAGES.items():
            if d["group"] != n:
                continue
            here = slug == current
            end = '<span class="here">You\'re here</span>' if here else f'<span class="go">{icon("arrow")}</span>'
            attrs = ' class="is-current" aria-current="page"' if here else ""
            cards += (f'<li><a href="/services/{slug}"{attrs}><span class="ic">{icon(d["icon"])}</span>'
                      f'<span class="txt"><b>{d["name"]}</b><span>{PRODUCT_SHORT[slug]}</span></span>{end}</a></li>')
        groups += f"""
    <div class="prod-group pg-{n}">
      <div class="pg-head"><p class="pg-sys">System {n}</p><h3>{title}</h3><p>{blurb}</p></div>
      <ul class="prod-list">{cards}</ul>
    </div>"""
    return f'<div class="prod-groups">{groups}\n    </div>'


SYS_JOIN = """
    <div class="sys-join">
      <svg class="sj-lines" viewBox="0 0 1000 70" preserveAspectRatio="none" aria-hidden="true">
        <path d="M250 0 C250 45 500 25 500 64" /><path d="M750 0 C750 45 500 25 500 64" /></svg>
      <a class="btn btn-mint" href="/services#how">See how the 2 systems work together {arrow}</a>
    </div>"""


def products_section(cls="products", eyebrow="What we do", h2="2 simple systems that help our plumbers make more money",
                     intro="One stops you losing the jobs you already get. The other wins you more jobs.",
                     join=False):
    joiner = SYS_JOIN.format(arrow=icon("arrow")) if join else ""
    return f"""
<section class="{cls}" id="system">
  <div class="wrap">
    <div class="sec-head"><p class="eyebrow">{eyebrow}</p><h2>{h2}</h2>
    <p>{intro}</p></div>
    {product_groups()}{joiner}
  </div>
</section>"""


def home():
    lose = "".join(f'<li><span class="dot no">{icon("x")}</span>{t}</li>' for t in
                   ["Infrequent reviews", "Not in the top 3 on Google Maps",
                    "Website buried below competitors", "Not mentioned by ChatGPT"])
    win = "".join(f'<li><span class="dot yes">{icon("check")}</span>{t}</li>' for t in
                  ["Fresh reviews every week", "Top 3 on Google Maps",
                   "Website ranks above competitors", "Recommended by ChatGPT"])

    JOBS = (["Dripping taps", "Small call-outs", "Cheapest-quote hunters"],
            ["Boiler installs", "Bathroom installs", "Full heating systems"])

    def jobs(side, cls):
        items = "".join(f"<li>{t}</li>" for t in JOBS[side])
        return f'<ul class="jobs {cls}">{items}</ul>'

    revs = ""
    for r in REVIEWS:
        quote = f"<blockquote>“{escape(r['text'])}”</blockquote>" if r["text"] else \
            '<blockquote class="muted"><em>Left a 5-star rating.</em></blockquote>'
        revs += f"""<figure class="rev">{stars(r['stars'])}{quote}
          <figcaption class="who"><span>{escape(r['name'])}</span>{G_LOGO}</figcaption></figure>"""

    faq = "".join(f"<details><summary>{q}{icon('chevron')}</summary><p>{a}</p></details>"
                  for q, a in FAQ_HOME if not q.startswith("How much"))

    hero_ticks = "".join(f'<li><span class="tick">{icon("check")}</span>{t}</li>' for t in
                         ["Free website, live in 3–5 days", "£197 a month, everything included",
                          "No contract, cancel anytime"])

    return f"""
<main>
<section class="hero dark hero-v2 hero-k">
  <div class="wrap">
    <div class="hero-copy">
      <h1>Website Design &amp; Marketing Systems <span class="accent">For Domestic Plumbers</span></h1>
      <div class="hero-row">
        <p class="hero-blurb"><span>No jargon, no magic tricks, no fake promises.</span><span>No agency... (including ours) has the miracle solution to all your problems. We'll give you the tools to win but you need to commit to using them!</span></p>
        <div class="hero-cta">
          <a class="btn btn-mint" href="{BOOK}">Book a call {icon('arrow')}</a>
          <small>15 minutes, no hard sell</small>
        </div>
      </div>
      <div class="rating-row"><a href="#reviews">{G_LOGO}<span><b>Google</b>{stars(5)}</span><em>{RATING}</em></a>
      <a href="{TRUSTPILOT['url']}" target="_blank" rel="noopener">{TP_ICON}<span><b>Trustpilot</b>{stars(5)}</span><em>{TRUSTPILOT['rating']}</em></a>
      <a href="{FACEBOOK['url'] or '#reviews'}"{' target="_blank" rel="noopener"' if FACEBOOK['url'] else ''}>{FB_LOGO}<span><b>Facebook</b>{stars(5)}</span><em>{FACEBOOK['rating']}</em></a></div>
    </div>
    {mascot("mascot hero-mascot", lazy=False)}
  </div>
</section>

<section class="reviews rev-band" id="reviews">
  <div class="wrap">
    <div class="rev-top">
      <div><p class="eyebrow">What our clients say</p><h2>Plumbers who vouch for us</h2></div>
    </div>
    <div class="rev-grid rev-carousel" tabindex="0" aria-label="Google reviews">{revs}</div>
    <div class="rev-dots" aria-label="Choose review"></div>
  </div>
</section>

{products_section(join=True)}

<section class="tint why">
  <div class="wrap">
    <div class="sec-head">
      <p class="eyebrow">Why it matters</p>
      <h2>Customers pick from the top of Google, and nowadays ChatGPT.</h2>
      <p>More homeowners now ask ChatGPT who to call. It recommends the businesses with the strongest reviews and clearest information online. If that isn't you, the job goes to a competitor.</p>
    </div>
    <div class="searchbar">{icon('search')}<span>plumber near me</span></div>
    <div class="vs">
      <div class="gbp">
        <p class="lbl">Your business</p>
        <h3>Your Plumbing Co.</h3>
        <p class="rating"><b>39 reviews</b> <span class="score">4.6 {stars(5)}</span></p>
        <div class="thumbs"><div>No photos</div><div></div><div></div><div></div></div>
        <ul class="checks">{lose}</ul>
        <div class="call quiet">Phone stays quiet</div>
        <p class="jobs-lbl">Jobs that do come in</p>
        {jobs(0, "small")}
      </div>
      <div class="vs-mid">VS</div>
      <div class="gbp win">
        <span class="badge1">#1 on Google</span>
        <p class="lbl">The business above you</p>
        <h3>Other Plumbing Ltd</h3>
        <p class="rating"><b>214 reviews</b> <span class="score">4.9 {stars(5)}</span></p>
        <div class="thumbs"><div>{icon('tool')}</div><div>{icon('flame')}</div><div>{icon('image')}</div><div>{icon('clock')}</div></div>
        <ul class="checks">{win}</ul>
        <div class="call ring">{icon('phone')} Gets the call</div>
        <p class="jobs-lbl">Jobs they're winning</p>
        {jobs(1, "big")}
      </div>
    </div>
  </div>
</section>

{process_steps()}




<section class="faq" id="faq">
  <div class="wrap">
    <div class="intro">
      <p class="eyebrow">Frequently asked questions</p>
      <h2>Got questions? We've got straight answers.</h2>
      <p>No jargon, no promises we can't keep. More on our <a href="/faq">full FAQ page</a>, or call <a href="tel:{SITE['phone_intl']}">{SITE['phone']}</a>.</p>
    </div>
    <div>{faq}</div>
  </div>
</section>

{final_cta()}
</main>"""


def book():
    ratings = (f'<a href="#">{G_LOGO}<span><b>Google</b>{stars(5)}</span><em>{RATING}</em></a>'
               f'<a href="{TRUSTPILOT["url"]}" target="_blank" rel="noopener">{TP_ICON}<span><b>Trustpilot</b>{stars(5)}</span><em>{TRUSTPILOT["rating"]}</em></a>'
               f'<a href="{FACEBOOK["url"] or "#"}" target="_blank" rel="noopener">{FB_LOGO}<span><b>Facebook</b>{stars(5)}</span><em>{FACEBOOK["rating"]}</em></a>')
    points = "".join(f'<li><span class="tick">{icon("check")}</span>{t}</li>' for t in [
        "We look at your Google profile and website together.",
        "We show you how the 2 systems would work for your business.",
        "No hard sell. If it's not right for you, we'll tell you.",
    ])
    return f"""
<main>
<section class="dark book-hero">
  <div class="wrap">
    <h1>Book your 15-minute call</h1>
    <p class="muted">Pick a time that suits you. 15 minutes on Google Meet.</p>
    <div class="rating-row book-ratings">{ratings}</div>
  </div>
</section>
<section class="book">
  <div class="wrap book-grid">
    <div class="book-info">
      <h2>What happens on the call</h2>
      <ul class="book-points">{points}</ul>
      <div class="worst-case">
        <p class="wc-lbl">Worst case?</p>
        <p>You spend 15 minutes and leave with a clear list of what to fix on your Google profile and website. Do it yourself, and we never work together. No hard feelings.</p>
      </div>
    </div>
    <div class="book-frame">
      <iframe class="booking" title="Book your 15-minute call" data-src="{SITE['booking_url']}" scrolling="no"></iframe>
    </div>
  </div>
  <p class="book-alt wrap">Can't find a time that works? Call or text <a href="tel:{SITE['phone_intl']}">{SITE['phone']}</a> and we'll sort one out.</p>
</section>
</main>
<script src="https://link.msgsndr.com/js/form_embed.js" defer></script>"""


LEGAL_DIR = __import__("pathlib").Path(__file__).parent / "legal"


def legal(name, heading):
    def body():
        content = (LEGAL_DIR / f"{name}.html").read_text(encoding="utf-8")
        return f"""
<main>
<section class="dark page-hero"><div class="wrap"><p class="eyebrow">Vouch Digital</p><h1>{heading}</h1></div></section>
<section class="legal"><div class="wrap">{content}</div></section>
</main>"""
    return body


ALL = [
    {"path": "/", "body": home,
     "title": "Marketing for Domestic Plumbers & Heating Engineers | Vouch Digital",
     "desc": "A free website plus missed-call text-back, Google reviews, your Google profile and local SEO "
             "for domestic plumbers. Set up for you, no contract."},
    {"path": "/book", "body": book, "noindex": True,
     "title": "Book a call | Vouch Digital",
     "desc": "Book a 15-minute call with Vouch Digital."},
    {"path": "/privacy", "body": legal("privacy", "Privacy Policy"),
     "title": "Privacy Policy | Vouch Digital",
     "desc": "How Vouch Digital (Bolotin Ltd) collects, uses and protects personal data."},
    {"path": "/terms", "body": legal("terms", "Terms of Service"),
     "title": "Terms of Service | Vouch Digital",
     "desc": "The terms on which Vouch Digital (Bolotin Ltd) provides its services."},
]
