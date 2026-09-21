import os
import requests

API_KEY = os.environ["ODDS_API_KEY"]

url = "https://api.the-odds-api.com/v4/sports"

response = requests.get(
    url,
    params={"apiKey": API_KEY},
    timeout=15
)

if response.status_code != 200:
    print("ERREUR API :", response.status_code)
    print(response.text)
    exit()

sports = response.json()

print("\n=== FOOTBALL DISPONIBLE ===\n")

for sport in sports:
    if "soccer" in sport["key"].lower():
        print(
            f'{sport["key"]} | '
            f'{sport["title"]} | '
            f'actif={sport["active"]}'
        )

print(f"\nNombre de compétitions football : {sum(1 for s in sports if "soccer" in s["key"].lower())}")
