from typing import List

import nextcord as discord
from nextcord.ext import commands

from autocompletion.AutoCompletions import schools_autocompletion
from database.database_requests import delete_school, schools_list, SchoolNotFoundError, is_name_correct
from other_functions.Functions import user_delete_account_info
from utils import messages


class DeleteSchool(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client

    @discord.slash_command(name=messages['delete_school_command'],
                           dm_permission=False,
                           force_global=True,
                           default_member_permissions=discord.Permissions(permissions=8))
    async def delete_school(self, interaction: discord.Interaction,
                            school_name: str = discord.SlashOption(name=messages['value_school_name'],
                                                                   required=True)):

        if not is_name_correct(name=school_name):
            await interaction.response.send_message(f"{messages['school_bad_name']}", ephemeral=True)
            return
        try:
            schools: List[str] = schools_list(guild_id=interaction.guild_id)
            if school_name not in schools:
                raise SchoolNotFoundError
            deleted_users: List[str] = delete_school(school_name=school_name, guild_id=interaction.guild_id)
            msg: discord.PartialInteractionMessage = await interaction.send(messages['deleting'], ephemeral=True)

            await user_delete_account_info(deleted_users=deleted_users, interaction=interaction)
            await msg.edit(messages['deleted_school'].replace('{school}', school_name))
        except SchoolNotFoundError:
            await interaction.response.send_message(f"{messages['school_not_found']}".replace("{name}", school_name),
                                                    ephemeral=True)

    @delete_school.on_autocomplete("school_name")
    async def get_schools(self, interaction: discord.Interaction, school_input: str):
        await interaction.response.send_autocomplete(schools_autocompletion(interaction=interaction,
                                                                            school_input=school_input))


def setup(client):
    client.add_cog(DeleteSchool(client))
