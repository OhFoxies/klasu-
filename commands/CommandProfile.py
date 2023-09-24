from datetime import datetime

import nextcord
import nextcord as discord
from nextcord.ext import commands

from database.database_requests import *
from utils import messages


class Profile(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client

    @discord.slash_command(name=messages['profile_command'],
                           dm_permission=False,
                           force_global=True)
    async def profile(self, interaction: discord.Interaction,
                      user: discord.Member = nextcord.SlashOption(name=messages['user_value'], required=False)):
        if not user:
            user: discord.Member = interaction.user
        user_data: List[Tuple[str, ...]] = get_user_data(guild_id=interaction.guild_id, user_id=user.id)
        if not user_data:
            embed: discord.Embed = discord.Embed(type="rich",
                                                 title=user.name,
                                                 colour=discord.Colour.dark_blue(),
                                                 timestamp=datetime.now(),
                                                 description=messages['user_no_account']
                                                 if user.id != interaction.user.id
                                                 else messages['no_account']
                                                 )
            embed.set_author(name=user.name, icon_url=user.avatar if user.avatar else nextcord.User.default_avatar)
            embed.set_thumbnail(url=user.avatar if user.avatar else nextcord.User.default_avatar)
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return
        embed: discord.Embed = discord.Embed(type="rich",
                                             title=user.name,
                                             colour=discord.Colour.dark_blue(),
                                             timestamp=datetime.now()
                                             )
        embed.add_field(name=messages['school'],
                        value=messages['your_school'].replace('{school}', user_data[0][1])
                        if user.id == interaction.user.id
                        else messages['user_school'].replace('{school}', user_data[0][1]))
        embed.add_field(name=messages['class'],
                        value=messages['your_class'].replace('{class}', user_data[0][0])
                        if user.id == interaction.user.id
                        else messages['user_class'].replace('{class}', user_data[0][0]))
        embed.add_field(name=messages['group'],
                        value=messages['your_group'].replace('{group}', user_data[0][2])
                        if user.id == interaction.user.id
                        else messages['user_group'].replace('{group}', user_data[0][2]))
        embed.add_field(name=messages['number'],
                        value=messages['your_number'].replace('{number}', user_data[0][3])
                        if user.id == interaction.user.id
                        else messages['user_number'].replace('{number}', user_data[0][3]))
        embed.set_author(name=user.name, icon_url=user.avatar if user.avatar else nextcord.User.default_avatar)
        embed.set_thumbnail(url=user.avatar if user.avatar else nextcord.User.default_avatar)
        await interaction.response.send_message(embed=embed, ephemeral=True)


def setup(client):
    client.add_cog(Profile(client))
