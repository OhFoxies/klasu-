from typing import List, Optional

import nextcord as discord

from database.database_requests import (Group,
                                        get_exams_in_group,
                                        ExamSaved,
                                        save_exams_to_group,
                                        save_changes_to_exam,
                                        delete_exam
                                        )
from embeds.embeds import exam_embed, exam_deletion_embed
from utils import logs_
from utils import messages
from vulcan.data import Exam
from vulcanrequests.exams import Exams


class ExamsSender:
    def __init__(self, group: Group, channel, thread):
        self.group = group
        self.channel = channel
        self.thread = thread

    async def start_tasks(self, exams_list: Exams):
        logs_.log(f"Starting sending exams in thread {self.thread}")

        if exams_list.new_exams:
            exams_in_group: List[Optional[ExamSaved]] = get_exams_in_group(group_id=self.group.id)
            exams_to_send: List[Exam] = [exam for exam in exams_list.new_exams if exam.id not in
                                         [j.exam_id for j in exams_in_group]]
            if exams_to_send:
                await self.send_new_exams(exams_to_send)

        if exams_list.upcoming_exams:
            await self.check_exams_edits(exams_list.upcoming_exams)

        if exams_list.all_exams:
            await self.check_for_exams_deletions(exams_list.all_exams)
        logs_.log(f"Done sending exams in thread {self.thread}")

    async def send_new_exams(self, exams):
        exams_to_save: List[ExamSaved] = []

        for exam in exams:
            embed: discord.Embed = exam_embed(exam)

            embed.set_author(
                name=messages['new_short_test'] if exam.type.lower() == "kartkówka" else messages['new_exam_normal'])

            msg: discord.Message = await self.channel.send(embed=embed, content=f"<@&{self.group.role_id}>" if self.group.role_id != 0 else "")
            exam_to_save: ExamSaved = ExamSaved(exam_id=exam.id,
                                                message_id=msg.id,
                                                date_modified=exam.date_modified.date_time,
                                                deadline=exam.deadline.date)
            exams_to_save.append(exam_to_save)
        save_exams_to_group(new_exams=exams_to_save, group_id=self.group.id)

    async def check_exams_edits(self, exams):
        exams_in_group: List[Optional[ExamSaved]] = get_exams_in_group(group_id=self.group.id)
        if not exams_in_group:
            return

        for exam in exams:
            if exam.date_modified.date_time != exam.date_created.date_time:
                exam_in_group: Optional[ExamSaved] = self.get_exam_by_id(exam_id=exam.id, exams_list=exams_in_group)
                if not exam_in_group:
                    continue

                if exam_in_group.date_modified != exam.date_modified.date_time:
                    try:
                        old_exam_msg: discord.Message = await self.channel.fetch_message(exam_in_group.message_id)
                        await old_exam_msg.delete()
                    except (discord.NotFound, discord.HTTPException, discord.Forbidden):
                        pass
                    embed: discord.Embed = exam_embed(exam)
                    embed.set_author(name=messages['short_test_edit'] if exam.type.lower() == "kartkówka"
                    else messages['exam_edit'])

                    msg: discord.Message = await self.channel.send(embed=embed, content=f"<@&{self.group.role_id}>" if self.group.role_id != 0 else "")
                    exam_in_group.date_modified = exam.date_modified.date_time
                    exam_in_group.deadline = exam.deadline.date
                    exam_in_group.message_id = msg.id
                    logs_.log(f"Updated exam in guild {self.group.guild_id}")
                    save_changes_to_exam(exam=exam_in_group, group_id=self.group.id)

    async def check_for_exams_deletions(self, all_exams):
        exams_in_group: List[Optional[ExamSaved]] = get_exams_in_group(group_id=self.group.id)
        all_exams_ids: List[int] = [i.id for i in all_exams]

        for exam_saved in exams_in_group:
            if exam_saved.exam_id not in all_exams_ids:
                try:
                    exam_msg: discord.Message = await self.channel.fetch_message(exam_saved.message_id)
                except (discord.NotFound, discord.HTTPException, discord.Forbidden):
                    continue

                subject = exam_msg.embeds[0].title
                date = exam_msg.embeds[0].fields[0].value
                exam_type = exam_msg.embeds[0].fields[3].value
                exam_desc = exam_msg.embeds[0].fields[4].value
                await exam_msg.delete()

                embed = exam_deletion_embed(date=date, subject=subject, desc=exam_desc, exam_type=exam_type)
                delete_exam(exam_id=exam_saved.exam_id, group_id=self.group.id)

                await self.channel.send(embed=embed)

    @staticmethod
    def get_exam_by_id(exam_id, exams_list: List[ExamSaved]) -> Optional[ExamSaved]:
        for exam in exams_list:
            if exam.exam_id == exam_id:
                return exam
        return None
