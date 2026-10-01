# ONLINE PLANT DISEASES - Deployment Guide (GitHub + Vercel)

AI-assisted plant disease detection portal: React/Vite frontend, FastAPI backend, MongoDB.

## Architecture (read this first)

Vercel hosts **static frontend only**. It cannot run the FastAPI server or MongoDB.
A working production setup therefore has three parts:

| Part | Where it runs | Why |
| --- | --- | --- |
| Frontend (React/Vite) | **Vercel** | Static build, free, global CDN |
| Backend (FastAPI) | **Render / Railway** | Needs a long-running Python process |
| Database (MongoDB) | **MongoDB Atlas** | Local MongoDB is not reachable from the internet |

Because the frontend and backend are on different domains, the browser makes
cross-origin calls. Two things must line up or every request fails:

- Frontend: `VITE_API_URL` = your backend URL + `/api`
- Backend: `CORS_ORIGINS` = your Vercel URL

## Environment variables

### Vercel (frontend) - Settings > Environment Variables

| Variable | Example value |
| --- | --- |
| `VITE_API_URL` | `https://plant-disease-api.onrender.com/api` |

Only that one variable is required. Any `VITE_*` value is embedded in the public
JavaScript bundle, so never put a secret here.

### Backend host (Render / Railway) - Environment Variables

| Variable | Example value |
| --- | --- |
| `SECRET_KEY` | long random string - **required**, rotate it |
| `MONGO_URI` | `mongodb+srv://user:pass@cluster.mongodb.net/?retryWrites=true&w=majority` |
| `MONGO_DB_NAME` | `greenroot_db` |
| `CORS_ORIGINS` | `https://your-app.vercel.app` |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | `1440` |
| `DEBUG` | `false` |
| `HOST` / `PORT` | `0.0.0.0` / leave `PORT` to the host |
| `UPLOAD_DIR` | path to a persistent disk, e.g. `/var/data/uploads` |
| `ADMIN_ACCOUNTS` | optional JSON array of extra admins |

Templates for every variable live in `backend/.env.example` and
`plant-care-portal/.env.example`. Generate a JWT secret with:

```bash
python -c "import secrets; print(secrets.token_urlsafe(64))"
```

### Backend start command

```
uvicorn app.main:app --host 0.0.0.0 --port $PORT
```

A `Procfile` in `backend/` already contains this line.

## Database setup (MongoDB Atlas)

1. Create a free Atlas account and a free **M0** cluster.
2. **Database Access** - create a user with a generated password.
3. **Network Access** - allow `0.0.0.0/0` (Render/Railway egress IPs are not static).
4. Copy the **SRV connection string** into the backend's `MONGO_URI`.
5. On first boot the app seeds the disease knowledge base automatically.

Rotating `SECRET_KEY` invalidates every issued token, so users must log in again.

## Uploads and storage

Uploaded leaf images are written to the `UPLOAD_DIR` folder on disk and served
from `/uploads`. Hosts such as Render and Railway use an **ephemeral**
filesystem, so images are deleted on every redeploy. For production either:

- attach a persistent disk and set `UPLOAD_DIR` to its mount path, or
- switch `app/services/image_service.py` to object storage (S3 / Cloudinary).

Note that `/uploads` is a static mount, so image URLs are readable by anyone
who has the link. Add access control before handling private user photos.

## Local development

```bash
# backend
cd backend
.venv\Scripts\activate
uvicorn app.main:app --reload

# frontend (second terminal)
cd plant-care-portal
npm install
npm run dev
```

`npm run dev` proxies `/api` to `http://127.0.0.1:8000`, so no `VITE_API_URL`
is needed locally. In a production build an unset `VITE_API_URL` falls back to
same-origin `/api`, never to `localhost`.

Tests: `cd backend && .venv\Scripts\python.exe auth_e2e_test.py` (46 checks).

## Automatic redeploys

The Vercel project is linked to the GitHub repository, so every `git push` to
the connected branch triggers a fresh build and deploy. No manual step needed.

```bash
git add -A
git commit -m "your change"
git push
```

Watch it in **Vercel dashboard > Deployments**. Only change
`VITE_API_URL` after the backend has its own public URL.

## Troubleshooting

| Symptom | Cause |
| --- | --- |
| Login returns a network/CORS error | `CORS_ORIGINS` missing the Vercel URL |
| Requests go to `localhost` | `VITE_API_URL` unset for that environment |
| `SECRET_KEY` warning on boot | Set a real random `SECRET_KEY` |
| Images vanish after a deploy | Ephemeral filesystem - use a persistent disk |