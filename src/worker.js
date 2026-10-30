// Cloudflare Worker: serves the static site from public/ and handles the enquiry form.
// The GHL inbound webhook URL is a secret: set GHL_WEBHOOK_URL in Cloudflare
// (Worker → Settings → Variables and Secrets). It is never stored in this repository.

const MIN_FILL_MS = 3000;

const SERVICES = ['missed-call-text-back', 'lead-follow-up', 'all-in-one-inbox', 'websites', 'google-reviews',
  'google-business-profile', 'marketing-campaigns'];
// Service pages merged in Oct 2026: local SEO and AI search now live on the Google profile page.
const MOVED = { 'local-seo': 'google-business-profile', 'ai-search': 'google-business-profile' };
const OLD_SERVICES = Object.fromEntries(SERVICES.map((s) => [s, s]));
Object.assign(OLD_SERVICES, {
  'reviews': 'google-reviews', 'review-management': 'google-reviews', 'google-review-management': 'google-reviews',
  'gbp': 'google-business-profile', 'google-business-profile-optimisation': 'google-business-profile',
  'gbp-optimisation': 'google-business-profile', 'website-design': 'websites', 'web-design': 'websites',
  'website': 'websites', 'seo': 'google-business-profile', 'local-seo': 'google-business-profile',
  'ai-seo': 'google-business-profile', 'ai-search': 'google-business-profile',
  'ai-search-optimisation': 'google-business-profile', 'missed-call-text-back': 'missed-call-text-back',
}); // faster than this is almost certainly a bot

export default {
  async fetch(request, env) {
    const url = new URL(request.url);

    if (url.pathname === '/api/slots') return handleSlots(env);
    if (url.pathname === '/api/book') {
      if (request.method !== 'POST') return new Response('Method not allowed', { status: 405 });
      return handleBook(request, env);
    }

    if (url.pathname === '/api/enquiry') {
      if (request.method !== 'POST') return new Response('Method not allowed', { status: 405 });
      return handleEnquiry(request, env);
    }

    // Old site (GHL) used /services/*-for-plumbers style URLs: send them to the matching new page.
    const old = url.pathname.match(/^\/services\/(.+?)-for-(plumbers|electricians)\/?$/);
    if (old) return Response.redirect(url.origin + (OLD_SERVICES[old[1]] ? '/services/' + OLD_SERVICES[old[1]] : '/services'), 301);

    const moved = url.pathname.match(/^\/services\/(local-seo|ai-search)\/?$/);
    if (moved) return Response.redirect(url.origin + '/services/' + MOVED[moved[1]], 301);

    // Electricians page retired (Oct 2026): the site is plumbers-only now.
    if (/^\/electricians\/?$/.test(url.pathname)) return Response.redirect(url.origin + '/plumbers', 301);

    return env.ASSETS.fetch(request);
  },
};

async function handleEnquiry(request, env) {
  let form;
  try {
    form = await request.formData();
  } catch {
    return json({ ok: false, error: 'bad_request' }, 400);
  }
  const get = (k) => String(form.get(k) || '').trim().slice(0, 500);

  // Spam checks: honeypot filled, or submitted too fast. Pretend success so bots learn nothing.
  if (get('company_url') || Number(get('t')) < MIN_FILL_MS) return json({ ok: true });

  const SOURCES = { 'free-website': 'Free website landing page (Meta ads)' };
  const WORK = { domestic: 'Domestic', mixed: 'Both domestic & commercial', commercial: 'Commercial only' };
  // Landing page quiz answers (fixed lists, so nothing free-text gets through)
  const STATE = { slow: 'Slow, needs jobs now', inconsistent: 'Okay, but not consistent', busy: 'Busy, booked solid', starting: 'Just starting' };
  const TIMELINE = { now: 'Right away', '1-2m': 'Next month or two', later: 'Later this year', browsing: 'Just looking' };
  const TURNOVER = { u5k: 'Under £5k/month', '5-15k': '£5k–£15k/month', '15-50k': '£15k–£50k/month', '50k+': '£50k+/month' };
  const lead = {
    name: get('name'),
    business_name: get('business'),
    phone: get('phone'),
    email: get('email'),
    work_type: WORK[get('work')] || '',
    business_state: STATE[get('state')] || '',
    timeline: TIMELINE[get('timeline')] || '',
    monthly_turnover: TURNOVER[get('turnover')] || '',
    source: SOURCES[get('src')] || 'vouchdigital.co.uk form',
    page: request.headers.get('Referer') || '',
  };
  if (!lead.name || !lead.business_name || !lead.phone || !lead.email) return json({ ok: false, error: 'missing_fields' }, 400);

  // Preferred (since 30 Oct 2026): create/update the contact straight in GHL with the API key (GHL_TOKEN), tagged so
  // GHL workflows can start from the tag "website quiz". The inbound webhook (GHL_WEBHOOK_URL) is the older route.
  if (env.GHL_TOKEN) {
    let phone = lead.phone.replace(/[^\d+]/g, '');
    if (/^0\d{10}$/.test(phone)) phone = '+44' + phone.slice(1); // same format as bookings, so it's one contact
    const [firstName, ...rest] = lead.name.split(/\s+/);
    const tags = ['website quiz'];
    if (lead.work_type) tags.push('work: ' + lead.work_type.toLowerCase());
    const r = await ghl(env, '/contacts/upsert', {
      method: 'POST',
      body: JSON.stringify({ locationId: LOCATION_ID, firstName, lastName: rest.join(' '), name: lead.name,
        email: lead.email, phone, companyName: lead.business_name, source: lead.source, tags }),
    });
    return r.ok ? json({ ok: true }) : json({ ok: false, error: 'upstream' }, 502);
  }

  if (!env.GHL_WEBHOOK_URL) return json({ ok: false, error: 'not_configured' }, 503);

  const res = await fetch(env.GHL_WEBHOOK_URL, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(lead),
  });
  return res.ok ? json({ ok: true }) : json({ ok: false, error: 'upstream' }, 502);
}

// ---------- Booking box on /book-call (Trade Scale style), via the GHL API ----------
// Needs secret GHL_TOKEN (a GHL Private Integration key with calendars + contacts scopes), set in Cloudflare.
// Without it /api/slots returns 503 and the page falls back to GHL's own calendar widget.
const GHL_API = 'https://services.leadconnectorhq.com';
const CALENDAR_ID = 'DrMkJxzFYMwX68pGXSZt'; // "15 Minute Chat with Tim"
const LOCATION_ID = 'L3s5HpDyg41gJv8rwS4n'; // Vouch Digital sub-account
const TIMEZONE = 'Europe/London';
const CALL_MINUTES = 15;
const MAX_DAYS = 4;

async function ghl(env, path, init = {}) {
  const headers = { Authorization: `Bearer ${env.GHL_TOKEN}`, Version: '2021-04-15', Accept: 'application/json' };
  if (init.body) headers['Content-Type'] = 'application/json';
  const res = await fetch(GHL_API + path, { ...init, headers });
  let data = {};
  try { data = await res.json(); } catch { /* empty body */ }
  return { ok: res.ok, status: res.status, data };
}

async function freeSlots(env) {
  const start = Date.now();
  const end = start + 14 * 864e5;
  const r = await ghl(env, `/calendars/${CALENDAR_ID}/free-slots?startDate=${start}&endDate=${end}&timezone=${encodeURIComponent(TIMEZONE)}`);
  if (!r.ok) return null;
  return Object.keys(r.data)
    .filter((k) => /^\d{4}-\d{2}-\d{2}$/.test(k))
    .sort()
    .map((date) => ({ date, slots: (r.data[date] && r.data[date].slots) || [] }))
    .filter((d) => d.slots.length)
    .slice(0, MAX_DAYS);
}

async function handleSlots(env) {
  if (!env.GHL_TOKEN) return json({ ok: false, error: 'not_configured' }, 503, true);
  const days = await freeSlots(env);
  if (!days) return json({ ok: false, error: 'upstream' }, 502, true);
  return json({ ok: true, timezone: TIMEZONE, days }, 200, true);
}

async function handleBook(request, env) {
  if (!env.GHL_TOKEN) return json({ ok: false, error: 'not_configured' }, 503, true);
  let body;
  try { body = await request.json(); } catch { return json({ ok: false, error: 'bad_request' }, 400, true); }
  const get = (k) => String(body[k] || '').trim().slice(0, 200);
  const name = get('name'), email = get('email'), business = get('business'), slot = get('slot');
  let phone = get('phone').replace(/[^\d+]/g, '');
  if (/^0\d{10}$/.test(phone)) phone = '+44' + phone.slice(1); // UK mobile -> +44 so GHL matches the quiz contact
  if (name.length < 2 || !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email) || phone.replace(/\D/g, '').length < 10 || !slot) {
    return json({ ok: false, error: 'missing_fields' }, 400, true);
  }

  // Only book a time GHL still lists as free (someone else may have just taken it)
  const days = await freeSlots(env);
  if (!days) return json({ ok: false, error: 'upstream' }, 502, true);
  if (!days.some((d) => d.slots.includes(slot))) return json({ ok: false, error: 'slot_taken' }, 409, true);

  const [firstName, ...rest] = name.split(/\s+/);
  const contact = await ghl(env, '/contacts/upsert', {
    method: 'POST',
    body: JSON.stringify({ locationId: LOCATION_ID, firstName, lastName: rest.join(' '), name, email, phone,
      companyName: business || undefined, source: 'Website booking' }),
  });
  const contactId = contact.data && contact.data.contact && contact.data.contact.id;
  if (!contact.ok || !contactId) return json({ ok: false, error: 'contact' }, 502, true);

  const startMs = Date.parse(slot);
  const appt = await ghl(env, '/calendars/events/appointments', {
    method: 'POST',
    body: JSON.stringify({
      calendarId: CALENDAR_ID, locationId: LOCATION_ID, contactId,
      startTime: slot, endTime: new Date(startMs + CALL_MINUTES * 60000).toISOString(),
      title: `Vouch Digital x ${name}: free website call`, appointmentStatus: 'confirmed', toNotify: true,
    }),
  });
  if (!appt.ok) return json({ ok: false, error: appt.status === 409 || appt.status === 422 ? 'slot_taken' : 'appointment' }, 502, true);
  return json({ ok: true, start: slot, email }, 200, true);
}

function json(body, status = 200, noStore = false) {
  const headers = { 'Content-Type': 'application/json' };
  if (noStore) headers['Cache-Control'] = 'no-store';
  return new Response(JSON.stringify(body), { status, headers });
}
