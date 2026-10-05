# Vouch Digital website — rules for anyone (or any chat) working on this site

## What this is
Marketing site for Vouch Digital (trading name of Bolotin Ltd): done-for-you Google reviews, Google
Business Profile, websites, local SEO and AI search for **electricians and plumbers in London & the
South East**. Dual-trade for now; may later become electricians-only.

## How it's built
- `src/site_data.py` — business facts, real reviews, homepage FAQ. Single source of truth.
- `src/pages.py` — page bodies. `src/build.py` — shared head/header/footer. Run `python3 src/build.py`.
- `public/` — built output plus `assets/site.css` and `assets/site.js`.
- `src/worker.js` + `wrangler.jsonc` — Cloudflare Worker serving `public/` and `/api/enquiry`,
  which forwards leads to GHL. Secret `GHL_WEBHOOK_URL` is set in Cloudflare, never in the repo.
- Pushing to `main` deploys automatically via Cloudflare.

## Design
Dark green `#04201b`, mint `#14d38a`, mint tint `#e9f8f1`. Headings Outfit, body Inter.
Based on the mockup Tim approved on 4 Oct 2026.

## Never
- Invent reviews, testimonials, case studies or results. Only real Google reviews of Vouch Digital
  (DMCC Act 2024 — and it's the whole point of the business).
- Promise rankings, timescales, review counts or AI recommendations.
- Say "UK" or "England" for the service area: it's London & the South East.
- Show prices on the site.

## Launch checklist
- [x] Set `noindex` to False in `src/site_data.py`
- [ ] Real logo file and hero photo
- [x] All pages built: services + 5 service pages, /plumbers, /electricians, about, faq, contact, privacy, terms (inner pages in `src/pages_more.py`, legal text in `src/legal/`)
- [x] 301 redirects from old `/services/*-for-plumbers` URLs (in `src/worker.js`)
- [ ] `GHL_WEBHOOK_URL` secret set and a test lead received in GHL
- [x] DNS moved to Cloudflare with all records kept (5 Oct 2026); site live on vouchdigital.co.uk and www
