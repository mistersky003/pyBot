from celery import Celery
from celery.schedules import crontab

from app_init import session
from database_models import ChatMember
from database_models import Session

app = Celery(broker = "redis://localhost:6379/0")


@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(
        crontab(hour = 0, minute = 0),
        clear_all.s(),
    )
    sender.add_periodic_task(
        60 * 60,
        remove_sessions.s(),
    )


@app.task
def clear_all():
    my_session = session()
    my_session.query(ChatMember).update({"count_messages": 0})
    my_session.commit()


@app.task
def remove_sessions():
    my_session = session()
    my_session.query(Session).delete()
    my_session.commit()
