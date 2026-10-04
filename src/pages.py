"""Page bodies. Each entry in ALL becomes one page."""
from html import escape

from icons import icon
from site_data import SITE, REVIEWS, FAQ_HOME


def stars(n, total=5):
    return f'<span class="stars" aria-label="{n} out of 5 stars">{"★" * n}<span class="off">{"★" * (total - n)}</span></span>'


def audit_form(eyebrow="Free for electricians &amp; plumbers"):
    ticks = "".join(f"<li>{icon('check')} {t}</li>" for t in
                    ["Honest advice, not a sales pitch", "Useful even if you never work with us",
                     "Fix it yourself, or we can do it for you"])
    return f"""
<div class="audit" id="audit">
  <p class="eyebrow">{eyebrow}</p>
  <h2>We'll find <mark>at least 5 ways you're losing jobs</mark> online, and show you how to fix them in 15 minutes, for free.</h2>
  <p class="small">We check everything your business has online, then walk you through your biggest opportunities to win more jobs on a 15-minute video call.</p>
  <ul>{ticks}</ul>
  <form class="enquiry" action="/api/enquiry" method="post" novalidate>
    <div class="field">{icon('user')}<input name="name" placeholder="Your name" autocomplete="name" required aria-label="Your name"></div>
    <div class="field">{icon('building')}<input name="business" placeholder="Business name" autocomplete="organization" required aria-label="Business name"></div>
    <div class="field">{icon('phone')}<input name="phone" type="tel" placeholder="Mobile number" autocomplete="tel" required aria-label="Mobile number"></div>
    <div class="field">{icon('mail')}<input name="email" type="email" placeholder="Email address" autocomplete="email" required aria-label="Email address"></div>
    <div class="hp" aria-hidden="true"><label>Leave this empty <input name="company_url" tabindex="-1" autocomplete="off"></label></div>
    <input type="hidden" name="t">
    <button class="btn btn-mint btn-block" type="submit">Find My Missed Jobs {icon('arrow')}</button>
    <p class="form-msg" role="status"></p>
    <p class="form-note">Next, you'll pick a time that suits you. We'll only use your details to arrange your call. <a href="/privacy">Privacy Policy</a>.</p>
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
                   ["Infrequent reviews", "Not in the top 3 on Google Maps",
                    "Website buried below competitors", "Not mentioned by ChatGPT"])
    win = "".join(f'<li><span class="dot yes">{icon("check")}</span>{t}</li>' for t in
                  ["Fresh reviews every week", "Top 3 on Google Maps",
                   "Website ranks above competitors", "Recommended by ChatGPT"])

    JOBS = {
        "electrician": (["Socket swaps", "Small call-outs", "Cheapest-quote hunters"],
                        ["Full rewires", "Consumer unit upgrades", "EV charger installs"]),
        "plumber": (["Dripping taps", "Small call-outs", "Cheapest-quote hunters"],
                    ["Boiler installs", "Bathroom installs", "Full heating systems"]),
    }

    def jobs(side, cls):
        out = ""
        for trade, lists in JOBS.items():
            items = "".join(f"<li>{t}</li>" for t in lists[side])
            hidden = "" if trade == "electrician" else " hidden"
            out += f'<ul class="jobs {cls}" data-for="{trade}"{hidden}>{items}</ul>'
        return out

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

    finds = "".join(f"""<li class="find"><span class="ic">{icon(i)}</span><div><h3>{t}</h3><p>{d}</p></div></li>"""
                    for i, t, d in [
                        ("star", "Your reviews", "How many you have, how recent they are, and whether you're replying, compared with the three businesses above you."),
                        ("pin", "Your Google profile", "Missing services, categories, service areas, hours and photos that stop you showing in the map results."),
                        ("search", "Where you rank", "Where you appear for searches like “electrician near me” and “emergency plumber” in your area."),
                        ("monitor", "Your website", "How it looks and loads on a phone, and whether it makes calling you easy."),
                        ("link", "Your listings", "Whether your name, address and number match on Yell, Checkatrade, Bing and Apple Maps."),
                        ("ai", "ChatGPT", "Who ChatGPT recommends when someone asks for a trade like yours in your area, and whether it's you."),
                    ])

    steps = "".join(f"""<li><div class="ring">{icon(i)}</div><h3>{n}. {t}</h3><p>{d}</p></li>"""
                    for n, (i, t, d) in enumerate([
                        ("clipboard", "Free audit", "We check your reviews, profile and website and show you at least 5 things to fix."),
                        ("target", "Your plan", "We agree what's worth doing for your business and your area."),
                        ("cog", "20-minute setup", "One short call to connect your Google profile and customer list. We handle everything else."),
                        ("chart", "It keeps working", "Reviews and visibility build every month while you're out on jobs."),
                    ], 1))

    faq = "".join(f"<details><summary>{q}{icon('chevron')}</summary><p>{a}</p></details>"
                  for q, a in FAQ_HOME)

    return f"""
<main>
<section class="hero dark has-img">
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
      <h2>Customers pick from the top of Google, and nowadays ChatGPT.</h2>
      <p>More homeowners now ask ChatGPT who to call. It recommends the businesses with the strongest reviews and clearest information online. If that isn't you, the job goes to a competitor.</p>
    </div>
    <div class="trade-toggle" role="group" aria-label="Show example for">
      <button type="button" data-trade="electrician" aria-pressed="true">Electricians</button>
      <button type="button" data-trade="plumber" aria-pressed="false">Plumbers</button>
    </div>
    <div class="searchbar">{icon('search')}<span data-swap="query">electrician near me</span></div>
    <div class="vs">
      <div class="gbp">
        <p class="lbl">Your business</p>
        <h3 data-swap="you">Your Electrical Co.</h3>
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
        <h3 data-swap="them">Other Electrical Ltd</h3>
        <p class="rating"><b>214 reviews</b> <span class="score">4.9 {stars(5)}</span></p>
        <div class="thumbs"><div>{icon('tool')}</div><div>{icon('bolt')}</div><div>{icon('image')}</div><div>{icon('clock')}</div></div>
        <ul class="checks">{win}</ul>
        <div class="call ring">{icon('phone')} Gets the call</div>
        <p class="jobs-lbl">Jobs they're winning</p>
        {jobs(1, "big")}
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

<section class="check">
  <div class="wrap">
    <div class="sec-head">
      <p class="eyebrow">Your free Missed Jobs Check</p>
      <h2>What we'll show you in 15 minutes</h2>
      <p>We look at your business the way a homeowner does when they search, then show you on screen exactly where jobs are slipping to competitors, and how to fix each one.</p>
    </div>
    <ul class="finds">{finds}</ul>
    <p class="check-cta"><a class="btn btn-mint" href="#audit">Find My Missed Jobs {icon('arrow')}</a><span>Fix it yourself afterwards, or we can do it for you.</span></p>
  </div>
</section>

<section class="services tint-soft">
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


def book():
    return f"""
<main>
<section class="dark book-hero">
  <div class="wrap">
    <p class="eyebrow">Step 2 of 2</p>
    <h1><span data-first>Nice one.</span> Now pick a time for your free check.</h1>
    <p class="muted">15 minutes on Google Meet. Your details are already filled in, so just choose a slot.</p>
  </div>
</section>
<section class="book">
  <div class="wrap">
    <div class="book-frame">
      <iframe class="booking" title="Book your free Missed Jobs Check" data-src="{SITE['booking_url']}"></iframe>
    </div>
    <p class="book-alt">Can't find a time that works? Call or text <a href="tel:{SITE['phone_intl']}">{SITE['phone']}</a> and we'll sort one out.</p>
  </div>
</section>
</main>
<script src="https://link.msgsndr.com/js/form_embed.js" defer></script>"""


ALL = [
    {"path": "/", "body": home,
     "title": "Marketing for Electricians & Plumbers in London | Vouch Digital",
     "desc": "We find at least 5 ways London and South East electricians and plumbers are losing jobs "
             "on Google, and fix them. Reviews, Google profile, websites, local SEO and AI search, done for you."},
    {"path": "/book", "body": book, "noindex": True,
     "title": "Pick a time | Vouch Digital",
     "desc": "Book your free 15-minute Missed Jobs Check with Vouch Digital."},
]
