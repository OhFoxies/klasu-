from typing import List

from database.database_requests import (Group,
                                        save_lucky_number,
                                        get_lucky_number_in_school, )
from utils import logs_
from vulcanrequests.get_lucky_number import get_lucky_number


async def check_lucky_number(groups_splitted: List[Group], thread_num: int):
    logs_.log(f"Starting checking if lucky numbers are correct. Thread: {thread_num}")
    checked = []
    for i in groups_splitted:
        if not (i.guild_id, i.school_name) in checked:
            lucky_num: int = await get_lucky_number(keystore=i.keystore,
                                                    account=i.account
                                                    )
            if get_lucky_number_in_school(guild_id=i.guild_id, school_name=i.school_name) != lucky_num:
                save_lucky_number(school_name=i.school_name, guild_id=i.guild_id, number=lucky_num)
                logs_.log(f"Lucky number for school {i.school_name} was incorrect. Correcting. (Guild id: {i.guild_id}")
            else:
                logs_.log(f"Lucky number for school {i.school_name} was correct. (Guild id: {i.guild_id}")
            checked.append((i.guild_id, i.school_name))
    logs_.log(f"Checking if lucky numbers are correct is done. Thread: {thread_num}")
