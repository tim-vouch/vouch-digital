"""Inner pages: services, trades, about, FAQ, contact.

House rules (see CLAUDE.md): no invented results or reviews, no promises of rankings,
results timescales or AI recommendations, no prices. Domestic plumbers only, UK-wide.
"""
from icons import icon
from site_data import SITE, FAQ_HOME, PLANS, EXTRAS, BILLING
from pages import process_steps, mascot, pricing_section, products_section, product_groups, final_cta, book_buttons
from services_data import SERVICE_PAGES, GROUPS


# ---------- building blocks ----------

def hero(eyebrow, h1, lede, form=True, form_eyebrow=None):
    """Light page heading for inner pages (only the homepage has the big dark hero).
    form=True adds the Book a call buttons (the old audit form is retired)."""
    buttons = book_buttons() if form else ""
    return f"""
<section class="page-hero">
  <div class="wrap">
    <p class="eyebrow">{eyebrow}</p>
    <h1>{h1}</h1>
    <p class="lede">{lede}</p>
    {buttons}
  </div>
</section>"""


def cards(items, eyebrow, h2, intro="", cls="", linked=False):
    """items: (icon, title, text) or (icon, title, text, href) when linked."""
    out = ""
    for it in items:
        i, t, d = it[0], it[1], it[2]
        inner = f'<span class="ic">{icon(i)}</span><div><h3>{t}</h3><p>{d}</p></div>'
        out += (f'<li><a class="find link" href="{it[3]}">{inner}</a></li>' if linked
                else f'<li class="find">{inner}</li>')
    intro_p = f"<p>{intro}</p>" if intro else ""
    return f"""
<section class="{cls}">
  <div class="wrap">
    <div class="sec-head"><p class="eyebrow">{eyebrow}</p><h2>{h2}</h2>{intro_p}</div>
    <ul class="finds">{out}</ul>
  </div>
</section>"""


def prose(eyebrow, h2, paras, cls=""):
    body = "".join(p if p.startswith("<") else f"<p>{p}</p>" for p in paras)
    return f"""
<section class="{cls}">
  <div class="wrap prose">
    <p class="eyebrow">{eyebrow}</p>
    <h2>{h2}</h2>
    {body}
  </div>
</section>"""


def split(h2, left_title, left, right_title, right, cls="tint"):
    li = lambda xs, ok: "".join(
        f'<li><span class="dot {"yes" if ok else "you"}">{icon("check" if ok else "user")}</span>{x}</li>' for x in xs)
    return f"""
<section class="{cls}">
  <div class="wrap">
    <div class="sec-head"><h2>{h2}</h2></div>
    <div class="split">
      <div class="split-col"><h3>{left_title}</h3><ul class="checks">{li(left, False)}</ul></div>
      <div class="split-col win"><h3>{right_title}</h3><ul class="checks">{li(right, True)}</ul></div>
    </div>
  </div>
</section>"""


steps = process_steps


def faq(items, h2="Got questions? We've got straight answers.", intro=None, h1=None, eyebrow="Frequently asked questions"):
    qs = "".join(f"<details><summary>{q}{icon('chevron')}</summary><p>{a}</p></details>" for q, a in items)
    intro = intro or f"No jargon, no promises we can't keep. Anything else, call <a href=\"tel:{SITE['phone_intl']}\">{SITE['phone']}</a>."
    return f"""
<section class="faq{' first' if h1 else ''}" id="faq">
  <div class="wrap">
    <div class="intro">
      <p class="eyebrow">{eyebrow}</p>
      {f'<h1>{h1}</h1>' if h1 else f'<h2>{h2}</h2>'}
      <p>{intro}</p>
    </div>
    <div>{qs}</div>
  </div>
</section>"""


def final(h2="Be the plumber everyone vouches for.", text=None):
    return final_cta(h2) if text is None else final_cta(h2, text)


def page(*sections):
    return "<main>" + "".join(sections) + "</main>"


# ---------- services ----------

# Content lives in services_data.py (one entry per service, in homepage order).


def benefits(items, tagline, name, h1=None):
    """h1: on a service page this section opens the page (one heading block: service name, H1, italic tagline)."""
    cells = "".join(f'<li><h3>{icon("check", "tick")}{t}</h3><p>{d}</p></li>' for t, d in items)
    heading = f"<h1>{h1}</h1>" if h1 else "<h2>Why plumbers use it</h2>"
    return f"""
<section class="svc-benefits{' first' if h1 else ''}">
  <div class="wrap">
    <div class="sec-head"><p class="eyebrow">{name}</p>{heading}<p class="svc-tag">{tagline}</p></div>
    <ul class="svc-bens">{cells}</ul>
  </div>
</section>"""


def demo(video, name):
    if not video:
        return ""
    return f"""
<section class="tint-soft">
  <div class="wrap">
    <div class="sec-head"><p class="eyebrow">See it in action</p><h2>Watch a short demo</h2></div>
    <div class="svc-video"><iframe src="{video}" title="{name} demo" loading="lazy" allowfullscreen></iframe></div>
  </div>
</section>"""


def explain(h2, items):
    cells = "".join(f'<li><span class="ic">{icon(i)}</span><h3>{t}</h3><p>{d}</p></li>' for i, t, d in items)
    return f"""
<section class="dark svc-explain">
  <div class="wrap">
    <div class="sec-head"><p class="eyebrow">How it works</p><h2>{h2}</h2></div>
    <ul class="svc-cards">{cells}</ul>
  </div>
</section>"""


def more_services(slug):
    return f"""
<section class="products svc-more">
  <div class="wrap">
    <div class="sec-head"><p class="eyebrow">The full system</p><h2>Everything that's included</h2>
    <p>Every service comes with the same plan, and we set it all up for you.</p></div>
    {product_groups(current=slug)}
  </div>
</section>"""


def service_page(slug):
    d = SERVICE_PAGES[slug]
    group = GROUPS[d["group"]][0]

    def body():
        return page(
            benefits(d["benefits"], d["tagline"], d["name"], h1=d["h1"]),
            demo(d["video"], d["name"]),
            explain(d["explain_h2"], d["explain"]),
            split("Your part vs our part", "What you do", d["split"][0], "What we do", d["split"][1]),
            faq(d["faq"], h2=f"Questions about {d['name'].lower()}"),
            more_services(slug),
            final(),
        )
    return body


# The customer's journey. Tags are (label, service slug) and can point at either system.
FLOW = [
    ("search", "They find you", "Someone searches \u201cplumber near me\u201d on Google or ChatGPT and sees your complete "
     "profile and strong reviews.",
     [("Google profile", "google-business-profile"), ("Reviews", "google-reviews"),
      ("Local SEO", "google-business-profile"), ("AI search", "google-business-profile")]),
    ("monitor", "They check you out", "Your website shows what you do and your real Google reviews, and makes getting "
     "in touch easy.", [("Website", "websites"), ("Reviews", "google-reviews")]),
    ("phone", "They get in touch", "Missed their call? They get a text back. Sent an enquiry? They get a reply straight away.",
     [("Text-back", "missed-call-text-back"), ("Follow-up", "lead-follow-up")]),
    ("mail", "You reply from one app", "Every call, text, email, Facebook and Instagram message lands in one inbox on "
     "your phone.", [("All-in-one inbox", "all-in-one-inbox")]),
    ("star", "Job done, review asked", "Every customer is automatically asked for a review and followed up, which "
     "helps the next homeowner find you.", [("Reviews", "google-reviews")]),
    ("target", "Automatic marketing campaigns", "Boiler service reminders, seasonal offers and referral nudges, "
     "sent to past customers automatically.", [("Marketing campaigns", "marketing-campaigns")]),
]


def flow():
    steps_html = ""
    for n, (i, t, d, slugs) in enumerate(FLOW, 1):
        tags = "".join(f'<a href="/services/{x}">{label}</a>' for label, x in slugs)
        steps_html += (f'<li><span class="fl-num">Step {n}</span><span class="fl-ic">{icon(i)}</span><h3>{t}</h3><p>{d}</p>'
                       f'<span class="fl-tags">{tags}</span></li>')
    return f"""
<section class="tint-soft flow" id="how">
  <div class="wrap">
    <div class="sec-head"><p class="eyebrow">How they fit together</p><h2>2 systems working together to win repeat business for life</h2>
    <p>Follow one homeowner through the 2 systems: found, booked, reviewed, referral, repeat.</p></div>
    <ol class="fl-steps">{steps_html}</ol>
    <div class="fl-return" aria-hidden="true"></div>
    <p class="fl-loop">{icon("trend")} Back to step 1: happy customers review you, come back and recommend you.</p>
  </div>
</section>"""


def services():
    return page(
        hero("Our services", "2 simple systems that help our plumbers <span class=\"accent\">win more boiler installs.</span>",
             "First we help more homeowners find you. Then we make sure you don't lose the work they bring. "
             "Everything works together, and we build and run it all for you."),
        f"""
<section class="products">
  <div class="wrap">
    {product_groups()}
  </div>
</section>""",
        flow(),
        steps(),
        final(),
    )


# ---------- trades ----------

TRADES = {
    "plumbers": {
        "title": "Marketing for Domestic Plumbers & Heating Engineers | Vouch Digital",
        "desc": "Google reviews, Google profile, websites, local SEO and AI search for domestic plumbers and heating engineers "
                "across the UK. A free website and everything else included for £197 a month.",
        "eyebrow": "For domestic plumbers &amp; heating engineers",
        "h1": "More boiler installs and better-paid jobs <span class=\"accent\">from Google and ChatGPT.</span>",
        "lede": "Boiler installs, bathrooms, full heating systems and emergency call-outs. "
                "The plumbers who win the best jobs are usually the ones with the strongest reputation online.",
        "jobs": [("flame", "Boiler installs", "A big decision for a homeowner, so recent reviews carry a lot of weight."),
                 ("bath", "Bathroom installs", "Customers want to see photos of your work and read what others said."),
                 ("radiator", "Heating systems", "Larger jobs where trust and a clear website make the difference."),
                 ("drop", "Emergency leaks", "Decided in minutes from the map results, mostly on reviews and distance."),
                 ("cog", "Boiler servicing", "Repeat work every year, so a strong reputation keeps paying back."),
                 ("search", "“Plumber near me”", "The top three on the map get most of the calls.")],
        "faq": [
            ("We're fully booked for winter. Should we wait?",
             "Reviews and visibility build over time, so the best time to start is while you're busy and have plenty of "
             "happy customers to ask. That way it's working for you before the quieter months."),
            ("Do you work with Gas Safe registered engineers?",
             "Yes. We make sure your Gas Safe registration is clearly shown on your Google profile and website, because "
             "customers look for it."),
            ("We do a lot of commercial work. Is this for us?",
             "It's most useful for domestic work, where customers search and compare online. If you want more domestic "
             "work alongside your contracts, it can help. If not, we'll say so."),
        ],
    },
}


def trade_page(slug):
    d = TRADES[slug]

    def body():
        return page(
            hero(d["eyebrow"], d["h1"], d["lede"],
                 form_eyebrow="Free for plumbers &amp; heating engineers"),
            cards(d["jobs"], "Where it makes a difference", "The jobs your online reputation wins you",
                  "Different jobs are won in different ways. Here's where reviews, your Google profile and your website "
                  "matter most."),
            products_section(cls="products tint-soft"),
            steps(),
            faq(d["faq"] + FAQ_HOME[2:4]),
            final(),
        )
    return body


# ---------- about, faq, contact ----------

def about():
    values = [
        ("star", "Genuine reviews only", "We never write, buy, incentivise or filter reviews. Every customer is asked, "
                                          "and that's how UK law says it should be done."),
        ("target", "Only plumbers", "We only work with domestic plumbers and heating engineers, so everything we do "
                                    "is built around how plumbing businesses win work."),
        ("check", "Honest advice", "If something won't help your business, we'll tell you, even if that means you don't "
                                    "need us."),
        ("clock", "No lock-in", "Month to month. We'd rather keep you because it's working than because of a contract."),
        ("building", "Your data, handled properly", f"Registered with the ICO ({SITE['ico']}) and careful with your "
                                                     "customers' details."),
        ("pin", "Anywhere in the UK", "Everything is done remotely over video call and phone, so it doesn't matter "
                                         "where you're based."),
    ]
    return page(
        hero("About us", "We help plumbers <span class=\"accent\">get the reputation they've earned.</span>",
             f"Vouch Digital is a small team run by Tim, working only with domestic plumbers and heating engineers "
             f"across {SITE['area']}.", form=False),
        prose("Why we started", "Good plumbers were losing jobs to busier-looking competitors", [
            "Most of the plumbers we speak to do brilliant work. Their customers are happy. But online, "
            "they look quieter than they are: a handful of old reviews, a half-finished Google profile, a website that's "
            "hard to use on a phone.",
            "Meanwhile, homeowners are deciding who to call in a couple of minutes, from Google Maps and increasingly from "
            "ChatGPT. The business that looks most trusted gets the call, not always the one that does the best work.",
            "We started Vouch Digital to fix that, and to do it the right way: genuine reviews from real customers, honest "
            "advice and no promises we can't keep.",
        ]),
        cards(values, "How we work", "What you can expect from us", cls="tint-soft"),
        prose("The company", "The details", [
            f"Vouch Digital is a trading name of {SITE['legal_name']}, registered in England and Wales "
            f"(company number {SITE['company_no']}). Registered office: {SITE['address']}. "
            f"ICO registration: {SITE['ico']}.",
            f"Call or text <a href=\"tel:{SITE['phone_intl']}\">{SITE['phone']}</a>, or email "
            f"<a href=\"mailto:{SITE['email']}\">{SITE['email']}</a>.",
        ]),
        final(),
    )


FAQ_MORE = [
    ("What happens on the call?",
     "A 15-minute Google Meet. We look at your business online beforehand, show you what's costing you jobs, explain "
     "how the system works and answer your questions. If it's a good fit, we get your free website started."),
    ("Do you work with plumbers outside London?",
     "Yes. We work with domestic plumbers and heating engineers anywhere in the UK. Everything is done remotely, "
     "over video call and phone."),
    ("Can you guarantee I'll get to the top of Google?",
     "No. Nobody can honestly promise rankings or AI recommendations. We fix what's holding you back and keep the work "
     "going month after month."),
    ("What do I need to give you?",
     "Manager access to your Google profile (we'll show you how), a list of past customers you're allowed to contact, "
     "and some photos from your jobs. That's usually it."),
    ("What happens to my customers' details?",
     "We only use them to send review requests on your behalf, keep them secure, and delete them when you stop working "
     "with us. See our <a href=\"/privacy\">Privacy Policy</a> for the details."),
]


def faq_page():
    return page(
        faq(FAQ_HOME + FAQ_MORE, h1="Straight answers to <span class=\"accent\">common questions.</span>", eyebrow="FAQ",
            intro="If your question isn't here, call or text us on "
                  f"<a href=\"tel:{SITE['phone_intl']}\">{SITE['phone']}</a>. We'd rather answer it properly than have you guess."),
        final(),
    )


def pricing_page():
    return page(
        pricing_section(h1="Simple pricing. <span class=\"accent\">A free website when you join.</span>",
                        lede="No contract, cancel anytime, or pay upfront and save."),
        steps(),
        faq(FAQ_HOME[:5], h2="Questions about pricing"),
        final(),
    )


def contact():
    ways = [
        ("phone", "Call or text", f'<a href="tel:{SITE["phone_intl"]}">{SITE["phone"]}</a>'),
        ("mail", "Email", f'<a href="mailto:{SITE["email"]}">{SITE["email"]}</a>'),
        ("clipboard", "Book a call", '<a href="/book">Pick a time</a> that suits you for a 15-minute call.'),
    ]
    return page(
        hero("Contact", "Let's get your <span class=\"accent\">free website started.</span>",
             "The quickest way to get started is a 15-minute call. Pick a time that suits you, "
             f"or call or text {SITE['phone']}."),
        cards(ways, "Get in touch", "Other ways to reach us", cls="tint-soft"),
    )


ALL_MORE = (
    [{"path": "/services", "body": services,
      "title": "Services for Plumbers & Heating Engineers | Vouch Digital",
      "desc": "Missed-call text-back, lead follow-up, an all-in-one inbox, websites, Google reviews and local SEO "
              "for domestic plumbers across the UK, all set up for you."}]
    + [{"path": f"/services/{slug}", "body": service_page(slug), "title": d["title"], "desc": d["desc"]}
       for slug, d in SERVICE_PAGES.items()]
    + [{"path": f"/{slug}", "body": trade_page(slug), "title": d["title"], "desc": d["desc"]}
       for slug, d in TRADES.items()]
    + [{"path": "/about", "body": about,
        "title": "About Vouch Digital | Marketing for Domestic Plumbers",
        "desc": "Vouch Digital helps domestic plumbers and heating engineers across the UK get the "
                "online reputation they've earned. Genuine reviews, honest advice."},
       {"path": "/pricing", "body": pricing_page,
        "title": "Pricing | Vouch Digital",
        "desc": "One plan for domestic plumbers: £197 a month, everything included, with a free website. No contract."},
       {"path": "/faq", "body": faq_page,
        "title": "FAQ | Vouch Digital",
        "desc": "Answers to common questions about Vouch Digital's services for domestic plumbers and heating engineers."},
       {"path": "/contact", "body": contact,
        "title": "Contact Vouch Digital | Book a Call",
        "desc": f"Call or text {SITE['phone']}, email {SITE['email']}, or book a 15-minute call."}]
)
