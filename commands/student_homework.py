import nextcord as discord
from nextcord.ext import commands

from database.database_requests import *
from embeds.embeds import homework_embed, connecting, error_embed, any_embed
from helpers.helpers import date_from_string
from utils import messages
from vulcan.data import Homework
from vulcanrequests.get_homework import get_homework


class HomeWork(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client

    @discord.slash_command(name=messages['homework_command'],
                           description=messages['homework_command_desc'],
                           dm_permission=False,
                           force_global=True)
    async def exams(self, interaction: discord.Interaction,
                    date_to: str = discord.SlashOption(name=messages['date_value'],
                                                       description=messages['date_value_desc'],
                                                       required=False)):

        user_data: User | None = get_user_data(user_id=interaction.user.id, guild_id=interaction.guild_id)
        if not user_data:
            err_embed: discord.Embed = error_embed(error=messages['need_to_register'])
            await interaction.response.send_message(embed=err_embed, ephemeral=True)
            return

        vulcan_data: VulcanData = get_vulcan_data(guild_id=interaction.guild_id,
                                                  school_name=user_data.school_name,
                                                  class_name=user_data.class_name,
                                                  group_name=user_data.group_name
                                                  )
        embed: discord.Embed = connecting()
        msg: discord.PartialInteractionMessage = await interaction.send(embed=embed, ephemeral=True)
        date = None
        if date_to:
            date = await date_from_string(date_to, msg)
            if not date:
                return

        homeworks: List[Homework | None] = await get_homework(keystore=vulcan_data.keystore,
                                                              account=vulcan_data.account,
                                                              date_to=date if date_to else None)

        if not homeworks:
            no_homework_embed: discord.Embed = any_embed(title=messages['no_homework_title'],
                                                         desc=messages['no_homework'])
            await msg.edit(embed=no_homework_embed)
        await msg.delete()
        for homework in homeworks:
            embed: discord.Embed = homework_embed(homework)
            embed.set_author(name=messages['homework'])
            await interaction.send(embed=embed, ephemeral=True)


def setup(client):
    client.add_cog(HomeWork(client))
