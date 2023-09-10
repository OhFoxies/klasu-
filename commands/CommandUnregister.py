import nextcord as discord
from nextcord.ext import commands


class Unregister(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client

    @discord.slash_command(description="Usuwa cię z bazy danych", name="wyrejestruj", dm_permission=False,
                           force_global=True)
    async def unregister(self, interaction: discord.Interaction):
        # removes user from database
        pass


def setup(client):
    client.add_cog(Unregister(client))
