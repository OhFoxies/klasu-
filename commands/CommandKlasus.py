import nextcord
from nextcord.ext import commands
from utils import messages


class KlasusCommand(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client

    @nextcord.slash_command(description="Opis klasusia", name="klasus", dm_permission=False, force_global=True)
    async def klasus_command(self, interaction: nextcord.Interaction):
        await interaction.response.send_message(f"{messages['klasus']}", ephemeral=True)


def setup(client):
    client.add_cog(KlasusCommand(client))
