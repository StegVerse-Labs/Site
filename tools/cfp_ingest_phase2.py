import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

CFP_BASE = "https://collegefootballplayoff.com"

def fetch_cfp_poll():
    print("[cfp] Discovering latest CFP rankings URL…")

    # 1. Load rankings index
    index_url = f"{CFP_BASE}/sports/football-rankings"
    resp = requests.get(index_url, timeout=20)
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, "html.parser")

    # 2. Find ranking page link
    link = soup.find("a", href=lambda x: x and "cfp-ranking" in x)
    if not link:
        raise RuntimeError("Could not find current CFP ranking link.")

    rankings_url = urljoin(CFP_BASE, link["href"])
    print(f"[cfp] Latest ranking page: {rankings_url}")

    # 3. Scrape ranking page
    resp2 = requests.get(rankings_url, timeout=20)
    resp2.raise_for_status()
    soup2 = BeautifulSoup(resp2.text, "html.parser")

    # 4. Extract ranking table
    table = soup2.find("table")
    if not table:
        raise RuntimeError("CFP ranking table not found.")

    poll = []
    for row in table.find_all("tr")[1:]:
        cols = [c.get_text(strip=True) for c in row.find_all("td")]
        if len(cols) < 4:
            continue
        poll.append({
            "rank": cols[0],
            "team": cols[1],
            "record": cols[2],
            "conference": cols[3],
        })

    return poll
