// Mobile menu
const menuBtn = document.querySelector('.menu-btn');
const nav = document.getElementById('nav');
if (menuBtn && nav) {
  menuBtn.addEventListener('click', () => {
    const open = nav.classList.toggle('open');
    menuBtn.setAttribute('aria-expanded', open);
  });
}

// "Why it matters" trade toggle
const SWAPS = {
  electrician: { query: 'electrician near me', you: 'Your Electrical Co.', them: 'Other Electrical Ltd' },
  plumber: { query: 'plumber near me', you: 'Your Plumbing Co.', them: 'Other Plumbing Ltd' },
};
document.querySelectorAll('[data-trade]').forEach((btn) => {
  btn.addEventListener('click', () => {
    document.querySelectorAll('[data-trade]').forEach((b) => b.setAttribute('aria-pressed', b === btn));
    const s = SWAPS[btn.dataset.trade];
    document.querySelectorAll('[data-swap]').forEach((el) => { el.textContent = s[el.dataset.swap]; });
    document.querySelectorAll('[data-for]').forEach((el) => { el.hidden = el.dataset.for !== btn.dataset.trade; });
  });
});

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
        name: data.get('name'), email: data.get('email'), phone: data.get('phone'),
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
  if (lead.email) params.set('email', lead.email);
  if (lead.phone) {
    // UK mobiles: 07700 900123 -> +447700900123 so GHL matches the same contact
    const digits = String(lead.phone).replace(/[^\d+]/g, '');
    params.set('phone', /^0\d{10}$/.test(digits) ? '+44' + digits.slice(1) : digits);
  }
  const qs = params.toString();
  booking.src = booking.dataset.src + (qs ? '?' + qs : '');
  const hi = document.querySelector('[data-first]');
  if (hi && first) hi.textContent = 'Nice one, ' + first + '.';
}
