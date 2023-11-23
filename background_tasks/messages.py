import json
from typing import List

import vulcan.data
from database.database_requests import Group, VulcanMessage, get_messages_in_group, save_message
import nextcord as discord
from embeds.embeds import message_embed
from utils import logs_


class MessagesSender:
    def __init__(self, group: Group, channel, thread):
        self.keywords = self.get_keywords()
        self.group = group
        self.channel = channel
        self.thread = thread

    async def check_for_new_messages(self, messages: List[vulcan.data.Message]):
        logs_.log(f"Starting sending messages in thread {self.thread}")

        sent_messages = get_messages_in_group(group_id=self.group.id)
        messages_to_send = [i for i in messages if i.id not in [j.msg_id for j in sent_messages]]

        for message in messages_to_send:
            msg = None
            for i in self.keywords:
                if i in message.content.lower() or i in message.subject.lower():
                    if "RE: " in message.subject:
                        continue
                    embed = message_embed(message)
                    try:
                        msg = await self.channel.send(embed=embed)
                    except discord.HTTPException:
                        pass
                    break

            message_to_save = VulcanMessage(msg_id=message.id, group_id=self.group.id, messsage_id=msg.id if msg else 0)
            save_message(message_to_save)
        logs_.log(f"Done sending messages in thread {self.thread}")

    @staticmethod
    def get_keywords():
        with open("./config/messages_keywords.json", "r") as keywords:
            try:
                decoded_keywords = json.load(keywords)
                return decoded_keywords
            except json.JSONDecodeError:
                print("Błąd pliku")
