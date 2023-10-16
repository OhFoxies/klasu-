from typing import List

import nextcord as discord

from database.database_requests import (get_lucky_numbers,
                                        get_lucky_number_in_school,
                                        save_lucky_number, Group)
from other_functions.GroupChannel import get_group_channel
from utils import messages, logs_
from vulcanrequests.get_lucky_number import get_lucky_number


async def lucky_numbers_sender(groups_splitted: List[Group], client: discord.Client, thread_num: int):
    logs_.log(f"Starting sending lucky numbers in thread {thread_num}")
    for i in groups_splitted:
        if not get_lucky_number_in_school(school_name=i.school_name, guild_id=i.guild_id):
            lucky_num: int = await get_lucky_number(keystore=i.keystore,
                                                    account=i.account)
            save_lucky_number(guild_id=i.guild_id, school_name=i.school_name, number=lucky_num)
        else:
            lucky_num: int = get_lucky_number_in_school(guild_id=i.guild_id, school_name=i.school_name)

        users_with_lucky: List[str] = get_lucky_numbers(school_name=i.school_name,
                                                        guild_id=i.guild_id,
                                                        number=lucky_num,
                                                        class_name=i.class_name,
                                                        group_name=i.group_name)
        try:
            guild: discord.Guild = await client.fetch_guild(i.guild_id)
        except (discord.Forbidden, discord.HTTPException):
            continue

        channel: discord.TextChannel | None = await get_group_channel(channel_id=i.channel_id,
                                                                      group=i.group_name,
                                                                      school=i.school_name,
                                                                      class_name=i.class_name,
                                                                      guild=guild)
        if not channel:
            continue

        if lucky_num == 0:
            await channel.send(messages['no_education'])
            continue
        if users_with_lucky:
            mentions: List[str] = []
            for j in users_with_lucky:
                try:
                    user: discord.Member = await guild.fetch_member(int(j))
                    mentions.append(user.mention)
                except (discord.Forbidden, discord.HTTPException):
                    await channel.send(messages['lucky_number'].replace('{school}', i.school_name).replace(
                        '{number}', str(lucky_num)).replace('{user}',
                                                            messages['lucky_number_no_users']))

            await channel.send(messages['lucky_number'].replace('{school}', i.school_name).replace(
                '{number}', str(lucky_num)).replace('{user}', ', '.join(mentions)))
            continue
        await channel.send(messages['lucky_number'].replace('{school}', i.school_name).replace(
            '{number}', str(lucky_num)).replace('{user}', messages['lucky_number_no_users']))
    logs_.log(f"Done sending lucky numbers in thread {thread_num}")
    return
