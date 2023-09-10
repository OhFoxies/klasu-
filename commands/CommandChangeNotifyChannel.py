import nextcord as discord
from nextcord.ext import commands


class ChangeChannel(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client

    @discord.slash_command(description="Zmienia kanał powiadomień dla danej grupy",
                           name="grupa-kanal",
                           dm_permission=False,
                           force_global=True)
    async def unregister(self, interaction: discord.Interaction):
        # optional argument for channel if not given returns current channel if given changes
        # current notify channel to new value
        pass


def setup(client):
    client.add_cog(ChangeChannel(client))
