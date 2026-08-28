(function (root, factory) {
  "use strict";
  var api = factory();
  if (typeof module === "object" && module.exports) module.exports = api;
  if (root) root.StegVerseMyKVDirectory = api;
}(typeof globalThis !== "undefined" ? globalThis : this, function () {
  "use strict";

  var DOMAINS = [
    { id: "pictures", label: "Pictures & Media", icon: "▣", path: "04_Media/Pictures", description: "Photos, image continuity, and related media records." },
    { id: "music", label: "Music", icon: "♫", path: "04_Media/Music", description: "Playlists, listening continuity, song moments, and music records." },
    { id: "email", label: "Email", icon: "✉", path: "03_Records/Email", description: "Governed email continuity records admitted into your KV." },
    { id: "finance", label: "Finance", icon: "$", path: "03_Records/Finance", description: "Accounts, spending, savings, retirement, tax analysis, rewards, and collateral." },
    { id: "assets", label: "Assets", icon: "◆", path: "03_Records/Assets", description: "Property, investments, cash-equivalents, valuables, and other owned resources." },
    { id: "liabilities", label: "Liabilities", icon: "−", path: "03_Records/Liabilities", description: "Loans, credit obligations, mortgages, and other amounts owed." },
    { id: "personal", label: "Personal Information", icon: "◉", path: "_Entities/Self", description: "Your self-profile and personal continuity records." },
    { id: "records", label: "Records", icon: "▤", path: "03_Records", description: "Private records and structured continuity documents." },
    { id: "projects", label: "Projects", icon: "◇", path: "05_Projects", description: "Project continuity, event records, and working context." },
    { id: "research", label: "Research", icon: "⌕", path: "02_Research", description: "Research notes, references, and inquiry continuity." },
    { id: "archive", label: "Archive", icon: "□", path: "06_Archive", description: "Archived continuity material retained under your KV policy." }
  ];

  function clone(value) {
    return JSON.parse(JSON.stringify(value));
  }

  function getDomain(id) {
    var normalized = String(id || "").trim().toLowerCase();
    var match = DOMAINS.find(function (entry) { return entry.id === normalized; });
    if (!match) throw new Error("Unknown KnowledgeVault directory");
    return clone(match);
  }

  function listDomains() {
    return clone(DOMAINS);
  }

  function directoryHref(id) {
    return "my-kv-directory.html?dir=" + encodeURIComponent(getDomain(id).id);
  }

  function assertSafeListing(value, path) {
    path = path || "listing";
    if (Array.isArray(value)) {
      value.forEach(function (item, index) { assertSafeListing(item, path + "[" + index + "]"); });
      return;
    }
    if (!value || typeof value !== "object") return;
    Object.keys(value).forEach(function (key) {
      var lower = key.toLowerCase();
      if (["password","secret","token","private_key","cvv","card_number","account_number","routing_number"].some(function (part) {
        return lower.indexOf(part) !== -1;
      })) throw new Error("Secret-bearing directory metadata prohibited at " + path + "." + key);
      assertSafeListing(value[key], path + "." + key);
    });
  }

  function loadDirectory(domainId, bridge) {
    var domain = getDomain(domainId);
    if (!bridge || typeof bridge.listDirectory !== "function") {
      return Promise.resolve({
        state: "BRIDGE_UNAVAILABLE",
        domain: domain,
        entries: [],
        message: "Connected KnowledgeVault directory bridge unavailable. No private files were listed."
      });
    }
    return Promise.resolve(bridge.listDirectory({
      schema: "stegverse.site.my-kv.directory-list-request/v1",
      directory_id: domain.id,
      canonical_path: domain.path,
      access: "READ_ONLY",
      authority_effect: "NONE"
    })).then(function (result) {
      if (!result || result.canonical_path !== domain.path || !Array.isArray(result.entries)) {
        throw new Error("FAIL_CLOSED: canonical directory listing was not confirmed");
      }
      assertSafeListing(result);
      return {
        state: "KV_LISTED",
        domain: domain,
        entries: clone(result.entries),
        message: "Directory loaded from your KnowledgeVault."
      };
    });
  }

  function openEntry(domainId, entry, bridge) {
    var domain = getDomain(domainId);
    if (!entry || typeof entry !== "object") return Promise.reject(new Error("Directory entry required"));
    if (!bridge || typeof bridge.openEntry !== "function") {
      return Promise.reject(new Error("FAIL_CLOSED: canonical KV file-open bridge unavailable"));
    }
    assertSafeListing(entry, "entry");
    return Promise.resolve(bridge.openEntry({
      schema: "stegverse.site.my-kv.open-entry-request/v1",
      directory_id: domain.id,
      canonical_path: domain.path,
      entry: clone(entry),
      access: "READ_ONLY",
      authority_effect: "NONE"
    }));
  }

  return {
    listDomains: listDomains,
    getDomain: getDomain,
    directoryHref: directoryHref,
    loadDirectory: loadDirectory,
    openEntry: openEntry,
    assertSafeListing: assertSafeListing
  };
}));