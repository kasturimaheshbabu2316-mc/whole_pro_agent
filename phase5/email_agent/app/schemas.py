from __future__ import annotations
from datetime import datetime
from typing import Any, Dict, Optional

from pydantic import BaseModel, EmailStr


class EmailSendRequest(BaseModel):
    recipient_email: EmailStr
    job_title: str
    company: str
    resume_id: int
    subject: Optional[str] = None
    template_name: Optional[str] = "job_application"
    personalization: Optional[Dict[str, Any]] = {}


class EmailStatusResponse(BaseModel):
    id: int
    recipient: EmailStr
    subject: str
    body: str
    status: str
    job_title: Optional[str]
    company: Optional[str]
    resume_id: Optional[int]
    template_name: Optional[str]
    personalization: Optional[Dict[str, Any]]
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


class TemplateListResponse(BaseModel):
    templates: list[str]
