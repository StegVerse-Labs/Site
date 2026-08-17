"use strict";

var CACHE_NAME = "stegos-web-bootstrap-v1";
var SHELL = [
  "./",
  "./index.html",
  "./stegos-bootstrap.js",
  "./manifest.webmanifest"
];

self.addEventListener("install", function (event) {
  event.waitUntil(caches.open(CACHE_NAME).then(function (cache) {
    return cache.addAll(SHELL);
  }));
});

self.addEventListener("activate", function (event) {
  event.waitUntil(caches.keys().then(function (keys) {
    return Promise.all(keys.filter(function (key) {
      return key !== CACHE_NAME;
    }).map(function (key) {
      return caches.delete(key);
    }));
  }));
});

self.addEventListener("fetch", function (event) {
  if (event.request.method !== "GET") {
    return;
  }
  event.respondWith(caches.match(event.request).then(function (cached) {
    if (cached) {
      return cached;
    }
    return fetch(event.request).then(function (response) {
      if (!response || response.status !== 200 || response.type === "opaque") {
        return response;
      }
      var copy = response.clone();
      caches.open(CACHE_NAME).then(function (cache) {
        cache.put(event.request, copy);
      });
      return response;
    });
  }));
});
