import nextcord as discord
from nextcord.ext import commands
from database.database_requests import *
from utils import messages


class SchoolList(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client

    @discord.slash_command(name="lista-szkoły",
                           description="Wyswietla listę szkół",
                           dm_permission=False,
                           force_global=True)
    async def schools(self, interaction: discord.Interaction):
        schools = schools_list(guild_id=interaction.guild_id)
        if schools:
            await interaction.response.send_message(f"{messages['schools']}".replace("{schools}", ", ".join(schools)),
                                                    ephemeral=True)
        else:
            await interaction.response.send_message(f"{messages['no_schools']}", ephemeral=True)


def setup(client):
    client.add_cog(SchoolList(client))
