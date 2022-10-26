from database_interfaces import WelcomeMessagesInterface
from database_models import WelcomeMessage
from app_init import session

for i in range(150):
    WelcomeMessagesInterface.add(-1, i)

messages = WelcomeMessagesInterface.get_messages_without_last(-1)
for message in messages:
    if message == 149:
        print("Error")

sess = session()
sess.query(WelcomeMessage).filter(WelcomeMessage.group_id == -1).delete()
sess.commit()