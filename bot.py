import os
import requests

TOKEN = os.environ["BOT_TOKEN"]
CHAT_ID = os.environ["CHAT_ID"]

url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"

message = """🤖 TEST DU BOT

✅ Connexion Telegram réussie !
📡 Le système de surveillance des cotes est prêt à être configuré.
"""

response = requests.post(
    url,
    json={
        "chat_id": CHAT_ID,
        "text": message
    },
    timeout=10
)

print(response.json())
