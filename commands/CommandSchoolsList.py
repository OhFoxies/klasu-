import nextcord as discord
from nextcord.ext import commands

from database.database_requests import *
from utils import messages
from embeds.embeds import any_embed, error_embed


class SchoolList(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client

    @discord.slash_command(name=messages['school_list_command'],
                           description=messages['school_list_desc'],
                           dm_permission=False,
                           force_global=True)
    async def schools(self, interaction: discord.Interaction):
        schools: List[str] = schools_list(guild_id=interaction.guild_id)
        if schools:
            embed: discord.Embed = any_embed(
                desc=messages['schools'] .replace("{schools}", ", ".join(schools)),
                title=messages['schools_list_title'])
            await interaction.response.send_message(embed=embed, ephemeral=True)
        else:
            embed: discord.Embed = error_embed(messages['no_schools'])
            await interaction.response.send_message(embed=embed, ephemeral=True)


def setup(client):
    client.add_cog(SchoolList(client))
