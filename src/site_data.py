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
    # GHL booking calendar for the 15-minute demo call. GHL's own domain (always works), not link.vouchdigital.co.uk
    "booking_url": "https://api.leadconnectorhq.com/widget/booking/xbAVu7ah9p5NXexCdiO8",
    # Keep True until the site is live on vouchdigital.co.uk
    "noindex": False,
    # Meta (Facebook) pixel. Only loads after a visitor accepts cookies (see the consent code in site.js).
    "meta_pixel_id": "1737681243973132",
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

# Trustpilot TrustScore, set by hand (5.0 from 1 review, 15 Oct 2026). Keep it equal to the public profile.
# Free plan: no Trustpilot logo/stars (brand assets) on our site, so it's shown as text with our own icon.
TRUSTPILOT = {"rating": "5.0", "url": "https://uk.trustpilot.com/review/vouchdigital.co.uk"}

# Facebook rating: Facebook has no simple reviews API, so this is set by hand. Keep it true to the page.
FACEBOOK = {"rating": "5.0", "url": "https://www.facebook.com/profile.php?id=61595114371482"}  # url: the Vouch Digital Facebook page, e.g. https://www.facebook.com/...

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
     "Yes. We only ask your real customers. We never write, buy, incentivise or remove reviews. That's how the Digital "
     "Markets, Competition and Consumers Act 2024 says it should be done."),
    ("Do you only work with plumbers?",
     "Yes. We only work with domestic plumbers and heating engineers, anywhere in the UK."),
]


# Pricing plans (shown on /pricing). Crossed-out prices must be real prices we charge.
PLANS = [
    {"name": "Growth Package", "price": 197, "tag": "Everything you need to win more jobs from Google and ChatGPT.",
     "featured": True, "lead": "What's included",
     "items": [("All-in-one inbox", "Calls, texts, emails and Facebook messages in one app"),
               ("Business phone number", "Keep work and personal separate"),
               ("Missed-call text-back", "An instant text when you can't pick up"),
               ("Automated lead follow-up", "Quotes and enquiries chased for you"),
               ("Review requests", "Every new and past customer asked for a genuine Google review"),
               ("Google Business Profile management", "Ongoing optimisation, photos and posts"),
               ("One-click marketing campaigns", "Win repeat work from past customers"),
               ("Local SEO &amp; AI search", "Listings, area pages and ChatGPT visibility, every month")],
     "extras": ["website"]},
]
# Second, higher plan. Shown only on /pricing, beside Growth as the price anchor (not on the homepage or
# service pages, which have no pages for these extras). Tailored per client, so it's sold on a call.
# Ad spend is paid by the client directly to Google. Billing follows the same toggle as Growth (10% / 25% off).
EXCLUSIVE = {
    "name": "Exclusive Package", "price": 997, "label": "Tailored to you",
    "note": "Plus ad spend",
    "pill": "Built around your business",
    "items": [("Google Ads (PPC) for boiler installs", "We set up and manage Google Ads that put you in front of homeowners searching for a new boiler in your area, so install enquiries come in now while your reviews and Google profile keep growing."),
              ("Instant online boiler quotes", "Homeowners answer a few quick questions on your website, see a price range straight away and book a free survey, so you win the people who want a price now instead of losing them to a national online installer."),
              ("Good, Better, Best quotes", "Every quote shows three options in your branding, with a short video explaining each boiler you fit. Customers compare your options instead of other plumbers' prices, and the better boilers become an easy step up."),
              ("Monthly payments for customers", "We help you get set up with a boiler finance partner and show monthly prices properly on your website and quotes. Spreading the cost helps you win more of your quotes and makes higher-end boilers easier to say yes to."),
              ("Your own boiler care plan", "A monthly plan covering each customer's annual service and priority call-outs, with the sign-up page, payments and reminders set up for you. You get steady income all year, including the quieter summer months, and customers who come to you first when their boiler needs replacing."),
              ("AI receptionist", "Calls you miss are answered, callers' details taken and surveys booked, so you stop losing installs to the engineer down the road while you're busy on a job."),
              ("Monthly sales training", "A monthly session with Tim and a sales specialist on turning more surveys into installs, so you get more out of every enquiry you pay for."),
              ("Priority support", "You go to the front of the queue whenever you need something, so changes and fixes happen quickly.")],
    "billing": {"monthly": (997, None, None),
                "quarterly": (897, "£2,691 every 3 months", "£1,200 a year"),
                "annual": (748, "£8,976 once a year", "£2,988 a year")},
}
# Billing options for Growth (Exclusive has its own figures in EXCLUSIVE["billing"]). Monthly is the default (matches the ads).
# Quarterly: 10% off, paid upfront. Annual: 25% off, paid upfront.
BILLING = [
    {"id": "monthly", "label": "Monthly", "per_month": 197, "billed": None, "save": None, "pill": None},
    {"id": "quarterly", "label": "Quarterly", "per_month": 177, "billed": "£531 every 3 months",
     "save": "£240 a year", "pill": "Save 10%"},
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
