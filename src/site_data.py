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
    "area": "London and the South East",
    # Keep True until the site is live on vouchdigital.co.uk
    "noindex": True,
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
    ("Do you only work with electricians and plumbers?",
     "Yes. We only work with electricians, plumbers and heating engineers in London and the South "
     "East. Everything we build, from the review request wording to the website pages, is shaped "
     "around how a local trade business actually wins work."),
    ("How long does it take to see results?",
     "We don't make promises about timescales. Reviews and visibility build over time as more "
     "genuine reviews come in and your profile stays active. We handle the setup and keep the "
     "work going month after month."),
    ("What areas do you work in?",
     "London and the South East. We know the local competition, and we're close enough to meet "
     "in person if you'd prefer."),
    ("Do I need a new website?",
     "Not always. If your current website works, we'll work with it. If it's slow, hard to use on "
     "a phone or not turning visitors into calls, a new one will do a better job. We'll tell you "
     "honestly on the call."),
    ("Are the reviews genuine?",
     "Yes. We only ask your real customers, every customer is asked, and we never filter out "
     "unhappy ones. We never write, buy, incentivise or remove reviews. That's how the Digital "
     "Markets, Competition and Consumers Act 2024 says it should be done."),
    ("Am I locked into a contract?",
     "No. It's month to month, with no lock-in. Pricing is discussed on the call once we've seen "
     "your business."),
]
