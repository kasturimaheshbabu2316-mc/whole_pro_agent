# Streamlit UI for Whole Agent

This Streamlit app provides a lightweight UI for the Whole Agent microservices:
- Auth Service
- Resume Builder Service
- Job Finder Service
- Email Agent Service

## Run locally

1. Install dependencies:

```bash
cd phase6/streamlit_app
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

2. Start the app:

```bash
streamlit run app.py
```

3. Open `http://localhost:8501` in your browser.

## Dockerized run

You can also run the Streamlit UI with Docker Compose from `phase1`:

```bash
cd phase1
docker compose up --build streamlit-ui
```

This builds the `phase6/streamlit_app` service and exposes Streamlit at `http://localhost:8501`.

## Configuration

The app uses the following default endpoints:
- Auth: `http://localhost:8001`
- Resume Builder: `http://localhost:8002`
- Job Finder: `http://localhost:8003`
- Email Agent: `http://localhost:8005`

To override defaults, create `.streamlit/secrets.toml` with:

```toml
AUTH_URL = "http://localhost:8001"
RESUME_URL = "http://localhost:8002"
JOB_URL = "http://localhost:8003"
EMAIL_URL = "http://localhost:8005"
```
