"""Business facts. Single source of truth — edit here, then rebuild."""

SITE = {
    "brand": "Vouch Digital",
    "legal_name": "Bolotin Ltd",
    "company_no": "17405583",
    "address": "167–169 Great Portland Street, 5th Floor, London, W1W 5PF",
    "ico": "ZC234151",
    "phone": "07984 003845",
    "phone_intl": "+447984003845",
    "email": "info@vouchdigital.co.uk",
    "domain": "https://vouchdigital.co.uk",
    "area": "the UK",
    # GHL calendar: Free Missed Jobs Check (permanent link, survives slug changes)
    "booking_url": "https://link.vouchdigital.co.uk/widget/booking/xbAVu7ah9p5NXexCdiO8",
    # Keep True until the site is live on vouchdigital.co.uk
    "noindex": False,
}

# Real Google reviews of Vouch Digital only. Never add invented reviews.
# Source: Vouch Digital Google Business Profile (via GHL review widget), Oct 2026.
REVIEWS = [
    {"name": "Paul McLoughlin", "date": "September 2026", "stars": 5,
     "text": "Tim is fantastic! We had a website before but Tim made a new one and we are "
             "actually noticing more calls. His team did the work quickly and kept us informed "
             "and up to date of what they're doing. Recommend highly"},
    {"name": "Matt", "date": "September 2026", "stars": 5,
     "text": "Great working with Tim and the team. They sorted our online presence and did "
             "everything they said they would"},
    {"name": "Ellie Balysz", "date": "September 2026", "stars": 5, "text": ""},
]

FAQ_HOME = [
    ("Do you only work with plumbers?",
     "Yes. We only work with domestic plumbers and heating engineers. Everything we build, from the "
     "review request wording to the website pages, is shaped around how a plumbing business actually "
     "wins work from homeowners."),
    ("How long does it take to see results?",
     "We don't make promises about timescales. Reviews and visibility build over time as more "
     "genuine reviews come in and your profile stays active. We handle the setup and keep the "
     "work going month after month."),
    ("How much of my time does this take?",
     "Very little: a short first call, a quick onboarding form, then a launch call where we walk "
     "you through everything. After that we run it in the background while you're out on jobs."),
    ("What areas do you work in?",
     "Anywhere in the UK. Everything is done remotely over video call and phone, so it doesn't "
     "matter where you're based."),
    ("Do I need a new website?",
     "Not always. If your current website works, we'll work with it. If it's slow, hard to use on "
     "a phone or not turning visitors into calls, a new one will do a better job. We'll tell you "
     "honestly on the call."),
    ("Are the reviews genuine?",
     "Yes. We only ask your real customers, every customer is asked, and we never filter out "
     "unhappy ones. We never write, buy, incentivise or remove reviews. That's how the Digital "
     "Markets, Competition and Consumers Act 2024 says it should be done."),
    ("Am I locked into a contract?",
     "No. It's month to month, with no lock-in. It's £197 a month, and you get a free website "
     "when you join. See our <a href=\"/pricing\">pricing</a>."),
]


# Pricing plans (shown on /pricing). Crossed-out prices must be real prices we charge.
PLANS = [
    {"name": "Growth", "price": 197, "tag": "Everything you need to win more jobs from Google and ChatGPT.",
     "featured": True, "lead": "What's included",
     "items": [("All-in-one inbox", "Calls, texts, emails and Facebook messages in one app"),
               ("Business phone number", "Keep work and personal separate"),
               ("Missed-call text-back", "An instant text when you can't pick up"),
               ("Automated lead follow-up", "Quotes and enquiries chased for you"),
               ("Review requests", "Every new and past customer asked for a genuine Google review"),
               ("Google Business Profile management", "Ongoing optimisation, photos and posts"),
               ("One-click marketing campaigns", "Win repeat work from past customers"),
               ("Local SEO &amp; AI search", "Listings, area pages and ChatGPT visibility, every month")],
     "extras": ["website", "gbp"]},
]
# Billing options for the single plan. Monthly is the default (matches the ads).
# Quarterly: 10% off, paid upfront. Annual: ~17% off (2 months free), paid upfront.
BILLING = [
    {"id": "monthly", "label": "Monthly", "per_month": 197, "billed": None, "save": None, "pill": None},
    {"id": "quarterly", "label": "Quarterly", "per_month": 177, "billed": "£531 every 3 months",
     "save": "£60 a quarter", "pill": "Save 10%"},
    {"id": "annual", "label": "Annually", "per_month": 164, "billed": "£1,970 once a year",
     "save": "£394 a year", "pill": "Save 17%"},
]

# (icon, title, description, normal price)
EXTRAS = {
    "website": ("monitor", "Lead-generating website",
                "Turns visitors into text conversations that go straight to your phone. Live in 3–5 days.", "£1,499"),
    "gbp": ("pin", "Google Business Profile setup",
            "Every section filled in properly, so you're set up to show on Google Maps.", "£299"),
}
