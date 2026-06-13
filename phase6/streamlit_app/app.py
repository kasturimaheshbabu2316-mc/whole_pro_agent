import os
import json

import requests
import streamlit as st


def get_service_url(name: str, default: str) -> str:
    return st.secrets.get(name, os.getenv(name, default))


AUTH_URL = get_service_url("AUTH_URL", "http://localhost:8001")
RESUME_URL = get_service_url("RESUME_URL", "http://localhost:8002")
JOB_URL = get_service_url("JOB_URL", "http://localhost:8003")
EMAIL_URL = get_service_url("EMAIL_URL", "http://localhost:8005")


def post_json(url: str, payload: dict, token: str | None = None):
    headers = {"Content-Type": "application/json"}
    if token:
        headers["Authorization"] = f"Bearer {token}"
    return requests.post(url, headers=headers, json=payload, timeout=10)


def get_json(url: str, params: dict | None = None, token: str | None = None):
    headers = {}
    if token:
        headers["Authorization"] = f"Bearer {token}"
    return requests.get(url, headers=headers, params=params, timeout=10)


def show_status_box(title: str, url: str):
    try:
        response = requests.get(url, timeout=5)
        if response.ok:
            st.success(f"{title} is reachable")
            st.json({"status_code": response.status_code, "body": response.text})
        else:
            st.error(f"{title} returned {response.status_code}")
            st.text(response.text)
    except Exception as exc:
        st.error(f"Unable to reach {title}: {exc}")


def login_panel():
    st.header("Login")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        payload = {"username": email, "password": password}
        try:
            response = post_json(f"{AUTH_URL}/login", payload)
            if response.ok:
                data = response.json()
                st.session_state["auth_token"] = data.get("access_token")
                st.success("Logged in successfully")
            else:
                st.error(f"Login failed: {response.status_code}")
                st.write(response.text)
        except Exception as exc:
            st.error(f"Login error: {exc}")

    if st.session_state.get("auth_token"):
        st.write("### Auth token stored")
        st.code(st.session_state["auth_token"])


def resume_builder_panel():
    st.header("Resume Builder")
    name = st.text_input("Name")
    title = st.text_input("Job Title")
    summary = st.text_area("Summary")
    skills = st.text_area("Skills (comma-separated)")
    experience = st.text_area("Experience")

    if st.button("Generate Resume"):
        payload = {
            "name": name,
            "title": title,
            "summary": summary,
            "skills": [skill.strip() for skill in skills.split(",") if skill.strip()],
            "experience": experience,
        }
        try:
            response = post_json(f"{RESUME_URL}/resume", payload, st.session_state.get("auth_token"))
            if response.ok:
                data = response.json()
                st.success("Resume generated")
                st.json(data)
                st.session_state["resume_id"] = data.get("id") or data.get("resume_id")
            else:
                st.error(f"Resume creation failed: {response.status_code}")
                st.text(response.text)
        except Exception as exc:
            st.error(f"Error creating resume: {exc}")

    if st.session_state.get("resume_id"):
        st.info(f"Current resume ID: {st.session_state['resume_id']}")


def job_search_panel():
    st.header("Job Search")
    resume_id = st.text_input("Resume ID", value=str(st.session_state.get("resume_id", "")))
    query = st.text_input("Search query", value="python")

    if st.button("Search Jobs"):
        params = {"resume_id": resume_id, "q": query}
        try:
            response = get_json(f"{JOB_URL}/search", params, st.session_state.get("auth_token"))
            if response.ok:
                data = response.json()
                st.success("Search completed")
                st.json(data)
            else:
                st.error(f"Job search failed: {response.status_code}")
                st.text(response.text)
        except Exception as exc:
            st.error(f"Error searching jobs: {exc}")


def email_outreach_panel():
    st.header("Email Outreach")
    recipient = st.text_input("Recipient email")
    job_title = st.text_input("Job title")
    company = st.text_input("Company")
    resume_id = st.text_input("Resume ID", value=str(st.session_state.get("resume_id", "")))
    custom_subject = st.text_input("Custom subject (optional)")
    template = st.selectbox("Template", ["job_application", "follow_up"])
    message = st.text_area("Personalization JSON", value=json.dumps({"first_name": "Hiring Team"}, indent=2))

    if st.button("Send Email"):
        try:
            personalization = json.loads(message)
        except json.JSONDecodeError as exc:
            st.error(f"Invalid personalization JSON: {exc}")
            return

        payload = {
            "recipient_email": recipient,
            "job_title": job_title,
            "company": company,
            "resume_id": int(resume_id) if resume_id.isdigit() else resume_id,
            "subject": custom_subject or None,
            "template_name": template,
            "personalization": personalization,
        }
        try:
            response = post_json(f"{EMAIL_URL}/email/send", payload, st.session_state.get("auth_token"))
            if response.ok:
                st.success("Email queued successfully")
                st.json(response.json())
            else:
                st.error(f"Email send failed: {response.status_code}")
                st.text(response.text)
        except Exception as exc:
            st.error(f"Error sending email: {exc}")


def status_panel():
    st.header("Service Status")
    st.write("This panel checks endpoint reachability for each service.")
    show_status_box("Auth Service", f"{AUTH_URL}/health")
    show_status_box("Resume Builder", f"{RESUME_URL}/health")
    show_status_box("Job Finder", f"{JOB_URL}/health")
    show_status_box("Email Agent", f"{EMAIL_URL}/health")


def main():
    st.set_page_config(page_title="Whole Agent Streamlit UI", layout="wide")
    st.title("Whole Agent Streamlit UI")

    page = st.sidebar.radio("Navigate", ["Status", "Login", "Resume Builder", "Job Search", "Email Outreach"])

    if page == "Status":
        status_panel()
    elif page == "Login":
        login_panel()
    elif page == "Resume Builder":
        resume_builder_panel()
    elif page == "Job Search":
        job_search_panel()
    elif page == "Email Outreach":
        email_outreach_panel()


if __name__ == "__main__":
    main()
