# 🏈 StegVerse NCAAF CFP Live Tracker

The **StegVerse CFP Live Tracker** is an automatically updating, fully client-side
NCAAF data viewer designed to:

- Display **live CFP Top 12 rankings**
- Identify **locked spots** and **in-play seeds**
- Provide **scenario paths** for all teams still eligible for movement
- Show **results & upcoming games**
- Display **AP, Coaches, and CFP polls side-by-side**
- Show live **conference standings** (all conferences)
- Provide **ticket links** through multiple major ticket sellers/resellers
- Support **config-driven affiliate URLs** (no code changes needed)

This system is fully modular and built around JSON data files so it can operate
on any static hosting environment (GitHub Pages, Vercel, Netlify, Render, etc.).

---

## 📁 File Structure

/cfp
├── cfp.html             # Main live page
├── cfp.css              # Stylesheet
├── cfp.js               # Client JS for rendering & data integration
├── cfp-data.json        # Rankings, standings, polls, game results
├── cfp-tickets.json     # Ticket provider config + affiliate patterns
└── README.md            # (this document)

---

## 🔧 Config-Driven Architecture

The Live Tracker requires **zero code changes** when:

- CFP rankings update  
- Polls update  
- Conference data updates  
- Affiliate links change  
- New ticket providers are added  

All dynamic data is read from:

### **`cfp-data.json`**
- CFP Top 12 rankings  
- Lock status and scenario paths  
- AP / Coaches / CFP polls  
- Conference standings  
- Games (results + scheduled)  
- Timestamps & data source references  

### **`cfp-tickets.json`**
Controls ticket seller integrations:

- Default ticket providers  
- Conference-specific providers  
- Team-specific providers  
- URL patterns for each seller  
- Affiliate query string parameters (optional now; you can add later)

Example:

```json
"patterns": {
  "seatgeek": "https://seatgeek.com/search?search={QUERY}&aid=YOUR_ID",
  "stubhub": "https://www.stubhub.com/find/s/?q={QUERY}&publisher_id=YOUR_ID"
}

🔗 Live Ticket Links (Config-Driven)

Each game automatically receives “Find Tickets” options based on:
	•	Home/away team
	•	Conference of the game
	•	Default providers
	•	Team-specific overrides
	•	Conference-specific overrides

Rendered buttons include:
	•	SeatGeek
	•	StubHub
	•	Ticketmaster
	•	Vivid Seats
	•		•	any others you add in cfp-tickets.json

⸻

🧩 Key Modules

Rankings Renderer
	•	CFP Top 12 table
	•	Status badges (Locked / In Play / Eliminated)
	•	Lock reasoning text
	•	Source marker (linked to the bottom of page)

Spot Details
	•	Shows all seeds not yet locked
	•	Lists eligible teams
	•	Lists scenarios required to secure each spot

Polls (CFP / AP / Coaches)
	•	Three poll cards
	•	Ranked tables
	•	Source markers [1] [2] [3]

Conference Standings
	•	Conference dropdown
	•	Loads standings dynamically
	•	PF/PA, conference record, overall record
	•	Source marker [4]

Games
	•	Final scores
	•	Scheduled games
	•	Notes
	•	Kickoff times
	•	Ticket provider buttons (from config)

⸻

📜 Data Sources

All tables include numbered markers ([1], [2]) linking to the footer.

Examples:
[1] CFP Rankings – https://collegefootballplayoff.com  
[2] AP Top 25 – https://apnews.com  
[3] Coaches Poll – https://sports.usatoday.com  
[4] Conference standings – https://espn.com/college-football/standings

You can add or remove sources by editing the sources array in cfp-data.json.

⸻

🚀 Deploying the CFP Tracker
	1.	Upload all files to your repository (e.g., StegVerse/site under /cfp).
	2.	Deploy via:
	•	GitHub Pages
	•	Netlify
	•	Render static site
	•	Vercel
	3.	Open:
https://yourdomain.com/cfp/cfp.html

All updates happen automatically whenever cfp-data.json changes.

⸻

🛠 Development / Editor Notes
	•	Editing from iPhone is supported — the entire system is JSON-driven.
	•	No build pipeline required.
	•	No backend required.
	•	No rate limits or API keys required (unless you add an API backend on purpose).

⸻

🧭 Future Enhancements (internal)

These features are planned as StegVerse expands:
	•	StegTickets
Real-time price comparisons across all sellers, updated continuously.
	•	StegOdds
Live odds + movement history for each CFP slot & game.
	•	StegSim CFP
Model-driven projections & chaos simulations based on remaining games.
	•	StegStats API
Exposes all CFP, poll, and standings data as an API endpoint.
	•	CFP Narrative Engine
AI-written stories, summaries, and automated social posts (via StegSocial).
	•	Affiliate Router Service
tickets.stegverse.com/<slug> redirects → affiliate URLs (rotatable).

⸻

🎉 Coming Soon (public-facing)

You can embed this in the public CFP page (near footer):

<div class="cfp-coming-soon">
  <h3>Coming Soon to StegVerse Sports</h3>
  <ul>
    <li>🔮 Live CFP probability forecasts</li>
    <li>📊 Real-time playoff path simulations</li>
    <li>🎟 Smart ticket finder with multi-site price tracking</li>
    <li>📢 Automated game summaries sent to your socials</li>
    <li>📈 Expanded analytics for every conference and team</li>
  </ul>
</div>
