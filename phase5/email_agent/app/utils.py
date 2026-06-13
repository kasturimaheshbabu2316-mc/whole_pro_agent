import logging
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from jinja2 import Template

logger = logging.getLogger(__name__)


def get_default_templates() -> dict[str, str]:
    return {
        "job_application": (
            "Dear Hiring Team,\n\n"
            "I am writing to express my interest in the {{ job_title }} role at {{ company }}. "
            "My recent resume (ID: {{ resume_id }}) demonstrates experience that maps closely to this position. "
            "I would love to discuss how I can contribute to your team.\n\n"
            "Best regards,\n"
            "Your Name"
        ),
        "follow_up": (
            "Hi {{ company }} hiring team,\n\n"
            "I recently applied for the {{ job_title }} role and wanted to follow up on my application. "
            "My resume (ID: {{ resume_id }}) highlights relevant experience and a strong fit for your team.\n\n"
            "Thank you for your time,\n"
            "Your Name"
        ),
    }


def render_email_body(template_name: str, context: dict) -> str:
    template_text = get_default_templates().get(template_name)
    if template_text is None:
        template_text = get_default_templates()["job_application"]

    template = Template(template_text)
    return template.render(**context)


def send_email(recipient: str, subject: str, body: str) -> bool:
    smtp_host = os.getenv("SMTP_HOST", "")
    smtp_port = int(os.getenv("SMTP_PORT", 587))
    smtp_username = os.getenv("SMTP_USERNAME", "")
    smtp_password = os.getenv("SMTP_PASSWORD", "")

    if not smtp_host:
        logger.info("SMTP not configured; dry run email to %s", recipient)
        logger.info("Subject: %s", subject)
        logger.info("Body:\n%s", body)
        return True

    message = MIMEMultipart()
    message["From"] = smtp_username or "no-reply@example.com"
    message["To"] = recipient
    message["Subject"] = subject
    message.attach(MIMEText(body, "plain"))

    try:
        with smtplib.SMTP(smtp_host, smtp_port, timeout=30) as smtp:
            smtp.starttls()
            if smtp_username and smtp_password:
                smtp.login(smtp_username, smtp_password)
            smtp.send_message(message)
        logger.info("Email delivered to %s", recipient)
        return True
    except Exception as exc:
        logger.exception("Failed to send email to %s: %s", recipient, exc)
        return False
