import nextcord as discord
from nextcord.ext import commands

from logs import logs_


class CommandLogger(commands.Cog):
    """
    Event to log any command usage in logs. Should be disabled but it's kinda cool
    """
    def __init__(self, client: commands.Bot):
        self.client = client

    @commands.Cog.listener()
    async def on_interaction(self, interaction: discord.Interaction):
        logs_.log(f"{interaction.user} used command /{interaction.application_command.name}")


def setup(client):
    client.add_cog(CommandLogger(client))
