from typing import List, Optional

import nextcord as discord

from database.database_requests import (ExamSaved,
                                        Group, get_exams_in_group,
                                        save_changes_to_exam)
from embeds.embeds import exam_embed
from other_functions.GroupChannel import get_group_channel
from utils import logs_
from vulcan.data import Exam

from vulcanrequests.get_exams import get_exams_klasus

def get_exam_by_id(exam_id, exams_list: List[ExamSaved]) -> Optional[ExamSaved]:
    for exam in exams_list:
        if exam.exam_id == exam_id:
            return exam
    return None


async def check_exams_edits(groups_splitted: List[Group], client: discord.Client, thread_num: int):
    logs_.log(f"Checking for exams edits in thread ({thread_num})")
    for i in groups_splitted:
        upcoming_exams: List[Exam | None] = await get_exams_klasus(keystore=i.keystore,
                                                            account=i.account)
                                                        
        if not upcoming_exams:
            continue
        exams_in_group: List[Optional[ExamSaved]] = get_exams_in_group(group_id=i.id)
        if not exams_in_group:
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

        for exam in upcoming_exams:
            if exam.date_modified.date_time != exam.date_created.date_time:
                exam_in_group: Optional[ExamSaved] = get_exam_by_id(exam_id=exam.id, exams_list=exams_in_group)
                if not exam_in_group:
                    continue
                if exam_in_group.date_modified != exam.date_modified.date_time:
                    try:
                        old_exam_msg: discord.Message = await channel.fetch_message(exam_in_group.message_id)
                        await old_exam_msg.delete()
                    except (discord.NotFound, discord.HTTPException, discord.Forbidden):
                        pass
                    embed: discord.Embed = exam_embed(exam)
                    embed.set_author(name="EDYCJA KARTKÓWKI!" if exam.type.lower() == "kartkówka"
                                     else "EDYCJA SPRAWDZIANU!")

                    msg: discord.Message = await channel.send(embed=embed)
                    exam_in_group.date_modified = exam.date_modified.date_time
                    exam_in_group.message_id = msg.id
                    logs_.log(f"Updated exam in guild {i.guild_id}")
                    save_changes_to_exam(exam=exam_in_group, group_id=i.id)
    logs_.log(f"Done checking exams edits in thread ({thread_num})")
    return
