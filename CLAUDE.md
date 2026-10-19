# Vouch Digital website — rules for anyone (or any chat) working on this site

## What this is
Marketing site for Vouch Digital (trading name of Bolotin Ltd): done-for-you Google reviews, Google
Business Profile, websites, local SEO and AI search for **domestic (Gas Safe) plumbers and heating
engineers across the UK**. Plumbers only since 14 Oct 2026 (electricians removed; /electricians 301s to
/plumbers in `src/worker.js`). Ads run nationwide, so never limit the service area to London.

**The pitch (since 14 Oct 2026, matches the Meta ads):** a free lead-generating website plus the system that
wins plumbers more jobs, £197/month, everything included, no contract. Every button is "Book a call" → /book
(GHL calendar). The old "Find My Missed Jobs" free-audit pitch is retired; don't bring it back.

## How it's built
- `src/site_data.py` — business facts, homepage FAQ, plans. Single source of truth.
- Google reviews and rating come from `src/google_reviews.json`, refreshed daily from Google Places by
  `.github/workflows/update-reviews.yml` (needs secret `GOOGLE_PLACES_API_KEY` and variable `GOOGLE_PLACE_ID`;
  find the ID with the "Find Place ID" workflow). Don't hand-edit that file except to remove a deleted review; `site_data.py` has a fallback list.
- Reviews carousel: dots on every screen size (one per scroll position, so fewer on desktop where three show at once), no scrollbar. Planned: once there are ~10 Google reviews, make it an endless looping carousel.
- The review updater keeps every review it has ever fetched (Google only returns the 5 newest) and adds new ones on top. If a reviewer deletes their review on Google, remove it from `src/google_reviews.json` by hand.
- Trustpilot TrustScore (hero) is set by hand in `TRUSTPILOT` in `src/site_data.py`; shown with the Trustpilot star logo at Tim's choice (15 Oct 2026, free plan; remove it if Trustpilot asks).
- Facebook rating (hero) is set by hand in `FACEBOOK` in `src/site_data.py`; keep it true to the Facebook page.
- Services: seven pages in two systems (1 Win more jobs: website, Google reviews, Google profile/local SEO/AI search,
  marketing campaigns; 2 Stop losing jobs: missed-call text-back, lead follow-up, inbox). Win more jobs leads (swapped 18 Oct 2026) to match the free-website ad. Content and order in
  `src/services_data.py`; homepage cards and /services both read from it. /services/local-seo and
  /services/ai-search 301 to /services/google-business-profile. Add a demo video by setting `video`.
  No prices on the homepage (pricing lives on /pricing only).
- `src/pages.py` — page bodies. `src/build.py` — shared head/header/footer. Run `python3 src/build.py`.
- `public/` — built output plus `assets/site.css` and `assets/site.js`.
- `src/worker.js` + `wrangler.jsonc` — Cloudflare Worker serving `public/` and `/api/enquiry`,
  which forwards leads to GHL. Secret `GHL_WEBHOOK_URL` is set in Cloudflare, never in the repo.
- Pushing to `main` deploys automatically via Cloudflare.
- Meta pixel (ID in `SITE["meta_pixel_id"]`): Meta's base code sits in every page's `<head>` (`PIXEL_HEAD` in
  `src/build.py`) paused with `fbq('consent','revoke')`; clicking Accept on the cookie banner calls
  `fbq('consent','grant')` and fires PageView (consent code at the end of `public/assets/site.js`; "Cookie settings"
  in the footer reopens it). Lead fires when the enquiry form is sent, only for visitors who accepted. Meta's
  `<noscript>` image is deliberately left out (it would track people who can't see the banner). Never add any tracking or non-essential cookies that load before consent,
  keep Reject on the banner as visible and easy as Accept (ICO), and update the privacy policy cookies section
  (`src/legal/privacy.html`) whenever tracking changes.

## Design
Dark green `#04201b`, mint `#14d38a`, mint tint `#e9f8f1`. Headings Outfit, body Inter.
Based on the mockup Tim approved on 4 Oct 2026. Mascot (Tim's own artwork): `public/assets/img/mascot.webp`, used via `mascot()` in `src/pages.py` (final CTA on every page, beside the pricing card).

## Never
- Invent reviews, testimonials, case studies or results. Only real Google reviews of Vouch Digital
  (DMCC Act 2024 — and it's the whole point of the business).
- Promise rankings, results timescales, review counts or AI recommendations. (Delivery times we control
  are fine: the website build is "roughly 3–5 days" in the 3-step process.)
- Mention electricians, or limit the service area to London & the South East: it's the whole UK.
- Show a crossed-out price that isn't a real price we charge (website £1,499 and GBP setup £299 are real).
  Plans live in `PLANS` in `src/site_data.py` and show on /pricing.

## Launch checklist
- [x] Set `noindex` to False in `src/site_data.py`
- [ ] Real logo file and hero photo
- [x] All pages built: services + 5 service pages, /plumbers, about, faq, contact, privacy, terms (inner pages in `src/pages_more.py`, legal text in `src/legal/`)
- [x] 301 redirects from old `/services/*-for-plumbers` URLs (in `src/worker.js`)
- [ ] `GHL_WEBHOOK_URL` secret set and a test lead received in GHL
- [x] DNS moved to Cloudflare with all records kept (5 Oct 2026); site live on vouchdigital.co.uk and www
