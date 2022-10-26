from celery import Celery

from app_init import bot

app = Celery(broker = "redis://localhost:6379/2")


@app.task
def delete_message_task(chat_id, message_id):
    print(f"Delete message: {chat_id} {message_id}")
    try:
        bot.delete_message(chat_id, message_id)
    except:
        pass