import nextcord as discord
from nextcord.ext import commands

from database.database_requests import *
from utils import messages


class AddSchool(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client

    @discord.slash_command(name=messages['add_school_command'],
                           description=messages['add_school_desc'],
                           dm_permission=False,
                           force_global=True,
                           default_member_permissions=discord.Permissions(permissions=8))
    async def add_school(self, interaction: discord.Interaction,
                         school_name: str = discord.SlashOption(name=messages['value_school_name'],
                                                                required=True)):
        if not is_name_correct(name=school_name):
            await interaction.response.send_message(f"{messages['school_bad_name']}", ephemeral=True)
            return
        if is_school_limit_reached(guild_id=interaction.guild_id):
            await interaction.response.send_message(f"{messages['limit_schools']}", ephemeral=True)
            return
        if school_name not in schools_list(guild_id=interaction.guild_id):
            create_school(guild_id=interaction.guild_id, school_name=school_name)
            await interaction.response.send_message(f"{messages['school_created']}".replace("{name}", school_name),
                                                    ephemeral=True)
            return
        await interaction.response.send_message(
            f"{messages['school_name_exists']}".replace("{name}", school_name), ephemeral=True)


def setup(client):
    client.add_cog(AddSchool(client))
