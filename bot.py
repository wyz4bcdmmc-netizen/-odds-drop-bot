import os
import json
from urllib.request import Request, urlopen
from urllib.parse import urlencode

BOT_TOKEN = os.environ["BOT_TOKEN"]
CHAT_ID = os.environ["CHAT_ID"]
API_KEY = os.environ["ODDS_API_KEY"]

# Compétition de test
SPORT = "soccer_epl"

# Marché : Over / Under
MARKET = "totals"

# Région des bookmakers
REGION = "us"


def get_odds():
    params = urlencode({
        "apiKey": API_KEY,
        "regions": REGION,
        "markets": MARKET,
        "oddsFormat": "decimal"
    })

    url = f"https://api.the-odds-api.com/v4/sports/{SPORT}/odds/?{params}"

    request = Request(
        url,
        headers={"User-Agent": "odds-drop-bot/1.0"}
    )

    with urlopen(request, timeout=20) as response:
        return json.loads(response.read().decode())


def send_telegram(message):
    params = urlencode({
        "chat_id": CHAT_ID,
        "text": message
    })

    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage?{params}"

    request = Request(
        url,
        headers={"User-Agent": "odds-drop-bot/1.0"}
    )

    with urlopen(request, timeout=15) as response:
        return response.read().decode()


try:
    events = get_odds()

    print(f"Nombre de matchs récupérés : {len(events)}")

    message = "⚽ TEST ODDS API\n\n"

    if not events:
        message += "❌ Aucun match disponible actuellement."
    else:
        for event in events[:5]:
            home = event.get("home_team", "?")
            away = event.get("away_team", "?")

            message += f"🏟️ {home} - {away}\n"

            bookmakers = event.get("bookmakers", [])

            found = False

            for bookmaker in bookmakers:
                for market in bookmaker.get("markets", []):
                    if market.get("key") != "totals":
                        continue

                    for outcome in market.get("outcomes", []):
                        name = outcome.get("name")
                        point = outcome.get("point")
                        price = outcome.get("price")

                        message += (
                            f"  {name} {point} → {price}\n"
                        )

                        found = True

            if not found:
                message += "  Aucun Over/Under trouvé.\n"

            message += "\n"

    send_telegram(message)

    print("Message Telegram envoyé.")

except Exception as e:
    print("ERREUR :", e)

    try:
        send_telegram(
            f"❌ ERREUR DU BOT\n\n{e}"
        )
    except Exception:
        pass

    raise
