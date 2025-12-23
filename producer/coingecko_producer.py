import requests
import time
import json
from datetime import datetime
from kafka import KafkaProducer

COINGECKO_URL = "https://api.coingecko.com/api/v3/simple/price"
ASSETS = ["bitcoin", "ethereum", "cardano", "solana", "dogecoin"]
CURRENCY = "usd"
POLL_INTERVAL = 10

producer = KafkaProducer(
    bootstrap_servers="localhost:9092",
    value_serializer=lambda v: json.dumps(v).encode("utf-8")
)

def fetch_prices():
    params = {
        "ids": ",".join(ASSETS),
        "vs_currencies": CURRENCY
    }
    response = requests.get(COINGECKO_URL, params=params, timeout=5)
    response.raise_for_status()
    return response.json()

def main():
    print("CoinGecko Producer → Kafka started")
    while True:
        try:
            data = fetch_prices()
            timestamp = datetime.utcnow().isoformat()

            for asset, price in data.items():
                event = {
                    "asset": asset,
                    "price_usd": price[CURRENCY],
                    "event_time": timestamp
                }
                producer.send("crypto_prices", value=event)
                print("Sent:", event)

            producer.flush()
        except Exception as e:
            print("ERROR:", e)

        time.sleep(POLL_INTERVAL)

if __name__ == "__main__":
    main()
