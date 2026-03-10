from flask import Flask, request, jsonify
import re
import os

app = Flask(__name__)

otp_store = {}

@app.route("/")
def home():
    return "OTP Server Running"

@app.route("/sms", methods=["POST"])
def receive_sms():
    data = request.json
    message = data.get("sms","")
    profile = data.get("number","default")

    otp = re.findall(r'\d{4,6}', message)
    if otp:
        otp_store[profile] = otp[0]

    return {"status":"ok"}

@app.route("/otp/<profile>")
def get_otp(profile):
    return jsonify({"otp": otp_store.get(profile,"")})

if __name__ == "__main__":
    port = int(os.environ.get("PORT",10000))
    app.run(host="0.0.0.0", port=port)
