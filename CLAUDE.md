# Vouch Digital website — rules for anyone (or any chat) working on this site

## What this is
Marketing site for Vouch Digital (trading name of Bolotin Ltd): done-for-you Google reviews, Google
Business Profile, websites, local SEO and AI search for **domestic (Gas Safe) plumbers and heating
engineers across the UK**. Plumbers only since 14 Oct 2026 (electricians removed; /electricians 301s to
/plumbers in `src/worker.js`). Ads run nationwide, so never limit the service area to London.

**The pitch (since 14 Oct 2026, matches the Meta ads):** a free lead-generating website plus the system that
wins plumbers more jobs, £197/month, everything included, no contract. Every "Book a call" button outside the funnel opens /demo-video (the ad landing page) in a new tab (`BOOK`/`NEWTAB` in `src/pages.py`, header/footer in `src/build.py`). The old "Find My Missed Jobs" free-audit pitch is retired; don't bring it back.

**Meta ads funnel (since 30 Oct 2026; old paths /free-website and /book deleted, no redirects; the landing page was renamed /book-form → /demo-video on 12 Nov 2026 for the Instagram "Demo Video" link, and /book-form 301s to it with the query string in `src/worker.js`):** ad → `/demo-video` → quiz popup → `/book-call` (5 Nov 2026: one Title Case headline, "Wait Darren! Watch This Short Video and Pick a Time for Your Free Call 👇" (no eyebrow, no sub-line, no ratings row, at Tim's choice), the 6m44 VSL on top (`SITE["vsl_url"]`, click-to-load, clear still `SITE["vsl_still"]`; placeholder box until set), the pre-filled calendar under it, then a secondary "Get Started" button to the £197/month Stripe Payment Link (`SITE["checkout_url"]`, hidden until set) with "£197/month · No contract · Free website included". The VSL outro says "pick a time below this video" and "tap Get started below this video", so keep both under it. A sticky "📅 Book your call" button (site.js) jumps to the calendar and hides while the calendar is on screen or once booked. Tim's 30-second clip was dropped). Booking is our own Trade Scale-style box (day buttons, time buttons, one "Book My Call"; quiz leads book in one tap with their quiz details). `src/worker.js` serves `/api/slots` and `/api/book` via the GHL API (calendar "15 Minute Chat with Tim" `DrMkJxzFYMwX68pGXSZt`, location `L3s5HpDyg41gJv8rwS4n`), using Cloudflare secret `GHL_TOKEN` (a GHL Private Integration key: calendars, calendar events, contacts). `/api/slots` hides about 10% of free times (`LOOK_BUSY` in `src/worker.js`, same ones every load, at least 2 kept per day) so the calendar doesn't look empty. If the API fails or the token is missing, site.js swaps in GHL's own widget from `<template id="booker-fallback">`. A successful booking fires the pixel's Schedule event (consent only) (the GHL booking box shows "Your call is booked" in place; the old `/booked` page was deleted 30 Oct 2026). The landing page copies Kai Stone's: one headline with the price,
the VSL thumbnail, one button; every CTA (and the header "Book a call" on that page) opens the quiz (`lp_quiz()` /
`QUIZ` in `src/pages.py`). The quiz is one question (type of work) then mobile, email, name and business; extra qualifying questions were cut on 30 Oct 2026 to keep friction low until ads prove out. The bar starts at 60%, creeps up and its stripes scroll right (endowed progress, `QUIZ_PROGRESS`). No privacy link inside the quiz at Tim's choice (footer links it). Not a plumber
or commercial-only → polite exit, nothing sent, no Lead event. Answers go to GHL via `/api/enquiry` (whitelisted in
`src/worker.js`): with `GHL_TOKEN` set, the Worker upserts the contact straight into GHL tagged `website quiz` and `work: domestic`/`work: both domestic & commercial` (workflows start from that tag); `GHL_WEBHOOK_URL` is only the older fallback. Below: video testimonials (`TESTIMONIAL_VIDEOS` in `src/site_data.py`: Darren/Flotech and Selvin/MJ Services since 30 Oct 2026, each with a result quote in their own words; MP4s in `public/assets/video/` compressed to 720×1280 H.264 with faststart, covers in `public/assets/img/testimonial-*.webp`; our own player in site.js: play/pause top left and full screen top right either side of the logo in the video, and a full-width progress bar along the bottom you can tap or drag to skip; pressing play shows no controls so the hook plays clean, a tap brings them up; in desktop full screen they become one normal bottom bar: play/pause, progress, full screen; iPhone full screen is Apple's own player), also shown on the homepage above the Google reviews, then Google reviews. The landing page thumbnail is a blurred still (`SITE["vsl_poster"]`, now a blurred homepage screenshot; swap for a blurred VSL frame) with a pulsing play button that opens the quiz. The VSL itself is `SITE["vsl_url"]` (YouTube unlisted embed, ideally youtube-nocookie.com; click-to-load) and sits at the top of /book-call. Don't run ads before `vsl_url` is set: the thumbnail promises a video. The booking box itself fires the pixel's Schedule event (consent only). Both pages are noindex. /demo-video and /book-call have a looks-only header and footer (`FUNNEL` in `src/build.py`; on /book-call the button is "Pick a time" → calendar): no menu, no phone, logo not linked, buttons open the quiz, privacy and terms open in a new tab.

## How it's built
- `src/site_data.py` — business facts, homepage FAQ, plans. Single source of truth.
- Google reviews and rating come from `src/google_reviews.json`, refreshed daily from Google Places by
  `.github/workflows/update-reviews.yml` (needs secret `GOOGLE_PLACES_API_KEY` and variable `GOOGLE_PLACE_ID`;
  find the ID with the "Find Place ID" workflow). Don't hand-edit that file except to remove a deleted review; `site_data.py` has a fallback list.
- Reviews carousel (30 Oct 2026, 7 reviews): Tim's spec after a long day of iPhone jank: copy the pre-loop carousel (commit b25ce52), which was smooth on his iPhone. So: the phone's own scrolling with scroll-snap (nothing of ours moves the cards); the reviews copied 5 times either side (`SIDE` in site.js) and it opens on the middle review, centred with neighbours peeking in; one review per swipe (`scroll-snap-align:center; scroll-snap-stop:always`). Dots are the pre-loop dots (plain buttons in a flex row, the pill a .2s width change) made endless: the pill starts in the middle and stays there; each swipe hands it to the next dot like before while a dot shrinks away at one end and a new one grows in at the other (`.rd.p0`-`.p5` classes by distance from the pill). Tried and rejected the same day, all fine in desktop Chrome's phone view but janky or worse on a real iPhone: invisible scroll jumps, our own touch carousel, Instagram dots that each slide and resize, a fixed pill with dots sliding under it, and Swiper (Tim: "looks worse than everything you built"). Desktop (981px+): exactly three reviews in a narrower band (`.rev-stage`, max 960px), the middle one centred, with round arrows either side (`.rev-arrow`, created in site.js, shown only on hover-capable screens). Always test carousel changes on a real iPhone. Reviewers show by first name only (`first_name()` in `src/pages.py`).
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
  `<noscript>` image is deliberately left out (it would track people who can't see the banner). Ahrefs Web Analytics (cookie-free, key in `loadAnalytics()` in site.js) also loads only after Accept, from the same consent code (10 Nov 2026). Never add any tracking or non-essential cookies that load before consent,
  keep Reject on the banner as visible and easy as Accept (ICO), and update the privacy policy cookies section
  (`src/legal/privacy.html`) whenever tracking changes.

## Design
Dark green `#04201b`, mint `#14d38a`, mint tint `#e9f8f1`. Headings Outfit, body Inter.
Based on the mockup Tim approved on 4 Oct 2026. Only the homepage has the big dark hero. Inner pages open with a light heading (`hero()` in `src/pages_more.py`, class `page-hero`); on /pricing and /faq the first section carries the H1 itself (class `first`), so nothing is said twice.
Mascot (Tim's own artwork): `public/assets/img/mascot.webp`, used via `mascot()` in `src/pages.py` (final CTA on every page, beside the pricing card).

## Never
- Invent reviews, testimonials, case studies or results. Only real Google reviews of Vouch Digital
  (DMCC Act 2024 — and it's the whole point of the business).
- Promise rankings, results timescales, review counts or AI recommendations. (Delivery times we control
  are fine: the website build is "roughly 3–5 days" in the 3-step process.)
- Mention electricians, or limit the service area to London & the South East: it's the whole UK.
- Show a crossed-out price that isn't a real price we charge (website £1,499 and GBP setup £299 are real).
  Plans live in `PLANS` in `src/site_data.py` and show on /pricing.
- Two plans on /pricing, side by side: Growth Package (`PLANS`) and Exclusive Package (`EXCLUSIVE` in
  `src/site_data.py`, from £997/month plus ad spend, tailored, "Book a call"). Exclusive is the price anchor; its
  extras have no service pages, so each opens in place. Not on the homepage or service pages. One billing toggle
  drives both cards (monthly, or annual upfront with 3 months free; quarterly removed 28 Oct 2026).
- 30-day guarantee (9 Nov 2026, matches the Meta ads): not happy with the system (any of the services, including the website; changed from website-only 10 Nov 2026 to match the ads "if you don't love our system in the first 30 days") → tell us within 30 days of the first
  payment and we refund it in full (the annual payment in full on an annual plan); the agreement ends at once and the
  website terms apply (taken down, or the £499 transfer fee). Once per business. It's a satisfaction guarantee, never a
  results guarantee (terms clause 8 still promises no outcomes). Lives in terms clause 5, under the Growth card on
  /pricing (`.pk-guar`), the pricing small print, and FAQ_HOME "What if I'm not happy?". Keep all four in step.

## Launch checklist
- [x] Set `noindex` to False in `src/site_data.py`
- [ ] Real logo file and hero photo
- [x] All pages built: services + 5 service pages, /plumbers, about, faq, contact, privacy, terms (inner pages in `src/pages_more.py`, legal text in `src/legal/`)
- [x] 301 redirects from old `/services/*-for-plumbers` URLs (in `src/worker.js`)
- [x] `GHL_TOKEN` secret set in Cloudflare (runtime); test booking 30 Oct 2026 worked (slots, appointment, Google Meet link, invite email). Contact went to an existing contact via upsert (same phone/email), so check with a fresh number
- [ ] The booking confirmation says "Check your WhatsApp: I've sent you a short video": the GHL "call booked" WhatsApp workflow must be live before ads run
- [x] DNS moved to Cloudflare with all records kept (5 Oct 2026); site live on vouchdigital.co.uk and www
