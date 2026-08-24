/* Page-side half of the offline queue: banner state + replay triggers.
   The service worker owns storage; this file only (a) tells the driver what
   is happening, (b) asks the SW to replay when connectivity returns, and
   (c) registers Background Sync where supported. */

(function () {
  'use strict';

  if (!('serviceWorker' in navigator)) return;

  const BANNER_ID = 'offline-banner';

  function ensureBanner() {
    let el = document.getElementById(BANNER_ID);
    if (el) return el;
    el = document.createElement('div');
    el.id = BANNER_ID;
    el.style.cssText =
      'display:none;padding:.6rem 1rem;border-radius:6px;margin:.5rem 0;font-size:.95rem';
    const card = document.querySelector('.card');
    if (card) card.prepend(el);
    return el;
  }

  function setBanner(text, background, color) {
    const el = ensureBanner();
    el.textContent = text;
    el.style.background = background;
    el.style.color = color;
    el.style.display = 'block';
  }

  function hideBanner() {
    const el = document.getElementById(BANNER_ID);
    if (el) el.style.display = 'none';
  }

  function askReplay() {
    if (!navigator.onLine) return Promise.resolve(0);
    return new Promise((resolve) => {
      const channel = new MessageChannel();
      channel.port1.onmessage = (event) => resolve(event.data || 0);
      navigator.serviceWorker.controller
        ? navigator.serviceWorker.controller.postMessage({ type: 'pumprun-replay' }, [channel.port2])
        : resolve(0);
    });
  }

  function updateStatus() {
    if (!navigator.onLine) {
      setBanner('Offline — completed stops will queue and send themselves.', '#fff3cd', '#7a5b00');
    } else {
      hideBanner();
      askReplay().then((left) => {
        if (left > 0) setBanner(left + ' stop(s) still queued — will retry automatically.', '#e6f4ea', '#14663b');
      });
    }
  }

  navigator.serviceWorker
    .register('/sw.js')
    .then((registration) => {
      if ('sync' in registration) {
        // Fire-and-forget: browsers without Background Sync simply skip this.
        registration.sync.register('pumprun-replay').catch(() => {});
      }
    })
    .catch(() => {});

  window.addEventListener('online', () => {
    askReplay().then(() => window.location.reload());
  });
  window.addEventListener('offline', updateStatus);
  updateStatus();
})();
