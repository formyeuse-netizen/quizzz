// Service worker de Break the Quiz : rend le site installable comme une appli.
// Le jeu a besoin d'internet (WebSocket) : on garde juste la page d'accueil et
// les icones en cache pour un demarrage rapide, et une page "hors ligne".
const CACHE = "btq-v1";
const COQUILLE = ["/", "/manifest.webmanifest", "/pwa/icon-192.png", "/pwa/icon-512.png"];

self.addEventListener("install", e => {
  e.waitUntil(caches.open(CACHE).then(c => c.addAll(COQUILLE)).then(() => self.skipWaiting()));
});
self.addEventListener("activate", e => {
  e.waitUntil(caches.keys().then(ks => Promise.all(
    ks.filter(k => k !== CACHE).map(k => caches.delete(k)))).then(() => self.clients.claim()));
});
self.addEventListener("fetch", e => {
  const req = e.request;
  if (req.method !== "GET") return;
  const url = new URL(req.url);
  if (url.origin !== location.origin) return;          // images externes : navigateur normal
  // Reseau d'abord (toujours la derniere version), cache si hors ligne.
  e.respondWith(
    fetch(req).then(r => {
      if (r.ok && (url.pathname === "/" || url.pathname.startsWith("/pwa/"))) {
        const copie = r.clone();
        caches.open(CACHE).then(c => c.put(req, copie));
      }
      return r;
    }).catch(() => caches.match(req).then(r => r || caches.match("/")))
  );
});
