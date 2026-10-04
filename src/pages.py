"""Page bodies. Each entry in ALL becomes one page."""
from html import escape

from icons import icon
from site_data import SITE, REVIEWS, FAQ_HOME


def stars(n, total=5):
    return f'<span class="stars" aria-label="{n} out of 5 stars">{"★" * n}<span class="off">{"★" * (total - n)}</span></span>'


def audit_form(eyebrow="Free for electricians &amp; plumbers"):
    ticks = "".join(f"<li>{icon('check')} {t}</li>" for t in
                    ["Video call, no hard sell", "No obligation",
                     "Fix it yourself, or we can do it for you"])
    return f"""
<div class="audit" id="audit">
  <p class="eyebrow">{eyebrow}</p>
  <h2>We'll find at least 5 ways you're losing jobs online, and show you how to fix them in 15 minutes, for free.</h2>
  <p class="small">We check your Google reviews, Business Profile and website, then walk you through the biggest opportunities on a video call.</p>
  <ul>{ticks}</ul>
  <form class="enquiry" action="/api/enquiry" method="post" novalidate>
    <div class="field">{icon('user')}<input name="name" placeholder="Your name" autocomplete="name" required aria-label="Your name"></div>
    <div class="field">{icon('building')}<input name="business" placeholder="Business name" autocomplete="organization" required aria-label="Business name"></div>
    <div class="field">{icon('phone')}<input name="phone" type="tel" placeholder="Mobile number" autocomplete="tel" required aria-label="Mobile number"></div>
    <div class="hp" aria-hidden="true"><label>Leave this empty <input name="company_url" tabindex="-1" autocomplete="off"></label></div>
    <input type="hidden" name="t">
    <button class="btn btn-mint btn-block" type="submit">Find My Missed Jobs {icon('arrow')}</button>
    <p class="form-msg" role="status"></p>
    <p class="form-note">No obligation, just honest advice. We'll only use your details to arrange your call. <a href="/privacy">Privacy Policy</a>.</p>
  </form>
</div>"""


SERVICES = [
    ("star", "Google Reviews", "/services/google-reviews",
     "Automatic review requests by text and email after every job, and a reply to every review."),
    ("pin", "Google Business Profile", "/services/google-business-profile",
     "Categories, services, areas, photos and posts set up so you show in the Google Maps results."),
    ("monitor", "Websites", "/services/websites",
     "Fast, mobile-friendly websites built to turn visitors into calls and enquiries."),
    ("trend", "Local SEO", "/services/local-seo",
     "Consistent listings on Bing, Apple Maps, Yell and Checkatrade, built for “near me” searches."),
    ("ai", "AI Search", "/services/ai-search",
     "Clear, trusted content so ChatGPT, Gemini and Google AI Overviews can find and understand you."),
]


def home():
    hero_ticks = "".join(
        f'<li><span class="tick">{icon("check")}</span>{t}</li>' for t in
        ["Genuine Google reviews", "A complete Google profile",
         "A website that converts", "Set up for ChatGPT &amp; AI search"])

    lose = "".join(f'<li><span class="dot no">{icon("x")}</span>{t}</li>' for t in
                   ["Last review 8 months ago", "Opening hours missing",
                    "No services listed", "Website buried below competitors"])
    win = "".join(f'<li><span class="dot yes">{icon("check")}</span>{t}</li>' for t in
                  ["Fresh reviews every week", "Open 24 hours", "Every service listed",
                   "In the local map pack", "Website answers customer questions"])

    trades = "".join(f"<li>{icon(i)}{n}</li>" for i, n in
                     [("bolt", "Electricians"), ("drop", "Plumbers"), ("radiator", "Heating Engineers"),
                      ("flame", "Boiler Installers"), ("plug", "EV Charger Installers"), ("bath", "Bathroom Fitters")])

    svc = "".join(f"""<a class="svc" href="{h}"><span class="ic">{icon(i)}</span>
      <span><h3>{n}</h3><p>{d}</p></span></a>""" for i, n, h, d in SERVICES)
    svc += f"""<a class="svc all" href="/services"><span class="ic">{icon('arrow')}</span>
      <span><h3>All five, working together</h3><p>Stronger as one system than as separate jobs. See how they fit.</p></span></a>"""

    revs = ""
    for r in REVIEWS:
        quote = f"<blockquote>“{escape(r['text'])}”</blockquote>" if r["text"] else \
            '<blockquote class="muted"><em>Left a 5-star rating.</em></blockquote>'
        revs += f"""<figure class="rev">{stars(r['stars'])}{quote}
          <figcaption class="who">{escape(r['name'])}<small>Google review · {r['date']}</small></figcaption></figure>"""

    steps = "".join(f"""<li><div class="ring">{icon(i)}</div><h3>{n}. {t}</h3><p>{d}</p></li>"""
                    for n, (i, t, d) in enumerate([
                        ("clipboard", "Free audit", "We check your reviews, profile and website and show you at least 5 things to fix."),
                        ("target", "Your plan", "We agree what's worth doing for your business and your area."),
                        ("cog", "We set it up", "Review requests, your Google profile, listings and website. You don't lift a finger."),
                        ("chart", "It keeps working", "Reviews and visibility build every month while you're out on jobs."),
                    ], 1))

    faq = "".join(f"<details><summary>{q}{icon('chevron')}</summary><p>{a}</p></details>"
                  for q, a in FAQ_HOME)

    return f"""
<main>
<section class="hero dark">
  <div class="wrap">
    <div>
      <p class="eyebrow">Be the local trade everyone vouches for</p>
      <h1>Win bigger, better-paying jobs from <span class="accent">Google and ChatGPT.</span></h1>
      <p class="lede">Reviews, Google profile, websites and AI search, done for you. <strong>Built only for electricians and plumbers in London &amp; the South East.</strong></p>
      <ul class="ticks">{hero_ticks}</ul>
    </div>
    {audit_form()}
  </div>
</section>

<section class="tint why">
  <div class="wrap">
    <div class="sec-head">
      <p class="eyebrow">Why it matters</p>
      <h2>Most customers choose a business from the top of Google.</h2>
      <p>If your profile or website isn't working for you, the call goes to a competitor.</p>
    </div>
    <div class="trade-toggle" role="group" aria-label="Show example for">
      <button type="button" data-trade="electrician" aria-pressed="true">Electricians</button>
      <button type="button" data-trade="plumber" aria-pressed="false">Plumbers</button>
    </div>
    <div class="searchbar">{icon('search')}<span data-swap="query">emergency electrician near me</span></div>
    <div class="vs">
      <div class="gbp">
        <p class="lbl">Your business</p>
        <h3 data-swap="you">Your Electrical Co.</h3>
        <p class="rating"><b>3.8</b> {stars(4)} (6 reviews)</p>
        <div class="thumbs"><div>No photos</div><div></div><div></div><div></div></div>
        <ul class="checks">{lose}</ul>
        <div class="call quiet">Phone stays quiet</div>
      </div>
      <div class="vs-mid">VS</div>
      <div class="gbp win">
        <span class="badge1">#1 on Google</span>
        <p class="lbl">The business above you</p>
        <h3 data-swap="them">Other Electrical Ltd</h3>
        <p class="rating"><b>4.9</b> {stars(5)} (127 reviews)</p>
        <div class="thumbs"><div>{icon('tool')}</div><div>{icon('bolt')}</div><div>{icon('image')}</div><div>{icon('clock')}</div></div>
        <ul class="checks">{win}</ul>
        <div class="call ring">{icon('phone')} Gets the call</div>
      </div>
    </div>
  </div>
</section>

<section class="trades">
  <div class="wrap">
    <h2>Trusted by electricians and plumbers across London &amp; the South East</h2>
    <ul>{trades}</ul>
  </div>
</section>

<section class="services">
  <div class="wrap">
    <div class="intro">
      <p class="eyebrow">Our services</p>
      <h2>Everything you need to win more local jobs</h2>
      <p>We help electricians and plumbers get found on Google and in AI search, turn clicks into calls, and look like the obvious choice. We handle all of it for you.</p>
      <a class="btn btn-mint" href="#audit">Find My Missed Jobs {icon('arrow')}</a>
    </div>
    <div class="svc-grid">{svc}</div>
  </div>
</section>

<section class="tint reviews">
  <div class="wrap">
    <div class="rev-top">
      <div><p class="eyebrow">What our clients say</p><h2>Trade businesses who vouch for us</h2></div>
      <div class="g-score"><b>5.0</b> {stars(5)} <span>on Google</span></div>
    </div>
    <div class="rev-grid">{revs}</div>
  </div>
</section>

<section class="dark process">
  <div class="wrap">
    <div class="sec-head"><p class="eyebrow">How it works</p><h2>A simple process, with nothing for you to learn</h2></div>
    <ol class="steps">{steps}</ol>
  </div>
</section>

<section class="faq">
  <div class="wrap">
    <div class="intro">
      <p class="eyebrow">Frequently asked questions</p>
      <h2>Got questions? We've got straight answers.</h2>
      <p>No jargon, no promises we can't keep. More on our <a href="/faq">full FAQ page</a>, or call <a href="tel:{SITE['phone_intl']}">{SITE['phone']}</a>.</p>
    </div>
    <div>{faq}</div>
  </div>
</section>

<section class="dark final">
  <div class="wrap">
    <p class="eyebrow">Free, 15 minutes, no hard sell</p>
    <h2>Be the electrician or plumber everyone vouches for.</h2>
    <p class="muted">We'll find at least 5 ways you're losing jobs to competitors on Google, and show you how to fix them.</p>
    <div class="row"><a class="btn btn-mint" href="#audit">Find My Missed Jobs {icon('arrow')}</a>
    <a class="btn btn-ghost" href="tel:{SITE['phone_intl']}">{icon('phone')} Call {SITE['phone']}</a></div>
  </div>
</section>
</main>"""


ALL = [
    {"path": "/", "body": home,
     "title": "Marketing for Electricians & Plumbers in London | Vouch Digital",
     "desc": "We find at least 5 ways London and South East electricians and plumbers are losing jobs "
             "on Google, and fix them. Reviews, Google profile, websites, local SEO and AI search, done for you."},
]
