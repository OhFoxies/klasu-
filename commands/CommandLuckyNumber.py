import nextcord as discord
from nextcord.ext import commands

from database.database_requests import (get_user_data,
                                        get_vulcan_data,
                                        get_lucky_number_in_school,
                                        save_lucky_number,
                                        User,
                                        VulcanData
                                        )
from utils import messages
from vulcanrequests.get_lucky_number import get_lucky_number
from embeds.embeds import lucky_number_embed, connecting, error_embed


class LuckyNumber(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client

    @discord.slash_command(name=messages['lucky_number_command'],
                           description=messages['lucky_number_desc'],
                           dm_permission=False,
                           force_global=True)
    async def lucky_number(self, interaction: discord.Interaction):
        user_data: User | None = get_user_data(user_id=interaction.user.id, guild_id=interaction.guild_id)
        if not user_data:
            err_embed: discord.Embed = error_embed(error=messages['need_to_register'])
            await interaction.response.send_message(embed=err_embed, ephemeral=True)
            return

        embed: discord.Embed = connecting()
        message: discord.PartialInteractionMessage = await interaction.send(embed=embed)
        lucky_in_school: int | None = get_lucky_number_in_school(school_name=user_data.school_name,
                                                                 guild_id=interaction.guild_id)
        if lucky_in_school:
            embed: discord.Embed = lucky_number_embed(lucky_num=lucky_in_school,
                                                      user=interaction.user,
                                                      school_name=user_data.school_name)
            await message.edit(embed=embed)
            return

        vulcan_data: VulcanData = get_vulcan_data(guild_id=interaction.guild_id,
                                                  school_name=user_data.school_name,
                                                  class_name=user_data.class_name,
                                                  group_name=user_data.group_name
                                                  )

        lucky_number: int = await get_lucky_number(keystore=vulcan_data.keystore, account=vulcan_data.account)
        save_lucky_number(guild_id=interaction.guild_id, school_name=user_data.school_name, number=lucky_number)

        embed: discord.Embed = lucky_number_embed(lucky_num=lucky_number,
                                                  user=interaction.user,
                                                  school_name=user_data.school_name)
        await message.edit(embed=embed)


def setup(client):
    client.add_cog(LuckyNumber(client))
