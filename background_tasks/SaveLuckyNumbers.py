from typing import Dict

import nextcord as discord

from database.database_requests import (is_group_registered,
                                        schools_list,
                                        get_groups_in_school,
                                        get_vulcan_data,
                                        save_lucky_number,
                                        get_lucky_number_in_school,
                                        reset_lucky_number
                                        )
from utils import logs_
from vulcanrequests.get_lucky_number import get_lucky_number


async def save_lucky_numbers(client: discord.Client):
    logs_.log("Clearing lucky numbers and saving new ones in every guild")
    reset_lucky_number()
    for guild in client.guilds:
        for school in schools_list(guild_id=guild.id):
            for group, class_name in get_groups_in_school(school_name=school, guild_id=guild.id):
                if is_group_registered(guild_id=guild.id, school_name=school, class_name=class_name, group_name=group):
                    if not get_lucky_number_in_school(guild_id=guild.id, school_name=school):
                        vulcan_data: Dict[str, Dict[str, str]] = get_vulcan_data(guild_id=guild.id,
                                                                                 school_name=school,
                                                                                 class_name=class_name,
                                                                                 group_name=group
                                                                                 )
                        lucky_num: int = await get_lucky_number(keystore=vulcan_data["keystore"],
                                                                account=vulcan_data["account"]
                                                                )
                        save_lucky_number(school_name=school, guild_id=guild.id, number=lucky_num)
