import nextcord as discord
from nextcord.ext import commands


class DeleteGroup(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client

    @discord.slash_command(description="Usuwa wybraną grupę", name="usun-grupe", dm_permission=False, force_global=True,
                           default_member_permissions=discord.Permissions(permissions=8)
                           )
    async def delete_group(self, interaction: discord.Interaction):
        # deletes given group, users in this group with message on group channel
        pass


def setup(client):
    client.add_cog(DeleteGroup(client))
