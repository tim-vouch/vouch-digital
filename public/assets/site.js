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
  const hi = document.querySelector('[data-first]');
  if (hi && first) hi.textContent = 'Nice one, ' + first + '.';
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

// Reviews carousel: one dot per review; the review nearest the middle is active
document.querySelectorAll('.rev-carousel').forEach((c) => {
  const dots = c.parentElement.querySelector('.rev-dots');
  const cards = [...c.children];
  if (!dots || cards.length < 2) { if (dots) dots.hidden = true; return; }
  dots.innerHTML = cards.map((_, i) => `<button type="button" aria-label="Show review ${i + 1}"></button>`).join('');
  const btns = [...dots.children];
  const centre = (el) => el.offsetLeft + el.offsetWidth / 2;
  const go = (i) => c.scrollTo({ left: centre(cards[i]) - c.clientWidth / 2, behavior: 'smooth' });
  const update = () => {
    const mid = c.scrollLeft + c.clientWidth / 2;
    let best = 0;
    cards.forEach((el, i) => { if (Math.abs(centre(el) - mid) < Math.abs(centre(cards[best]) - mid)) best = i; });
    cards.forEach((el, i) => el.classList.toggle('is-active', i === best));
    btns.forEach((b, i) => b.setAttribute('aria-current', String(i === best)));
  };
  btns.forEach((b, i) => b.addEventListener('click', () => go(i)));
  cards.forEach((el, i) => el.addEventListener('click', () => go(i)));
  c.addEventListener('scroll', update, { passive: true });
  window.addEventListener('resize', update);
  update();
});
