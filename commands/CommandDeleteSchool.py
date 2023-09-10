import nextcord as discord
from nextcord.ext import commands


class DeleteSchool(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client

    @discord.slash_command(description="Usuwa wybraną szkołę", name="usun-szkole", dm_permission=False,
                           force_global=True,
                           default_member_permissions=discord.Permissions(permissions=8)
                           )
    async def delete_school(self, interaction: discord.Interaction):
        # deletes given school, all classes, groups and users in this school with messages on group channel
        pass


def setup(client):
    client.add_cog(DeleteSchool(client))
