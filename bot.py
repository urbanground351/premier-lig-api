import requests
import json
from datetime import datetime, timedelta

def fetch_matches():
    today = datetime.now()
    start_date = today.strftime("%Y%m%d")
    end_date = (today + timedelta(days=7)).strftime("%Y%m%d")
    
    # Sadece bu satır değişti: tur.1 yerine eng.1 (Premier Lig)
    url = f"https://site.api.espn.com/apis/site/v2/sports/soccer/eng.1/scoreboard?dates={start_date}-{end_date}"
    
    final_data = {
        "last_updated": datetime.now().isoformat(),
        "source": "ESPN Açık API (Premier Lig)",
        "matches": []
    }
    
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            data = response.json()
            
            for event in data.get("events", []):
                competitors = event["competitions"][0]["competitors"]
                home = next((c["team"]["displayName"] for c in competitors if c["homeAway"] == "home"), "Ev Sahibi")
                away = next((c["team"]["displayName"] for c in competitors if c["homeAway"] == "away"), "Deplasman")
                
                utc_time = datetime.strptime(event["date"], "%Y-%m-%dT%H:%MZ")
                tr_time = utc_time + timedelta(hours=3)
                
                final_data["matches"].append({
                    "league": "İngiltere Premier Lig",
                    "home": home,
                    "away": away,
                    "time": tr_time.strftime("%H:%M"),
                    "date": tr_time.strftime("%d.%m.%Y")
                })
    except Exception as e:
        print(f"Hata: {e}")

    with open("matches.json", "w", encoding="utf-8") as f:
        json.dump(final_data, f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    fetch_matches()
