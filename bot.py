import os
import json
from urllib.request import Request, urlopen
from urllib.parse import urlencode

print("=== DEMARRAGE DU BOT ===")

try:
    API_KEY = os.environ["ODDS_API_KEY"]
    BOT_TOKEN = os.environ["BOT_TOKEN"]
    CHAT_ID = os.environ["CHAT_ID"]

    print("✅ Les 3 secrets sont présents")

except Exception as e:
    print("❌ PROBLEME AVEC LES SECRETS :", e)
    raise


SPORT = "soccer_epl"
REGION = "us"
MARKET = "totals"


try:
    params = urlencode({
        "apiKey": API_KEY,
        "regions": REGION,
        "markets": MARKET,
        "oddsFormat": "decimal"
    })

    url = f"https://api.the-odds-api.com/v4/sports/{SPORT}/odds/?{params}"

    print("📡 Connexion à Odds API...")

    request = Request(
        url,
        headers={"User-Agent": "odds-drop-bot"}
    )

    with urlopen(request, timeout=20) as response:
        data = response.read().decode("utf-8")

    events = json.loads(data)

    print("✅ Odds API fonctionne")
    print("Nombre de matchs :", len(events))


except Exception as e:
    print("❌ ERREUR ODDS API :", e)
    raise


message = "⚽ TEST ODDS API\n\n"

for event in events[:5]:

    home = event.get("home_team", "?")
    away = event.get("away_team", "?")

    message += f"🏟️ {home} - {away}\n"

    for bookmaker in event.get("bookmakers", []):

        for market in bookmaker.get("markets", []):

            if market.get("key") != "totals":
                continue

            for outcome in market.get("outcomes", []):

                name = outcome.get("name")
                point = outcome.get("point")
                price = outcome.get("price")

                message += f"{name} {point} → {price}\n"

    message += "\n"


try:

    telegram_url = (
        f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage?"
        + urlencode({
            "chat_id": CHAT_ID,
            "text": message
        })
    )

    print("📲 Envoi Telegram...")

    request = Request(
        telegram_url,
        headers={"User-Agent": "odds-drop-bot"}
    )

    with urlopen(request, timeout=15) as response:
        telegram_response = response.read().decode("utf-8")

    print("✅ Telegram fonctionne")
    print(telegram_response)

except Exception as e:

    print("❌ ERREUR TELEGRAM :", e)
    raise
