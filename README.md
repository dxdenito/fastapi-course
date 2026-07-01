# FastAPI Course

A structured FastAPI learning project, built step by step using Claude as a tutor.

## Tech Stack

- Python 3.14.6
- FastAPI
- Pydantic v2
- Uvicorn
- Ruff (linting + formatting)

## Setup

```bash
# Clone the repo
git clone https://github.com/dxdenito/fastapi-course.git
cd fastapi-course

# Create and activate virtual environment
python -m venv venv
venv\Scripts\activate  # Windows

# Install dependencies
pip install -r requirements.txt

# Run the development server
uvicorn app.main:app --reload
```

## API Docs

Once running, visit:
- Swagger UI → http://127.0.0.1:8000/docs
- ReDoc → http://127.0.0.1:8000/redoc

## Project Structure

```
fastapi-course/
├── app/
│   ├── main.py
│   ├── dependencies.py
│   ├── schemas/
│   │   ├── trade.py
│   │   ├── position.py
│   │   ├── product.py
│   │   └── backtest.py
│   └── routers/
│       ├── trades.py
│       ├── positions.py
│       ├── products.py
│       └── backtests.py
├── venv/
├── .gitignore
├── requirements.txt
├── ruff.toml
└── README.md
```

## Course Progress

| Module | Topic | Status |
|--------|-------|--------|
| Module 0 | Git & Project Setup | ✅ Complete |
| Module 1 | FastAPI Foundations | ✅ Complete |
| Module 2 | Pydantic v2 In Depth | ✅ Complete |
| Module 3 | Routing & Architecture | ✅ Complete |
| Module 4 | Database Integration | ⏳ Pending |
| Module 5 | Auth & Security | ⏳ Pending |
| Module 6 | Advanced Patterns | ⏳ Pending |
| Module 7 | Testing & DevOps | ⏳ Pending |

## Concepts Covered So Far

- ASGI vs WSGI, request lifecycle
- Path, query, and body parameters
- Pydantic v2 — `Field()`, `@field_validator`, `@model_validator`
- Nested models, response models, input/output schema separation
- Project structure — `routers/` and `schemas/` separation
- Dependency injection — function-based, router-level, chaining
- `HTTPException` and proper status code usage
- Conventional Commits, `.gitignore`, Ruff linting/formatting
