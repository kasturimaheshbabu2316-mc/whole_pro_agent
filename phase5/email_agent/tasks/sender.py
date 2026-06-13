import os
from celery.utils.log import get_task_logger
from sqlalchemy.orm import Session

from email_agent.app.celery_worker import app
from email_agent.app.database import SessionLocal
from email_agent.app.models import EmailMessage
from email_agent.app.utils import send_email

logger = get_task_logger(__name__)


@app.task(name="email_agent.tasks.sender.send_email_task")
def send_email_task(message_id: int):
    db: Session = SessionLocal()
    message = None
    try:
        message = db.get(EmailMessage, message_id)
        if message is None:
            logger.error("Email message %s not found", message_id)
            return {"status": "not_found"}

        message.status = "sending"
        db.commit()
        db.refresh(message)

        success = send_email(message.recipient, message.subject, message.body)
        message.status = "sent" if success else "failed"
        db.commit()
        db.refresh(message)

        return {"status": message.status, "message_id": message.id}
    except Exception as exc:
        logger.exception("Failed to process email send task %s", message_id)
        if message is not None:
            message.status = "failed"
            db.commit()
        raise exc
    finally:
        db.close()
