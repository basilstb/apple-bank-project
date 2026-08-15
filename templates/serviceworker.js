const CACHE_NAME = 'nexus-bank-cache-v1';
const urlsToCache = [
    '/',
    '/login/',
    '/static/images/nexus_app_icon.png',
    '/static/images/nexus_logo.png'
];

// Install Service Worker
self.addEventListener('install', event => {
    event.waitUntil(
        caches.open(CACHE_NAME)
            .then(cache => {
                // We use cache.addAll but catch errors so that if any URL fails to load,
                // it doesn't break the service worker installation.
                return cache.addAll(urlsToCache).catch(err => console.warn('PWA: Cache addAll failed:', err));
            })
    );
});

// Cache and return requests (Network-first fallback to cache)
self.addEventListener('fetch', event => {
    // Only handle GET requests
    if (event.request.method !== 'GET') return;

    event.respondWith(
        fetch(event.request)
            .then(response => {
                // If valid response, clone and cache it (optional, but let's just return it)
                return response;
            })
            .catch(() => {
                // If network fails, try to serve from cache
                return caches.match(event.request);
            })
    );
});

// Update a service worker
self.addEventListener('activate', event => {
    const cacheWhitelist = [CACHE_NAME];
    event.waitUntil(
        caches.keys().then(cacheNames => {
            return Promise.all(
                cacheNames.map(cacheName => {
                    if (cacheWhitelist.indexOf(cacheName) === -1) {
                        return caches.delete(cacheName);
                    }
                })
            );
        })
    );
});
