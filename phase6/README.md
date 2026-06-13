# Phase 6 – Front-End / CLI

This phase includes the front-end for the Whole Agent project.

## Streamlit UI

A Streamlit-based UI has been added at `phase6/streamlit_app/`.

### Run

```bash
cd phase6/streamlit_app
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
streamlit run app.py
```

Default service endpoints are configured for local development with the following URLs:
- Auth: `http://localhost:8001`
- Resume Builder: `http://localhost:8002`
- Job Finder: `http://localhost:8003`
- Email Agent: `http://localhost:8005`
