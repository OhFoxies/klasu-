import datetime as dt
import json
from typing import Any, List, Optional

import vulcan.data
from vulcan import Vulcan, Keystore, Account


class GetMessages:
    def __init__(self, keystore, account):
        self.keywords = self.get_keywords()
        self.keystore = keystore
        self.account = account

    async def get_messages(self, how_old: dt.timedelta = dt.timedelta(days=14)) -> List[Optional[vulcan.data.Message]]:
        keystore_: Any = Keystore.load(self.keystore)
        account_: Any = Account.load(self.account)
        user: Vulcan = Vulcan(account=account_, keystore=keystore_)
        async with user:
            await user.select_student()
            boxes = await user.data.get_message_boxes()

            messages_list: List[Optional[vulcan.data.Message]] = []

            async for box in boxes:
                messages = await user.data.get_messages(box.global_key)
                async for message in messages:
                    if message.sent_date.date_time >= dt.datetime.today() - how_old:
                        for i in self.keywords:
                            if i in message.content.lower() or i in message.subject.lower():
                                if "RE: " in message.subject:
                                    continue
                                if message not in messages_list:
                                    messages_list.append(message)
                break
            messages_list.sort(key=lambda x: x.sent_date.date_time, reverse=True)
            return messages_list

    @staticmethod
    def get_keywords():
        with open("./config/messages_keywords.json", "r") as keywords:
            try:
                decoded_keywords = json.load(keywords)
                return decoded_keywords
            except json.JSONDecodeError:
                print("Błąd pliku")
