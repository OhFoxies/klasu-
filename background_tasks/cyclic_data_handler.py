from typing import List

import nextcord as discord

import vulcan.data
from background_tasks.exams import ExamsSender
from background_tasks.messages import MessagesSender
from database.database_requests import Group
from helpers.group_channel import get_group_channel
from vulcanrequests.exams import Exams
from vulcanrequests.get_cyclic_data import CyclicDataGetter


class CyclicDataSender:
    def __init__(self, thread_num: int, client: discord.Client, groups: List[Group]):
        self.thread_num: int = thread_num
        self.client: discord.Client = client
        self.groups: List[Group] = groups

    async def handle_data(self):
        for group in self.groups:
            cyclic_data = CyclicDataGetter(keystore=group.keystore, account=group.account)
            await cyclic_data.create_data()

            try:
                guild: discord.Guild = await self.client.fetch_guild(group.guild_id)
            except (discord.Forbidden, discord.HTTPException):
                continue

            channel = await get_group_channel(guild=guild,
                                              school=group.school_name,
                                              class_name=group.class_name,
                                              group=group.group_name,
                                              channel_id=group.channel_id)

            if not channel:
                continue

            if cyclic_data.messages:
                await self.handle_messages_data(messages=cyclic_data.messages, group=group, channel=channel)

            if cyclic_data.exams.all_exams:
                await self.handle_exams_data(exams_list=cyclic_data.exams, group=group, channel=channel)

    async def handle_messages_data(self, messages: List[vulcan.data.Message], group: Group,
                                   channel: discord.TextChannel):
        messages_sender: MessagesSender = MessagesSender(channel=channel, thread=self.thread_num, group=group)
        await messages_sender.check_for_new_messages(messages=messages)

    async def handle_exams_data(self, group: Group, channel: discord.TextChannel, exams_list: Exams):
        exam_sender: ExamsSender = ExamsSender(channel=channel, thread=self.thread_num, group=group)
        await exam_sender.start_tasks(exams_list=exams_list)
