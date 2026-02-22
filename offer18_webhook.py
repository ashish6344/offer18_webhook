@app.route("/offer18-webhook", methods=["GET", "POST"])
@app.route("/offer18-webhook/", methods=["GET", "POST"])
def handle_postback():
    # GET + POST दोनों पढ़ो
    args = request.args.to_dict()
    form = request.form.to_dict()

    # दोनों merge करो
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

    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    requests.post(url, data={
        "chat_id": TELEGRAM_CHANNEL,
        "text": message
    })

    return "OK", 200
