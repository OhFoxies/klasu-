from typing import List

import nextcord as discord

from database.database_requests import Group, get_old_exams, remove_exam, get_today_exams
from other_functions.GroupChannel import get_group_channel
from utils import logs_


async def update_exams_dates(groups_splitted: List[Group], client: discord.Client, thread_num: int):
    logs_.log(f"Updating exams dates in thread ({thread_num})")
    for group in groups_splitted:
        try:
            guild: discord.Guild = await client.fetch_guild(group.guild_id)
        except (discord.Forbidden, discord.HTTPException):
            continue

        channel: discord.TextChannel | None = await get_group_channel(channel_id=group.channel_id,
                                                                      group=group.group_name,
                                                                      school=group.school_name,
                                                                      class_name=group.class_name,
                                                                      guild=guild)
        if not channel:
            continue
        old_exams = get_old_exams(group_id=group.id)
        for exam in old_exams:
            try:
                msg: discord.Message = await channel.fetch_message(exam.message_id)
            except (discord.NotFound, discord.HTTPException, discord.Forbidden):
                continue
            x = msg.embeds
            date_field_title = x[0].fields[1].name
            date_field_value = "Ten sprawdzian już się odbył." if "Sprawdzianu" in date_field_title \
                else "Ta kartkówka już się odbyła."
            x[0].set_field_at(index=1, value=date_field_value, inline=True, name=date_field_title)
            remove_exam(group_id=group.id, exam_id=exam.exam_id)
            await msg.edit(embed=x[0])

        today_exams = get_today_exams(group_id=group.id)
        for exam in today_exams:
            try:
                msg: discord.Message = await channel.fetch_message(exam.message_id)
            except (discord.NotFound, discord.HTTPException, discord.Forbidden):
                continue

            x = msg.embeds
            date_field_title = x[0].fields[1].name
            date_field_value = "Ten sprawdzian jest dzisiaj!" if "Sprawdzianu" in date_field_title \
                else "Ta kartkówka jest dzisiaj!"
            x[0].set_field_at(index=1, value=date_field_value, inline=True, name=date_field_title)
            await msg.edit(embed=x[0])
    logs_.log(f"Done Updating exams dates in thread ({thread_num})")
