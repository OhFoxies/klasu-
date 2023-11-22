import json
from typing import List
from database.database_requests import Group, VulcanMessage, get_messages_in_group, save_message
import nextcord as discord
from helpers.group_channel import get_group_channel
from vulcanrequests.get_messages import get_new_messages
from embeds.embeds import message_embed


class MessagesSender:
    def __init__(self, thread_num: int, groups_splitted: List[Group], client: discord.Client, old=False):
        self.thread_num = thread_num
        self.groups_list = groups_splitted
        self.client = client
        self.keywords = self.get_keywords()
        self.old_message = old

    async def check_for_new_messages(self):
        for group in self.groups_list:
            try:
                guild: discord.Guild = await self.client.fetch_guild(group.guild_id)
            except (discord.Forbidden, discord.HTTPException):
                continue

            channel: discord.TextChannel | None = await get_group_channel(guild=guild,
                                                                          school=group.school_name,
                                                                          class_name=group.class_name,
                                                                          group=group.group_name,
                                                                          channel_id=group.channel_id)

            if not channel:
                continue

            messages = await get_new_messages(keystore=group.keystore, account=group.account, old=self.old_message)
            sent_messages = get_messages_in_group(group_id=group.id)
            messages_to_send = [i for i in messages if i.id not in [j.msg_id for j in sent_messages]]
            for message in messages_to_send:
                msg = None
                for i in self.keywords:

                    if i in message.content or i in message.subject:
                        if "RE: " in message.subject:
                            continue
                        embed = message_embed(message)
                        try:
                            msg = await channel.send(embed=embed)
                        except discord.HTTPException:
                            pass
                        break

                message_to_save = VulcanMessage(msg_id=message.id, group_id=group.id, messsage_id=msg.id if msg else 0)
                save_message(message_to_save)

    @staticmethod
    def get_keywords():
        with open("./config/messages_keywords.json", "r") as keywords:
            try:
                decoded_keywords = json.load(keywords)
                return decoded_keywords
            except json.JSONDecodeError:
                print("Błąd pliku")
