import nextcord as discord
from nextcord.ext import commands


class DeleteClass(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client

    @discord.slash_command(description="Usuwa wybraną klasę", name="usun-klase", dm_permission=False, force_global=True,
                           default_member_permissions=discord.Permissions(permissions=8)
                           )
    async def delete_class(self, interaction: discord.Interaction):
        # deletes class and groups in class with messages on groups channels if
        # possible. Also deletes all user in this class
        pass


def setup(client):
    client.add_cog(DeleteClass(client))
