from typing import List, Tuple, Dict

import nextcord as discord
from nextcord.ext import commands

from database.database_requests import (get_user_data,
                                        get_vulcan_data,
                                        get_lucky_number_in_school,
                                        save_lucky_number
                                        )
from utils import messages
from vulcanrequests.get_lucky_number import get_lucky_number


class LuckyNumber(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client

    @discord.slash_command(name=messages['lucky_number_command'],
                           description=messages['lucky_number_desc'],
                           dm_permission=False,
                           force_global=True)
    async def lucky_number(self, interaction: discord.Interaction):
        user_data: List[Tuple[str, ...]] = get_user_data(user_id=interaction.user.id, guild_id=interaction.guild_id)
        if not user_data:
            await interaction.response.send_message(messages['need_to_register'], ephemeral=True)
            return

        message: discord.PartialInteractionMessage = await interaction.send(messages['connecting_to_vulcan'])
        lucky_in_school: int | None = get_lucky_number_in_school(school_name=user_data[0][1],
                                                                 guild_id=interaction.guild_id)
        if lucky_in_school:
            if lucky_in_school != 0:
                msg: str = messages['lucky_number'].replace('{school}', user_data[0][1]).replace(
                    '{number}', str(lucky_in_school)).replace('Użytkownik: {user}', '')
                await message.edit(msg)
                return

            await message.edit(messages['no_education'])
            return

        vulcan_data: Dict[str, Dict[str, str]] = get_vulcan_data(guild_id=interaction.guild_id,
                                                                 school_name=user_data[0][1],
                                                                 class_name=user_data[0][0],
                                                                 group_name=user_data[0][2]
                                                                 )

        lucky_number: int = await get_lucky_number(keystore=vulcan_data['keystore'], account=vulcan_data['account'])
        save_lucky_number(guild_id=interaction.guild_id, school_name=user_data[0][1], number=lucky_number)
        if lucky_number == 0:
            await message.edit(messages['no_education'])
            return
        msg: str = messages['lucky_number'].replace('{school}', user_data[0][1]).replace(
            '{number}', str(lucky_number)).replace('Użytkownik: {user}', '')
        await message.edit(msg)


def setup(client):
    client.add_cog(LuckyNumber(client))
