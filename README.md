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
