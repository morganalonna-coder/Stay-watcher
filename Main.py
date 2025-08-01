from flask import Flask, render_template
import json
import os

app = Flask(__name__)

@app.route("/")
def index():
    with open("instagram_users.txt", "r") as f:
        users = [line.strip() for line in f if line.strip()]
    with open("checked_users.json", "r") as f:
        statuses = json.load(f)
    return render_template("index.html", users=users, statuses=statuses)

@app.route("/healthz")
def health_check():
    return "OK", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 3000)))
