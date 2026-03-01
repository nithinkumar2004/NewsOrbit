# 🌍 NewsOrbit AI

Production-ready SaaS platform for country-based AI-curated news and CPC advertising.

## Stack
- **Backend:** FastAPI, MongoDB Atlas, Firebase Admin Auth verify, Gemini API, GNews API, APScheduler, JWT, SlowAPI rate limits.
- **Frontend:** HTML5, Bootstrap 5, Vanilla JS, Axios, Firebase Web SDK, dark mode, toast UX.

## Project Structure
```
newsorbit/
├── server/
└── client/
```

## Backend Setup
```bash
cd server
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp ../.env.example .env
uvicorn main:app --host 0.0.0.0 --port 10000 --reload
```

## Frontend Setup
Serve `client/` as static files (or Render Static Site). For local testing:
```bash
cd client
python -m http.server 5500
```

## Environment Variables
See `.env.example`.

## Render Deployment
### Backend (Render Web Service)
- Root Directory: `newsorbit/server`
- Build Command: `pip install -r requirements.txt`
- Start Command: `uvicorn main:app --host 0.0.0.0 --port 10000`
- Add env vars from `.env.example`

### Frontend (Render Static Site)
- Root Directory: `newsorbit/client`
- Build command: *(none)*
- Publish directory: `.`
- Set API base URL in browser local storage key `apiBase` to backend URL.

## Business Logic Included
- Firebase login (Google + phone OTP)
- JWT session issuance
- RBAC (`user`, `advertiser`, `admin`)
- AI article transformation + filtering by importance > 6
- News cron refresh every 30 minutes
- Ad insertion cadence (every 5 cards) + CPC stop on budget exhaustion
- Campaign analytics and advertiser revenue tracking

## Notes
- Add your Firebase Web config in `client/js/app.js`
- Provide Firebase service account JSON path in backend env.
