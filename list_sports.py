import os
import json
from urllib.request import urlopen
from urllib.parse import urlencode

API_KEY = os.environ["ODDS_API_KEY"]

url = "https://api.the-odds-api.com/v4/sports?" + urlencode({
    "apiKey": API_KEY
})

with urlopen(url, timeout=15) as response:
    sports = json.loads(response.read().decode())

print("=== FOOTBALL DISPONIBLE ===")

count = 0

for sport in sports:
    if "soccer" in sport.get("key", "").lower():
        print(
            sport["key"],
            "|",
            sport["title"],
            "| actif =",
            sport["active"]
        )
        count += 1

print()
print("Nombre de compétitions football :", count)
