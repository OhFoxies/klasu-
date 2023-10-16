from typing import List

import nextcord as discord

from database.database_requests import (get_last_exams_ids,
                                        save_last_exams_ids,
                                        Group)
from embeds.embeds import exam_embed
from other_functions.GroupChannel import get_group_channel
from utils import logs_
from vulcan.data import Exam
from vulcanrequests.get_new_exams import get_new_exams


async def exams_sender(groups_splitted: List[Group], client: discord.Client, thread_num: int):
    logs_.log(f"Starting sending exams in new thread ({thread_num}")
    for i in groups_splitted:
        exams_list: List[Exam | None] = await get_new_exams(keystore=i.keystore,
                                                            account=i.account
                                                            )
        last_exams_ids: List[str] | None = get_last_exams_ids(guild_id=i.guild_id,
                                                              school_name=i.school_name,
                                                              class_name=i.class_name,
                                                              group_name=i.group_name
                                                              )
        if not exams_list:
            continue
        exams_list_new: List[Exam | None] = []
        founded_new_exams = []

        if not last_exams_ids:
            save_last_exams_ids(guild_id=i.guild_id,
                                school_name=i.school_name,
                                class_name=i.class_name,
                                group_name=i.group_name,
                                new_exams=[str(j.id) for j in exams_list])
            exams_list_new = exams_list
        else:
            for exam in exams_list:
                if str(exam.id) not in last_exams_ids:
                    exams_list_new.append(exam)
                    founded_new_exams.append(exam)

            save_last_exams_ids(guild_id=i.guild_id,
                                school_name=i.school_name,
                                class_name=i.class_name,
                                group_name=i.group_name,
                                new_exams=[str(j.id) for j in founded_new_exams])
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

        for exam in exams_list_new:
            embed: discord.Embed = exam_embed(exam)

            embed.set_author(name="Nowa kartkówka! :(" if exam.type.lower() == "kartkówka"
                             else "Nowy sprawdzian! :(")
            await channel.send(embed=embed)
            logs_.log("New exam found RIP")
    logs_.log(f"Done sending exams in thread {thread_num}")
    return
