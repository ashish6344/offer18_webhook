from flask import Flask, request
import requests

app = Flask(__name__)

# === TELEGRAM SETTINGS ===
TELEGRAM_BOT_TOKEN = "7800645235:AAHMjePhblo2PYByKjFa3J5qvGbBfaMkdIo"
TELEGRAM_CHANNEL = "@conversionalert"


@app.route("/", methods=["GET"])
def home():
    return "Webhook service running", 200


@app.route("/offer18-webhook", methods=["GET", "POST"])
@app.route("/offer18-webhook/", methods=["GET", "POST"])
def handle_postback():
    try:
        # GET + POST दोनों data capture करो
        args = request.args.to_dict()
        form = request.form.to_dict()

        # Merge both
        data = {**args, **form}

        print("Incoming Data:", data)

        offer_id = data.get("offerid")
        sub_id = data.get("aff_sub1") or data.get("aff_click_id")
        payout = data.get("payout")
        event = data.get("event_token")
        ip = data.get("ip")

        message = f"""🟢 New Conversion Recorded!

🎯 Offer ID: {offer_id}
👤 Sub ID: {sub_id}
💰 Payout: {payout}
⚙️ Event: {event}
🌐 IP: {ip}

⚡️ Powered by @conversionalert
"""

        telegram_url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"

        requests.post(
            telegram_url,
            data={
                "chat_id": TELEGRAM_CHANNEL,
                "text": message
            },
            timeout=10
        )

        return "OK", 200

    except Exception as e:
        print("ERROR:", str(e))
        return "ERROR", 500
