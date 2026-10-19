// Mobile menu
const menuBtn = document.querySelector('.menu-btn');
const nav = document.getElementById('nav');
if (menuBtn && nav) {
  menuBtn.addEventListener('click', () => {
    const open = nav.classList.toggle('open');
    menuBtn.setAttribute('aria-expanded', open);
  });
}

// Enquiry forms: save the lead, then go to the booking page
const started = Date.now();
document.querySelectorAll('form.enquiry').forEach((form) => {
  const msg = form.querySelector('.form-msg');
  const show = (cls, text) => { msg.className = 'form-msg ' + cls; msg.textContent = text; };
  form.addEventListener('submit', async (e) => {
    e.preventDefault();
    const missing = [...form.querySelectorAll('[required]')].find((el) => !el.value.trim());
    if (missing) { show('err', 'Please fill in ' + missing.getAttribute('aria-label').toLowerCase() + '.'); missing.focus(); return; }
    const email = form.querySelector('[name=email]');
    if (email && !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email.value.trim())) { show('err', 'Please check your email address.'); email.focus(); return; }
    form.querySelector('[name=t]').value = String(Date.now() - started);
    const btn = form.querySelector('button[type=submit]');
    btn.disabled = true;
    const data = new FormData(form);
    try {
      // Save the lead to GHL. Even if this fails, the booking step still captures them.
      await fetch(form.action, { method: 'POST', body: data });
    } catch (_) { /* carry on to booking */ }
    try {
      sessionStorage.setItem('vouch_lead', JSON.stringify({
        name: data.get('name'), business: data.get('business'), email: data.get('email'), phone: data.get('phone'),
      }));
    } catch (_) { /* private mode: the calendar will just ask again */ }
    // Meta pixel Lead event (only exists if the visitor accepted cookies)
    if (window.fbq) window.fbq('track', 'Lead');
    window.location.href = '/book';
  });
});

// Booking page: load the GHL calendar with the visitor's details pre-filled
const booking = document.querySelector('iframe.booking');
if (booking) {
  let lead = {};
  try { lead = JSON.parse(sessionStorage.getItem('vouch_lead') || '{}'); } catch (_) {}
  const [first = '', ...rest] = String(lead.name || '').trim().split(/\s+/);
  const params = new URLSearchParams();
  if (first) params.set('first_name', first);
  if (rest.length) params.set('last_name', rest.join(' '));
  if (lead.name) params.set('full_name', String(lead.name).trim());
  if (lead.business) params.set('company_name', String(lead.business).trim());
  if (lead.email) params.set('email', lead.email);
  if (lead.phone) {
    // UK mobiles: 07700 900123 -> +447700900123 so GHL matches the same contact
    const digits = String(lead.phone).replace(/[^\d+]/g, '');
    params.set('phone', /^0\d{10}$/.test(digits) ? '+44' + digits.slice(1) : digits);
  }
  const qs = params.toString();
  // GHL's resize script expects the id format <calendarId>_<timestamp>
  booking.id = booking.dataset.src.split('/').pop() + '_' + Date.now();
  booking.src = booking.dataset.src + (qs ? '?' + qs : '');
}

// Pricing: monthly / quarterly / annual toggle
const pk = document.querySelector('.pk[data-base]');
if (pk) {
  const base = Number(pk.dataset.base);
  const opts = Object.fromEntries([...pk.querySelectorAll('template[data-bill-opt]')].map((t) => [t.dataset.billOpt, t.dataset]));
  const show = (id) => {
    const o = opts[id];
    document.querySelectorAll('[data-bill]').forEach((b) => b.setAttribute('aria-selected', b.dataset.bill === id));
    pk.querySelector('.pk-num').textContent = '£' + o.per;
    const was = pk.querySelector('.pk-was');
    was.hidden = Number(o.per) === base;
    pk.querySelector('.pk-billed').textContent = o.billed ? 'Billed ' + o.billed + '.' : 'Billed monthly.';
    // The pill is always shown (keeps the card the same height): savings upfront, "no contract" monthly.
    const save = pk.querySelector('.pk-save');
    save.classList.toggle('is-note', !o.save);
    save.innerHTML = o.save ? 'You save <b></b>' : 'No contract, cancel anytime';
    if (o.save) save.querySelector('b').textContent = o.save;
  };
  document.querySelectorAll('[data-bill]').forEach((b) => b.addEventListener('click', () => show(b.dataset.bill)));
}

// Header turns solid once the page scrolls (it stays fixed at the top)
{
  const head = document.querySelector('.site-head');
  const onScroll = () => head && head.classList.toggle('scrolled', window.scrollY > 10);
  window.addEventListener('scroll', onScroll, { passive: true });
  onScroll();
}

// Reviews carousel (mobile and desktop): one dot per position the row can scroll to (one per review on a phone,
// fewer on desktop where three show at once). Worked out live, so it stays right after fonts load or a resize.
document.querySelectorAll('.rev-carousel').forEach((c) => {
  const dots = c.parentElement.querySelector('.rev-dots');
  const cards = [...c.children];
  if (!dots || cards.length < 2) return;
  let stops = [];
  const build = () => {
    const max = c.scrollWidth - c.clientWidth;
    stops = [...new Set(cards.map((el) => Math.round(Math.min(el.offsetLeft - cards[0].offsetLeft, max))))];
    dots.hidden = stops.length < 2;
    dots.innerHTML = stops.map((_, i) => `<button type="button" aria-label="Show reviews, position ${i + 1} of ${stops.length}"></button>`).join('');
    [...dots.children].forEach((b, i) => b.addEventListener('click', () => c.scrollTo({ left: stops[i], behavior: 'smooth' })));
    update();
  };
  const update = () => {
    const x = c.scrollLeft;
    let best = 0;
    stops.forEach((s, i) => { if (Math.abs(s - x) < Math.abs(stops[best] - x)) best = i; });
    [...dots.children].forEach((b, i) => b.setAttribute('aria-current', String(i === best)));
  };
  c.addEventListener('scroll', update, { passive: true });
  let t;
  window.addEventListener('resize', () => { clearTimeout(t); t = setTimeout(build, 150); });
  window.addEventListener('load', build);
  build();
});

// Cookie consent + Meta pixel. The pixel only loads after the visitor clicks Accept (UK PECR / UK GDPR).
// Choice is remembered in localStorage; "Cookie settings" in the footer reopens the banner.
{
  const KEY = 'vouch_cookie_consent';
  const pixelId = document.querySelector('meta[name="meta-pixel-id"]')?.content;
  const get = () => { try { return localStorage.getItem(KEY); } catch (_) { return null; } };
  const set = (v) => { try { localStorage.setItem(KEY, v); } catch (_) { /* private mode */ } };

  const loadPixel = () => {
    if (!pixelId || window.fbq) return;
    /* Meta's standard base code */
    !function(f,b,e,v,n,t,s){if(f.fbq)return;n=f.fbq=function(){n.callMethod?
    n.callMethod.apply(n,arguments):n.queue.push(arguments)};if(!f._fbq)f._fbq=n;
    n.push=n;n.loaded=!0;n.version='2.0';n.queue=[];t=b.createElement(e);t.async=!0;
    t.src=v;s=b.getElementsByTagName(e)[0];s.parentNode.insertBefore(t,s)}(window,
    document,'script','https://connect.facebook.net/en_US/fbevents.js');
    window.fbq('init', pixelId);
    window.fbq('track', 'PageView');
  };

  // Remove Meta's cookies if someone withdraws consent
  const clearMetaCookies = () => {
    const host = location.hostname.replace(/^www\./, '');
    ['_fbp', '_fbc'].forEach((name) => {
      [location.hostname, '.' + host].forEach((d) => {
        document.cookie = `${name}=; Max-Age=0; path=/; domain=${d}`;
      });
      document.cookie = `${name}=; Max-Age=0; path=/`;
    });
  };

  let banner;
  const close = () => { if (banner) { banner.remove(); banner = null; } };
  const showBanner = () => {
    if (banner) return;
    banner = document.createElement('div');
    banner.className = 'cookie-banner';
    banner.setAttribute('role', 'dialog');
    banner.setAttribute('aria-label', 'Cookie choices');
    banner.innerHTML = `
      <p><strong>Allow cookies from Vouch Digital?</strong>
      <span>Learn more in our <a href="/privacy#cookies">Privacy Policy</a>.</span></p>
      <div class="cookie-actions">
        <button type="button" class="btn cookie-reject" data-consent="denied">Reject</button>
        <button type="button" class="btn btn-mint" data-consent="granted">Accept</button>
      </div>`;
    banner.querySelectorAll('[data-consent]').forEach((b) => b.addEventListener('click', () => {
      const choice = b.dataset.consent;
      const before = get();
      set(choice);
      close();
      if (choice === 'granted') loadPixel();
      else if (before === 'granted') { clearMetaCookies(); location.reload(); } // stop a pixel that's already running
    }));
    document.body.appendChild(banner);
  };

  document.querySelectorAll('[data-cookie-settings]').forEach((b) => b.addEventListener('click', showBanner));
  const choice = get();
  if (choice === 'granted') loadPixel();
  else if (choice !== 'denied') showBanner();
}
