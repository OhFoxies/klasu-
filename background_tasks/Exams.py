import datetime
import json
import random
from typing import List, Tuple

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
from utils import messages
from vulcan.data import Exam
from vulcanrequests.get_new_exams import get_new_exams


async def exams(client: discord.Client):
    logs_.log("Checking exams...")
    for guild in client.guilds:
        for school in schools_list(guild_id=guild.id):
            for group, class_name in get_groups_in_school(school_name=school, guild_id=guild.id):
                if is_group_registered(guild_id=guild.id, school_name=school, class_name=class_name, group_name=group):
                    vulcan_data: List[Tuple[str]] = get_vulcan_data(guild_id=guild.id,
                                                                    school_name=school,
                                                                    class_name=class_name,
                                                                    group_name=group)
                    keystore: dict = json.loads(vulcan_data[0][0].replace("'", '"'))
                    account: dict = json.loads(vulcan_data[0][1].replace("'", '"'))
                    last_exams_ids: List[str] | None = get_last_exams_ids(guild_id=guild.id,
                                                                          school_name=school,
                                                                          class_name=class_name,
                                                                          group_name=group)
                    exams_list: List[Exam | None] = await get_new_exams(keystore=keystore, account=account)
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
                    group_channel: str = get_channel(guild_id=guild.id,
                                                     school_name=school,
                                                     class_name=class_name,
                                                     group_name=group)

                    try:
                        channel: discord.TextChannel = await guild.fetch_channel(int(group_channel))
                    except discord.NotFound:
                        system_channel: discord.TextChannel = guild.system_channel
                        msg: str = messages['channel_not_found'].replace('{school}', school)
                        msg: str = msg.replace('{class}', class_name)
                        msg: str = msg.replace('{group}', group)
                        if system_channel:
                            await system_channel.send(msg)
                            continue
                        random_channel: discord.TextChannel = random.choice(guild.text_channels)
                        await random_channel.send(msg)
                        continue
                    except discord.HTTPException:
                        continue
                    except discord.InvalidData:
                        continue
                    for exam in exams_list_new:

                        match exam.type.lower():
                            case "sprawdzian":
                                type_formatted: str = messages['exam_form2']
                            case "kartkówka":
                                type_formatted: str = messages['short_test_form2']
                            case _:
                                type_formatted: str = "testu"
                        embed: discord.Embed = discord.Embed(type="rich", title=exam.subject.name,
                                                             color=discord.Color.green()
                                                             if exam.type == "Kartkówka" else
                                                             discord.Color.red(),
                                                             timestamp=datetime.datetime.now()
                                                             )

                        embed.set_author(name="Nowa kartkówka! :(" if exam.type.lower() == "kartkówka"
                                         else "Nowy sprawdzian! :(")
                        embed.add_field(name=messages['date'].replace('{type}', type_formatted),
                                        value=exam.deadline.date,
                                        inline=False
                                        )
                        if exam.deadline.date == datetime.date.today():
                            embed.add_field(name=messages['time_left'].replace('{type}', type_formatted),
                                            value="Ten sprawdzian jest dzisiaj!"
                                            if exam.type.lower() == "sprawdzian" else "Ta kartkówka jest dzisiaj!",
                                            inline=False)
                        else:
                            embed.add_field(name=messages['time_left'].replace('{type}', type_formatted),
                                            value=f"{exam.deadline.date - datetime.date.today()}".replace(", 0:00:00", "")
                                            .replace("days", "dni")
                                            .replace("day", "dzień")
                                            .replace("month", "miesiąc")
                                            .replace("months", "miesięcy"),
                                            inline=False)
                        embed.add_field(name=messages['teacher'],
                                        value=f"{exam.creator.name} {exam.creator.surname}",
                                        inline=False)
                        embed.add_field(name=messages['type'], value=exam.type, inline=False)
                        embed.add_field(name=messages['description'], value=exam.topic, inline=False)
                        await channel.send(embed=embed)
                        logs_.log("New exam found RIP")
