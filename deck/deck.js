// Motorul comun. ← → spațiu PgUp PgDn Home End, F = ecran complet,
// click pe jumătatea dreaptă = înainte, swipe pe telefon.
(() => {
  const stage = document.querySelector('.stage');
  const slides = [...stage.querySelectorAll('.slide')];
  const total = slides.length;
  let cur = 0;

  const fit = () => {
    const s = Math.min(innerWidth / 1600, innerHeight / 900);
    stage.style.setProperty('--s', s);
  };

  // Pregătiri o singură dată: lungimi de linii SVG, număr de caractere tastate.
  stage.querySelectorAll('.typed').forEach((el) => {
    el.style.setProperty('--n', Math.max(1, el.textContent.length));
  });
  stage.querySelectorAll('.draw').forEach((el) => {
    if (el.getTotalLength) el.style.setProperty('--len', Math.ceil(el.getTotalLength()));
  });
  // [data-stagger] dă decalaje copiilor: --d = start + i * pas.
  stage.querySelectorAll('[data-stagger]').forEach((box) => {
    const [start, step] = box.dataset.stagger.split(',').map(Number);
    [...box.children].forEach((c, i) => c.style.setProperty('--d', (start + i * step).toFixed(2) + 's'));
  });

  const go = (n) => {
    n = Math.max(0, Math.min(total - 1, n));
    slides.forEach((el, k) => {
      el.classList.toggle('is-on', k === n);
      el.classList.toggle('is-past', k < n);
      el.inert = k !== n;
    });
    cur = n;
    document.documentElement.style.setProperty('--progress', total > 1 ? n / (total - 1) : 1);
    document.dispatchEvent(new CustomEvent('slide', { detail: { index: n, total, el: slides[n] } }));
    history.replaceState(null, '', '#' + (n + 1));
  };

  addEventListener('keydown', (e) => {
    if (e.metaKey || e.ctrlKey || e.altKey) return;
    const k = e.key;
    if (['ArrowRight', 'ArrowDown', 'PageDown', ' ', 'Enter', 'l', 'j'].includes(k)) { e.preventDefault(); go(cur + 1); }
    else if (['ArrowLeft', 'ArrowUp', 'PageUp', 'Backspace', 'h', 'k'].includes(k)) { e.preventDefault(); go(cur - 1); }
    else if (k === 'Home') go(0);
    else if (k === 'End') go(total - 1);
    else if (k === 'f' || k === 'F') {
      if (document.fullscreenElement) document.exitFullscreen();
      else document.documentElement.requestFullscreen?.();
    }
  });

  addEventListener('click', (e) => {
    if (e.target.closest('a, button, input, [data-noclick]')) return;
    go(e.clientX > innerWidth / 3 ? cur + 1 : cur - 1);
  });

  let tx = null;
  addEventListener('touchstart', (e) => { tx = e.touches[0].clientX; }, { passive: true });
  addEventListener('touchend', (e) => {
    if (tx === null) return;
    const dx = e.changedTouches[0].clientX - tx;
    if (Math.abs(dx) > 40) go(dx < 0 ? cur + 1 : cur - 1);
    tx = null;
  });

  addEventListener('resize', fit);
  fit();
  const start = parseInt(location.hash.slice(1), 10);
  go(Number.isFinite(start) ? start - 1 : 0);

  const hint = document.createElement('div');
  hint.className = 'hint';
  hint.textContent = '← →  ·  F';
  document.body.append(hint);
  setTimeout(() => hint.classList.add('gone'), 3500);

  window.deck = { go, get index() { return cur; }, total };
})();
