// Cloudflare Worker: serves the static site from public/ and handles the enquiry form.
// The GHL inbound webhook URL is a secret: set GHL_WEBHOOK_URL in Cloudflare
// (Worker → Settings → Variables and Secrets). It is never stored in this repository.

const MIN_FILL_MS = 3000;

const SERVICES = ['google-reviews', 'google-business-profile', 'websites', 'local-seo', 'ai-search'];
const OLD_SERVICES = Object.fromEntries(SERVICES.map((s) => [s, s]));
Object.assign(OLD_SERVICES, {
  'reviews': 'google-reviews', 'review-management': 'google-reviews', 'google-review-management': 'google-reviews',
  'gbp': 'google-business-profile', 'google-business-profile-optimisation': 'google-business-profile',
  'gbp-optimisation': 'google-business-profile', 'website-design': 'websites', 'web-design': 'websites',
  'website': 'websites', 'seo': 'local-seo', 'ai-seo': 'ai-search', 'ai-search-optimisation': 'ai-search',
}); // faster than this is almost certainly a bot

export default {
  async fetch(request, env) {
    const url = new URL(request.url);

    if (url.pathname === '/api/enquiry') {
      if (request.method !== 'POST') return new Response('Method not allowed', { status: 405 });
      return handleEnquiry(request, env);
    }

    // Old site (GHL) used /services/*-for-plumbers style URLs: send them to the matching new page.
    const old = url.pathname.match(/^\/services\/(.+?)-for-(plumbers|electricians)\/?$/);
    if (old) return Response.redirect(url.origin + (OLD_SERVICES[old[1]] ? '/services/' + OLD_SERVICES[old[1]] : '/services'), 301);

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

  const lead = {
    name: get('name'),
    business_name: get('business'),
    phone: get('phone'),
    email: get('email'),
    source: 'vouchdigital.co.uk audit form',
    page: request.headers.get('Referer') || '',
  };
  if (!lead.name || !lead.business_name || !lead.phone || !lead.email) return json({ ok: false, error: 'missing_fields' }, 400);

  if (!env.GHL_WEBHOOK_URL) return json({ ok: false, error: 'not_configured' }, 503);

  const res = await fetch(env.GHL_WEBHOOK_URL, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(lead),
  });
  return res.ok ? json({ ok: true }) : json({ ok: false, error: 'upstream' }, 502);
}

function json(body, status = 200) {
  return new Response(JSON.stringify(body), { status, headers: { 'Content-Type': 'application/json' } });
}
