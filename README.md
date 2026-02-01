🚀 GitHub Webhook Activity Tracker

This project is a backend + frontend system that listens to GitHub Webhooks, stores relevant activity in MongoDB, and displays a real-time GitHub Activity Feed using React.

It is built as part of the TechStax assignment.

📌 Features

Receives GitHub webhook events

Supports:

PUSH

PULL REQUEST

MERGE (bonus feature)

Stores events in MongoDB (UTC time)

Exposes /events API for frontend

Converts timestamps from UTC → IST

Prevents duplicate / stale data using a rolling time window

Clean, responsive React UI

🏗️ Project Structure
webhook-repo/
├── app.py                 # Flask backend
├── frontend/              # React frontend
│   ├── src/
│   ├── public/
│   └── package.json
├── trigger.txt            # Dummy file to trigger webhook
├── README.md
├── .gitignore
└── venv/                  # Python virtual environment (ignored)

🔧 Tech Stack
Backend

Python

Flask

MongoDB (local)

PyMongo

Flask-CORS

Frontend

React

Fetch API

CSS (custom UI)

Tools

GitHub Webhooks

Ngrok (local webhook tunneling)

MongoDB Compass

🔁 How Webhooks Work

GitHub sends events to /webhook

Backend processes the event

Event is normalized and stored in MongoDB

/events API returns recent events

React UI polls /events every few seconds

📡 Supported Events
1️⃣ Push Event

Triggered when code is pushed to a branch.

Stored as:

PUSH → author pushed to branch

2️⃣ Pull Request Event

Triggered when a PR is opened or updated.

Stored as:

PULL_REQUEST → author opened PR

⭐ 3️⃣ Merge Event (Bonus)

GitHub does not send a separate merge event.

Merge is detected when:

event_type = pull_request

action = closed

merged = true

Stored as:

MERGE → author merged branch into main

⏰ Time Handling (IMPORTANT)

All timestamps are stored in UTC in MongoDB

API converts time to IST (UTC + 5:30) before sending to UI

UI always displays IST time

🧠 Rule-2 Handling (No Duplicate / Stale Data)

To avoid showing already displayed data:

/events API returns only events from the last 60 seconds

Older events remain in DB but are not sent to UI

This ensures:

No duplicate rendering

No stale data on refresh

🗄️ MongoDB Schema (events collection)
{
  "_id": "ObjectId",
  "request_id": "string",
  "author": "string",
  "action": "PUSH | PULL_REQUEST | MERGE",
  "from_branch": "string",
  "to_branch": "string",
  "timestamp": "UTC datetime"
}

▶️ How to Run Locally
Backend
cd webhook-repo
python app.py


Backend runs on:

http://localhost:5000

Frontend
cd frontend
npm install
npm start


Frontend runs on:

http://localhost:3000

🔗 GitHub Repositories (Submission)

Action Repo (dummy pushes)
https://github.com/Om-2611/action-repo

Webhook Repo (backend + UI)
https://github.com/Om-2611/webhook-repo
