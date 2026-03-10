from flask import Flask, request, jsonify, redirect, url_for
from datetime import datetime
import os

app = Flask(__name__)

otp_table = []  # Stores OTPs

# Word → Number mapping
word_map = {
    "zero":"0",
    "one":"1",
    "two":"2",
    "three":"3",
    "four":"4",
    "five":"5",
    "six":"6",
    "seven":"7",
    "eight":"8",
    "nine":"9"
}

def convert_otp(text):
    parts = text.lower().split("-")
    digits = ""
    for p in parts:
        if p in word_map:
            digits += word_map[p]
    return digits

# Receive OTP via API
@app.route("/receive", methods=["POST"])
def receive():
    data = request.json
    mobile = data.get("mobile")         # Your profile number
    otp_word = data.get("otp")          # OTP word
    source_number = data.get("from")    # Source number
    message_text = data.get("text","")  # Full SMS text (optional)

    # Filter: only accept messages starting with "IVACBD"
    if not message_text.upper().startswith("IVACBD"):
        return {"status":"ignored"}  # Ignore other messages

    otp_number = convert_otp(otp_word)

    otp_table.append({
        "mobile": mobile,
        "source_number": source_number,
        "otp_word": otp_word,
        "otp_number": otp_number,
        "time": datetime.now().strftime("%H:%M:%S")
    })
    return {"status":"ok"}

# Clear all OTPs
@app.route("/clear_all", methods=["GET"])
def clear_all():
    otp_table.clear()
    return redirect(url_for("home"))

# Clear OTPs of a specific profile (mobile)
@app.route("/clear/<mobile>", methods=["GET"])
def clear_profile(mobile):
    global otp_table
    otp_table = [row for row in otp_table if row["mobile"] != mobile]
    return redirect(url_for("home"))

# Display OTP table
@app.route("/")
def home():
    html = """
    <h2>IVAC OTP Monitor</h2>
    <a href="/clear_all" style="padding:5px 10px; background:red; color:white; text-decoration:none; border-radius:4px;">Clear All OTPs</a>
    <br><br>
    <table border='1' cellpadding='5'>
    <tr>
        <th>Profile Mobile</th>
        <th>Source Number</th>
        <th>OTP Word</th>
        <th>OTP Number</th>
        <th>Time</th>
        <th>Action</th>
    </tr>
    """
    for row in otp_table:
        html += f"""
        <tr>
            <td>{row['mobile']}</td>
            <td>{row['source_number']}</td>
            <td>{row['otp_word']}</td>
            <td>{row['otp_number']}</td>
            <td>{row['time']}</td>
            <td><a href="/clear/{row['mobile']}" style="color:red;">Clear Profile</a></td>
        </tr>
        """
    html += "</table>"
    return html

# Use Render PORT
port = int(os.environ.get("PORT", 10000))
app.run(host="0.0.0.0", port=port)
