// Lets phones install KCGM Docs as an app. It saves nothing offline; every request goes to the network as normal.
self.addEventListener('install', () => self.skipWaiting());
self.addEventListener('activate', e => e.waitUntil(self.clients.claim()));
self.addEventListener('fetch', () => {});
