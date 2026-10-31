const CACHE='kitaca-shell-v7';
const FILES=['./','./index.html','./manifest.json','./logo_kitACA.png','./kitaca-icon-192.png','./kitaca-icon-512.png'];
self.addEventListener('install', event => { event.waitUntil(caches.open(CACHE).then(cache => cache.addAll(FILES))); self.skipWaiting(); });
self.addEventListener('activate', event => { event.waitUntil((async () => { const keys=await caches.keys(); await Promise.all(keys.filter(key=>key.startsWith('kitaca-shell-')&&key!==CACHE).map(key=>caches.delete(key))); await self.clients.claim(); })()); });
self.addEventListener('fetch', event => { const url=new URL(event.request.url); if(url.origin===self.location.origin&&event.request.method==='GET') event.respondWith(caches.match(event.request).then(response=>response||fetch(event.request))); });
