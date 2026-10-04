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
  electrician: { query: 'emergency electrician near me', you: 'Your Electrical Co.', them: 'Other Electrical Ltd' },
  plumber: { query: 'emergency plumber near me', you: 'Your Plumbing Co.', them: 'Other Plumbing Ltd' },
};
document.querySelectorAll('[data-trade]').forEach((btn) => {
  btn.addEventListener('click', () => {
    document.querySelectorAll('[data-trade]').forEach((b) => b.setAttribute('aria-pressed', b === btn));
    const s = SWAPS[btn.dataset.trade];
    document.querySelectorAll('[data-swap]').forEach((el) => { el.textContent = s[el.dataset.swap]; });
  });
});

// Enquiry forms: submit without leaving the page
const started = Date.now();
document.querySelectorAll('form.enquiry').forEach((form) => {
  const msg = form.querySelector('.form-msg');
  const show = (cls, text) => { msg.className = 'form-msg ' + cls; msg.textContent = text; };
  form.addEventListener('submit', async (e) => {
    e.preventDefault();
    const missing = [...form.querySelectorAll('[required]')].find((el) => !el.value.trim());
    if (missing) { show('err', 'Please fill in ' + missing.getAttribute('aria-label').toLowerCase() + '.'); missing.focus(); return; }
    form.querySelector('[name=t]').value = String(Date.now() - started);
    const btn = form.querySelector('button[type=submit]');
    btn.disabled = true;
    try {
      const res = await fetch(form.action, { method: 'POST', body: new FormData(form) });
      if (!res.ok) throw new Error(res.status);
      form.reset();
      show('ok', "Thanks, we've got your details. We'll be in touch shortly to book your free audit.");
    } catch {
      show('err', 'Something went wrong sending that. Please call 07984 003845 or email info@vouchdigital.co.uk.');
    } finally {
      btn.disabled = false;
    }
  });
});
