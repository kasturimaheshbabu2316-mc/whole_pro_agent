import os

from celery import Celery

broker_url = os.getenv("CELERY_BROKER_URL", "amqp://guest:guest@rabbitmq:5672//")
backend_url = os.getenv("CELERY_RESULT_BACKEND", "redis://redis:6379/0")

app = Celery("email_agent", broker=broker_url, backend=backend_url)
app.conf.task_routes = {
    "email_agent.tasks.sender.send_email_task": {"queue": "email_sender"}
}
app.conf.task_serializer = "json"
app.conf.result_serializer = "json"
app.conf.accept_content = ["json"]
app.conf.result_extended = True

# Import task modules so Celery can register them
import email_agent.tasks.sender  # noqa: F401
