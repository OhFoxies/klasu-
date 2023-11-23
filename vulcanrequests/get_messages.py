from typing import Any
from vulcan import Vulcan, Keystore, Account
import datetime as dt


async def get_new_messages(keystore, account, old=False):
    keystore_: Any = Keystore.load(keystore)
    account_: Any = Account.load(account)
    user: Vulcan = Vulcan(account=account_, keystore=keystore_)
    async with user:
        await user.select_student()
        boxes = await user.data.get_message_boxes()

        messages_list = []

        async for i in boxes:
            messages = await user.data.get_messages(i.global_key)
            async for message in messages:
                if old:
                    if message.sent_date.date_time >= dt.datetime(2023, 10, 1):
                        messages_list.append(message)

                elif message.sent_date.date_time >= dt.datetime.today() - dt.timedelta(days=1):
                    messages_list.append(message)
        return messages_list
