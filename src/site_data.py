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
    # GHL booking calendar for the free 15-minute call (permanent link, survives slug changes)
    "booking_url": "https://link.vouchdigital.co.uk/widget/booking/xbAVu7ah9p5NXexCdiO8",
    # Keep True until the site is live on vouchdigital.co.uk
    "noindex": False,
}

# Real Google reviews of Vouch Digital only. Never add invented reviews.
# Live data: src/google_reviews.json, refreshed daily from Google Places by .github/workflows/update-reviews.yml.
# The list below is only a fallback for before that file exists.
import json as _json
from pathlib import Path as _Path

_FALLBACK = {"rating": "5.0", "count": 3, "maps_url": "", "reviews": [
    {"name": "Paul McLoughlin", "date": "September 2026", "stars": 5,
     "text": "Tim is fantastic! We had a website before but Tim made a new one and we are "
             "actually noticing more calls. His team did the work quickly and kept us informed "
             "and up to date of what they're doing. Recommend highly"},
    {"name": "Matt", "date": "September 2026", "stars": 5,
     "text": "Great working with Tim and the team. They sorted our online presence and did "
             "everything they said they would"},
    {"name": "Ellie Balysz", "date": "September 2026", "stars": 5, "text": ""},
]}
_live = _Path(__file__).parent / "google_reviews.json"
GOOGLE = _json.loads(_live.read_text(encoding="utf-8")) if _live.exists() else _FALLBACK
REVIEWS = GOOGLE["reviews"]
RATING = GOOGLE["rating"]

# Facebook rating: Facebook has no simple reviews API, so this is set by hand. Keep it true to the page.
FACEBOOK = {"rating": "5.0", "url": "https://www.facebook.com/profile.php?id=61595114371482"}  # set rating to None to hide  # url: the Vouch Digital Facebook page, e.g. https://www.facebook.com/...

FAQ_HOME = [
    ("Why is the website free?",
     "Because it's part of the system. When you join the monthly plan, we build your website for free so it works "
     "hand in hand with your reviews, Google profile and lead follow-up. If you only want a website on its own, "
     "it's £1,499 as a one-off."),
    ("How much does it cost?",
     "£197 a month, everything included. You can also pay quarterly and save 10%, or yearly and save 25%. "
     "See our <a href=\"/pricing\">pricing</a>."),
    ("Am I locked into a contract?",
     "No. The monthly plan has no contract, so you can cancel anytime."),
    ("Do I own my domain?",
     "Yes. Your domain is registered in your business's name, not ours."),
    ("How long does it take to get set up?",
     "Your website is usually live within 3–5 days of us receiving your onboarding form. Then we walk you through "
     "everything on a 25-minute launch call."),
    ("How much of my time does this take?",
     "Very little: a 15-minute first call, a short onboarding form, then the launch call. After that we run it in "
     "the background while you're out on jobs."),
    ("Are the reviews genuine?",
     "Yes. We only ask your real customers, every customer is asked, and we never filter out "
     "unhappy ones. We never write, buy, incentivise or remove reviews. That's how the Digital "
     "Markets, Competition and Consumers Act 2024 says it should be done."),
    ("Do you only work with plumbers?",
     "Yes. We only work with domestic plumbers and heating engineers, anywhere in the UK. Everything is done "
     "remotely over video call and phone."),
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
# Quarterly: 10% off, paid upfront. Annual: 25% off, paid upfront.
BILLING = [
    {"id": "monthly", "label": "Monthly", "per_month": 197, "billed": None, "save": None, "pill": None},
    {"id": "quarterly", "label": "Quarterly", "per_month": 177, "billed": "£531 every 3 months",
     "save": "£60 a quarter", "pill": "Save 10%"},
    {"id": "annual", "label": "Annually", "per_month": 148, "billed": "£1,776 once a year",
     "save": "£588 a year", "pill": "Save 25%"},
]

# (icon, title, description, normal price)
EXTRAS = {
    "website": ("monitor", "Lead-generating website",
                "Turns visitors into text conversations that go straight to your phone. Live in 3–5 days.", "£1,499"),
    "gbp": ("pin", "Google Business Profile setup",
            "Every section filled in properly, so you're set up to show on Google Maps.", "£299"),
}
