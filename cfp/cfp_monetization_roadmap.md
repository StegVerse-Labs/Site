# StegVerse CFP Monetization Roadmap

This roadmap tracks how the StegVerse CFP module can evolve from:
- a **clean, ad-free fan tool**, into
- a **multi-sport, multi-league ticket + data + analytics platform**, with
- **automated data feeds** and **minimal manual maintenance**.

Use the checkboxes to mark items as complete (`[x]`) as we ship them.

---

## 0. Ground Rules (Safety, Rights, & Positioning)

**Goal:** Make sure monetization doesn’t collide with league/IP/data rights and keeps StegVerse “fan-first”.

- [ ] Confirm league/data licensing constraints for:
  - NCAAF (CFP, conferences)
  - NFL
  - NCAAB (Men’s & Women’s)
- [ ] Define StegVerse’s position:
  - “Fan analytics + ticket discovery layer” (not an official league product)
- [ ] Add a short public disclaimer on CFP pages:
  - Data sources listed
  - Not affiliated with CFP / NCAA / NFL
- [ ] Decide and document:
  - Which data is **raw pulled** (APIs/scrapes)
  - Which data is **derived/analytics** (our IP we can license)

---

## 1. Product Foundation (What Exists + Near-Term)

### 1.1 CFP Product Core

- [x] Initial CFP public pages:
  - Bracket layout / seed-based bracket view
  - Top 12 rankings view
  - Conference standings section
  - Ticket links (SeatGeek / StubHub / etc.) via config file
- [ ] Championship Weekend page:
  - All conference title games (NCAAF)
  - Links to tickets, kickoff times, and simple summaries
- [ ] Top-12 Team Pages:
  - For each CFP Top 12 team:
    - [ ] “Best case / Most likely / Nightmare” path to the title
    - [ ] Remaining games + results since last CFP release
    - [ ] Ticket links for upcoming games
    - [ ] Simple historical context (last few years postseason)

### 1.2 Data Plumbing (CFP + Sources)

- [ ] Implement CFP data fetcher (SCW-API module) that:
  - [ ] Pulls latest CFP rankings from a trusted source (e.g. cfbd, official CFP site, or another API)
  - [ ] Normalizes into our own `cfp_rankings` schema
  - [ ] Stores results into a cache/JSON used by the site (or SCW-API JSON endpoint)
- [ ] Implement game results and schedule fetch:
  - [ ] For CFP-eligible teams
  - [ ] With score, opponent, neutral-site markers, etc.
- [ ] Implement conference standings fetch:
  - [ ] Per conference (Big 12, SEC, Big Ten, etc.)
- [ ] Implement poll fetcher:
  - [ ] AP Top 25
  - [ ] Coaches Poll
  - [ ] (Optionally) other ranking systems as comparison

### 1.3 Automation & Low Maintenance

- [ ] GitHub Actions / cron-style tasks to:
  - [ ] Update CFP data after each official CFP release
  - [ ] Update games + standings on game days (e.g. Saturdays, bowl games)
- [ ] SCW-API `/cfp/cache` endpoint:
  - [ ] Returns a single bundle (`rankings`, `games`, `standings`, `polls`, `sources`) for the frontend
- [ ] Frontend CFP page is **fully data-driven**:
  - [ ] Renders everything from the SCW-API JSON, no manual edits

---

## 2. Ticket & Affiliate Monetization

**Goal:** Turn traffic into revenue with minimal UX clutter.

### 2.1 Basic Affiliate Links (Current + Next Steps)

- [x] Ticket provider config file (e.g. `cfp-tickets.json`) with:
  - [x] Default providers (SeatGeek, StubHub, Ticketmaster, Vivid Seats, etc.)
  - [x] Conference- and team-specific overrides
- [ ] Add real affiliate IDs to provider URL patterns:
  - [ ] SeatGeek affiliate param
  - [ ] StubHub affiliate param
  - [ ] Others as accounts are created
- [ ] Track basic click metrics (even just via SCW-API or a simple redirect pattern later).

### 2.2 Smart Ticket Discovery

- [ ] Add multi-site “best price” summary per game:
  - [ ] “From $X (across N sites)” label
- [ ] Add filters per user preference:
  - [ ] Sections / rows
  - [ ] Price ceilings
  - [ ] 3-seats-together vs “2+1 front/back” layout
- [ ] Integrate simple logic:
  - [ ] Highlight games where price dip occurs (price drop from last snapshot)
- [ ] Add “Watch this game” feature:
  - [ ] Let logged-in (future) StegVerse users subscribe to a game for ticket-watch alerts

### 2.3 Medium-Term Ticket Revenue Streams

- [ ] Build basic **StegTickets** concept page:
  - [ ] Explain that StegVerse curates multiple ticket providers
  - [ ] Show example “Best current deals” grid
- [ ] Validate affiliate revenue:
  - [ ] Simple goal: $X/mo across NCAAF + NFL + NCAAB
- [ ] Add simple “Deals” / “Last-minute tickets” section:
  - [ ] Pull in games with unusually low prices or important matchups

---

## 3. Data & Analytics Monetization

**Goal:** Make our **derived data & analytics** the actual product.

### 3.1 Fan-Facing Analytics

- [ ] CFP movement charts:
  - [ ] Weekly ranking history for each team
  - [ ] “What changed since last release?” highlights
- [ ] Chaos & scenario engine:
  - [ ] For each CFP slot:
    - [ ] Shows all teams still eligible
    - [ ] Shows conditions (“if X wins, Y loses…”) 
- [ ] Team “health” panels:
  - [ ] Offensive / defensive efficiency metrics (via integration with e.g. cfbd or similar)
  - [ ] Key injuries or absences (future integration)
- [ ] Upset probability & match quality:
  - [ ] For each game, approximate:
    - [ ] Upset chance
    - [ ] “Game quality” (two good teams vs blowout probabilities)

### 3.2 Paid Fan Products (B2C)

- [ ] “Plus” tier concept:
  - [ ] Ad-free (if we ever use ads)
  - [ ] Extra analytics visualizations (charts, simulation tools)
  - [ ] Early access to bracket sims / bowl projections
- [ ] Email / text summaries:
  - [ ] Weekly CFP briefing
  - [ ] Best ticket opportunities by team / region
- [ ] Consider small subscription or one-time purchase:
  - [ ] Low barrier ($3–5/month to start)

### 3.3 Data-as-a-Service (B2B / B2Dev)

- [ ] Define StegVerse CFP data schema as a public spec:
  - [ ] Rankings
  - [ ] Paths / scenarios
  - [ ] Ticket “opportunity” flags
- [ ] Build SCW-API endpoints for external consumers:
  - [ ] `/api/cfp/current` (public-lite)
  - [ ] `/api/cfp/analytics` (paid tier)
- [ ] Explore integration with external open projects:
  - [ ] Example: CFBD or similar — we provide derived analytics in exchange for historical/statistic depth
- [ ] Draft “data usage terms”:
  - [ ] Attribution requirements
  - [ ] Rate limits
  - [ ] Paid tiers vs free

---

## 4. Expansion: Sports, Seasons & Historical

**Goal:** Reuse the CFP engine pattern across sports & years.

### 4.1 New Sports / Leagues

- [ ] Extend model to:
  - [ ] NCAAB Men’s
  - [ ] NCAAB Women’s
  - [ ] NFL (regular season + playoffs)
- [ ] For each sport:
  - [ ] Define ranking/seeding model
  - [ ] Define bracket/road-to-title views
  - [ ] Ticket providers by league/team

### 4.2 Seasonal Lifecycle

- [ ] NCAAF:
  - [ ] During season:
    - Live CFP & conference tracking
  - [ ] Off-season:
    - [ ] Collapse into a season summary page (Year-in-review)
    - [ ] Archive final ranking, bracket, champion path
- [ ] NCAAB:
  - [ ] Regular season:
    - [ ] Focus on top 25 and bubble teams
  - [ ] March Madness:
    - [ ] Bracket view + ticket links per round / site
- [ ] NFL:
  - [ ] Regular season focus on:
    - [ ] Playoff odds
    - [ ] Division standings & wildcard paths
  - [ ] Playoffs / Super Bowl:
    - [ ] High-intent ticket & viewing experience

### 4.3 Historical Data & Archives

- [ ] Build StegVerse **Sports Archive**:
  - [ ] Section per year (e.g., `NCAAF 2024`, `NCAAF 2025`)
  - [ ] Capture:
    - [ ] Final rankings
    - [ ] Brackets
    - [ ] Champion paths
    - [ ] “Best ticket deals we recorded” (optional)

---

## 5. Marketing & Traffic

**Goal:** Get enough eyes on the platform to make affiliate/data monetization meaningful.

### 5.1 Social Content Engine

- [ ] Create simple CFP social templates:
  - [ ] “This week’s biggest CFP movers”
  - [ ] “Team X’s updated path to the playoff”
  - [ ] “Best ticket values for this weekend”
- [ ] Add a StegSocial-style script:
  - [ ] Generates weekly posts (Twitter/X, Threads, Facebook)
  - [ ] Pulls data from CFP JSON / SCW-API
- [ ] Add a small “Share this view” link on team and bracket pages.

### 5.2 Targeted Communities

- [ ] Identify most relevant communities:
  - [ ] Subreddits (CFB, team-specific)
  - [ ] Team forums / Discords
- [ ] Share:
  - [ ] Clean, neutral tools (no spammy tone)
  - [ ] Visuals that help *their* discussions (e.g. bracket scenarios, odds, etc.)

### 5.3 Partnerships & Sponsorships

- [ ] Make a one-page deck for:
  - [ ] “StegVerse Sports: Analytics + Tickets”
- [ ] Approach:
  - [ ] Sports bars / viewing venues
  - [ ] Regional fan clubs
  - [ ] Smaller content creators needing better visuals
- [ ] Offer:
  - [ ] Custom embeds / white-label dashboards
  - [ ] Revenue-sharing via ticket affiliates or data tiers

---

## 6. Tech & Ops: Keeping It Low-Maintenance

**Goal:** Don’t let sports modules eat all your focus away from core StegVerse.

### 6.1 Automation & Self-Healing

- [ ] SCW-API monitors for:
  - [ ] Data pull failures (CFP, standings, polls)
  - [ ] API timeouts from upstream sources
- [ ] Alerting:
  - [ ] Simple log + “needs attention” flag
  - [ ] (Future) StegVerse agent pings you via StegTalk or email
- [ ] Fallbacks:
  - [ ] If one data source fails:
    - [ ] Use backup provider where possible
    - [ ] Mark affected data as “stale” but keep UI running

### 6.2 Separation of Concerns

- [ ] Keep CFP/CFB logic in a dedicated module:
  - [ ] `cfp/` or `sports/cfb/` in site repo
  - [ ] `cfp` module or namespace in SCW-API
- [ ] Enforce simple, clear interfaces:
  - [ ] “Frontend only talks to SCW-API JSON”
  - [ ] “SCW-API only talks to upstream data providers”

### 6.3 Time Budgeting

- [ ] Define a **max weekly time allotment** for sports work (e.g. 3–5 hours/week).
- [ ] Once automation is in place:
  - [ ] Keep sports work inside that budget
  - [ ] Redirect remaining energy toward higher-priority StegVerse modules (TV/TVC, core SCW, etc.)

---

## 7. Progress Log

Keep a short running log here as you go:

- `[2025-11-xx]` – Initial CFP pages scaffolded; ticket config stub added.
- `[2025-11-xx]` – SCW-API health endpoints hardened; CFP Phase 2 design started.
- `[    –    ]` – (you) Add each noticeable milestone here.

---

## How to Use This File

- As you complete items, change `[ ]` → `[x]`.
- When we add new sports (NCAAB, NFL), clone this structure:
  - e.g. `ncaab_monetization_roadmap.md` with sport-specific items.
- Treat this file as:
  - A **visual “what’s left” map**, and
  - A **bridge** between:
    - engineering tasks,
    - marketing, and
    - eventual revenue.
