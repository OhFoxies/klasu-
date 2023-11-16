from typing import List, Optional

import nextcord as discord

from database.database_requests import (ExamSaved,
                                        Group,
                                        get_exams_in_group,
                                        save_exams_to_group)
from embeds.embeds import exam_embed
from helpers.group_channel import get_group_channel
from utils import logs_, messages
from vulcan.data import Exam
from vulcanrequests.get_all_exams import get_all_exams, Exams
from .exams_edits import check_exams_edits
from .deleted_exams import check_for_exams_deletions


async def exams_sender(groups_splitted: List[Group], client: discord.Client, thread_num: int):
    logs_.log(f"Starting sending exams in new thread ({thread_num})")
    for i in groups_splitted:
        try:
            guild: discord.Guild = await client.fetch_guild(i.guild_id)
        except (discord.Forbidden, discord.HTTPException):
            continue

        channel: discord.TextChannel | None = await get_group_channel(guild=guild,
                                                                      school=i.school_name,
                                                                      class_name=i.class_name,
                                                                      group=i.group_name,
                                                                      channel_id=i.channel_id)

        if not channel:
            continue

        exams_list: Exams = await get_all_exams(keystore=i.keystore,
                                                account=i.account)

        if not exams_list.new_exams:
            await check_for_exams_deletions(group=i, all_exams=exams_list.all_exams, channel=channel)
            await check_exams_edits(group=i, exams=exams_list.upcoming_exams, channel=channel)
            continue

        exams_in_group: List[Optional[ExamSaved]] = get_exams_in_group(group_id=i.id)
        exams_to_send: List[Exam] = [exam for exam in exams_list.new_exams if exam.id not in
                                     [j.exam_id for j in exams_in_group]]

        if not exams_to_send:
            await check_for_exams_deletions(group=i, all_exams=exams_list.all_exams, channel=channel)
            await check_exams_edits(group=i, exams=exams_list.upcoming_exams, channel=channel)
            continue
        exams_to_save: List[ExamSaved] = []

        for exam in exams_to_send:
            embed: discord.Embed = exam_embed(exam)

            embed.set_author(name=messages['new_short_test'] if exam.type.lower() == "kartkówka"
                             else messages['new_exam_normal'])
            msg: discord.Message = await channel.send(embed=embed)
            exam_to_save: ExamSaved = ExamSaved(exam_id=exam.id,
                                                message_id=msg.id,
                                                date_modified=exam.date_modified.date_time,
                                                deadline=exam.deadline.date)
            exams_to_save.append(exam_to_save)
            logs_.log("New exam found RIP")
        save_exams_to_group(new_exams=exams_to_save, group_id=i.id)

        await check_for_exams_deletions(group=i, all_exams=exams_list.all_exams, channel=channel)
        await check_exams_edits(group=i, exams=exams_list.upcoming_exams, channel=channel)
    logs_.log(f"Done sending exams in thread ({thread_num})")
    return
