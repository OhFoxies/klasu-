import nextcord as discord
from nextcord.ext import commands

from utils import messages


class HowToConnect(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client

    @discord.slash_command(name="vulcan-pomoc",
                           description="Wyświetla pomoc związaną z łączeniem do vulcana",
                           dm_permission=False,
                           force_global=True,
                           default_member_permissions=discord.Permissions(permissions=8))
    async def connect_to_vulcan(self, interaction: discord.Interaction):
        embed1: discord.Embed = discord.Embed(type="rich",
                                              colour=discord.Colour.dark_blue(),
                                              title=f"{messages['help_title']}")
        embed1.add_field(name=f"{messages['why_connect_title']}",
                         value=f"{messages['why_connect']}")
        embed1.add_field(name=f"{messages['how_to_connect_title1']}",
                         value=f"{messages['how_to_connect1']}")

        embed2: discord.Embed = discord.Embed(type="rich",
                                              colour=discord.Colour.dark_blue(),
                                              title=f"{messages['help_title']}")

        embed2.add_field(name=f"{messages['how_to_connect_save_title']}",
                         value=f"{messages['how_to_connect_save']}")

        embed2.add_field(name=f"{messages['how_to_connect_title2']}",
                         value=f"{messages['how_to_connect2']}")

        embed2.add_field(name=f"{messages['how_to_connect_title3']}",
                         value=f"{messages['how_to_connect3']}")

        embed2.add_field(name=f"{messages['how_to_connect_title4']}",
                         value=f"{messages['how_to_connect4']}")
        embed1.set_image("https://i.imgur.com/Ibw7p6o.png")
        embed2.set_image("https://i.imgur.com/BJHamLr.png")
        await interaction.response.send_message(embeds=[embed1, embed2], ephemeral=True)


def setup(client):
    client.add_cog(HowToConnect(client))
