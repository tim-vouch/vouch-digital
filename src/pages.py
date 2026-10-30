"""Page bodies. Each entry in ALL becomes one page."""
from html import escape

from icons import icon
from services_data import SERVICE_PAGES, GROUPS
from site_data import SITE, REVIEWS, RATING, GOOGLE, FACEBOOK, TRUSTPILOT, FAQ_HOME, PLANS, EXTRAS, BILLING, EXCLUSIVE, TESTIMONIAL_VIDEOS


TP_ICON = '<svg class="tp-ico" viewBox="0 0 48 48" aria-hidden="true"><path fill="#00B67A" d="M24 3l5.6 15.6H46L32.7 28.2 37.8 44 24 34.3 10.2 44l5.1-15.8L2 18.6h16.4z"/><path fill="#005128" d="M33.6 30.9l-1-2.7-8.6 6.1z"/></svg>'
FB_LOGO = '<svg class="fb-logo" viewBox="0 0 48 48" aria-hidden="true"><circle cx="24" cy="24" r="24" fill="#1877F2"/><path fill="#fff" d="M33.3 30.9l1.1-6.9h-6.6v-4.5c0-1.9.9-3.7 3.9-3.7h3v-5.9s-2.7-.5-5.4-.5c-5.5 0-9 3.3-9 9.2V24h-6.1v6.9h6.1V48c1.2.2 2.5.3 3.8.3s2.5-.1 3.8-.3V30.9h5.4z"/></svg>'
G_LOGO = '<svg class="g-logo" viewBox="0 0 48 48" aria-hidden="true"><path fill="#EA4335" d="M24 9.5c3.5 0 6.6 1.2 9.1 3.6l6.8-6.8C35.8 2.4 30.3 0 24 0 14.6 0 6.6 5.4 2.6 13.3l7.9 6.2C12.4 13.6 17.7 9.5 24 9.5z"/><path fill="#4285F4" d="M46.1 24.5c0-1.6-.1-3.1-.4-4.5H24v9h12.4c-.5 2.9-2.2 5.3-4.6 6.9l7.1 5.5c4.2-3.9 6.6-9.6 6.6-16.9z"/><path fill="#FBBC05" d="M10.5 28.6c-.5-1.4-.8-3-.8-4.6s.3-3.2.8-4.6l-7.9-6.2C.9 16.5 0 20.1 0 24s.9 7.5 2.6 10.8l7.9-6.2z"/><path fill="#34A853" d="M24 48c6.5 0 11.9-2.1 15.9-5.8l-7.1-5.5c-2.2 1.5-5 2.3-8.8 2.3-6.3 0-11.6-4.2-13.5-9.9l-7.9 6.2C6.6 42.6 14.6 48 24 48z"/></svg>'


def first_name(name):
    """Reviewers are shown by first name only everywhere (no surname, no initial)."""
    return (name or "").strip().split()[0] if (name or "").strip() else ""


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
                    ("Demo call", "15 mins",
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


BOOK = "/book-form"  # every "Book a call" outside the funnel opens the landing page in a new tab
NEWTAB = ' target="_blank" rel="noopener"'



def book_buttons(second=("See pricing", "/pricing")):
    return (f'<div class="row"><a class="btn btn-mint" href="{BOOK}"{NEWTAB}>Book a call {icon("arrow")}</a>'
            f'<a class="btn btn-ghost" href="{second[1]}">{second[0]}</a></div>')


def final_cta(h2="Be the plumber everyone vouches for.",
              text="Book a 15-minute call. We'll show you how it works and get your free website started."):
    return f"""
<section class="dark final has-mascot">
  <div class="wrap">
    <div class="final-copy">
    <p class="eyebrow">15-minute demo call</p>
    <h2>{h2}</h2>
    <p class="muted">{text}</p>
    <div class="row"><a class="btn btn-mint" href="{BOOK}"{NEWTAB}>Book a call {icon('arrow')}</a>
    <a class="btn btn-ghost" href="tel:{SITE['phone_intl']}">{icon('phone')} Call {SITE['phone']}</a></div>
    </div>
    {mascot()}
  </div>
</section>"""


def pricing_section(h1=None, lede=None):
    """Growth and Exclusive side by side (Exclusive is the price anchor), with one monthly/annual toggle.
    h1: on /pricing the section is the top of the page, so it carries the page's H1 (no separate banner)."""
    p, x = PLANS[0], EXCLUSIVE
    # Growth items open in place (a short benefit) with a link to their service page.
    def more(summary, text, href=None):
        link = f' <a href="{href}">Learn more</a>' if href else ""
        return f'<li class="pk-more"><details><summary>{summary}</summary><p>{text}{link}</p></details></li>'
    # The free website is the headline bonus, so it gets its own highlighted box above the list.
    w = EXTRAS["website"]
    free = f"""<div class="pk-bonus">
        <p class="pk-bonus-tag">Free bonus when you join</p>
        <p class="pk-bonus-name">{w[1]}</p>
        <p class="pk-bonus-price"><span>Normally <b>{w[3]}</b></span><strong>FREE</strong></p>
        <p class="pk-bonus-note">Built for you in roughly 3–5 days to turn visitors into enquiries. <a href="/services/websites">Learn more</a></p>
      </div>"""
    items = ""
    for n, (title, _) in sorted(GROUPS.items()):  # System 1 (Win more jobs) first: seen as more valuable
        items += "".join(more(d["name"], PRODUCT_SHORT[slug], f"/services/{slug}")
                         for slug, d in SERVICE_PAGES.items() if d["group"] == n and slug != "websites")
    # Exclusive extras have no service pages, so each one opens to explain itself.
    x_items = "".join(more(t, d) for t, d in x["items"])
    tabs = ""
    for i, b in enumerate(BILLING):
        pill = f"<span>{b['pill']}</span>" if b["pill"] else ""
        selected = "true" if i == 0 else "false"
        tabs += (f'<button type="button" role="tab" id="bill-{b["id"]}" data-bill="{b["id"]}" '
                 f'aria-selected="{selected}">{b["label"]}{pill}</button>')
    tpl = lambda bid, per, billed, save: (f'<template data-bill-opt="{bid}" data-per="{per}" '
                                          f'data-billed="{billed or ""}" data-save="{save or ""}"></template>')
    g_data = "".join(tpl(b["id"], b["per_month"], b["billed"], b["save"]) for b in BILLING)
    x_data = "".join(tpl(bid, *v) for bid, v in x["billing"].items())
    return f"""
<section class="tint pricing{' first' if h1 else ''}" id="pricing">
  <div class="wrap">
    <div class="sec-head"><p class="eyebrow">Pricing</p>{f'<h1>{h1}</h1>' if h1 else '<h2>Our pricing</h2>'}
    <p>{lede or 'Pay monthly with no contract, or pay upfront and save.'}</p></div>
    <div class="bill-tabs" role="tablist" aria-label="Billing period">{tabs}</div>
    <div class="pk-stage"><img class="pk-lean" src="/assets/img/mascot-lean.webp" width="320" height="475" loading="lazy" alt="Vouch Digital mascot leaning on the pricing card, giving a thumbs up">
    <div class="pk-row">
    <div class="pk" data-base="{p['price']}" data-note="No contract, cancel anytime">{g_data}
      <h3>{p['name']}</h3>
      <p class="pk-price"><s class="pk-was" hidden>£{p['price']}</s><b class="pk-num">£{p['price']}</b><span>/month</span></p>
      <p class="pk-billed">Billed monthly.</p>
      <p class="pk-save is-note">No contract, cancel anytime</p>
      {free}
      <ul>{items}</ul>
      <a class="pk-btn" href="{BOOK}"{NEWTAB}>Book a call</a>
    </div>
    <div class="pk pk-x" data-base="{x['price']}" data-note="{x['pill']}">{x_data}
      <h3>{x['name']}</h3>
      <p class="pk-price"><s class="pk-was" hidden>£{x['price']}</s><b class="pk-num">£{x['price']}</b><span>/month</span></p>
      <p class="pk-billed">Billed monthly.</p>
      <p class="pk-save is-note">{x['pill']}</p>
      <p class="pk-ads">{x['note']}</p>
      <p class="pk-all">Everything in the {p['name']}, plus:</p>
      <ul>{x_items}</ul>
      <a class="pk-btn" href="{BOOK}"{NEWTAB}>Book a call</a>
    </div>
    </div>
    </div>
    <p class="pr-foot">Want just the website? It's £1,499 as a one-off, yours to keep.</p>
  </div>
</section>"""


# One short benefit line per service card (homepage + services page). Groups, names and order
# come from SERVICE_PAGES in services_data.py.
PRODUCT_SHORT = {
    "missed-call-text-back": "Callers get a text back, so they don't ring the next plumber.",
    "lead-follow-up": "Every enquiry answered instantly, so they don't move on to the next plumber.",
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


def products_section(cls="products", eyebrow="What we do", h2="2 simple systems that help our plumbers win more boiler installs",
                     intro="One wins you more jobs. The other makes sure you don't lose the ones you get.",
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
          <figcaption class="who"><span>{escape(first_name(r['name']))}</span>{G_LOGO}</figcaption></figure>"""

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
          <a class="btn btn-mint" href="{BOOK}"{NEWTAB}>Book a call {icon('arrow')}</a>
        </div>
      </div>
      <div class="rating-row"><a href="#reviews">{G_LOGO}<span><b>Google</b>{stars(5)}</span><em>{RATING}</em></a>
      <a href="#reviews">{TP_ICON}<span><b>Trustpilot</b>{stars(5)}</span><em>{TRUSTPILOT['rating']}</em></a>
      <a href="#reviews">{FB_LOGO}<span><b>Facebook</b>{stars(5)}</span><em>{FACEBOOK['rating']}</em></a></div>
    </div>
    {mascot("mascot hero-mascot", lazy=False)}
  </div>
</section>

<section class="reviews rev-band" id="reviews">
  <div class="wrap">
    <div class="rev-top">
      <div><p class="eyebrow">What our clients say</p><h2>Plumbers who vouch for us</h2></div>
    </div>
    {lp_video_tests()}
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


def book_intro():
    """Trade Scale style: Tim's ~30-second portrait clip, right above the calendar. Placeholder until recorded.
    The full VSL is not here (it would slow booking down); it goes out on WhatsApp after booking."""
    if not SITE.get("book_video"):
        return ('<div class="book-intro book-ph"><span class="vp-btn" aria-hidden="true"><svg viewBox="0 0 24 24">'
                '<path d="M9 6.5v11l9-5.5z"/></svg></span><p>Tim\'s 30-second video<br><small>coming soon</small></p></div>')
    poster = f' poster="{SITE["book_video_poster"]}"' if SITE.get("book_video_poster") else ""
    return (f'<div class="book-intro"><video controls playsinline preload="metadata"{poster}>'
            f'<source src="{SITE["book_video"]}" type="video/mp4"></video></div>')


def book_vsl_below():
    """The full walkthrough promised on the landing page, under the calendar so it never slows booking down."""
    if not SITE.get("vsl_url"):
        return ""
    return f"""
  <div class="wrap book-vsl-below"><p class="eyebrow">Here's the video</p><h2>How it all works</h2>{vsl_player()}</div>"""


def book():
    """'Wait, here's what happens next' (Chris Dylan): Tim's 30-second clip, then the calendar straight under it,
    nothing else to distract (Trade Scale layout)."""
    ratings = (f'<a href="#">{G_LOGO}<span><b>Google</b>{stars(5)}</span><em>{RATING}</em></a>'
               f'<a href="{TRUSTPILOT["url"]}" target="_blank" rel="noopener">{TP_ICON}<span><b>Trustpilot</b>{stars(5)}</span><em>{TRUSTPILOT["rating"]}</em></a>'
               f'<a href="{FACEBOOK["url"] or "#"}" target="_blank" rel="noopener">{FB_LOGO}<span><b>Facebook</b>{stars(5)}</span><em>{FACEBOOK["rating"]}</em></a>')
    if SITE.get("calendar_ready"):
        # Our own Trade Scale-style booking box (times from GHL via /api/slots). If that fails (e.g. no GHL_TOKEN
        # in Cloudflare), site.js swaps in GHL's own calendar widget from the template.
        cal = (f'<div class="bk" id="booker" aria-live="polite"><p class="bk-loading">Loading available times…</p></div>'
               f'<template id="booker-fallback"><iframe class="booking" title="Book your 15-minute call" '
               f'data-src="{SITE['booking_url']}" scrolling="no"></iframe></template>')
    else:
        cal = '<div class="cal-ph"><p><b>Booking calendar</b><br>Pick a time for your free 15-minute call here.</p></div>'
    return f"""
<main>
<section class="book-hero book-light">
  <div class="wrap">
    <h1>Wait<span data-first></span>! There's 1&nbsp;More&nbsp;Step&nbsp;<span aria-hidden="true">👇</span></h1>
    <p class="muted">Watch this quick video on what happens next.<br>Then pick a time for your free call below.</p>
    <div class="rating-row book-ratings lp-ratings">{ratings}</div>
    {book_intro()}
  </div>
</section>
<section class="book book-one" id="calendar">
  <div class="wrap">
    <div class="book-frame">{cal}</div>
  </div>
  {book_vsl_below()}
</section>
</main>
<script src="https://link.msgsndr.com/js/form_embed.js" defer></script>"""


# ---------- Meta ads funnel (Oct 2026): ad → /book-form (quiz) → /book-call (clip + booking box); the VSL goes out on WhatsApp ----------
# Kai Stone's flow: they book, then watch the video before the call so they arrive pre-sold.
# Ben Heath (10.2): match the ad, lots of proof, one action, every CTA goes back to the same form.

# Landing page: every Google review with text, newest first (same source as the homepage).


def lp_reviews():
    out = ""
    for r in REVIEWS:
        if not r["text"]:
            continue
        first = escape(first_name(r["name"]))
        out += f"""<figure class="rev">{stars(r['stars'])}<blockquote>“{escape(r['text'])}”</blockquote>
          <figcaption class="who"><span>{first}</span>{G_LOGO}</figcaption></figure>"""
    return out


def lp_cases(only=None):
    cases = [
        ("lp-flotech.webp", 940, 530, "Flotech Heating and Plumbing",
         "<em>12 new</em> Google reviews in his first week",
         "Darren went from 195 to 200 reviews in a single day. He never has to worry about Google reviews again.",
         "Darren's Google reviews, the day before and 24 hours later",
         "Real client, real reviews. Results vary by business."),
        ("lp-mst.webp", 885, 543, "MST Plumbing and Heating",
         "A premium website, <em>done for him</em>",
         "Custom-designed for Andres, with a premium feel to match the high-end London homes he works in.",
         "Andres approving his new website on WhatsApp, next to the site on a phone",
         "The site we built for MST Plumbing and Heating, West London."),
    ]
    out = ""
    for img, w, h, biz, h3, text, alt, note in cases:
        if only and img != only:
            continue
        out += f"""
      <article class="lp-case">
        <img src="/assets/img/{img}" width="{w}" height="{h}" alt="{alt}" loading="lazy">
        <div class="lp-case-copy"><p class="lp-biz">{biz}</p><h3>{h3}</h3><p>{text}</p><p class="lp-note">{note}</p></div>
      </article>"""
    return out


def lp_stack():
    """Offer stack. Cut from the landing page on 30 Oct 2026 (Hormozi: shorter converts better). Kept to re-test."""
    p = PLANS[0]
    free = "".join(f'<li class="free"><span class="tick">{icon("check")}</span><span><b>{EXTRAS[k][1]}</b>'
                   f'<small>{EXTRAS[k][2]}</small></span><em><s>{EXTRAS[k][3]}</s> FREE</em></li>'
                   for k in p["extras"])
    items = "".join(f'<li><span class="tick">{icon("check")}</span><span><b>{n}</b><small>{d}</small></span></li>'
                    for n, d in p["items"])
    return f"""
<section class="tint lp-stack">
  <div class="wrap">
    <div class="sec-head"><p class="eyebrow">What you get</p><h2>Everything in the Vouch System</h2>
    <p>One plan, done for you. Your website comes free when you join.</p></div>
    <div class="lp-stack-card">
      <p class="lp-stack-lbl">Your joining bonus</p>
      <ul>{free}</ul>
      <p class="lp-stack-lbl">Every month, set up and run for you</p>
      <ul>{items}</ul>
      <div class="lp-price"><p><b>£{p['price']}</b><span>/month</span></p><p>No contract. Cancel anytime.</p></div>
      <a class="btn btn-mint btn-block" href="#start">Book my free call {icon('arrow')}</a>
    </div>
  </div>
</section>"""


def vsl_player(cls="lp-vsl"):
    """The VSL as a click-to-play facade: nothing loads from the video host until the visitor presses play."""
    vsl = SITE.get("vsl_url")
    if not vsl:
        return ""
    sep = "&" if "?" in vsl else "?"
    return (f'<div class="svc-video {cls}"><button type="button" class="vsl-play" data-embed="{vsl}{sep}autoplay=1" '
            f'aria-label="Play the video">{vsl_poster_inner()}</button></div>')


def vsl_poster_inner():
    if SITE.get("vsl_poster"):
        art = f'<img src="{SITE["vsl_poster"]}" alt="" loading="lazy">'
    else:
        art = (f'<span class="vp-art"><span class="vp-copy"><b>How we win plumbers more jobs</b>'
               f'<small>A quick walkthrough with Tim, founder of Vouch Digital</small></span>'
               f'<img src="/assets/img/mascot-sm.webp" alt="" width="320" height="431" loading="lazy"></span>')
    return f'{art}<span class="vp-btn" aria-hidden="true"><svg viewBox="0 0 24 24"><path d="M9 6.5v11l9-5.5z"/></svg></span>'


QUIZ = [
    # (field, question, [(value, label)]) for choices, or (field, question, input type, placeholder, autocomplete)
    ("work", "What kind of work do you do?", [
        ("domestic", "Domestic (homeowners)"), ("commercial", "Commercial"),
        ("mixed", "Both domestic &amp; commercial"), ("not", "I'm not a plumber or heating engineer")]),
    ("phone", "Your mobile number", "tel", "07700 900123", "tel"),
    ("email", "What's your best email?", "email", "you@yourbusiness.co.uk", "email"),
    ("name", "Your name", "text", "First and last name", "name"),
    ("business", "What's your business called?", "text", "e.g. Smith Plumbing &amp; Heating", "organization"),
]
# Endowed-progress bar (as on Kai Stone's quiz): starts at 60% and creeps up, so it always feels nearly done.
QUIZ_PROGRESS = [60, 76, 86, 93, 98]


def lp_quiz():
    steps = ""
    last = len(QUIZ) - 1
    for i, q in enumerate(QUIZ):
        field, question = q[0], q[1]
        if isinstance(q[2], list):
            body = "".join(f'<button type="button" class="qz-choice" data-value="{v}">{t}</button>' for v, t in q[2])
            body = f'<div class="qz-choices">{body}</div>'
        else:
            _, _, typ, ph, auto = q
            btn = "Yes, I want more jobs" if i == last else "Continue"
            mode = ' inputmode="tel"' if typ == "tel" else ""
            body = (f'<input class="qz-input" type="{typ}" name="{field}" placeholder="{ph}" autocomplete="{auto}"{mode} '
                    f'aria-label="{question}"><p class="qz-err" role="alert"></p>'
                    f'<button type="button" class="qz-next">{btn}</button>')
        steps += (f'<div class="qz-step" data-field="{field}" data-progress="{QUIZ_PROGRESS[i]}" hidden>'
                  f'<h3 id="qz-q{i}">{question}</h3>{body}</div>')
    steps += f"""<div class="qz-step qz-end" data-end hidden>
        <h3>Thanks for your interest</h3>
        <p>We only work with domestic plumbing and heating businesses, so we're not the right fit for you. If that changes, call or text {SITE['phone']}.</p>
        <button type="button" class="qz-next" data-quiz-close>Close</button></div>"""
    return f"""
<div class="qz" id="quiz" hidden>
  <div class="qz-box" role="dialog" aria-modal="true" aria-labelledby="qz-title">
    <button type="button" class="qz-x" data-quiz-close aria-label="Close">{icon('x')}</button>
    <p class="qz-title" id="qz-title">We Help Plumbers Get More Jobs For Just <b>£197/month</b></p>
    <div class="qz-top"><button type="button" class="qz-back">← Back</button>
    <div class="qz-bar" role="progressbar" aria-label="Progress" aria-valuemin="0" aria-valuemax="100"><span></span><em></em></div></div>
    <form class="qz-form" action="/api/enquiry" method="post" novalidate>
      {steps}
      <input type="hidden" name="src" value="free-website"><input type="hidden" name="t" value="">
      <input type="hidden" name="work">
      <label class="hp" aria-hidden="true">Leave this empty<input type="text" name="company_url" tabindex="-1" autocomplete="off"></label>
    </form>
  </div>
</div>"""


def lp_video_tests():
    """Client video testimonials: still + red play button, the client's result quote beside it. Self-hosted MP4,
    nothing loads until play is pressed (no third-party cookies)."""
    if not TESTIMONIAL_VIDEOS:
        return ""
    play = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M9 6.5v11l9-5.5z"/></svg>'
    cards = "".join(f"""
      <figure class="vt">
        <div class="vt-media">
          <video preload="none" playsinline disablepictureinpicture controlslist="nodownload noplaybackrate" poster="{v['poster']}" aria-label="Video testimonial from {v['name']}, {v['business']}"><source src="{v['src']}" type="video/mp4"></video>
          <button type="button" class="vt-play" aria-label="Play {v['name']}'s video"><span class="vp-btn">{play}</span><span class="vt-len">{v.get('length', '')}</span></button>
        </div>
        <figcaption>
          {stars(5)}
          <blockquote>“{'<br>'.join(v['quote']) if isinstance(v['quote'], list) else v['quote']}”</blockquote>
          <p class="vt-who"><b>{v['name']}</b><small>{v['business']}</small></p>
        </figcaption>
      </figure>""" for v in TESTIMONIAL_VIDEOS)
    return f'<div class="vt-grid">{cards}\n    </div>'


def free_website():
    """Kai Stone's layout (30 Oct 2026): one headline with the price, the VSL thumbnail, one button that opens a
    multi-step quiz popup, then video testimonials and Google reviews. Every CTA opens the same quiz."""
    ratings = (f'<a href="#reviews">{G_LOGO}<span><b>Google</b>{stars(5)}</span><em>{RATING}</em></a>'
               f'<a href="#reviews">{TP_ICON}<span><b>Trustpilot</b>{stars(5)}</span><em>{TRUSTPILOT["rating"]}</em></a>'
               f'<a href="#reviews">{FB_LOGO}<span><b>Facebook</b>{stars(5)}</span><em>{FACEBOOK["rating"]}</em></a>')
    # Kai Stone style: a blurred still with a big play button. Clicking it (or the button) opens the quiz; the
    # video itself comes after (below the calendar on /book-call and on WhatsApp).
    media = f'<button type="button" class="lp-poster" data-quiz-open aria-label="Watch the video">{vsl_poster_inner()}</button>'
    cta = "Click to see how it works"
    return f"""
<main class="lp lp-k">
<section class="lp-k-hero">
  <div class="wrap">
    <h1>We Help Plumbers Get More Jobs With 5-Star Reviews, Smart Websites, and Referrals For Just</h1>
    <p class="lp-k-price">£197/month <span aria-hidden="true">👇</span></p>
    <p class="lp-k-free">+ your new website <b>FREE</b> (normally £1,499) · No contract</p>
    <div class="lp-k-media">{media}</div>
    <a class="lp-k-btn" href="/book-call" data-quiz-open>{cta}</a>
    <div class="rating-row lp-ratings">{ratings}</div>
  </div>
</section>

<section class="lp-k-proof tint" id="reviews">
  <div class="wrap">
    <div class="sec-head"><h2>Plumbers who vouch for us</h2></div>
    {lp_video_tests()}
    <div class="rev-grid rev-carousel lp-revs" tabindex="0" aria-label="Google reviews">{lp_reviews()}</div>
    <div class="rev-dots" aria-label="Choose review"></div>
    <p class="lp-k-again"><a class="lp-k-btn" href="/book-call" data-quiz-open>{cta}</a></p>
  </div>
</section>
{lp_quiz()}
</main>"""


LEGAL_DIR = __import__("pathlib").Path(__file__).parent / "legal"


def legal(name, heading):
    def body():
        content = (LEGAL_DIR / f"{name}.html").read_text(encoding="utf-8")
        return f"""
<main>
<section class="page-hero"><div class="wrap"><p class="eyebrow">Vouch Digital</p><h1>{heading}</h1></div></section>
<section class="legal"><div class="wrap">{content}</div></section>
</main>"""
    return body


ALL = [
    {"path": "/", "body": home,
     "title": "Marketing for Domestic Plumbers & Heating Engineers | Vouch Digital",
     "desc": "A free website plus missed-call text-back, Google reviews, your Google profile and local SEO "
             "for domestic plumbers. Set up for you, no contract."},
    {"path": "/book-call", "body": book, "noindex": True,
     "title": "Book a call | Vouch Digital",
     "desc": "Book a 15-minute call with Vouch Digital."},
    {"path": "/book-form", "body": free_website, "noindex": True,
     "title": "Get a FREE website built to win boiler installs | Vouch Digital",
     "desc": "Join the Vouch System for £197 a month and get your new website free (normally £1,499). "
             "Done for you, no contract."},
    {"path": "/privacy", "body": legal("privacy", "Privacy Policy"),
     "title": "Privacy Policy | Vouch Digital",
     "desc": "How Vouch Digital (Bolotin Ltd) collects, uses and protects personal data."},
    {"path": "/terms", "body": legal("terms", "Terms of Service"),
     "title": "Terms of Service | Vouch Digital",
     "desc": "The terms on which Vouch Digital (Bolotin Ltd) provides its services."},
]
