from flask import Flask, render_template
import requests
import json
import time
import os
import smtplib
from email.mime.text import MIMEText

app = Flask(__name__)

INSTAGRAM_USERS_FILE = "instagram_users.txt"
CHECKED_USERS_FILE = "checked_users.json"

EMAIL_ADDRESS = os.environ.get("Morganalonna@gmail.com")
EMAIL_PASSWORD = os.environ.get("#Sidekick3")
TARGET_EMAIL = os.environ.get("Morganalonna@gmail.com")

def load_users():
    with open(INSTAGRAM_USERS_FILE, "r") as f:
        return [line.strip() for line in f if line.strip()]

def load_checked_users():
    if os.path.exists(CHECKED_USERS_FILE):
        with open(CHECKED_USERS_FILE, "r") as f:
            return json.load(f)
    return {}

def save_checked_users(data):
    with open(CHECKED_USERS_FILE, "w") as f:
        json.dump(data, f)

def is_live(user):
    url = f"https://www.instagram.com/{user}/?__a=1&__d=dis"
    headers = {"User-Agent": "Mozilla/5.0"}
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200 and '"is_live":true' in response.text:
            return True
    except Exception:
        pass
    return False

def send_email(subject, body):
    if not EMAIL_ADDRESS or not EMAIL_PASSWORD:
        print("Missing email credentials.")
        return
    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = EMAIL_ADDRESS
    msg["To"] = TARGET_EMAIL
    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            server.send_message(msg)
    except Exception as e:
        print(f"Email failed: {e}")

@app.route("/")
def index():
    users = load_users()
    return render_template("index.html", users=users)

@app.route("/healthz")
def health_check():
    return "STAY-Watcher is healthy 🧡", 200

@app.route("/check")
def check_live_status():
    users = load_users()
    checked_users = load_checked_users()

    for user in users:
        currently_live = is_live(user)
        was_live = checked_users.get(user, False)

        if currently_live and not was_live:
            subject = f"{user} just went live!"
            body = f"Hey STAY, {user} just started an Instagram Live!"
            send_email(subject, body)
            checked_users[user] = True
        elif not currently_live:
            checked_users[user] = False

    save_checked_users(checked_users)
    return "Checked all users.", 200

if __name__ == "__main__":
    app.run(debug=True)
