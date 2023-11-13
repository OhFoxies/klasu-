import vulcan.data

from typing import List, Optional
from database.database_requests import get_exams_in_group, Group, ExamSaved, delete_exam
import nextcord as discord
from embeds.embeds import exam_deletion_embed


async def check_for_exams_deletions(all_exams: List[vulcan.data.Exam], group: Group, channel: discord.TextChannel):
    exams_in_group: List[Optional[ExamSaved]] = get_exams_in_group(group_id=group.id)
    all_exams_ids: List[int] = [i.id for i in all_exams]

    for exam_saved in exams_in_group:

        if exam_saved.exam_id not in all_exams_ids:
            try:
                exam_msg: discord.Message = await channel.fetch_message(exam_saved.message_id)
            except (discord.NotFound, discord.HTTPException, discord.Forbidden):
                continue

            subject = exam_msg.embeds[0].title
            date = exam_msg.embeds[0].fields[0].value
            exam_type = exam_msg.embeds[0].fields[3].value
            exam_desc = exam_msg.embeds[0].fields[4].value
            await exam_msg.delete()

            embed = exam_deletion_embed(date=date, subject=subject, desc=exam_desc, exam_type=exam_type)
            delete_exam(exam_id=exam_saved.exam_id, group_id=group.id)

            await channel.send(embed=embed)
