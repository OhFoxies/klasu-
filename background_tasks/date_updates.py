from typing import List

import nextcord as discord

from database.database_requests import (Group,
                                        get_today_exams,
                                        get_today_homework,
                                        get_old_exams,
                                        get_old_homework,
                                        remove_exam,
                                        remove_homework)
from helpers.group_channel import get_group_channel
from utils import logs_


class UpdateDates:
    def __init__(self, thread_num: int, client: discord.Client, groups: List[Group]):
        self.thread_num: int = thread_num
        self.client: discord.Client = client
        self.groups: List[Group] = groups

    async def update_dates(self):
        for group in self.groups:
            try:
                guild: discord.Guild = await self.client.fetch_guild(group.guild_id)
            except (discord.Forbidden, discord.HTTPException):
                continue

            channel: discord.TextChannel | None = await get_group_channel(channel_id=group.channel_id,
                                                                          group=group.group_name,
                                                                          school=group.school_name,
                                                                          class_name=group.class_name,
                                                                          guild=guild)
            if not channel:
                continue

            today_exams = get_today_exams(group_id=group.id)
            old_exams = get_old_exams(group_id=group.id)

            today_homework = get_today_homework(group_id=group.id)
            old_homework = get_old_homework(group_id=group.id)

            await self.update_exams_date(today_exams=today_exams, old_exams=old_exams, channel=channel, group=group)
            await self.update_homework_dates(today_homework=today_homework, old_homework=old_homework, channel=channel,
                                             group=group)

    async def update_exams_date(self, today_exams, old_exams, channel: discord.TextChannel, group: Group):
        logs_.log(f"Starting updating exams dates in thread ({self.thread_num})")

        for exam in old_exams:
            try:
                msg: discord.Message = await channel.fetch_message(exam.message_id)
            except (discord.NotFound, discord.HTTPException, discord.Forbidden):
                continue
            x = msg.embeds
            date_field_title = x[0].fields[1].name
            date_field_value = "Ten sprawdzian już się odbył." if "Sprawdzianu" in date_field_title \
                else "Ta kartkówka już się odbyła."
            x[0].set_field_at(index=1, value=date_field_value, inline=False, name=date_field_title)
            remove_exam(group_id=group.id, exam_id=exam.exam_id)
            await msg.edit(embed=x[0])

        for exam in today_exams:
            try:
                msg: discord.Message = await channel.fetch_message(exam.message_id)
            except (discord.NotFound, discord.HTTPException, discord.Forbidden):
                continue

            x = msg.embeds
            date_field_title = x[0].fields[1].name
            date_field_value = "Ten sprawdzian jest dzisiaj!" if "Sprawdzianu" in date_field_title \
                else "Ta kartkówka jest dzisiaj!"
            x[0].set_field_at(index=1, value=date_field_value, inline=False, name=date_field_title)
            await msg.edit(embed=x[0])

        logs_.log(f"Done updating exams dates in thread ({self.thread_num})")

    async def update_homework_dates(self, today_homework, old_homework, channel: discord.TextChannel, group: Group):
        logs_.log(f"Starting updating homeworks dates in thread ({self.thread_num})")

        for homework in old_homework:
            try:
                msg: discord.Message = await channel.fetch_message(homework.message_id)
            except (discord.NotFound, discord.HTTPException, discord.Forbidden):
                continue
            x = msg.embeds
            date_field_title = x[0].fields[1].name
            date_field_value = "Termin zadania minął!"
            x[0].set_field_at(index=1, value=date_field_value, inline=False, name=date_field_title)
            remove_homework(group_id=group.id, homework_id=homework.homework_id)
            await msg.edit(embed=x[0])

        for homework in today_homework:
            try:
                msg: discord.Message = await channel.fetch_message(homework.message_id)
            except (discord.NotFound, discord.HTTPException, discord.Forbidden):
                continue

            x = msg.embeds
            date_field_title = x[0].fields[1].name
            date_field_value = "To zadanie jest na dzisiaj!"
            x[0].set_field_at(index=1, value=date_field_value, inline=False, name=date_field_title)
            await msg.edit(embed=x[0])

        logs_.log(f"Done updating homeworks dates in thread ({self.thread_num})")
