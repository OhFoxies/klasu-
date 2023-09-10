import nextcord as discord
from nextcord.ext import commands
from utils import messages


class Ping(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client

    @discord.slash_command(name="ping", description="Ping klasusia", dm_permission=False, force_global=True)
    async def ping(self, interaction: discord.Interaction):
        await interaction.response.send_message(
            f"{messages['ping_pong']}\n{messages['ping']}".replace("{value}", f"{round(self.client.latency * 1000)}"),
            ephemeral=True
        )


def setup(client):
    client.add_cog(Ping(client))
