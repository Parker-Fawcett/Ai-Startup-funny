/* PumpRun service worker: offline complete-form queue + replay.
   Strategy:
   - POST /jobs/<id>/complete/ while online: pass through.
   - Same POST while offline: store the full FormData (photo included) in
     IndexedDB, answer the page with a "queued" screen so the driver keeps
     moving; replay fires on window 'online' (offline.js) and via Background
     Sync when the browser supports it.
   - GET */complete/* pages: network-first with cache fallback so drivers can
     re-open a stop they already loaded.
   Replay sends X-CSRFToken from the live csrftoken cookie, so rotated tokens
   never break queued submissions. */

const CACHE = 'pumprun-v1';
const DB = 'pumprun-queue';
const STORE = 'submissions';

self.addEventListener('install', () => self.skipWaiting());
self.addEventListener('activate', (event) => event.waitUntil(self.clients.claim()));

self.addEventListener('fetch', (event) => {
  const req = event.request;
  if (req.method !== 'GET' && req.method !== 'POST') return;
  const url = new URL(req.url);
  if (url.origin !== self.location.origin) return;

  if (req.method === 'POST' && /\/jobs\/\d+\/complete\/$/.test(url.pathname)) {
    event.respondWith(passThroughOrQueue(req));
    return;
  }
  if (req.method === 'GET' && url.pathname.includes('/complete/')) {
    event.respondWith(networkFirst(req));
  }
});

self.addEventListener('sync', (event) => {
  if (event.tag === 'pumprun-replay') {
    event.waitUntil(replayAll());
  }
});

async function passThroughOrQueue(req) {
  try {
    return await fetch(req);
  } catch (offline) {
    await enqueue(req);
    return new Response(
      queuedPage(),
      { status: 200, headers: { 'Content-Type': 'text/html; charset=utf-8' } },
    );
  }
}

async function networkFirst(req) {
  try {
    const fresh = await fetch(req);
    if (fresh.ok) {
      const cache = await caches.open(CACHE);
      cache.put(req, fresh.clone());
    }
    return fresh;
  } catch (offline) {
    const cached = await caches.match(req);
    return cached || caches.match('/');
  }
}

function openDb() {
  return new Promise((resolve, reject) => {
    const open = indexedDB.open(DB, 1);
    open.onupgradeneeded = () => open.result.createObjectStore(STORE, { keyPath: 'id', autoIncrement: true });
    open.onsuccess = () => resolve(open.result);
    open.onerror = () => reject(open.error);
  });
}

async function enqueue(req) {
  const form = await req.clone().formData();
  const entry = { url: req.url, fields: {}, file: null };
  for (const [key, value] of form.entries()) {
    if (typeof value === 'string') entry.fields[key] = value;
    else if (value instanceof File && value.size > 0) {
      entry.file = { key, name: value.name, type: value.type, blob: value };
    }
  }
  const db = await openDb();
  await new Promise((resolve, reject) => {
    const tx = db.transaction(STORE, 'readwrite');
    tx.objectStore(STORE).add(entry);
    tx.oncomplete = resolve;
    tx.onerror = () => reject(tx.error);
  });
}

async function replayAll() {
  const db = await openDb();
  const entries = await new Promise((resolve, reject) => {
    const tx = db.transaction(STORE, 'readonly');
    const all = tx.objectStore(STORE).getAll();
    all.onsuccess = () => resolve(all.result || []);
    all.onerror = () => reject(all.error);
  });
  const keep = [];
  for (const entry of entries) {
    try {
      const ok = await replayOne(entry);
      if (!ok) keep.push(entry);
    } catch (stillOffline) {
      keep.push(entry);
    }
  }
  await new Promise((resolve, reject) => {
    const tx = db.transaction(STORE, 'readwrite');
    const store = tx.objectStore(STORE);
    store.clear();
    for (const entry of keep) store.add(entry);
    tx.oncomplete = resolve;
    tx.onerror = () => reject(tx.error);
  });
}

async function replayOne(entry) {
  const form = new FormData();
  for (const [key, value] of Object.entries(entry.fields)) form.append(key, value);
  if (entry.file) form.append(entry.file.key, entry.file.blob, entry.file.name);
  const response = await fetch(entry.url, {
    method: 'POST',
    body: form,
    credentials: 'same-origin',
  });
  return response.ok || response.status === 302;
}

self.addEventListener('message', (event) => {
  if (!event.data || event.data.type !== 'pumprun-replay') return;
  event.waitUntil(
    replayAll().then(async () => {
      const db = await openDb();
      const remaining = await new Promise((resolve, reject) => {
        const tx = db.transaction(STORE, 'readonly');
        const count = tx.objectStore(STORE).count();
        count.onsuccess = () => resolve(count.result);
        count.onerror = () => reject(count.error);
      });
      if (event.ports[0]) event.ports[0].postMessage(remaining);
    }),
  );
});
function queuedPage() {
  return `<!doctype html><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Queued — PumpRun</title>
<body style="font-family:-apple-system,system-ui,sans-serif;max-width:30rem;margin:10% auto;padding:1rem;background:#f5f5f0;color:#1a1a1a;text-align:center">
  <div style="background:#fff;border-radius:8px;padding:2rem 1.25rem;box-shadow:0 1px 3px rgba(0,0,0,.12)">
    <h1 style="font-size:1.3rem">No signal — stop saved on your phone</h1>
    <p>It will send itself automatically the moment you have bars again.</p>
    <a href="/" style="color:#14663b">Back to route</a>
  </div>
</body>`;
}
