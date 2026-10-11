/* Landing page: the hero animation plays on its own only when the visitor has not asked for less motion.
 * With reduced motion (or when playback is blocked) the page shows a still frame and a "Play" button. */
(function () {
  const v = document.getElementById('hero-video');
  const btn = document.getElementById('hero-toggle');
  if (!v) return;
  const reduce = window.matchMedia && matchMedia('(prefers-reduced-motion: reduce)').matches;

  function label() { btn.textContent = v.paused ? 'Play the animation' : 'Pause the animation'; }
  function show() { btn.hidden = false; label(); }

  if (btn) {
    btn.addEventListener('click', () => { if (v.paused) v.play().catch(() => {}); else v.pause(); label(); });
    v.addEventListener('play', label);
    v.addEventListener('pause', label);
  }

  if (reduce) { v.pause(); if (btn) show(); return; }

  /* Autoplay only while the video is on screen, so it does not use data or battery below the fold. */
  const start = () => {
    const p = v.play();
    if (p && p.catch) p.catch(() => { if (btn) show(); });
    else if (btn) show();
  };
  if ('IntersectionObserver' in window) {
    new IntersectionObserver((entries) => {
      entries.forEach((e) => { if (e.isIntersecting) start(); else v.pause(); });
    }, { threshold: 0.25 }).observe(v);
  } else {
    start();
  }
  if (btn) show();
})();
