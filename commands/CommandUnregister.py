import nextcord as discord
from nextcord.ext import commands

from database.database_requests import get_user_data, clear_user_data, User
from utils import messages


class Unregister(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client

    @discord.slash_command(name=messages['unregister_command'],
                           description=messages['unregister_command_desc'],
                           dm_permission=False,
                           force_global=True)
    async def unregister(self, interaction: discord.Interaction):
        user: discord.Member = interaction.user
        user_data: User | None = get_user_data(guild_id=interaction.guild_id, user_id=user.id)
        if not user_data:
            await interaction.response.send_message(messages['need_to_register_to_unregister'], ephemeral=True)
            return
        clear_user_data(guild_id=interaction.guild_id, user_id=user.id)
        await interaction.response.send_message(messages['unregistered'], ephemeral=True)


def setup(client):
    client.add_cog(Unregister(client))
