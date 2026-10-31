"""
يجلب مباريات أمس واليوم وغدًا من football-data.org ويكتب matches.json
التشغيل:  FOOTBALL_DATA_TOKEN=مفتاحك python update_matches.py
المفتاح المجاني: https://www.football-data.org/client/register
جدولة (كل 5 دقائق) عبر cron:
  */5 * * * * cd /path/to/site && FOOTBALL_DATA_TOKEN=xxx python3 update_matches.py
أو عبر GitHub Actions + GitHub Pages (مجاني) – انظر الملف .github/workflows/update.yml
"""
import json, os, urllib.request
from datetime import datetime, timedelta, timezone

TOKEN = os.environ["FOOTBALL_DATA_TOKEN"]
today = datetime.now(timezone.utc).date()
url = ("https://api.football-data.org/v4/matches"
       f"?dateFrom={today - timedelta(days=1)}&dateTo={today + timedelta(days=2)}")

req = urllib.request.Request(url, headers={"X-Auth-Token": TOKEN})
with urllib.request.urlopen(req, timeout=30) as r:
    raw = json.load(r)

# روابط البث الرسمي المرخّص فقط (اختياري): {"match_id": "https://..."}
OFFICIAL = {}
if os.path.exists("official_links.json"):
    OFFICIAL = json.load(open("official_links.json", encoding="utf-8"))

STATUS = {"IN_PLAY": "LIVE", "PAUSED": "LIVE", "FINISHED": "FINISHED"}
out = []
for m in raw.get("matches", []):
    ft = m["score"]["fullTime"]
    out.append({
        "league": m["competition"]["name"],
        "home": m["homeTeam"].get("shortName") or m["homeTeam"]["name"],
        "away": m["awayTeam"].get("shortName") or m["awayTeam"]["name"],
        "utc": m["utcDate"],
        "status": STATUS.get(m["status"], "SCHEDULED"),
        "hs": ft["home"], "as": ft["away"],
        "minute": None,
        "hc": m["homeTeam"].get("crest"), "ac": m["awayTeam"].get("crest"),
        "le": m["competition"].get("emblem"),
        "watch": OFFICIAL.get(str(m["id"])),
    })

with open("matches.json", "w", encoding="utf-8") as f:
    json.dump({"updated": datetime.now(timezone.utc).isoformat(), "matches": out},
              f, ensure_ascii=False)
print(f"تم تحديث {len(out)} مباراة")
