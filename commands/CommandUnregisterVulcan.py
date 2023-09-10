import nextcord as discord
from nextcord.ext import commands


class DeleteVulcan(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client

    @discord.slash_command(description="Usuwa połączenie vulcana z wybraną klasą", name="vulcan-odlacz",
                           dm_permission=False, force_global=True,
                           default_member_permissions=discord.Permissions(permissions=8)
                           )
    async def delete_vulcan(self, interaction: discord.Interaction):
        # it disconnects group from vulcan notify users and clear user data from group
        pass


def setup(client):
    client.add_cog(DeleteVulcan(client))
