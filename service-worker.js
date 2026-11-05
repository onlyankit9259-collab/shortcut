const CACHE_NAME = "shortcut-guru-v9";

const FILES_TO_CACHE = [
  "/shortcut/",
  "/shortcut/index.html",
  "/shortcut/manifest.json",
  "/shortcut/assets/site.css",
  "/shortcut/icons/icon-192.png",
  "/shortcut/icons/icon-512.png"
];

// New version takes over right away (no waiting for every tab to close),
// so phones that keep tabs open for days still get updates.
self.addEventListener("install", (event) => {
  self.skipWaiting();
  event.waitUntil(
    caches.open(CACHE_NAME).then((cache) => {
      return cache.addAll(FILES_TO_CACHE);
    })
  );
});

self.addEventListener("activate", (event) => {
  event.waitUntil(
    caches.keys().then((keys) => {
      return Promise.all(
        keys
          .filter((key) => key !== CACHE_NAME)
          .map((key) => caches.delete(key))
      );
    }).then(() => self.clients.claim())
  );
});

// Network first: always show the latest page when online,
// fall back to the cached copy when offline.
self.addEventListener("fetch", (event) => {
  if (event.request.method !== "GET") return;
  if (new URL(event.request.url).origin !== self.location.origin) return;

  event.respondWith(
    fetch(event.request)
      .then((response) => {
        if (response.ok) {
          const copy = response.clone();
          caches.open(CACHE_NAME).then((cache) => cache.put(event.request, copy));
        }
        return response;
      })
      .catch(() =>
        caches.match(event.request).then((cached) => cached || caches.match("/shortcut/"))
      )
  );
});
