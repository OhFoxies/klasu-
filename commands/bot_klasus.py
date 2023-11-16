import nextcord as discord
from nextcord.ext import commands

from utils import messages
import datetime


class KlasusCommand(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client

    @discord.slash_command(name=messages['command_klasus'],
                           description=messages['klasus_desc'],
                           dm_permission=False,
                           force_global=True)
    async def klasus_command(self, interaction: discord.Interaction):
        embed: discord.Embed = discord.Embed(type="rich", title=messages['klasus_title'],
                                             color=discord.Color.green(),
                                             timestamp=datetime.datetime.now(),
                                             description=messages['klasus'])
        embed.set_author(name=self.client.user.name, icon_url=self.client.user.avatar)

        await interaction.response.send_message(embed=embed, ephemeral=True)


def setup(client):
    client.add_cog(KlasusCommand(client))
