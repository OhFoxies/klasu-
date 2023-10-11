from other_functions.group_channel import get_group_channel
from typing import List, Dict

import nextcord as discord

from database.database_requests import (is_group_registered,
                                        schools_list,
                                        get_groups_in_school,
                                        get_vulcan_data,
                                        get_channel,
                                        get_last_exams_ids,
                                        save_last_exams_ids
                                        )
from utils import logs_
from vulcan.data import Exam
from vulcanrequests.get_new_exams import get_new_exams
from embeds.embeds import exam_embed


async def exams(client: discord.Client):
    logs_.log("Checking exams...")
    for guild in client.guilds:
        for school in schools_list(guild_id=guild.id):
            for group, class_name in get_groups_in_school(school_name=school, guild_id=guild.id):
                if is_group_registered(guild_id=guild.id, school_name=school, class_name=class_name, group_name=group):
                    vulcan_data: Dict[str, Dict[str, str]] = get_vulcan_data(guild_id=guild.id,
                                                                             school_name=school,
                                                                             class_name=class_name,
                                                                             group_name=group
                                                                             )
                    exams_list: List[Exam | None] = await get_new_exams(keystore=vulcan_data["keystore"],
                                                                        account=vulcan_data["account"]
                                                                        )
                    last_exams_ids: List[str] | None = get_last_exams_ids(guild_id=guild.id,
                                                                          school_name=school,
                                                                          class_name=class_name,
                                                                          group_name=group
                                                                          )
                    if not exams_list:
                        continue
                    exams_list_new: List[Exam | None] = []
                    founded_new_exams = []

                    if not last_exams_ids:
                        save_last_exams_ids(guild_id=guild.id,
                                            school_name=school,
                                            class_name=class_name,
                                            group_name=group,
                                            new_exams=[str(i.id) for i in exams_list])
                        exams_list_new = exams_list
                    else:
                        for exam in exams_list:
                            if str(exam.id) not in last_exams_ids:
                                exams_list_new.append(exam)
                                founded_new_exams.append(exam)

                        save_last_exams_ids(guild_id=guild.id,
                                            school_name=school,
                                            class_name=class_name,
                                            group_name=group,
                                            new_exams=[str(i.id) for i in founded_new_exams])
                    group_channel_id: str = get_channel(guild_id=guild.id,
                                                        school_name=school,
                                                        class_name=class_name,
                                                        group_name=group)

                    channel: discord.TextChannel | None = await get_group_channel(guild=guild,
                                                                                  school=school,
                                                                                  class_name=class_name,
                                                                                  group=group,
                                                                                  channel_id=int(group_channel_id))
                    if not channel:
                        continue

                    for exam in exams_list_new:
                        embed: discord.Embed = exam_embed(exam)

                        embed.set_author(name="Nowa kartkówka! :(" if exam.type.lower() == "kartkówka"
                                         else "Nowy sprawdzian! :(")
                        await channel.send(embed=embed)
                        logs_.log("New exam found RIP")
