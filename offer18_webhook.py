from flask import Flask, request
import requests
import os

app = Flask(__name__)

TELEGRAM_BOT_TOKEN = "7800645235:AAHMjePhblo2PYByKjFa3J5qvGbBfaMkdIo"
TELEGRAM_CHANNEL = "@conversionalert"

@app.route("/", methods=["GET"])
def root():
    return "Webhook service running", 200

@app.route("/offer18-webhook", methods=["GET"])
@app.route("/offer18-webhook/", methods=["GET"])
def handle_postback():
    args = request.args.to_dict()

    offer_id = args.get("offerid")
    sub_id = args.get("aff_sub1") or args.get("aff_click_id") or args.get("sub_aff_id")
    payout = args.get("payout")
    event = args.get("event_token")
    ip = args.get("ip")

    message = (
        f"🟢 New Conversion Recorded!\n\n"
        f"🎯 Offer ID: {offer_id}\n"
        f"👤 Sub ID: {sub_id}\n"
        f"💰 Payout: {payout}\n"
        f"⚙️ Event: {event}\n"
        f"🌐 IP: {ip}\n\n"
        f"⚡️ Powered by @conversionalert"
    )

    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    data = {
        "chat_id": TELEGRAM_CHANNEL,
        "text": message,
        "parse_mode": "Markdown"
    }

    try:
        r = requests.post(url, data=data, timeout=10)
        print("Telegram Response:", r.text)
    except Exception as e:
        print("Telegram Error:", e)

    return "OK", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
