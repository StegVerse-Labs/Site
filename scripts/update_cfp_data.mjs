// scripts/update_cfp_data.mjs
//
// StegVerse CFP Data Updater
// --------------------------
// - Fetches latest CFP-style rankings from an external API
// - Normalizes into our data model
// - Writes:
//     data/cfp-2025.json   (raw rankings snapshot)
//     data/cfp-data.json   (Top 12 + bracket-friendly summary)
//     data/cfp-teams.json  (team metadata used by team pages)
//
// IMPORTANT:
//   1. Set CFP_API_URL in the workflow or repo secrets.
//   2. CFP_API_URL should return JSON shaped like:
//
//      [
//        {
//          "rank": 1,
//          "team": "Texas Tech",
//          "id": "ttu",
//          "record": "12-0",
//          "conf": "Big 12",
//          "lastRank": 2,
//          "projRank": 1,
//          "logo": "https://...",
//          "primaryColor": "#CC0000"
//        },
//        ...
//      ]
//
//   If your upstream shape differs, just adjust `normalizeTeam()` below.

import fs from "fs";
import path from "path";
import { fileURLToPath } from "url";

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

// ---------- Config ----------
const CFP_API_URL =
  process.env.CFP_API_URL || "https://example.com/stegrank/cfp-2025.json";

// Output files (relative to repo root)
const DATA_DIR = path.join(__dirname, "..", "data");
const FILE_CFP_2025 = path.join(DATA_DIR, "cfp-2025.json");
const FILE_CFP_DATA = path.join(DATA_DIR, "cfp-data.json");
const FILE_CFP_TEAMS = path.join(DATA_DIR, "cfp-teams.json");

// ---------- Helpers ----------
function log(...args) {
  // Keep logs short for Actions view
  console.log("[cfp-update]", ...args);
}

async function fetchJson(url) {
  log("Fetching:", url);
  const resp = await fetch(url, { method: "GET" });
  if (!resp.ok) {
    throw new Error(`HTTP ${resp.status} from ${url}`);
  }
  return await resp.json();
}

// Normalize a single team object from upstream into our house shape
function normalizeTeam(raw) {
  return {
    id: String(raw.id ?? raw.team).toLowerCase().replace(/\s+/g, "-"),
    rank: Number(raw.rank),
    team: String(raw.team),
    record: String(raw.record ?? ""),
    conf: String(raw.conf ?? ""),
    lastRank: raw.lastRank != null ? Number(raw.lastRank) : null,
    projRank: raw.projRank != null ? Number(raw.projRank) : null,
    logo: raw.logo ?? "",
    primaryColor: raw.primaryColor ?? "#111827",
  };
}

// ---------- Writers ----------
function writeJson(filePath, data) {
  const pretty = JSON.stringify(data, null, 2);
  fs.writeFileSync(filePath, pretty + "\n", "utf8");
  log("Wrote", path.relative(process.cwd(), filePath));
}

// Build `cfp-data.json` (Top 12 + bracket info)
function buildCfpData(normalized) {
  const sorted = [...normalized].sort((a, b) => a.rank - b.rank);
  const top12 = sorted.filter((t) => t.rank >= 1 && t.rank <= 12);

  return {
    generatedAt: new Date().toISOString(),
    release: {
      // You can override these with real release metadata later
      label: "Most recent CFP release",
      season: 2025,
      week: null,
    },
    top12,
    // basic bracket seeds for now; front-end can derive bracket from rank
    bracketSeeds: top12.map((t) => ({
      seed: t.rank,
      teamId: t.id,
    })),
  };
}

// Build `cfp-teams.json` (team metadata keyed by ID)
function buildCfpTeams(normalized) {
  const teams = {};
  for (const t of normalized) {
    teams[t.id] = {
      id: t.id,
      name: t.team,
      conf: t.conf,
      record: t.record,
      primaryColor: t.primaryColor,
      logo: t.logo,
      // room to expand with more metadata later
    };
  }
  return {
    generatedAt: new Date().toISOString(),
    teams,
  };
}

// ---------- Main ----------
async function main() {
  try {
    if (!CFP_API_URL || CFP_API_URL.includes("example.com")) {
      log(
        "CFP_API_URL is not configured (or still example.com).",
        "Skipping update so we don't overwrite existing data."
      );
      process.exit(0);
    }

    const raw = await fetchJson(CFP_API_URL);

    if (!Array.isArray(raw) || raw.length === 0) {
      throw new Error("Upstream CFP payload is empty or not an array.");
    }

    const normalized = raw.map(normalizeTeam).filter((t) => !isNaN(t.rank));
    if (!normalized.length) {
      throw new Error("No valid team entries after normalization.");
    }

    // 1) Full snapshot
    writeJson(FILE_CFP_2025, {
      generatedAt: new Date().toISOString(),
      source: CFP_API_URL,
      teams: normalized,
    });

    // 2) Bracket/top-12 view
    const cfpData = buildCfpData(normalized);
    writeJson(FILE_CFP_DATA, cfpData);

    // 3) Team metadata (for team pages)
    const cfpTeams = buildCfpTeams(normalized);
    writeJson(FILE_CFP_TEAMS, cfpTeams);

    log("CFP data update complete.");
  } catch (err) {
    console.error("[cfp-update] ERROR:", err?.message || err);
    process.exit(1);
  }
}

main();
