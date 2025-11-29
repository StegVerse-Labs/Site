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
