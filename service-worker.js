const CACHE='kitaca-shell-v1';
const FILES=['./','./index.html','./manifest.json','./pdfs/icono-192.png','./pdfs/icono-512.png'];
self.addEventListener('install',e=>e.waitUntil(caches.open(CACHE).then(c=>c.addAll(FILES))));
self.addEventListener('activate',e=>e.waitUntil(self.clients.claim()));
self.addEventListener('fetch',e=>{const u=new URL(e.request.url);if(u.origin===self.location.origin&&e.request.method==='GET')e.respondWith(caches.match(e.request).then(r=>r||fetch(e.request)));});