/* OATutor app-shell service worker.
   Caches the HTML/JS/CSS shell and icons. Lesson JSON and textbook figures
   stay on the network so the worker does not try to store the content library.
*/
const CACHE = "oatutor-shell-v2";

const SHELL = [
  "/",
  "/index.html",
  "/manifest.json",
  "/favicon.png",
  "/icons/icon-180.png",
  "/icons/icon-192.png",
  "/icons/icon-512.png",
  "/icons/icon-512-maskable.png",
];

function isLibraryPath(pathname) {
  return (
    pathname.startsWith("/static/images/figures/") ||
    pathname.startsWith("/static/content/")
  );
}

function isShellAsset(pathname) {
  return (
    pathname.startsWith("/static/js/") ||
    pathname.startsWith("/static/css/") ||
    pathname.startsWith("/static/media/") ||
    pathname.startsWith("/icons/") ||
    pathname === "/manifest.json" ||
    pathname === "/favicon.png" ||
    pathname === "/asset-manifest.json"
  );
}

async function precacheShell(cache) {
  const urls = new Set(SHELL);
  try {
    const response = await fetch("/asset-manifest.json", { cache: "no-store" });
    if (response.ok) {
      const manifest = await response.json();
      const files = manifest && manifest.files ? Object.values(manifest.files) : [];
      files.forEach((file) => {
        if (typeof file !== "string" || isLibraryPath(file)) return;
        if (/\.(js|css|png|svg|webp|gif|ico|woff2?)$/i.test(file)) urls.add(file);
      });
    }
  } catch (err) {
    // The shell list above is enough for installability if the manifest is missing.
  }

  await Promise.all(
    [...urls].map(async (url) => {
      try {
        const response = await fetch(url, { cache: "no-store" });
        if (response && response.ok) {
          await cache.put(url === "/" ? "/index.html" : url, response);
        }
      } catch (err) {
        // Skip a missing optional asset rather than failing installation.
      }
    })
  );
}

self.addEventListener("install", (event) => {
  event.waitUntil(
    caches
      .open(CACHE)
      .then((cache) => precacheShell(cache))
      .then(() => self.skipWaiting())
  );
});

self.addEventListener("activate", (event) => {
  event.waitUntil(
    caches
      .keys()
      .then((keys) =>
        Promise.all(keys.filter((key) => key !== CACHE).map((key) => caches.delete(key)))
      )
      .then(() => self.clients.claim())
  );
});

self.addEventListener("fetch", (event) => {
  const request = event.request;
  if (request.method !== "GET") return;

  const url = new URL(request.url);
  if (url.origin !== self.location.origin) return;

  if (isLibraryPath(url.pathname)) {
    event.respondWith(fetch(request));
    return;
  }

  if (request.mode === "navigate" || url.pathname === "/" || url.pathname.endsWith(".html")) {
    event.respondWith(
      fetch(request)
        .then((response) => {
          const copy = response.clone();
          caches.open(CACHE).then((cache) => cache.put("/index.html", copy));
          return response;
        })
        .catch(() => caches.match("/index.html"))
    );
    return;
  }

  if (isShellAsset(url.pathname)) {
    event.respondWith(
      caches.match(request).then((cached) => {
        const network = fetch(request)
          .then((response) => {
            if (response && response.ok) {
              const copy = response.clone();
              caches.open(CACHE).then((cache) => cache.put(request, copy));
            }
            return response;
          })
          .catch(() => cached);
        return cached || network;
      })
    );
  }
});
