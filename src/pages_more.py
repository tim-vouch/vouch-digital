"""Inner pages: services, trades, about, FAQ, contact.

House rules (see CLAUDE.md): no invented results or reviews, no promises of rankings,
timescales or AI recommendations, no prices, service area is London & the South East.
"""
from icons import icon
from site_data import SITE, FAQ_HOME
from pages import audit_form


# ---------- building blocks ----------

def hero(eyebrow, h1, lede, form=True, form_eyebrow="Free for electricians &amp; plumbers"):
    if form:
        return f"""
<section class="hero">
  <div class="wrap">
    <div>
      <p class="eyebrow">{eyebrow}</p>
      <h1>{h1}</h1>
      <p class="lede">{lede}</p>
    </div>
    {audit_form(form_eyebrow)}
  </div>
</section>"""
    return f"""
<section class="dark page-hero">
  <div class="wrap">
    <p class="eyebrow">{eyebrow}</p>
    <h1>{h1}</h1>
    <p class="muted">{lede}</p>
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


def steps(cls="dark process"):
    s = "".join(f"""<li><div class="ring">{icon(i)}</div><h3>{n}. {t}</h3><p>{d}</p></li>"""
                for n, (i, t, d) in enumerate([
                    ("clipboard", "Free check", "We look at your reviews, Google profile, website and listings, and show you at least 5 things to fix."),
                    ("target", "Your plan", "We agree what's worth doing for your business and your area. Nothing you don't need."),
                    ("cog", "20-minute setup", "One short call to connect your Google profile and customer list. We handle the rest."),
                    ("chart", "It keeps working", "We run it month after month in the background while you're out on jobs."),
                ], 1))
    return f"""
<section class="{cls}">
  <div class="wrap">
    <div class="sec-head"><p class="eyebrow">How it works</p><h2>A simple process, with nothing for you to learn</h2></div>
    <ol class="steps">{s}</ol>
  </div>
</section>"""


def faq(items, h2="Got questions? We've got straight answers.", intro=None):
    qs = "".join(f"<details><summary>{q}{icon('chevron')}</summary><p>{a}</p></details>" for q, a in items)
    intro = intro or f"No jargon, no promises we can't keep. Anything else, call <a href=\"tel:{SITE['phone_intl']}\">{SITE['phone']}</a>."
    return f"""
<section class="faq" id="faq">
  <div class="wrap">
    <div class="intro">
      <p class="eyebrow">Frequently asked questions</p>
      <h2>{h2}</h2>
      <p>{intro}</p>
    </div>
    <div>{qs}</div>
  </div>
</section>"""


def final(h2="Be the business locals vouch for.",
          text="We'll find at least 5 ways you're losing jobs to competitors online, and show you how to fix them."):
    return f"""
<section class="dark final">
  <div class="wrap">
    <p class="eyebrow">Free, 15 minutes, no hard sell</p>
    <h2>{h2}</h2>
    <p class="muted">{text}</p>
    <div class="row"><a class="btn btn-mint" href="#audit">Find My Missed Jobs {icon('arrow')}</a>
    <a class="btn btn-ghost" href="tel:{SITE['phone_intl']}">{icon('phone')} Call {SITE['phone']}</a></div>
  </div>
</section>"""


def page(*sections):
    return "<main>" + "".join(sections) + "</main>"


# ---------- services ----------

SERVICE_PAGES = {
    "google-reviews": {
        "icon": "star", "name": "Google Reviews",
        "title": "Google Reviews for Electricians & Plumbers | Vouch Digital",
        "desc": "Automatic, compliant Google review requests after every job, and a reply to every review. "
                "For electricians and plumbers in London and the South East.",
        "h1": "Turn happy customers into <span class=\"accent\">a steady stream of Google reviews.</span>",
        "lede": "Every customer gets a friendly text and email after the job, asking for a review. "
                "We reply to every review for you. Genuine, compliant, and fully done for you.",
        "why": ["Reviews are one of the biggest things homeowners look at before they ring anyone. "
                "Most will compare the top three businesses on Google Maps and call the one with the most recent, "
                "most convincing reviews.",
                "The problem isn't that your customers aren't happy. It's that nobody asks them at the right moment, "
                "and after a long day on the tools you've got better things to do. That's the bit we take off your plate."],
        "includes": [
            ("mail", "Text and email requests", "Sent automatically after each job, worded for your trade and signed off as your business."),
            ("clock", "Polite follow-ups", "A gentle reminder if they haven't left one, then we stop. No nagging."),
            ("star", "A reply to every review", "Thoughtful replies that mention the job and the area, so they help future customers too."),
            ("link", "Past customers too", "A one-off request to customers from the last couple of years, where you're allowed to contact them."),
            ("user", "Private feedback route", "Customers can also tell you privately if something wasn't right, so you can put it right."),
            ("chart", "Monthly summary", "How many requests went out, how many reviews came in, and what customers said."),
        ],
        "split": (["Send us your customer list once (or connect your job software)",
                   "Do great work, like you already do"],
                  ["Write and send every review request", "Chase politely, then stop",
                   "Reply to every review", "Keep it all compliant with UK law"]),
        "faq": [
            ("Are the reviews genuine?",
             "Yes. We only ask your real customers, every customer is asked, and we never filter out unhappy ones. "
             "We never write, buy, incentivise or remove reviews. That's how the Digital Markets, Competition and "
             "Consumers Act 2024 says it should be done."),
            ("What if someone leaves a bad review?",
             "It happens to every business. We'll write a calm, professional reply for you to approve. A good reply to a "
             "bad review often reassures future customers more than another five stars."),
            ("Can you get my customer list from my job software?",
             "Often, yes. Tools like Tradify, ServiceM8, Jobber and Powered Now can usually be connected so new "
             "customers are added automatically. If not, a simple spreadsheet export works fine."),
            ("Is it OK to text my old customers?",
             "Only where the law allows. Before we contact anyone, we check you have a lawful basis to contact them, "
             "such as being a recent customer who didn't opt out."),
        ],
    },
    "google-business-profile": {
        "icon": "pin", "name": "Google Business Profile",
        "title": "Google Business Profile for Electricians & Plumbers | Vouch Digital",
        "desc": "We set up and manage your Google Business Profile: services, categories, areas, photos and posts. "
                "For electricians and plumbers in London and the South East.",
        "h1": "Make your Google profile <span class=\"accent\">work as hard as you do.</span>",
        "lede": "Your Google profile is often the first thing a customer sees, before your website. "
                "We fill in every section properly and keep it active, so Google understands exactly what you do and where.",
        "why": ["When someone searches “electrician near me” or “emergency plumber”, the businesses that show on the map "
                "are chosen partly by how complete, accurate and active their Google profile is.",
                "Most trade profiles are half-finished: missing services, the wrong categories, no service areas, "
                "a handful of old photos. Each gap is a search you could be showing up for but aren't."],
        "includes": [
            ("pin", "Categories and service areas", "The right primary and extra categories, and the areas you actually want work from."),
            ("clipboard", "Every service listed", "Rewires, consumer units, boiler installs, leak repairs: each with a clear description."),
            ("image", "Photos that sell", "Your real job and van photos, added regularly, because customers want to see your work."),
            ("trend", "Regular posts", "Short updates about recent jobs and services, so your profile stays active."),
            ("building", "Details kept accurate", "Hours, phone number, website and description checked and kept up to date."),
            ("search", "Keeping an eye on it", "We check for unwanted edits and suggested changes from the public."),
        ],
        "split": (["Add us as a manager on your Google profile (we'll show you, it takes two minutes)",
                   "Send us photos from your jobs when you can"],
                  ["Fill in every section properly", "Write service descriptions",
                   "Post updates and photos regularly", "Watch for unwanted changes"]),
        "faq": [
            ("Do I lose control of my Google profile?",
             "No. You stay the owner. We're added as a manager, which you can remove at any time in your Google settings."),
            ("I don't have a shop. Can I still show on Google Maps?",
             "Yes. Most trades are set up as a “service-area business”, which hides your home address and shows the "
             "areas you cover instead."),
            ("Will this get me to the top of Google Maps?",
             "We can't promise rankings, and anyone who does is guessing. What we can do is fix the things that hold "
             "profiles back and keep yours complete and active, month after month."),
        ],
    },
    "websites": {
        "icon": "monitor", "name": "Websites",
        "title": "Websites for Electricians & Plumbers | Vouch Digital",
        "desc": "Fast, mobile-friendly websites for electricians and plumbers, built to turn visitors into calls. "
                "London and the South East.",
        "h1": "A website that <span class=\"accent\">turns visitors into calls.</span>",
        "lede": "Most of your customers will look at your site on a phone, often in a hurry. "
                "We build fast, clear websites that make it easy to see what you do and ring you.",
        "why": ["Your website backs up everything else. A customer who finds you on Google or ChatGPT will often check "
                "your site before they call. If it's slow, out of date or hard to use on a phone, they go back and ring "
                "the next one.",
                "It also matters for search. A clear page for each service and each area you cover helps Google and AI "
                "tools understand exactly what you do and where."],
        "includes": [
            ("monitor", "Mobile-first design", "Built for phones first, with your number and a call button always in reach."),
            ("clock", "Fast to load", "Lightweight pages that open quickly, even on a weak signal."),
            ("clipboard", "A page per service", "Rewires, EV chargers, boiler installs and more, each with its own clear page."),
            ("pin", "Your areas covered", "Clear information about the towns and boroughs you work in."),
            ("star", "Your real reviews", "Genuine Google reviews shown on your site, never made-up testimonials."),
            ("mail", "Enquiries straight to you", "Forms that send leads to your phone and inbox, with spam filtering."),
        ],
        "split": (["Tell us about your business on a short call", "Send photos of your work",
                   "Check the draft and tell us what to change"],
                  ["Write the words", "Design and build the site",
                   "Set up hosting and security", "Keep it updated as your business changes"]),
        "faq": [
            ("I already have a website. Do I need a new one?",
             "Not always. If your current site works, we'll work with it. If it's slow, hard to use on a phone or not "
             "turning visitors into calls, a new one will do a better job. We'll tell you honestly on the call."),
            ("Who owns the website?",
             "We'll explain exactly who owns what, and what's included, before you agree to anything."),
            ("How long does a new website take?",
             "It depends on how quickly we get your details and photos. We'll give you a realistic timeline on the call "
             "rather than a number that sounds good."),
        ],
    },
    "local-seo": {
        "icon": "trend", "name": "Local SEO",
        "title": "Local SEO for Electricians & Plumbers | Vouch Digital",
        "desc": "Consistent listings on Bing, Apple Maps, Yell and trade directories, and a website built for local "
                "searches. For electricians and plumbers in London and the South East.",
        "h1": "Show up when locals search for <span class=\"accent\">a trade like yours.</span>",
        "lede": "Local SEO is everything that helps search engines trust where you work and what you do: "
                "consistent listings across the web, and local pages on your website.",
        "why": ["Google, Bing, Apple Maps and AI tools all cross-check your business details across the internet. "
                "If your name, address and number are different on Yell, Checkatrade and Bing, it creates doubt.",
                "Getting these details consistent, and making sure your website clearly covers your services and areas, "
                "is slow, fiddly work. It's exactly the kind of job that gets put off, so we do it for you."],
        "includes": [
            ("link", "Listings cleaned up", "Your details made consistent on Bing, Apple Maps, Yell and other directories."),
            ("search", "Local search terms", "We find what people in your area actually type, and make sure you cover it."),
            ("pin", "Area pages", "Clear pages for the main towns and boroughs you want work from."),
            ("monitor", "Website basics fixed", "Page titles, headings and business information set up properly."),
            ("building", "Business information", "Structured details that help search engines and AI read your site correctly."),
            ("chart", "Progress updates", "What we've done each month, in plain English."),
        ],
        "split": (["Confirm your correct business details once", "Approve any changes to your website"],
                  ["Find and fix listings across the web", "Research local search terms",
                   "Build and improve area pages", "Report back in plain English"]),
        "faq": [
            ("What's the difference between this and my Google profile?",
             "Your Google profile is one listing. Local SEO is everything around it: other directories, your website and "
             "the consistency between them, which all feed into whether you show up."),
            ("I already pay someone for SEO. Do I need this?",
             "Maybe not. Many SEO packages only work on the website and ignore listings and your Google profile. On the "
             "free check we'll show you what's actually been done, and you can decide."),
            ("How quickly will I see results?",
             "We don't make promises about timescales. Local SEO builds over time, which is why we keep working on it "
             "month after month rather than doing it once."),
        ],
    },
    "ai-search": {
        "icon": "ai", "name": "AI Search",
        "title": "AI Search (ChatGPT) for Electricians & Plumbers | Vouch Digital",
        "desc": "Clear, trusted information about your business so ChatGPT, Gemini and Google's AI answers can find "
                "and understand you. For electricians and plumbers in London and the South East.",
        "h1": "When someone asks ChatGPT for a tradesperson, <span class=\"accent\">be easy to find.</span>",
        "lede": "More homeowners are asking ChatGPT, Gemini and Google's AI answers who to call. "
                "These tools pull from reviews, listings and websites. We make sure yours tell a clear, consistent story.",
        "why": ["AI tools don't have a “top three” you can pay for. They draw on what's written about you across the "
                "internet: your reviews, your Google profile, your listings and your website.",
                "If that information is thin or inconsistent, they're more likely to recommend someone else. "
                "Nobody can promise an AI will recommend you, and we won't. But we can make sure everything it reads "
                "about you is clear, accurate and up to date."],
        "includes": [
            ("ai", "AI check", "We ask the main AI tools who they recommend for your trade and area, and show you the answers."),
            ("star", "Reviews that say something", "Reviews that mention the job and the area give AI tools useful detail."),
            ("monitor", "Clear website content", "Plain answers to the questions customers ask, written so AI can understand them."),
            ("building", "Structured business details", "Information on your site that tells machines exactly who you are."),
            ("link", "Consistent listings", "The same name, number and services everywhere AI tools look."),
            ("chart", "Regular re-checks", "We check what the AI tools say again over time, and keep improving."),
        ],
        "split": (["Answer a few questions about your business", "Approve website changes"],
                  ["Check what AI tools say about you", "Improve your website content",
                   "Tidy up listings and business details", "Re-check regularly"]),
        "faq": [
            ("Can you guarantee ChatGPT will recommend me?",
             "No, and be wary of anyone who says they can. AI answers change, and nobody controls them. We improve the "
             "information these tools rely on, which gives you the best chance of being mentioned."),
            ("Is this different from normal SEO?",
             "It overlaps a lot. Good reviews, a complete Google profile and a clear website help with both. The "
             "difference is that we write and structure things so AI tools can read and repeat them easily."),
            ("Which AI tools do you check?",
             "ChatGPT, Gemini, Google's AI answers, and others where relevant. We'll show you the actual answers on your "
             "free check."),
        ],
    },
}


def service_page(slug):
    d = SERVICE_PAGES[slug]

    def body():
        return page(
            hero(d["name"], d["h1"], d["lede"]),
            prose(d["name"], "Why it matters for your business", d["why"], cls="tint-soft"),
            cards(d["includes"], "What's included", "What we do for you"),
            split("Your part vs our part", "What you do", d["split"][0], "What we do", d["split"][1]),
            steps(),
            faq(d["faq"], h2=f"Questions about {d['name']}"),
            final(),
        )
    return body


def services():
    items = [(d["icon"], d["name"], d["desc"].split(". ")[0] + ".", f"/services/{slug}")
             for slug, d in SERVICE_PAGES.items()]
    return page(
        hero("Our services", "Everything you need to <span class=\"accent\">win more local jobs.</span>",
             "Reviews, your Google profile, your website, local listings and AI search. Five jobs that work best "
             "together, all done for you by one team."),
        cards(items, "Five services, one system", "Pick a service to see what's included", linked=True),
        prose("How they fit together", "Stronger together than as separate jobs", [
            "Reviews build trust. Your Google profile gets you seen on the map. Your website turns that interest into a "
            "phone call. Local listings and AI search make sure every place a customer looks tells the same, "
            "convincing story.",
            "You can start with one, and many of our clients start with reviews. On the free check we'll show you which "
            "will make the biggest difference for your business first.",
        ], cls="tint-soft"),
        steps(),
        final(),
    )


# ---------- trades ----------

TRADES = {
    "electricians": {
        "title": "Marketing for Electricians in London & the South East | Vouch Digital",
        "desc": "Google reviews, Google profile, websites, local SEO and AI search for electricians in London and the "
                "South East. Find out how many jobs you're missing with a free check.",
        "eyebrow": "For electricians",
        "h1": "More of the jobs you actually want, <span class=\"accent\">from Google and ChatGPT.</span>",
        "lede": "Rewires, consumer unit upgrades, EV chargers and landlord EICRs. Whether you want more call-outs or "
                "more of the bigger jobs, it starts with how you look online.",
        "jobs": [("bolt", "Rewires", "Homeowners compare reviews closely before trusting someone with a full rewire."),
                 ("plug", "EV charger installs", "A fast-growing search, and customers often ask AI tools who to use."),
                 ("cog", "Consumer unit upgrades", "A clear service listing helps you show up for “fuse box” searches."),
                 ("clipboard", "EICRs for landlords", "Repeat work every few years, so a strong reputation keeps paying back."),
                 ("clock", "Emergency call-outs", "Decided in minutes from the map results, mostly on reviews and distance."),
                 ("search", "Fault finding", "“Electrician near me” searches where the top three on the map get the calls.")],
        "faq": [
            ("I'm busy already. Why would I need this?",
             "Most electricians we speak to are busy. The point isn't just more work, it's more of the work you "
             "want, at prices you're happy with, so you can be choosier about which jobs you take."),
            ("I get most of my work from builders. Is this still worth it?",
             "Only if you want more direct work from homeowners. If you're happy with the mix you have, we'll tell you so "
             "on the call."),
            ("Do you work with NICEIC and NAPIT registered electricians?",
             "Yes. We make sure your registration is clearly shown on your Google profile and website, because "
             "customers look for it."),
        ],
    },
    "plumbers": {
        "title": "Marketing for Plumbers & Heating Engineers in London & the South East | Vouch Digital",
        "desc": "Google reviews, Google profile, websites, local SEO and AI search for plumbers and heating engineers in "
                "London and the South East. Find out how many jobs you're missing with a free check.",
        "eyebrow": "For plumbers &amp; heating engineers",
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
                 form_eyebrow="Free for electricians" if slug == "electricians" else "Free for plumbers &amp; heating engineers"),
            cards(d["jobs"], "Where it makes a difference", "The jobs your online reputation wins you",
                  "Different jobs are won in different ways. Here's where reviews, your Google profile and your website "
                  "matter most."),
            cards([(SERVICE_PAGES[s]["icon"], SERVICE_PAGES[s]["name"], SERVICE_PAGES[s]["desc"].split(". ")[0] + ".",
                    f"/services/{s}") for s in SERVICE_PAGES],
                  "What we do", "Five services, all done for you", cls="tint-soft", linked=True),
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
        ("target", "Only the trades", "We only work with electricians, plumbers and heating engineers, so everything we do "
                                       "is built around how trade businesses win work."),
        ("check", "Honest advice", "If something won't help your business, we'll tell you, even if that means you don't "
                                    "need us."),
        ("clock", "No lock-in", "Month to month. We'd rather keep you because it's working than because of a contract."),
        ("building", "Your data, handled properly", f"Registered with the ICO ({SITE['ico']}) and careful with your "
                                                     "customers' details."),
        ("pin", "Local", f"Based in London, working with trade businesses across {SITE['area']}."),
    ]
    return page(
        hero("About us", "We help local trades <span class=\"accent\">get the reputation they've earned.</span>",
             f"Vouch Digital is a small, London-based team run by Tim, working only with electricians, plumbers and "
             f"heating engineers across {SITE['area']}.", form=False),
        prose("Why we started", "Good tradespeople were losing jobs to busier-looking competitors", [
            "Most of the electricians and plumbers we speak to do brilliant work. Their customers are happy. But online, "
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
    ("What does the free check involve?",
     "A 15-minute Google Meet. Before the call we look at your reviews, Google profile, website, listings and what AI "
     "tools say about you. On the call we show you at least 5 things that are costing you jobs, and how to fix them. "
     "You can fix them yourself afterwards, or ask us to."),
    ("How much does it cost?",
     "Pricing depends on what your business actually needs, so we talk about it on the call once we've seen your "
     "business. There's no lock-in: it's month to month."),
    ("Do you work outside London?",
     "We work across London and the South East, including Surrey, Hertfordshire, Kent, Essex, Berkshire and Sussex."),
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
        hero("FAQ", "Straight answers to <span class=\"accent\">common questions.</span>",
             "If your question isn't here, call or text us. We'd rather answer it properly than have you guess.",
             form=False),
        faq(FAQ_HOME + FAQ_MORE, h2="Everything you might want to ask"),
        final(),
    )


def contact():
    ways = [
        ("phone", "Call or text", f'<a href="tel:{SITE["phone_intl"]}">{SITE["phone"]}</a>'),
        ("mail", "Email", f'<a href="mailto:{SITE["email"]}">{SITE["email"]}</a>'),
        ("clipboard", "Book a free check", '<a href="#audit">Fill in the form</a> and pick a time that suits you.'),
        ("building", "Registered office", f"{SITE['address']}. This is our registered address, not a walk-in office."),
    ]
    return page(
        hero("Contact", "Let's find the jobs <span class=\"accent\">you're missing.</span>",
             "The quickest way to get started is the free 15-minute check. Fill in the form and pick a time, "
             f"or call or text {SITE['phone']}.", form_eyebrow="Free 15-minute check"),
        cards(ways, "Get in touch", "Other ways to reach us", cls="tint-soft"),
    )


ALL_MORE = (
    [{"path": "/services", "body": services,
      "title": "Services for Electricians & Plumbers | Vouch Digital",
      "desc": "Google reviews, Google Business Profile, websites, local SEO and AI search for electricians and plumbers "
              "in London and the South East, all done for you."}]
    + [{"path": f"/services/{slug}", "body": service_page(slug), "title": d["title"], "desc": d["desc"]}
       for slug, d in SERVICE_PAGES.items()]
    + [{"path": f"/{slug}", "body": trade_page(slug), "title": d["title"], "desc": d["desc"]}
       for slug, d in TRADES.items()]
    + [{"path": "/about", "body": about,
        "title": "About Vouch Digital | Marketing for Local Trades in London",
        "desc": "Vouch Digital helps electricians, plumbers and heating engineers in London and the South East get the "
                "online reputation they've earned. Genuine reviews, honest advice."},
       {"path": "/faq", "body": faq_page,
        "title": "FAQ | Vouch Digital",
        "desc": "Answers to common questions about Vouch Digital's services for electricians and plumbers."},
       {"path": "/contact", "body": contact,
        "title": "Contact Vouch Digital | Free Missed Jobs Check",
        "desc": f"Call or text {SITE['phone']}, email {SITE['email']}, or book a free 15-minute Missed Jobs Check."}]
)
