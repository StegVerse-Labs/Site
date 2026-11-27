/*
 * Conference Championship Projections — computed in the browser at page load.
 *
 * The data file (/data/championship-projections.json) carries INPUTS ONLY:
 * per conference — team conference/overall records, contenders' conference
 * game logs, remaining conference games, and the conference's tiebreak
 * procedure encoded as an ordered list of steps. Nothing in the data file is
 * precomputed: no pairings, no statuses.
 *
 * Method: enumerate every remaining conference game in the inputs (win/loss
 * both ways). For each outcome combination, compute final records and resolve
 * the championship berths, applying the encoded tiebreak steps to any tie
 * straddling a berth. A tie that survives every encoded step (e.g. a rating
 * or a draw, which cannot be computed) is reported UNRESOLVED — every tied
 * team counts as a possible berth holder, never a guessed one, and a berth
 * that depends on an unresolved tie never counts as secured.
 *
 * Statuses: CLINCHED = certain berth in every combination; ELIMINATED = no
 * berth in any; CONTROLS_OWN_PATH = certain berth in every combination where
 * the team wins its remaining games; NEEDS_HELP = every other live team.
 * The projected pairing is the berth set under the "standings-hold"
 * combination (each remaining game won by the team with the better current
 * conference winning percentage, then overall winning percentage, then the
 * home team). Deciding games are the remaining games whose outcome changes
 * the berth set in at least one paired scenario.
 */
(function () {
  "use strict";

  var PROJ_URL = (typeof window !== "undefined" && window.CFP_PROJECTIONS_URL) || "/data/championship-projections.json";

  // ---------------------------------------------------------------- helpers
  function escapeHtml(value) {
    return String(value == null ? "" : value)
      .replaceAll("&", "&amp;")
      .replaceAll("<", "&lt;")
      .replaceAll(">", "&gt;")
      .replaceAll('"', "&quot;")
      .replaceAll("'", "&#039;");
  }

  function pct(w, l) {
    return w + l === 0 ? 0 : w / (w + l);
  }

  function clone(obj) {
    return JSON.parse(JSON.stringify(obj));
  }

  // ------------------------------------------------------- tiebreak resolver
  // resultsOf(teamName, state) -> { opponentName: "W"|"L" } for conference
  // games, combining the input log with the scenario's applied outcomes.
  function resultsOf(name, state) {
    var out = {};
    var base = state.logs[name] || {};
    Object.keys(base).forEach(function (k) { out[k] = base[k]; });
    (state.applied[name] || []).forEach(function (g) {
      out[g.opponent] = g.won ? "W" : "L";
    });
    return out;
  }

  function recordVs(name, opponents, state) {
    var res = resultsOf(name, state);
    var w = 0, l = 0;
    opponents.forEach(function (opp) {
      if (res[opp] === "W") w += 1;
      else if (res[opp] === "L") l += 1;
    });
    return { w: w, l: l, played: w + l };
  }

  // Order a tied group for `spots` berths. Returns { order: [...names],
  // unresolved: bool } — order is best-first; when unresolved is true the
  // first `spots` entries cannot be separated from the rest of the group by
  // the encoded steps and all group members must be treated as possible.
  function resolveTie(group, spots, conf, state, steps) {
    if (group.length <= spots) return { order: group.slice(), unresolved: false };
    if (spots <= 0) return { order: group.slice(), unresolved: true };
    steps = steps || conf.tiebreak.steps;
    if (!steps.length) return { order: group.slice(), unresolved: true };
    var step = steps[0];
    var rest = steps.slice(1);
    var partitioned = partitionByStep(group, step, conf, state);
    if (!partitioned) {
      // Step cannot separate this group at all; move to the next step.
      return resolveTie(group, spots, conf, state, rest);
    }
    // partitioned: array of subgroups, best first.
    var order = [];
    var remaining = spots;
    var unresolved = false;
    for (var i = 0; i < partitioned.length; i++) {
      var sub = partitioned[i];
      if (remaining <= 0) { order = order.concat(sub); continue; }
      if (sub.length <= remaining) {
        order = order.concat(sub);
        remaining -= sub.length;
      } else if (sub.length === 1) {
        order = order.concat(sub);
        remaining -= 1;
      } else {
        // This subgroup straddles the cut: restart the full tiebreak inside
        // it (the standard "revert" behaviour once a team is separated).
        var inner = resolveTie(sub, remaining, conf, state, conf.tiebreak.steps);
        if (inner.unresolved && steps.length && rest.length === 0 && inner.order.length === sub.length) {
          // Restarting looped without progress and no steps remain distinct:
          // fall through with unresolved flagged.
        }
        order = order.concat(inner.order);
        if (inner.unresolved) unresolved = true;
        remaining = 0;
      }
    }
    // If the step separated nothing (single subgroup equal to the group),
    // partitionByStep returns null, handled above. If it separated but the
    // straddling subgroup could not be resolved, unresolved is set.
    return { order: order, unresolved: unresolved };
  }

  // Returns an array of subgroups (best first) if the step separates the
  // group into at least two distinct ranks, else null.
  function partitionByStep(group, step, conf, state) {
    var scored = group.map(function (name) {
      return { name: name, key: stepKey(name, group, step, conf, state) };
    });
    // A null key means the step does not apply to that team (e.g. no
    // head-to-head played). If any key is null in a way that blocks a full
    // ordering, the step is treated as non-separating unless it still
    // identifies a unique top or bottom (handled inside stepKey logic by
    // returning comparable sentinel values).
    var distinct = {};
    scored.forEach(function (s) { distinct[String(s.key)] = true; });
    if (Object.keys(distinct).length < 2) return null;
    scored.sort(function (a, b) { return b.key - a.key; });
    var groups = [];
    var current = [scored[0]];
    for (var i = 1; i < scored.length; i++) {
      if (scored[i].key === scored[i - 1].key) current.push(scored[i]);
      else { groups.push(current); current = [scored[i]]; }
    }
    groups.push(current);
    return groups.map(function (g) { return g.map(function (s) { return s.name; }); });
  }

  // Numeric key for one team under one step; higher is better. Returns a
  // number in all cases (using -Infinity-style sentinels via large negative
  // values) so partitions can form; a step that genuinely cannot rank the
  // group yields identical keys for everyone and partitionByStep returns null.
  function stepKey(name, group, step, conf, state) {
    var others = group.filter(function (n) { return n !== name; });
    if (step === "head_to_head") {
      var rec = recordVs(name, others, state);
      if (group.length === 2) {
        if (rec.played < 1) return 0; // did not play: step cannot separate
        return rec.w === 1 ? 1001 : 0;
      }
      // Multi-team: the step separates only a team that beat every other
      // tied team (unique top) or lost to every other tied team (unique
      // bottom). Anything else is inconclusive and falls to the next step.
      var playedAll = rec.played === others.length;
      var groupRecs = group.map(function (n) { return recordVs(n, group.filter(function (x) { return x !== n; }), state); });
      var beatAll = groupRecs.filter(function (r, i) {
        var o = group.filter(function (x) { return x !== group[i]; });
        return r.played === o.length && r.l === 0 && r.w > 0;
      }).length;
      var lostAll = groupRecs.filter(function (r, i) {
        var o = group.filter(function (x) { return x !== group[i]; });
        return r.played === o.length && r.w === 0 && r.l > 0;
      }).length;
      if (beatAll === 1 && playedAll && rec.l === 0 && rec.w > 0) return 3000;
      if (lostAll === 1 && playedAll && rec.w === 0 && rec.l > 0) return -3000;
      return 0;
    }
    if (step === "common_opponents") {
      var common = commonOpponents(group, state);
      if (!common.length) return 0;
      var r = recordVs(name, common, state);
      if (r.played < common.length) return 0;
      return pct(r.w, r.l) * 1000 + r.w;
    }
    if (step === "best_common_opponent") {
      var common2 = commonOpponents(group, state);
      if (!common2.length) return 0;
      // Order common opponents by final standing (best first); build a
      // positional score: win over the best common opponent counts most.
      var ordered = common2.slice().sort(function (a, b) {
        var ra = state.records[a], rb = state.records[b];
        var pa = pct(ra.cw, ra.cl), pb = pct(rb.cw, rb.cl);
        if (pb !== pa) return pb - pa;
        return rb.cw - ra.cw;
      });
      var res = resultsOf(name, state);
      var score = 0;
      for (var i = 0; i < ordered.length; i++) {
        var weight = (ordered.length - i) * 100;
        if (res[ordered[i]] === "W") score += weight;
        else if (res[ordered[i]] === "L") score += 0;
        else return 0; // did not play one of them: step cannot rank this team
      }
      return score;
    }
    if (step === "opponent_win_pct") {
      // Combined (cumulative) conference winning percentage of all
      // conference opponents — total opponent conference wins over total
      // opponent conference games, as the published procedures define it.
      var resAll = resultsOf(name, state);
      var opps = Object.keys(resAll);
      if (!opps.length) return 0;
      var wSum = 0, lSum = 0;
      opps.forEach(function (opp) {
        var r = state.records[opp];
        if (r) { wSum += r.cw; lSum += r.cl; }
      });
      return Math.round(pct(wSum, lSum) * 100000);
    }
    if (step === "total_wins") {
      var rec2 = state.records[name];
      return rec2.ow * 1000 + rec2.ol * -1;
    }
    return 0; // rating / draw / unknown steps cannot be computed
  }

  function commonOpponents(group, state) {
    var sets = group.map(function (name) {
      return new Set(Object.keys(resultsOf(name, state)));
    });
    var first = sets[0];
    var out = [];
    first.forEach(function (opp) {
      if (group.indexOf(opp) !== -1) return;
      if (sets.every(function (s) { return s.has(opp); })) out.push(opp);
    });
    return out;
  }

  // ------------------------------------------------------------- simulation
  // Build the per-scenario state: records for every team after applying the
  // outcomes of the enumerated remaining conference games.
  function buildState(conf, outcomes) {
    var records = {};
    var logs = {};
    var applied = {};
    conf.teams.forEach(function (t) {
      records[t.name] = { cw: t.conf[0], cl: t.conf[1], ow: t.overall[0], ol: t.overall[1] };
      logs[t.name] = t.conf_results || {};
      applied[t.name] = [];
    });
    conf.remaining_games.forEach(function (g, idx) {
      var homeWon = outcomes[idx];
      var home = records[g.home], away = records[g.away];
      if (!home || !away) return;
      if (homeWon) { home.cw += 1; away.cl += 1; home.ow += 1; away.ol += 1; }
      else { away.cw += 1; home.cl += 1; away.ow += 1; home.ol += 1; }
      applied[g.home].push({ opponent: g.away, won: homeWon });
      applied[g.away].push({ opponent: g.home, won: !homeWon });
    });
    return { records: records, logs: logs, applied: applied };
  }

  function rankKey(rec) {
    // Conference winning percentage, then conference wins.
    return pct(rec.cw, rec.cl) * 10000 + rec.cw;
  }

  // The set of teams taking the berths in one scenario.
  function berthSet(conf, state) {
    if (conf.format === "divisions") {
      var winners = [], certain = [], possible = [];
      var unresolved = false;
      conf.divisions.forEach(function (div) {
        var members = conf.teams.filter(function (t) { return t.division === div; })
          .map(function (t) { return t.name; });
        var top = topTeams(members, 1, conf, state);
        winners = winners.concat(top.teams);
        certain = certain.concat(top.certain);
        possible = possible.concat(top.possible);
        if (top.unresolved) unresolved = true;
      });
      return { teams: winners, certain: certain, possible: possible, unresolved: unresolved };
    }
    var all = conf.teams.map(function (t) { return t.name; });
    return topTeams(all, 2, conf, state);
  }

  // Top `spots` teams from `names` under final records + tiebreaks.
  // Returns { teams, certain, possible, unresolved }: `certain` berths are
  // established by record or by a fully resolved tiebreak; a berth that
  // depends on a tie the encoded steps cannot resolve is only `possible`
  // (every member of the unresolved group counts as possible, none as
  // certain — certainty is never overstated).
  function topTeams(names, spots, conf, state) {
    var sorted = names.slice().sort(function (a, b) {
      return rankKey(state.records[b]) - rankKey(state.records[a]);
    });
    var chosen = [];
    var possible = [];
    var unresolved = false;
    var i = 0;
    while (i < sorted.length && chosen.length < spots) {
      var j = i;
      while (j < sorted.length && rankKey(state.records[sorted[j]]) === rankKey(state.records[sorted[i]])) j++;
      var group = sorted.slice(i, j);
      var room = spots - chosen.length;
      if (group.length <= room) {
        chosen = chosen.concat(group);
      } else {
        var res = resolveTie(group, room, conf, state, conf.tiebreak.steps);
        if (res.unresolved) {
          unresolved = true;
          possible = possible.concat(group);
          // The remaining berths are contested by this group alone; teams
          // below it are strictly worse by record and take no berth in
          // this scenario.
          break;
        } else {
          chosen = chosen.concat(res.order.slice(0, room));
        }
      }
      i = j;
    }
    return { teams: chosen.concat(possible), certain: chosen, possible: possible, unresolved: unresolved };
  }

  // Full race computation for one conference.
  function computeRace(conf) {
    var games = conf.remaining_games || [];
    var n = games.length;
    var total = Math.pow(2, n);
    var berthCount = {};
    var berthCertainCount = {};
    var winOutBerth = {};   // berths in scenarios where the team wins out
    var winOutCertain = {}; // certain berths in scenarios where the team wins out
    var winOutTotal = {};
    conf.teams.forEach(function (t) {
      berthCount[t.name] = 0;
      berthCertainCount[t.name] = 0;
      winOutBerth[t.name] = 0;
      winOutCertain[t.name] = 0;
      winOutTotal[t.name] = 0;
    });
    var berthSets = [];
    var favoritesOutcomes = games.map(function (g) {
      var home = conf.teams.find(function (t) { return t.name === g.home; });
      var away = conf.teams.find(function (t) { return t.name === g.away; });
      var ph = pct(home.conf[0], home.conf[1]);
      var pa = pct(away.conf[0], away.conf[1]);
      if (ph !== pa) return ph > pa;
      var oh = pct(home.overall[0], home.overall[1]);
      var oa = pct(away.overall[0], away.overall[1]);
      if (oh !== oa) return oh > oa;
      return true; // home team
    });
    var favoritesBerths = null;
    var favoritesCertain = null;
    var favoritesUnresolved = false;

    for (var mask = 0; mask < total; mask++) {
      var outcomes = [];
      for (var i = 0; i < n; i++) outcomes.push(Boolean(mask & (1 << i)));
      var state = buildState(conf, outcomes);
      var berths = berthSet(conf, state);
      berthSets.push({ teams: berths.teams, certain: berths.certain });
      berths.teams.forEach(function (name) { berthCount[name] += 1; });
      berths.certain.forEach(function (name) { berthCertainCount[name] += 1; });
      // Win-out tracking per team.
      conf.teams.forEach(function (t) {
        var rem = teamRemaining(conf, t.name);
        var wonAll = rem.every(function (g) {
          var idx = games.indexOf(g);
          return g.home === t.name ? outcomes[idx] : !outcomes[idx];
        });
        if (wonAll) {
          winOutTotal[t.name] += 1;
          if (berths.teams.indexOf(t.name) !== -1) winOutBerth[t.name] += 1;
          if (berths.certain.indexOf(t.name) !== -1) winOutCertain[t.name] += 1;
        }
      });
      var isFav = outcomes.every(function (v, idx) { return v === favoritesOutcomes[idx]; });
      if (isFav) { favoritesBerths = berths.teams; favoritesCertain = berths.certain; favoritesUnresolved = berths.unresolved; }
    }

    // Deciding games: flipping only that game changes the berth set somewhere.
    var deciding = [];
    games.forEach(function (g, idx) {
      var flips = false;
      for (var mask2 = 0; mask2 < total && !flips; mask2++) {
        var other = mask2 ^ (1 << idx);
        if (other < mask2) continue;
        var a = berthSets[mask2].teams.slice().sort().join("|");
        var b = berthSets[other].teams.slice().sort().join("|");
        if (a !== b) flips = true;
      }
      if (flips) deciding.push(g);
    });

    // Statuses. CLINCHED and CONTROLS_OWN_PATH are asserted only on
    // CERTAIN berths — a berth that rides on an unresolved tie is possible,
    // never secured.
    var contenders = conf.teams.map(function (t) {
      var bc = berthCount[t.name];
      var certain = berthCertainCount[t.name];
      var status;
      if (certain === total) status = "CLINCHED";
      else if (bc === 0) status = "ELIMINATED";
      else if (winOutTotal[t.name] > 0 && winOutCertain[t.name] === winOutTotal[t.name]) status = "CONTROLS_OWN_PATH";
      else status = "NEEDS_HELP";
      var rem = teamRemaining(conf, t.name);
      var mustWinOut = bc > 0 && rem.length > 0 &&
        scenariosWhereBerthWithoutWinningOut(conf, games, berthSets, t.name) === 0;
      return {
        team: t.name,
        division: t.division || null,
        overall: t.overall,
        conf: t.conf,
        status: status,
        berth_scenarios: bc,
        berth_certain: certain,
        total_scenarios: total,
        must_win_out: mustWinOut,
        remaining: rem
      };
    });

    var pairingSet = favoritesBerths && favoritesCertain && total > 0 &&
      berthSets.every(function (s) {
        return s.teams.length === s.certain.length &&
          s.certain.slice().sort().join("|") === favoritesCertain.slice().sort().join("|");
      });

    return {
      contenders: contenders,
      projected: favoritesBerths || [],
      projected_unresolved: favoritesUnresolved,
      pairing_set: Boolean(pairingSet),
      deciding_games: deciding,
      total_scenarios: total
    };
  }

  function teamRemaining(conf, name) {
    return (conf.remaining_games || []).filter(function (g) {
      return g.home === name || g.away === name;
    });
  }

  function scenariosWhereBerthWithoutWinningOut(conf, games, berthSets, name) {
    var count = 0;
    var total = berthSets.length;
    var n = games.length;
    for (var mask = 0; mask < total; mask++) {
      if (berthSets[mask].teams.indexOf(name) === -1) continue;
      var rem = teamRemaining(conf, name);
      var wonAll = rem.every(function (g) {
        var idx = games.indexOf(g);
        var homeWon = Boolean(mask & (1 << idx));
        return g.home === name ? homeWon : !homeWon;
      });
      if (!wonAll) count += 1;
    }
    return count;
  }

  // --------------------------------------------------------------- rendering
  function statusBadge(status) {
    if (status === "CLINCHED") return '<span class="cfp-badge cfp-badge-clinched">Clinched</span>';
    if (status === "CONTROLS_OWN_PATH") return '<span class="cfp-badge cfp-badge-controls">Controls own path</span>';
    if (status === "NEEDS_HELP") return '<span class="cfp-badge cfp-badge-needshelp">Needs help</span>';
    if (status === "ELIMINATED") return '<span class="cfp-badge cfp-badge-elim">Eliminated</span>';
    return "";
  }

  function fmtRecord(r) { return r[0] + "-" + r[1]; }

  function fmtDate(iso) {
    var d = new Date(iso + "T12:00:00Z");
    if (Number.isNaN(d.getTime())) return iso;
    return d.toLocaleDateString("en-US", { weekday: "short", month: "short", day: "numeric", timeZone: "UTC" });
  }

  function pathLine(c, conf) {
    if (c.status === "CLINCHED") return "Berth secured — in the championship game in every remaining outcome.";
    if (c.status === "ELIMINATED") return "No remaining outcome puts this team in the championship game.";
    var remText = c.remaining.map(function (g) {
      return (g.home === c.team ? "vs " : "at ") + (g.home === c.team ? g.away : g.home) + " (" + fmtDate(g.date) + ")";
    }).join(", ");
    if (c.status === "CONTROLS_OWN_PATH") {
      return "Win " + (c.remaining.length > 1 ? "out" : "its remaining game") + (remText ? " — " + remText : "") + " — and the berth is theirs, no help needed.";
    }
    var base = "Berth in " + c.berth_scenarios + " of " + c.total_scenarios + " remaining outcome combinations.";
    if (c.berth_certain != null && c.berth_certain < c.berth_scenarios) {
      base += " Locked in " + c.berth_certain + " of them; the rest ride on a tie the encoded steps cannot fully resolve.";
    }
    if (c.must_win_out) base += " Must win out" + (remText ? " (" + remText + ")" : "") + " and still needs help.";
    else if (remText) base += " Remaining: " + remText + ".";
    return base;
  }

  function renderConference(conf, race) {
    var cg = conf.championship_game || {};
    var live = race.contenders.filter(function (c) { return c.status !== "ELIMINATED"; });
    var elimRelevant = (conf.spotlight_eliminated || []).map(function (name) {
      return race.contenders.find(function (c) { return c.team === name; });
    }).filter(Boolean);
    var shown = live.concat(elimRelevant);
    var rows = shown.map(function (c) {
      return "<tr><td>" + escapeHtml(c.team) + (c.division ? ' <span style="opacity:0.65;">(' + escapeHtml(c.division) + ")</span>" : "") + "</td>" +
        "<td>" + fmtRecord(c.overall) + "</td><td>" + fmtRecord(c.conf) + "</td>" +
        "<td>" + statusBadge(c.status) + "</td>" +
        '<td style="font-size:0.82rem;">' + escapeHtml(pathLine(c, conf)) + "</td></tr>";
    }).join("");
    var deciding = race.deciding_games.map(function (g) {
      return "<li><strong>" + escapeHtml(g.away) + " at " + escapeHtml(g.home) + "</strong> — " + fmtDate(g.date) + "</li>";
    }).join("");
    var decidesLine;
    if (race.pairing_set) decidesLine = "The matchup is set — every remaining outcome produces this pairing.";
    else if (race.deciding_games.length) {
      decidesLine = "Turns on: " + race.deciding_games.map(function (g) {
        return g.away + " at " + g.home + " (" + fmtDate(g.date) + ")";
      }).join("; ") + ".";
    } else decidesLine = "No remaining game changes the projected pairing.";
    var tieNote = conf.tiebreak.basis === "PARTIAL"
      ? ' Tiebreak basis: <strong>PARTIAL</strong> — ' + escapeHtml(conf.tiebreak.basis_note || "only the verified steps are encoded.")
      : ' Tiebreak basis: conference procedure as encoded from the sources below.';
    if (race.projected_unresolved) tieNote += " The projected pairing survives every encoded tiebreak step unresolved and is shown in current standings order.";
    return '<div class="cfp-spot-card" id="championship-' + escapeHtml(conf.id) + '">' +
      '<div class="cfp-spot-card-header"><div class="cfp-spot-card-title"><a href="#championship-' + escapeHtml(conf.id) + '" title="Link to this projection" style="color:inherit;text-decoration:none;">' + escapeHtml(conf.name) + ' <span style="opacity:0.55;font-size:0.78em;">¶</span></a></div>' +
      "<div>" + fmtDate(cg.date) + (cg.site ? " • " + escapeHtml(cg.site) : "") + "</div></div>" +
      '<div style="font-size:1.05rem;margin-bottom:0.5rem;">Projected: <strong>' +
      race.projected.map(escapeHtml).join("</strong> vs <strong>") + "</strong>" +
      (race.pairing_set ? ' <span class="cfp-badge cfp-badge-clinched">Set</span>' : ' <span class="cfp-badge cfp-badge-controls">Projection</span>') +
      "</div>" +
      (cg.note ? '<p style="margin:0.25rem 0;">' + escapeHtml(cg.note) + "</p>" : "") +
      '<table class="cfp-conf-table"><thead><tr><th>Team</th><th>Overall</th><th>Conf</th><th>Status</th><th>Path</th></tr></thead><tbody>' +
      rows + "</tbody></table>" +
      (deciding ? '<div style="margin-top:0.6rem;"><strong>Deciding games</strong><ul style="margin:0.3rem 0 0 1.1rem;">' + deciding + "</ul></div>" : "") +
      '<p style="margin-top:0.6rem;font-size:0.85rem;">' + escapeHtml(decidesLine) + tieNote + "</p>" +
      ((conf.sources && conf.sources.length)
        ? '<p style="font-size:0.78rem;opacity:0.85;">Sources: ' + conf.sources.map(function (s) {
            return '<a href="' + escapeHtml(s.url) + '" target="_blank" rel="noopener">' + escapeHtml(s.label) + "</a>";
          }).join(" • ") + "</p>"
        : "") +
      "</div>";
  }

  function render(data) {
    var el = document.getElementById("cfp-championship");
    var meta = document.getElementById("cfp-championship-meta");
    if (!el) return;
    if (meta) {
      meta.textContent = "Standings as of " + (data.updated_at_display || data.updated_at || "unknown") +
        " • Projections computed on this page load from the input standings — " + (data.snapshot_scope || "") +
        ((data.in_progress && data.in_progress.length)
          ? " Still in progress at input time: " + data.in_progress.join(" ")
          : "");
    }
    var confs = data.conferences || [];
    var picker = '<div style="margin-bottom:0.9rem;"><label for="cfp-conf-picker" style="font-size:0.88rem;opacity:0.85;">Conference: </label>' +
      '<select id="cfp-conf-picker" style="background:#141a26;color:#e8ecf3;border:1px solid #2c3646;border-radius:6px;padding:0.3rem 0.5rem;font-size:0.92rem;">' +
      '<option value="">All conferences</option>' +
      confs.map(function (conf) {
        return '<option value="' + escapeHtml(conf.id) + '">' + escapeHtml(conf.name) + "</option>";
      }).join("") + "</select></div>";
    el.innerHTML = picker + confs.map(function (conf) {
      return renderConference(conf, computeRace(conf));
    }).join("");
    bindRefresh();
    var pickerEl = document.getElementById("cfp-conf-picker");
    function applyFilter(id, scroll) {
      var cards = el.querySelectorAll(".cfp-spot-card");
      for (var i = 0; i < cards.length; i++) {
        cards[i].style.display = (!id || cards[i].id === "championship-" + id) ? "" : "none";
      }
      if (scroll && id) {
        var target = document.getElementById("championship-" + id);
        if (target) target.scrollIntoView();
      }
    }
    if (pickerEl) {
      pickerEl.addEventListener("change", function () {
        var id = pickerEl.value;
        applyFilter(id, false);
        if (window.history && history.replaceState) {
          history.replaceState(null, "", id ? "#championship-" + id : window.location.pathname + window.location.search);
        }
      });
    }
    var hashId = ((typeof window !== "undefined" && window.location && window.location.hash) || "").replace(/^#championship-/, "");
    if (hashId && confs.some(function (conf) { return conf.id === hashId; })) {
      if (pickerEl) pickerEl.value = hashId;
      applyFilter(hashId, false);
      setTimeout(function () { applyFilter(hashId, true); }, 0);
    }
  }

  function bindRefresh() {
    var rb = document.getElementById("cfp-refresh-btn");
    if (rb && !rb.dataset.champBound) {
      rb.dataset.champBound = "1";
      rb.addEventListener("click", load);
    }
  }

  function load() {
    var el = document.getElementById("cfp-championship");
    if (!el) return;
    fetch(PROJ_URL + "?t=" + Date.now())
      .then(function (r) { if (!r.ok) throw new Error("HTTP " + r.status); return r.json(); })
      .then(render)
      .catch(function (err) {
        console.error(err);
        el.innerHTML = "<p>Championship projections are unavailable right now; no stale projection is substituted.</p>";
      });
  }

  if (typeof document !== "undefined") {
    if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", load);
    else load();
  }

  if (typeof window !== "undefined") {
    window.CFPChampionship = { reload: load };
  }

  if (typeof module !== "undefined" && module.exports) {
    module.exports = { computeRace: computeRace, berthSet: berthSet, buildState: buildState };
  }
})();
