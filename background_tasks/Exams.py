from typing import List, Optional

import nextcord as discord

from database.database_requests import (ExamSaved,
                                        Group, get_exams_in_group, save_exams_to_group)
from embeds.embeds import exam_embed
from other_functions.GroupChannel import get_group_channel
from utils import logs_
from vulcan.data import Exam
from vulcanrequests.get_exams import get_exams_klasus


async def exams_sender(groups_splitted: List[Group], client: discord.Client, thread_num: int):
    logs_.log(f"Starting sending exams in new thread ({thread_num})")
    for i in groups_splitted:
        exams_list: List[Exam | None] = await get_exams_klasus(keystore=i.keystore,
                                                            account=i.account)
        if not exams_list:
            continue
        exams_in_group: List[Optional[ExamSaved]] = get_exams_in_group(group_id=i.id)
        exams_to_send: List[Exam] = [exam for exam in exams_list if exam.id not in [j.exam_id for j in exams_in_group]]
        if not exams_to_send:
            continue
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

        exams_to_save: List[ExamSaved] = []
        for exam in exams_to_send:
            embed: discord.Embed = exam_embed(exam)

            embed.set_author(name="Nowa kartkówka! :(" if exam.type.lower() == "kartkówka"
                             else "Nowy sprawdzian! :(")
            msg: discord.Message = await channel.send(embed=embed)
            exam_to_save: ExamSaved = ExamSaved(exam_id=exam.id,
                                                message_id=msg.id,
                                                date_modified=exam.date_modified.date_time)
            exams_to_save.append(exam_to_save)
            logs_.log("New exam found RIP")
        save_exams_to_group(new_exams=exams_to_save, group_id=i.id)
    logs_.log(f"Done sending exams in thread ({thread_num})")
    return
