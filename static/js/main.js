/* ===================================================================
   C&C — main.js
   Navegación · contadores · reveal · formulario
=================================================================== */

(() => {
  'use strict';

  // -----------------------------------------------------------------
  // 1.  NAV — sombra al hacer scroll + menú móvil
  // -----------------------------------------------------------------
  const nav     = document.getElementById('nav');
  const burger  = document.getElementById('nav-burger');
  const links   = document.querySelector('.nav__links');

  const onScroll = () => {
    if (window.scrollY > 20) nav.classList.add('is-scrolled');
    else                     nav.classList.remove('is-scrolled');
  };
  onScroll();
  window.addEventListener('scroll', onScroll, { passive: true });

  burger?.addEventListener('click', () => {
    burger.classList.toggle('is-open');
    links.classList.toggle('is-open');
  });

  // cerrar el menú móvil al hacer clic en un enlace
  links?.querySelectorAll('a').forEach(a => {
    a.addEventListener('click', () => {
      burger.classList.remove('is-open');
      links.classList.remove('is-open');
    });
  });

  // -----------------------------------------------------------------
  // 2.  CONTADORES (odómetro) — animan al entrar al viewport
  // -----------------------------------------------------------------
  const counters = document.querySelectorAll('[data-count]');
  const countObserver = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (!entry.isIntersecting) return;
      const el = entry.target;
      const target = parseInt(el.dataset.count, 10);
      const suffix = el.dataset.suffix || '';
      const duration = 1400;
      const start = performance.now();

      const tick = (now) => {
        const t = Math.min((now - start) / duration, 1);
        // ease-out cuadrática
        const eased = 1 - Math.pow(1 - t, 3);
        el.textContent = Math.round(target * eased) + suffix;
        if (t < 1) requestAnimationFrame(tick);
      };
      requestAnimationFrame(tick);
      countObserver.unobserve(el);
    });
  }, { threshold: 0.5 });
  counters.forEach(c => countObserver.observe(c));

  // -----------------------------------------------------------------
  // 3.  REVEAL ON SCROLL — añade clases a las secciones
  // -----------------------------------------------------------------
  // marcar elementos
  const toReveal = [
    '.about__head',
    '.about__body',
    '.about__badge',
    '.section-head',
    '.vehicle',
    '.pillar',
    '.adv',
    '.sector',
    '.cat-group',
    '.contact__copy',
    '.contact__form',
    '.cert',
  ];
  toReveal.forEach(sel => {
    document.querySelectorAll(sel).forEach(el => el.classList.add('reveal'));
  });

  // grupos con stagger
  ['.cat-group__cards', '.sectors__grid', '.advantages__grid', '.policies__grid', '.fleet__list', '.about__quickstats'].forEach(sel => {
    document.querySelectorAll(sel).forEach(el => el.classList.add('reveal-stagger'));
  });

  const revealObserver = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.classList.add('is-visible');
        revealObserver.unobserve(entry.target);
      }
    });
  }, { threshold: 0.12, rootMargin: '0px 0px -80px 0px' });

  document.querySelectorAll('.reveal, .reveal-stagger')
    .forEach(el => revealObserver.observe(el));

  // -----------------------------------------------------------------
  // 4.  FORMULARIO DE COTIZACIÓN
  // -----------------------------------------------------------------
  const form   = document.getElementById('form-cotizar');
  const status = document.getElementById('form-status');

  form?.addEventListener('submit', async (e) => {
    e.preventDefault();
    const btn = form.querySelector('button[type="submit"]');
    const original = btn.innerHTML;

    btn.disabled = true;
    btn.innerHTML = 'Enviando…';
    status.className = 'form__status';
    status.textContent = '';

    const data = Object.fromEntries(new FormData(form).entries());

    try {
      const res = await fetch('/api/cotizar', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data),
      });
      const json = await res.json();

      if (json.ok) {
        status.classList.add('is-ok');
        status.textContent = `✓ ${json.mensaje} (Rad. ${json.radicado})`;
        form.reset();
      } else {
        status.classList.add('is-error');
        status.textContent = `× ${json.error || 'No se pudo enviar.'}`;
      }
    } catch (err) {
      status.classList.add('is-error');
      status.textContent = '× Error de conexión. Intente nuevamente.';
    } finally {
      btn.disabled = false;
      btn.innerHTML = original;
    }
  });

  // -----------------------------------------------------------------
  // 5.  PARALLAX MUY SUTIL EN EL CAMIÓN DEL HERO
  // -----------------------------------------------------------------
  const truck = document.querySelector('.hero__truck');
  if (truck && window.matchMedia('(prefers-reduced-motion: no-preference)').matches) {
    let raf = null;
    window.addEventListener('scroll', () => {
      if (raf) return;
      raf = requestAnimationFrame(() => {
        const y = Math.min(window.scrollY, 600);
        truck.style.transform = `translateY(${y * 0.08}px)`;
        raf = null;
      });
    }, { passive: true });
  }

})();
