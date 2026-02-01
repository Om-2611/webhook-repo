# ================================
# Imports
# ================================
from flask import Flask, request, jsonify
from pymongo import MongoClient
from datetime import datetime, timezone, timedelta
from flask_cors import CORS


# ================================
# App Initialization
# ================================
app = Flask(__name__)
CORS(app)  # Allows frontend (React) to access backend APIs


# ================================
# MongoDB Configuration (Local)
# ================================
# Connect to local MongoDB running on port 27017
client = MongoClient("mongodb://localhost:27017/")

# Database name: techstax
db = client["techstax"]

# Collection name: events
collection = db["events"]


# ================================
# Health Check Route
# ================================
@app.route("/")
def home():
    """
    Simple health check route to verify
    that Flask server is running.
    """
    return "Webhook server is running"


# ================================
# GitHub Webhook Receiver
# ================================
@app.route("/webhook", methods=["POST"])
def webhook():
    """
    Receives GitHub webhook events.
    Handles:
    - PUSH events
    - PULL REQUEST events
    Stores required data into MongoDB.
    """

    payload = request.json
    event_type = request.headers.get("X-GitHub-Event")

    data = None

    # ----------------
    # PUSH EVENT
    # ----------------
    if event_type == "push":
        data = {
            # Commit hash is used as request_id
            "request_id": payload.get("after"),

            # Name of the GitHub user who pushed
            "author": payload["pusher"]["name"],

            # Action type
            "action": "PUSH",

            # Branch name
            "from_branch": payload["ref"].split("/")[-1],
            "to_branch": payload["ref"].split("/")[-1],

            # Always store timestamp in UTC in DB
            "timestamp": datetime.utcnow()
        }

    # ----------------
    # PULL REQUEST EVENT
    # ----------------
    elif event_type == "pull_request":
        pr = payload["pull_request"]

        data = {
            # PR ID as request_id
            "request_id": str(pr["id"]),

            # GitHub username
            "author": pr["user"]["login"],

            # Action type
            "action": "PULL_REQUEST",

            # Source and target branches
            "from_branch": pr["head"]["ref"],
            "to_branch": pr["base"]["ref"],

            # UTC timestamp
            "timestamp": datetime.utcnow()
        }

    # ----------------
    # IGNORE OTHER EVENTS
    # ----------------
    else:
        return jsonify({"status": "ignored"}), 200

    # ----------------
    # Save to MongoDB
    # ----------------
    collection.insert_one(data)
    print("Saved to MongoDB:", data)

    return jsonify({"status": "stored"}), 200


# ================================
# Events API (Used by UI)
# ================================
@app.route("/events", methods=["GET"])
def get_events():
    """
    Returns latest GitHub events for UI.
    - Sorted by timestamp (latest first)
    - Converts UTC time to IST
    - Sends clean, readable data
    """

    events = []

    # Fetch latest 10 events from MongoDB
    from datetime import datetime, timedelta

    cutoff_time = datetime.utcnow() - timedelta(seconds=60)

    cursor = collection.find(
    {"timestamp": {"$gte": cutoff_time}}
    ).sort("timestamp", -1)


    for doc in cursor:
        # Convert UTC → IST (UTC + 5:30)
        ist_time = doc["timestamp"].replace(
            tzinfo=timezone.utc
        ) + timedelta(hours=5, minutes=30)

        events.append({
            "id": str(doc["_id"]),
            "author": doc["author"],
            "action": doc["action"],
            "from_branch": doc["from_branch"],
            "to_branch": doc["to_branch"],

            # Human-readable IST timestamp
            "timestamp": ist_time.strftime("%d %b %Y - %I:%M %p IST")
        })

    return jsonify(events), 200


# ================================
# Run Flask Server
# ================================
if __name__ == "__main__":
    app.run(port=5000)
