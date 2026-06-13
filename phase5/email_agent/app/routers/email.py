from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..database import get_db
from ..models import EmailMessage
from ..schemas import EmailSendRequest, EmailStatusResponse, TemplateListResponse
from ..tasks.sender import send_email_task
from ..utils import render_email_body

router = APIRouter()


@router.post("/send", response_model=EmailStatusResponse)
def send_email(request: EmailSendRequest, db: Session = Depends(get_db)):
    subject = request.subject or f"Application for {request.job_title} at {request.company}"
    body = render_email_body(
        request.template_name,
        {
            "job_title": request.job_title,
            "company": request.company,
            "resume_id": request.resume_id,
            **(request.personalization or {}),
        },
    )

    message = EmailMessage(
        recipient=request.recipient_email,
        subject=subject,
        body=body,
        status="queued",
        job_title=request.job_title,
        company=request.company,
        resume_id=request.resume_id,
        template_name=request.template_name,
        personalization=request.personalization,
    )
    db.add(message)
    db.commit()
    db.refresh(message)

    send_email_task.delay(message.id)

    return message


@router.get("/{message_id}", response_model=EmailStatusResponse)
def get_email_status(message_id: int, db: Session = Depends(get_db)):
    message = db.get(EmailMessage, message_id)
    if not message:
        raise HTTPException(status_code=404, detail="Email message not found")
    return message


@router.get("/templates", response_model=TemplateListResponse)
def list_templates():
    from ..utils import get_default_templates

    return TemplateListResponse(templates=list(get_default_templates().keys()))
