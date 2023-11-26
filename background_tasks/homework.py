from typing import List, Optional

import nextcord as discord

from database.database_requests import (Group,
                                        get_homework_in_group,
                                        HomeworkSaved,
                                        delete_homework,
                                        save_homeworks_to_group)
from embeds.embeds import homework_deletion_embed, homework_embed
from utils import logs_
from vulcan.data import Homework
from vulcanrequests.serializables import Homeworks
from utils import messages


class HomeworkSender:
    def __init__(self, group: Group, channel, thread):
        self.group = group
        self.channel = channel
        self.thread = thread

    async def start_tasks(self, homework: Homeworks):
        logs_.log(f"Starting sending homework in thread {self.thread}")

        if homework.new_homeworks:
            homework_in_group: List[Optional[HomeworkSaved]] = get_homework_in_group(group_id=self.group.id)
            homework_to_send: List[Homework] = [_homework for _homework in homework.new_homeworks if
                                                int(_homework.homework_id) not in
                                                [j.homework_id for j in homework_in_group]]
            if homework_to_send:
                await self.send_new_homework(homework_to_send)

        if homework.all_homeworks:
            await self.check_for_homework_deletions(homework.all_homeworks)
        logs_.log(f"Done sending homework in thread {self.thread}")

    async def check_for_homework_deletions(self, homeworks):
        homework_in_group: List[Optional[HomeworkSaved]] = get_homework_in_group(group_id=self.group.id)
        all_homework_ids: List[int] = [i.homework_id for i in homeworks]

        for homework_saved in homework_in_group:
            if str(homework_saved.homework_id) not in all_homework_ids:
                try:
                    homework_msg: discord.Message = await self.channel.fetch_message(homework_saved.message_id)
                except (discord.NotFound, discord.HTTPException, discord.Forbidden):
                    continue

                subject = homework_msg.embeds[0].title
                date = homework_msg.embeds[0].fields[0].value
                homework_desc = homework_msg.embeds[0].fields[3].value
                await homework_msg.delete()

                embed = homework_deletion_embed(date=date, subject=subject, desc=homework_desc)
                delete_homework(homework_id=homework_saved.homework_id, group_id=self.group.id)

                await self.channel.send(embed=embed)

    async def send_new_homework(self, homeworks: List[Homework]):
        homeworks_to_save = []
        for homework in homeworks:
            embed = homework_embed(homework)
            embed.set_author(name=messages['new_homework'])
            msg = await self.channel.send(embed=embed,
                                          content=f"<@&{self.group.role_id}>" if self.group.role_id != 0 else "")
            homework_saved = HomeworkSaved(homework_id=homework.homework_id, message_id=msg.id,
                                           deadline=homework.deadline.date_time)
            homeworks_to_save.append(homework_saved)
        save_homeworks_to_group(homeworks=homeworks_to_save, group_id=self.group.id)
