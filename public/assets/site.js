// /booked: GHL's calendar may open the thank-you page inside its own iframe. Same site, so lift it to the full window.
const framed = window.top !== window.self && document.querySelector('[data-break-frame]');
if (framed) { try { window.top.location.href = location.href; } catch (_) { /* leave it */ } }

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
    // Commercial-only businesses aren't a fit: say so politely, don't send them to the calendar,
    // and don't tell Meta it was a lead (so the ads don't learn to find more of them).
    if (data.get('work') === 'commercial') {
      btn.disabled = false;
      show('ok', "Thanks! We only work with domestic plumbing and heating businesses, so we're probably not the right fit. We've got your details and Tim will be in touch if we can help.");
      return;
    }
    try {
      sessionStorage.setItem('vouch_lead', JSON.stringify({
        name: data.get('name'), business: data.get('business'), email: data.get('email'), phone: data.get('phone'),
      }));
    } catch (_) { /* private mode: the calendar will just ask again */ }
    // Meta pixel Lead event (only exists if the visitor accepted cookies)
    try { if (window.fbq && localStorage.getItem('vouch_cookie_consent') === 'granted') window.fbq('track', 'Lead'); } catch (_) {}
    window.location.href = '/book-call';
  });
});

// Landing page quiz (/book-form): a multi-step popup. Every [data-quiz-open] opens it (falls back to /book-call).
const quiz = document.getElementById('quiz');
if (quiz) {
  const form = quiz.querySelector('.qz-form');
  const steps = [...quiz.querySelectorAll('.qz-step:not([data-end])')];
  const end = quiz.querySelector('[data-end]');
  const bar = quiz.querySelector('.qz-bar');
  const back = quiz.querySelector('.qz-back');
  let i = 0, opened = 0, lastFocus = null;
  const go = (n) => {
    i = n;
    [...steps, end].forEach((s) => { s.hidden = true; });
    const s = steps[i];
    s.hidden = false;
    const pct = s.dataset.progress;
    bar.querySelector('span').style.width = pct + '%';
    bar.querySelector('em').textContent = pct + '%';
    bar.setAttribute('aria-valuenow', pct);
    back.style.visibility = i ? 'visible' : 'hidden';
    (s.querySelector('input') || s.querySelector('button')).focus({ preventScroll: true });
  };
  const open = () => {
    lastFocus = document.activeElement;
    if (!opened) opened = Date.now();
    quiz.hidden = false;
    document.documentElement.classList.add('qz-on');
    go(i);
  };
  const close = () => {
    quiz.hidden = true;
    document.documentElement.classList.remove('qz-on');
    if (lastFocus) lastFocus.focus({ preventScroll: true });
  };
  document.querySelectorAll('[data-quiz-open]').forEach((el) => el.addEventListener('click', (e) => { e.preventDefault(); open(); }));
  quiz.querySelectorAll('[data-quiz-close]').forEach((el) => el.addEventListener('click', close));
  quiz.addEventListener('click', (e) => { if (e.target === quiz) close(); });
  document.addEventListener('keydown', (e) => { if (e.key === 'Escape' && !quiz.hidden) close(); });
  back.addEventListener('click', () => { if (i > 0) go(i - 1); });

  // Multiple-choice steps: pick an answer and move on. Not a plumber, or commercial only: polite exit.
  quiz.querySelectorAll('.qz-choice').forEach((b) => b.addEventListener('click', () => {
    const step = b.closest('.qz-step');
    form.elements[step.dataset.field].value = b.dataset.value;
    step.querySelectorAll('.qz-choice').forEach((x) => x.classList.toggle('on', x === b));
    if (step.dataset.field === 'work' && (b.dataset.value === 'not' || b.dataset.value === 'commercial')) {
      steps.forEach((s) => { s.hidden = true; });
      end.hidden = false;
      back.style.visibility = 'visible';
      end.querySelector('button').focus();
      return;
    }
    setTimeout(() => go(i + 1), 180);
  }));

  // Typed steps: check the answer, then continue (Enter works too). The last one sends the lead.
  const checks = {
    phone: (v) => v.replace(/[^\d]/g, '').length >= 10 || 'Please enter your mobile number.',
    email: (v) => /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(v) || 'Please check your email address.',
    name: (v) => v.length > 1 || 'Please enter your name.',
    business: (v) => v.length > 1 || 'Please enter your business name.',
  };
  const submit = async (btn) => {
    btn.disabled = true;
    form.elements.t.value = String(Date.now() - opened);
    const data = new FormData(form);
    try { await fetch(form.action, { method: 'POST', body: data }); } catch (_) { /* the calendar still captures them */ }
    try {
      sessionStorage.setItem('vouch_lead', JSON.stringify({
        name: data.get('name'), business: data.get('business'), email: data.get('email'), phone: data.get('phone'),
      }));
    } catch (_) {}
    try { if (window.fbq && localStorage.getItem('vouch_cookie_consent') === 'granted') window.fbq('track', 'Lead'); } catch (_) {}
    window.location.href = '/book-call';
  };
  quiz.querySelectorAll('.qz-next:not([data-quiz-close])').forEach((btn) => {
    const step = btn.closest('.qz-step');
    const input = step.querySelector('input');
    const err = step.querySelector('.qz-err');
    const next = () => {
      const ok = checks[step.dataset.field](input.value.trim());
      if (ok !== true) { err.textContent = ok; input.focus(); return; }
      err.textContent = '';
      if (step === steps[steps.length - 1]) submit(btn); else go(i + 1);
    };
    btn.addEventListener('click', next);
    input.addEventListener('keydown', (e) => { if (e.key === 'Enter') { e.preventDefault(); next(); } });
  });
}

// VSL: click-to-play, so nothing loads from the video host until the visitor presses play
document.querySelectorAll('.vsl-play').forEach((b) => b.addEventListener('click', () => {
  const f = document.createElement('iframe');
  f.src = b.dataset.embed;
  f.title = 'Video from Tim at Vouch Digital';
  f.allow = 'autoplay; fullscreen; picture-in-picture';
  f.allowFullscreen = true;
  b.replaceWith(f);
}));

// Booking page: "Wait Darren!" when they've just come from the form
{
  const h = document.querySelector('[data-first]');
  let lead = {};
  try { lead = JSON.parse(sessionStorage.getItem('vouch_lead') || '{}'); } catch (_) {}
  const first = String(lead.name || '').trim().split(/\s+/)[0];
  if (h && first) h.textContent = (h.closest('.booked-hero') ? ', ' : ' ') + first;
}

// Booking page: GHL's own calendar widget, pre-filled with the visitor's details (fallback for the booking box)
const getLead = () => { try { return JSON.parse(sessionStorage.getItem('vouch_lead') || '{}'); } catch (_) { return {}; } };
const ukPhone = (p) => { const d = String(p || '').replace(/[^\d+]/g, ''); return /^0\d{10}$/.test(d) ? '+44' + d.slice(1) : d; };
function loadGhlCalendar(booking) {
  const lead = getLead();
  const [first = '', ...rest] = String(lead.name || '').trim().split(/\s+/);
  const params = new URLSearchParams();
  if (first) params.set('first_name', first);
  if (rest.length) params.set('last_name', rest.join(' '));
  if (lead.name) params.set('full_name', String(lead.name).trim());
  if (lead.business) params.set('company_name', String(lead.business).trim());
  if (lead.email) params.set('email', lead.email);
  if (lead.phone) params.set('phone', ukPhone(lead.phone)); // +44 so GHL matches the same contact
  const qs = params.toString();
  // GHL's resize script expects the id format <calendarId>_<timestamp>
  booking.id = booking.dataset.src.split('/').pop() + '_' + Date.now();
  booking.src = booking.dataset.src + (qs ? '?' + qs : '');
}
document.querySelectorAll('iframe.booking').forEach(loadGhlCalendar);

// Booking page: our own booking box (Trade Scale style). Day buttons, time buttons, one "Book My Call".
// Quiz leads book in one tap (details come from the quiz); anyone else fills in name, mobile and email.
const booker = document.getElementById('booker');
if (booker) {
  const TZ = 'Europe/London';
  const lead = getLead();
  const known = lead.name && lead.email && lead.phone;
  const fallback = () => {
    const tpl = document.getElementById('booker-fallback');
    booker.replaceWith(tpl.content.cloneNode(true));
    document.querySelectorAll('iframe.booking:not([src])').forEach(loadGhlCalendar);
  };
  const fmt = (iso, opts) => new Intl.DateTimeFormat('en-GB', { timeZone: TZ, ...opts }).format(new Date(iso));
  const esc = (v) => String(v).replace(/[&<>"]/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]));
  let days = [], day = 0, slot = null;

  const render = () => {
    const d = days[day];
    booker.innerHTML = `
      <p class="bk-title"><svg viewBox="0 0 24 24" aria-hidden="true"><circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/></svg>Book your free 15-minute call</p>
      <div class="bk-days" role="group" aria-label="Choose a day">${days.map((x, i) => `
        <button type="button" class="bk-day" data-i="${i}" aria-pressed="${i === day}">
          <small>${fmt(x.slots[0], { weekday: 'short' })}</small><b>${fmt(x.slots[0], { day: 'numeric' })}</b><small>${fmt(x.slots[0], { month: 'short' })}</small></button>`).join('')}</div>
      <div class="bk-times" role="group" aria-label="Choose a time">${d.slots.map((s) => `
        <button type="button" class="bk-time" data-slot="${s}" aria-pressed="${s === slot}">${fmt(s, { hour: '2-digit', minute: '2-digit', hourCycle: 'h23' })}</button>`).join('')}</div>
      ${known ? '' : `<div class="bk-fields">
        <input name="name" placeholder="Your name" autocomplete="name" aria-label="Your name" value="${esc(lead.name || '')}">
        <input name="phone" type="tel" inputmode="tel" placeholder="Mobile number" autocomplete="tel" aria-label="Mobile number" value="${esc(lead.phone || '')}">
        <input name="email" type="email" placeholder="Email address" autocomplete="email" aria-label="Email address" value="${esc(lead.email || '')}">
      </div>`}
      <button type="button" class="bk-btn" ${slot ? '' : 'disabled'}>Book My Call</button>
      <p class="bk-msg" role="alert"></p>
      <p class="bk-tz">Times shown in UK time · 15 minutes on Google Meet</p>`;
    booker.querySelectorAll('.bk-day').forEach((b) => b.addEventListener('click', () => { keep(); day = +b.dataset.i; slot = null; render(); }));
    booker.querySelectorAll('.bk-time').forEach((b) => b.addEventListener('click', () => { keep(); slot = b.dataset.slot; render(); }));
    booker.querySelector('.bk-btn').addEventListener('click', book);
  };
  // keep anything typed into the fields when the box re-renders
  const keep = () => booker.querySelectorAll('.bk-fields input').forEach((i) => { lead[i.name] = i.value; });

  const load = async () => {
    try {
      const r = await fetch('/api/slots', { cache: 'no-store' });
      const data = await r.json();
      if (!r.ok || !data.ok) throw new Error('slots');
      days = data.days || [];
      if (!days.length) {
        booker.innerHTML = '<p class="bk-empty"><b>No times free this week.</b><br>Keep an eye on your phone: Tim will be in touch to find a time that suits you.</p>';
        return;
      }
      day = Math.min(day, days.length - 1);
      render();
    } catch (_) { fallback(); }
  };

  const book = async () => {
    keep();
    const msg = booker.querySelector('.bk-msg');
    const who = { name: (lead.name || '').trim(), phone: (lead.phone || '').trim(), email: (lead.email || '').trim(), business: lead.business || '' };
    if (who.name.length < 2) { msg.textContent = 'Please enter your name.'; return; }
    if (who.phone.replace(/\D/g, '').length < 10) { msg.textContent = 'Please enter your mobile number.'; return; }
    if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(who.email)) { msg.textContent = 'Please check your email address.'; return; }
    const btn = booker.querySelector('.bk-btn');
    btn.disabled = true; btn.textContent = 'Booking…';
    try {
      const r = await fetch('/api/book', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ ...who, slot }) });
      const data = await r.json().catch(() => ({}));
      if (data.ok) {
        try { sessionStorage.setItem('vouch_lead', JSON.stringify({ ...getLead(), ...who })); } catch (_) {}
        try { if (window.fbq && localStorage.getItem('vouch_cookie_consent') === 'granted') window.fbq('track', 'Schedule'); } catch (_) {}
        booker.innerHTML = `<div class="bk-done"><span class="bk-tick"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M5 12.5l4.5 4.5L19 7.5"/></svg></span>
          <h3>Your call is booked</h3>
          <p>Scheduled for ${fmt(slot, { weekday: 'long', day: 'numeric', month: 'long' })} at ${fmt(slot, { hour: '2-digit', minute: '2-digit', hourCycle: 'h23' })}. We'll send a confirmation to ${esc(who.email)}.</p></div>`;
        return;
      }
      if (data.error === 'slot_taken') { slot = null; msg.textContent = ''; await load(); booker.querySelector('.bk-msg').textContent = 'Sorry, that time has just gone. Please pick another.'; return; }
      throw new Error(data.error || 'book');
    } catch (_) {
      btn.disabled = false; btn.textContent = 'Book My Call';
      msg.textContent = 'Something went wrong. Please try again, or call or text us and we\'ll book you in.';
    }
  };
  load();
}

// Pricing: monthly / annual toggle, applied to every plan card at once
const pks = [...document.querySelectorAll('.pk[data-base]')];
if (pks.length) {
  const cards = pks.map((pk) => ({
    pk, base: Number(pk.dataset.base), note: pk.dataset.note,
    opts: Object.fromEntries([...pk.querySelectorAll('template[data-bill-opt]')].map((t) => [t.dataset.billOpt, t.dataset])),
  }));
  const show = (id) => {
    document.querySelectorAll('[data-bill]').forEach((b) => b.setAttribute('aria-selected', b.dataset.bill === id));
    cards.forEach(({ pk, base, note, opts }) => {
      const o = opts[id];
      if (!o) return;
      pk.querySelector('.pk-num').textContent = '£' + o.per;
      pk.querySelector('.pk-was').hidden = Number(o.per) === base;
      pk.querySelector('.pk-billed').textContent = o.billed ? 'Billed ' + o.billed + '.' : 'Billed monthly.';
      // The pill is always shown (keeps the cards level): savings upfront, the card's own note monthly.
      const save = pk.querySelector('.pk-save');
      save.classList.toggle('is-note', !o.save);
      save.innerHTML = o.save ? 'You save <b></b>' : note;
      if (o.save) save.querySelector('b').textContent = o.save;
    });
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

  // The pixel base code is in every page's <head>, paused with fbq('consent','revoke').
  // Accept switches it on with Meta's own consent call, then records the page view.
  let granted = false;
  const loadPixel = () => {
    if (!window.fbq || granted) return;
    granted = true;
    window.fbq('consent', 'grant');
    window.fbq('track', 'PageView');
    // Page-specific standard event, e.g. Schedule on /booked (someone booked a call)
    const ev = document.querySelector('[data-pixel-event]')?.dataset.pixelEvent;
    if (ev && !framed) window.fbq('track', ev);
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
  const close = () => {
    if (!banner) return;
    const b = banner;
    banner = null;
    b.classList.add('is-leaving'); // quick slide down, then remove
    setTimeout(() => b.remove(), 320);
  };
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
      else if (before === 'granted') { if (window.fbq) window.fbq('consent', 'revoke'); clearMetaCookies(); location.reload(); } // stop a pixel that's already running
    }));
    document.body.appendChild(banner);
  };

  document.querySelectorAll('[data-cookie-settings]').forEach((b) => b.addEventListener('click', showBanner));
  const choice = get();
  if (choice === 'granted') loadPixel();
  else if (choice !== 'denied') {
    // On phones, wait for the first scroll or tap so visitors see the hero and ratings first
    const phone = window.matchMedia && window.matchMedia('(max-width: 600px)').matches;
    if (phone && window.scrollY < 40) {
      const onScroll = () => { if (window.scrollY >= 40) go(); };
      const go = () => {
        window.removeEventListener('scroll', onScroll);
        window.removeEventListener('pointerdown', go);
        showBanner();
      };
      window.addEventListener('scroll', onScroll, { passive: true });
      window.addEventListener('pointerdown', go);
    } else showBanner();
  }
}
