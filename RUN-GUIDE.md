# ONLINE PLANT DISEASES — How to Run (Frontend + Backend)

This file contains the commands to set up and run the **backend (FastAPI)** and the
**frontend (React + Vite)** of the ONLINE PLANT DISEASES portal, including the
authentication system and the admin dashboard.

---

## Authentication at a glance

| Area | Where |
| --- | --- |
| Sign-in page | `http://localhost:5173/#/login` |
| Sign-up page | `http://localhost:5173/#/register` |
| User dashboard | `http://localhost:5173/#/dashboard` |
| Admin dashboard | `http://localhost:5173/#/admin` |
| API docs | `http://localhost:8000/docs` |

**Admin accounts** (development credentials — rotate before deploying) live in
`backend/.env` under `ADMIN_ACCOUNTS`. They are bcrypt-hashed before being written
to MongoDB, are never sent to the browser, and are never displayed on the site.

To create, reset or remove an admin without editing any file:

```cmd
cd backend
python -m scripts.create_admin --username darshit --email darshit@example.com
python -m scripts.create_admin --username darshit --reset-password
```

Run the automated auth test suite (46 checks) with:

```cmd
cd backend
.venv\Scripts\python.exe auth_e2e_test.py
```

---

## 1. Prerequisites

Install these before starting:

| Tool         | Version | Check command     |
| ------------ | ------- | ----------------- |
| Python       | 3.12+   | `python --version` |
| Node.js      | 18+     | `node --version`   |
| MongoDB      | 7+      | `mongod --version` |

> **Windows note:** If PowerShell blocks `npm`, use `npm.cmd` instead of `npm`.

---

## 2. Backend (FastAPI)

Open a terminal inside the `backend` folder.

### Step 1 — Create the virtual environment

```powershell
cd backend
python -m venv .venv
```

### Step 2 — Activate it

Windows (PowerShell):

```powershell
.venv\Scripts\activate
```

Windows (Command Prompt):

```cmd
.venv\Scripts\activate.bat
```

macOS / Linux:

```bash
source .venv/bin/activate
```

### Step 3 — Install dependencies

```powershell
pip install -r requirements.txt
```

### Step 4 — Configure environment variables

```powershell
copy .env.example .env
```

Then open `.env` and update:

- `SECRET_KEY` — generate one with:

  ```powershell
  python -c "import secrets; print(secrets.token_hex(32))"
  ```

- `MONGO_URI` / `MONGO_DB_NAME` — if your MongoDB is not on the default local port.

### Step 5 — Start MongoDB

Make sure MongoDB is running first:

```powershell
mongod
```

(or start the `MongoDB` Windows service if it is installed as one.)

### Step 6 — Run the backend

```powershell
uvicorn app.main:app --reload
```

The API will be available at:

- API base: `http://localhost:8000`
- Swagger docs: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`
- Health check: `http://localhost:8000/health`

> Seed data (the disease library plus any admins listed in `ADMIN_ACCOUNTS`) is
> created automatically on first boot. Accounts that already exist are left
> untouched, so changing a password in `.env` alone will not rotate it — use
> `scripts/create_admin.py` for that.

---

## 3. Frontend (React + Vite)

Open a **second** terminal inside the `plant-care-portal` folder.

### Step 1 — Install dependencies

```powershell
cd plant-care-portal
npm install
```

### Step 2 — Configure the API URL (optional)

The default `.env` already points to the backend:

```
VITE_API_URL=http://localhost:8000/api
```

No change is needed if the backend runs on port `8000`.

### Step 3 — Run the frontend

```powershell
npm run dev
```

The portal will open at: `http://localhost:5173`

---

## 4. Quick Reference

| Task                      | Command                                    | Where               |
| ------------------------- | ------------------------------------------ | ------------------- |
| Run backend               | `uvicorn app.main:app --reload`            | `backend/`          |
| Run frontend              | `npm run dev`                              | `plant-care-portal/` |
| Install backend deps      | `pip install -r requirements.txt`          | `backend/`          |
| Install frontend deps     | `npm install`                              | `plant-care-portal/` |
| Build frontend            | `npm run build`                            | `plant-care-portal/` |
| Preview production build  | `npm run preview`                          | `plant-care-portal/` |

### One-time setup (first run only)

```powershell
# Backend
cd backend
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env

# Frontend
cd ..\plant-care-portal
npm install
```

### Every run

```powershell
# Terminal 1 — backend
cd backend
.venv\Scripts\activate
uvicorn app.main:app --reload

# Terminal 2 — frontend
cd plant-care-portal
npm run dev
```

---

## 5. Troubleshooting

| Problem                              | Fix                                                                 |
| ------------------------------------ | ------------------------------------------------------------------- |
| `ModuleNotFoundError`                | Make sure the virtual env is active and deps are installed.         |
| Backend won't start / DB errors      | Verify MongoDB is running (`mongod`).                               |
| `npm` is not recognized              | Use `npm.cmd install` on Windows PowerShell.                        |
| Port 8000 or 5173 already in use     | Change `PORT` in `backend/.env` / use `npm run dev -- --port 5174`. |
| Frontend shows "offline mode"        | Backend is not running — start it on `http://localhost:8000`.       |
