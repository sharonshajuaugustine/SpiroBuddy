/* SpiroBuddy service worker – makes the patient app installable and lets it open with no internet.
 *  - API calls (/api/...) are never cached: live data only.
 *  - Pages, scripts and styles: network first, cached copy only when offline (so nothing goes stale).
 *  - Voice clips (/audio/...): cache first – they never change and are the offline voice. */
const CACHE = 'spirobuddy-v1';
const SHELL = ['app.html', 'css/styles.css', 'js/icons.js', 'js/api.js', 'js/breath.js', 'js/sources.js', 'js/voice.js',
  'manifest.webmanifest', 'icons/icon-192.png', 'audio/cues.json'];

self.addEventListener('install', (e) => {
  e.waitUntil(caches.open(CACHE).then((c) => c.addAll(SHELL)).catch(() => {}).then(() => self.skipWaiting()));
});
self.addEventListener('activate', (e) => {
  e.waitUntil(caches.keys().then((keys) => Promise.all(keys.filter((k) => k !== CACHE).map((k) => caches.delete(k)))).then(() => self.clients.claim()));
});
self.addEventListener('fetch', (e) => {
  const req = e.request, url = new URL(req.url);
  if (req.method !== 'GET' || url.origin !== location.origin || url.pathname.startsWith('/api/') || req.headers.has('range')) return;
  const put = (res) => { if (res && res.ok) { const copy = res.clone(); caches.open(CACHE).then((c) => c.put(req, copy)); } return res; };
  if (url.pathname.startsWith('/audio/')) {
    e.respondWith(caches.match(req).then((hit) => hit || fetch(req).then(put)));
    return;
  }
  if (url.pathname.startsWith('/showcase/videos/')) return;      // large files: straight from the network
  e.respondWith(fetch(req).then(put).catch(() => caches.match(req, { ignoreSearch: true })));
});
