from typing import List

from database.database_requests import (save_lucky_number,
                                        get_lucky_number_in_school,
                                        reset_lucky_number,
                                        Group
                                        )
from utils import logs_
from vulcanrequests.get_lucky_number import get_lucky_number


async def save_and_clear_lucky_numbers(groups_splitted: List[Group], thread_num: int):
    logs_.log(f"Clearing all lucky number and saving new ones. Thread: {thread_num}")
    reset_lucky_number()
    for i in groups_splitted:
        if not get_lucky_number_in_school(guild_id=i.guild_id, school_name=i.school_name):
            lucky_num: int = await get_lucky_number(keystore=i.keystore,
                                                    account=i.account)
            save_lucky_number(school_name=i.school_name, guild_id=i.guild_id, number=lucky_num)
    logs_.log(f"Saved and cleared lucky numbers. Thread {thread_num}")
