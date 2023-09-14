import nextcord as discord
from database.database_requests import (is_group_registered,
                                        get_lucky_numbers,
                                        schools_list,
                                        get_groups_in_guild,
                                        get_vulcan_data,
                                        get_channel
                                        )
from vulcanrequests.get_lucky_number import get_lucky_number
import json
from typing import List, Tuple
from utils import messages
import random


async def lucky_number(client: discord.Client):
    for guild in client.guilds:
        for school in schools_list(guild_id=guild.id):
            for group, class_name in get_groups_in_guild(school_name=school, guild_id=guild.id):
                if is_group_registered(guild_id=guild.id, school_name=school, class_name=class_name, group_name=group):
                    vulcan_data: List[Tuple[str]] = get_vulcan_data(guild_id=guild.id,
                                                                    school_name=school,
                                                                    class_name=class_name,
                                                                    group_name=group)
                    keystore: dict = json.loads(vulcan_data[0][0].replace("'", '"'))
                    account: dict = json.loads(vulcan_data[0][1].replace("'", '"'))
                    lucky_num: int = await get_lucky_number(keystore=keystore, account=account)
                    group_channel: str = get_channel(guild_id=guild.id,
                                                     school_name=school,
                                                     class_name=class_name,
                                                     group_name=group)
                    users_with_lucky: List[str] = get_lucky_numbers(school_name=school,
                                                                    guild_id=guild.id,
                                                                    number=lucky_num,
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

                    if lucky_num == 0:
                        await channel.send(messages['no_education'])
                        continue
                    if users_with_lucky:
                        mentions: List[str] = []
                        for i in users_with_lucky:
                            try:
                                user: discord.Member = await guild.fetch_member(int(i))
                                mentions.append(user.mention)
                            except (discord.Forbidden, discord.HTTPException):
                                pass

                        await channel.send(messages['lucky_number'].replace('{school}', school).replace(
                            '{number}', str(lucky_num)).replace('{user}', ', '.join(mentions)))
                        continue
                    await channel.send(messages['lucky_number'].replace('{school}', school).replace(
                        '{number}', str(lucky_num)).replace('{user}', 'Brak użytkownika z tym numerem w tej grupie'))
