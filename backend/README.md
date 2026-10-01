# GreenRoot Backend

REST API for the **Online Plant Disease Detection Portal**.
Built with **FastAPI**, **Motor** (async MongoDB) and **JWT** authentication —
ready to connect to the React frontend in `../plant-care-portal`.

## Tech Stack

| Layer       | Technology                              |
| ----------- | --------------------------------------- |
| Language    | Python 3.12+                            |
| Framework   | FastAPI + Uvicorn                       |
| Database    | MongoDB (async driver: Motor)           |
| Validation  | Pydantic v2 / pydantic-settings         |
| Auth        | JWT (PyJWT) + bcrypt password hashing   |
| Uploads     | python-multipart + Pillow               |

## Project Structure

```
backend/
│── app/
│   ├── main.py            # app factory, lifespan, CORS, routers, static files
│   ├── config.py          # typed settings from environment variables
│   ├── database.py        # Motor client, Database wrapper, indexes
│   ├── seed.py            # starter disease knowledge base + optional admin
│   ├── models/            # Pydantic domain models (MongoDB documents)
│   ├── schemas/           # request/response DTOs
│   ├── routes/            # controllers (users, diseases, uploads, predictions, feedback)
│   ├── services/          # business logic layer
│   ├── middleware/        # request logging + global error handling
│   ├── auth/              # security helpers, auth service, auth router
│   ├── utils/             # hashing, JWT, logging, pagination, image validation
│   └── dependencies/      # FastAPI dependencies (db, auth, pagination)
│
├── uploads/               # uploaded leaf images (created at runtime)
├── requirements.txt
├── .env.example
└── README.md
```

## Setup

```bash
cd backend

# 1) Create a virtual environment
python -m venv .venv
.venv\Scripts\activate          # Windows
# source .venv/bin/activate    # Linux / macOS

# 2) Install dependencies
pip install -r requirements.txt

# 3) Configure environment
copy .env.example .env          # Windows
# cp .env.example .env         # Linux / macOS
#   - Edit .env: MONGO_URI, SECRET_KEY, ADMIN_* etc.

# 4) Make sure MongoDB is running locally (mongod), then start the API
uvicorn app.main:app --reload
```

The API will be available at <http://localhost:8000>.
Interactive docs: <http://localhost:8000/docs> (Swagger) and `/redoc`.

## Environment Variables

| Variable                 | Default                       | Description                        |
| ------------------------ | ----------------------------- | ---------------------------------- |
| `MONGO_URI`              | `mongodb://localhost:27017`   | MongoDB connection string          |
| `MONGO_DB_NAME`          | `greenroot_db`                | Database name                      |
| `SECRET_KEY`             | *(change me)*                 | JWT signing secret                 |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | `1440`                    | Token lifetime in minutes          |
| `CORS_ORIGINS`           | `http://localhost:5173,...`   | Allowed frontend origins           |
| `MAX_UPLOAD_SIZE_MB`     | `5`                           | Upload size limit                  |
| `ADMIN_USERNAME`/`ADMIN_EMAIL`/`ADMIN_PASSWORD` | *(empty)* | Creates an admin on first boot |

Generate a strong secret with:

```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

## Authentication

1. `POST /api/auth/register` to create an account.
2. `POST /api/auth/login` to get a token.
3. Send the token on protected routes:

```
Authorization: Bearer <access_token>
```

Roles: `user` (default) and `admin`. Admin endpoints manage the disease
knowledge base and view all feedback.

## API Endpoints

All endpoints are prefixed with `/api`.

### Auth
| Method | Endpoint           | Auth | Description                              |
| ------ | ------------------ | ---- | ---------------------------------------- |
| POST   | `/api/auth/register` | no  | Register a user                          |
| POST   | `/api/auth/login`  | no   | Login, returns `{access_token, user}`    |
| GET    | `/api/auth/me`     | yes  | Current user profile                     |

**Register**
```json
// POST /api/auth/register
{
  "username": "priya",
  "email": "priya@example.com",
  "password": "Garden123",
  "full_name": "Priya Garden"
}
```
```json
// 201 Created
{
  "id": "64c9...", "username": "priya", "email": "priya@example.com",
  "full_name": "Priya Garden", "role": "user", "is_active": true,
  "created_at": "2026-08-05T10:00:00"
}
```

**Login**
```json
// POST /api/auth/login
{ "identifier": "priya", "password": "Garden123" }
```
```json
// 200 OK
{
  "access_token": "eyJhbGciOiJIUzI1NiIs...",
  "token_type": "bearer",
  "expires_in": 86400,
  "user": { "id": "64c9...", "username": "priya", "role": "user", ... }
}
```

### Users
| Method | Endpoint     | Auth | Description               |
| ------ | ------------ | ---- | ------------------------- |
| GET    | `/api/users/me`  | yes | Profile                  |
| PATCH  | `/api/users/me`  | yes | Update profile           |
| DELETE | `/api/users/me`  | yes | Delete account           |

### Diseases
| Method | Endpoint               | Auth | Description                       |
| ------ | ---------------------- | ---- | --------------------------------- |
| GET    | `/api/diseases`        | no   | Search + paginate                 |
| GET    | `/api/diseases/categories` | no | Distinct categories            |
| GET    | `/api/diseases/{id}`   | no   | Get one disease                   |
| POST   | `/api/diseases`        | admin | Create disease                   |
| PATCH  | `/api/diseases/{id}`   | admin | Update disease                    |
| DELETE | `/api/diseases/{id}`   | admin | Delete disease                    |

**Search**
```
GET /api/diseases?q=blight&category=Fungal&page=1&page_size=10
```
```json
// 200 OK
{
  "items": [
    { "id": "64c9...", "name": "Early Blight", "category": "Fungal",
      "severity": "High", "symptoms": ["dark spots", "target rings"],
      "treatment": ["Copper fungicide", "Stake plants"], ... }
  ],
  "total": 1, "page": 1, "page_size": 10, "pages": 1
}
```

### Uploads
| Method | Endpoint        | Auth | Description                    |
| ------ | --------------- | ---- | ------------------------------ |
| POST   | `/api/uploads`  | yes  | Upload image (multipart/form-data, field `file`) |
| GET    | `/api/uploads/{id}` | yes | Upload metadata             |

```
POST /api/uploads  (multipart/form-data: file=<leaf.jpg>)
```
```json
// 201 Created
{
  "image_id": "64ca...", "filename": "a1b2c3d4.jpg",
  "content_type": "image/jpeg", "size_bytes": 245000,
  "url": "/uploads/<user_id>/a1b2c3d4.jpg",
  "sha256": "9f86d0...", "width": 1200, "height": 900,
  "uploaded_at": "2026-08-05T10:05:00"
}
```

### Predictions
| Method | Endpoint             | Auth | Description                      |
| ------ | -------------------- | ---- | -------------------------------- |
| POST   | `/api/predictions`   | yes  | Run disease detection            |
| GET    | `/api/predictions`   | yes  | Prediction history (paginated)   |
| GET    | `/api/predictions/{id}` | yes | Get one prediction             |

**Run detection**
```json
// POST /api/predictions
{
  "image_id": "64ca...",
  "symptoms": ["brown spots", "yellowing"]
}
```
```json
// 201 Created
{
  "id": "64cb...",
  "disease_id": "64c9...",
  "disease_name": "Early Blight",
  "confidence": 0.59,
  "status": "completed",
  "model_version": "rule-demo-v1",
  "symptoms": ["brown spots", "yellowing"],
  "image_id": "64ca...",
  "predicted_at": "2026-08-05T10:10:00",
  "disease": { "id": "64c9...", "name": "Early Blight", "treatment": [...], ... }
}
```

> The prediction pipeline currently uses a transparent rule-based matcher.
> To plug in a real ML model, replace `PredictionService.predict` in
> `app/services/prediction_service.py`.

### Feedback
| Method | Endpoint              | Auth | Description                |
| ------ | --------------------- | ---- | -------------------------- |
| POST   | `/api/feedback`       | yes  | Submit rating (1–5) + message |
| GET    | `/api/feedback/average` | no  | Overall average rating     |
| GET    | `/api/feedback`       | admin | List all feedback         |

```json
// POST /api/feedback
{ "rating": 5, "message": "Love the detection tool!", "prediction_id": "64cb..." }
```

## Error Handling

All errors return a consistent JSON body:

```json
{ "detail": "Human readable message" }
```

Validation failures return 422 with a field list:
```json
{
  "detail": "Validation error",
  "errors": [ { "field": "password", "message": "String should have at least 8 characters" } ]
}
```

Common status codes: `401` (unauthorized), `403` (forbidden/disabled),
`404` (not found), `409` (duplicate), `413` (file too large),
`415` (bad file type), `422` (validation), `500` (server error).

## Connecting to the React Frontend

The frontend is configured with the Vite proxy so API calls go to
`/api/*` and are forwarded to `http://localhost:8000`. CORS already allows
`http://localhost:5173`.

1. Start MongoDB.
2. Run the backend: `uvicorn app.main:app --reload`
3. Run the frontend: `npm run dev` (from `../plant-care-portal`)

## License

For demonstration / education. Replace the demo prediction service with a real
ML model for production use.
