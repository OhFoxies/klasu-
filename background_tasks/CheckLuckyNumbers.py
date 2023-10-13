import nextcord as discord

from database.database_requests import (is_group_registered,
                                        schools_list,
                                        get_groups_in_school,
                                        get_vulcan_data,
                                        save_lucky_number,
                                        get_lucky_number_in_school,
                                        VulcanData
                                        )
from utils import logs_
from vulcanrequests.get_lucky_number import get_lucky_number


async def check_lucky_number(client: discord.Client):
    logs_.log("Checking if all lucky numbers are correct")
    for guild in client.guilds:
        for school in schools_list(guild_id=guild.id):
            for group, class_name in get_groups_in_school(school_name=school, guild_id=guild.id):
                if is_group_registered(guild_id=guild.id, school_name=school, class_name=class_name, group_name=group):
                    vulcan_data: VulcanData = get_vulcan_data(guild_id=guild.id,
                                                              school_name=school,
                                                              class_name=class_name,
                                                              group_name=group
                                                              )
                    lucky_num: int = await get_lucky_number(keystore=vulcan_data.keystore,
                                                            account=vulcan_data.account
                                                            )
                    if get_lucky_number_in_school(guild_id=guild.id, school_name=school) != lucky_num:
                        save_lucky_number(school_name=school, guild_id=guild.id, number=lucky_num)
                        logs_.log(f"Lucky number for school {school} was incorrect. Correcting. (Guild id: {guild.id}")
                        break
                    logs_.log(f"Lucky number for school {school} was correct. (Guild id: {guild.id}")
                    break
