from typing import List, Optional

import nextcord as discord

from database.database_requests import (ExamSaved,
                                        Group, get_exams_in_group,
                                        save_changes_to_exam)
from embeds.embeds import exam_embed
from utils import logs_, messages
from vulcan.data import Exam


def get_exam_by_id(exam_id, exams_list: List[ExamSaved]) -> Optional[ExamSaved]:
    for exam in exams_list:
        if exam.exam_id == exam_id:
            return exam
    return None


async def check_exams_edits(group: Group, exams: List[Optional[Exam]], channel: discord.TextChannel):
    if not exams:
        return

    exams_in_group: List[Optional[ExamSaved]] = get_exams_in_group(group_id=group.id)

    if not exams_in_group:
        return

    for exam in exams:
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
                embed.set_author(name=messages['short_test_edit'] if exam.type.lower() == "kartkówka"
                                 else messages['exam_edit'])

                msg: discord.Message = await channel.send(embed=embed)
                exam_in_group.date_modified = exam.date_modified.date_time
                exam_in_group.message_id = msg.id
                logs_.log(f"Updated exam in guild {group.guild_id}")
                save_changes_to_exam(exam=exam_in_group, group_id=group.id)
