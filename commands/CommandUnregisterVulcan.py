from typing import List

import nextcord as discord
from nextcord.ext import commands

from autocompletion.AutoCompletions import schools_autocompletion, classes_autocompletion, groups_autocompletion
from database.database_requests import (SchoolNotFoundError,
                                        class_list,
                                        group_list,
                                        is_group_registered,
                                        delete_vulcan_connection
                                        )
from other_functions.Functions import user_delete_account_info
from utils import messages


class DeleteVulcan(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client

    @discord.slash_command(name=messages['command_vulcan_disconnect'],
                           dm_permission=False,
                           force_global=True,
                           default_member_permissions=discord.Permissions(permissions=8))
    async def delete_vulcan(self, interaction: discord.Interaction,
                            school_name: str = discord.SlashOption(name=messages['value_school_name'],
                                                                   required=True),
                            class_name: str = discord.SlashOption(name=messages['value_class_name'],
                                                                  required=True),
                            group_name: str = discord.SlashOption(name=messages['value_group_name'],
                                                                  required=True)):
        try:
            classes: List[str] = class_list(guild_id=interaction.guild_id, school_name=school_name)
            if class_name in classes:
                groups_list: List[str] = group_list(guild_id=interaction.guild_id,
                                                    school_name=school_name,
                                                    class_name=class_name
                                                    )
                if group_name in groups_list:
                    if not is_group_registered(guild_id=interaction.guild_id,
                                               school_name=school_name,
                                               class_name=class_name,
                                               group_name=group_name):
                        await interaction.response.send_message(messages['group_not_connected'], ephemeral=True)
                        return
                    deleted_users: List[str] = delete_vulcan_connection(guild_id=interaction.guild_id,
                                                                        school_name=school_name,
                                                                        class_name=class_name,
                                                                        group_name=group_name
                                                                        )
                    msg: discord.PartialInteractionMessage = await interaction.send(messages['deleting'],
                                                                                    ephemeral=True)
                    await user_delete_account_info(deleted_users=deleted_users, interaction=interaction)
                    await msg.edit(messages['group_disconnected'].replace('{group}', group_name))
                    return
                await interaction.response.send_message(messages['group_not_found'.replace('{name}', group_name)],
                                                        ephemeral=True)
                return
            await interaction.response.send_message(
                f"{messages['class_not_found']}".replace("{name}", class_name), ephemeral=True)
            return
        except SchoolNotFoundError:
            await interaction.response.send_message(
                f"{messages['school_not_found']}".replace("{name}", school_name), ephemeral=True)
            return

    @delete_vulcan.on_autocomplete("school_name")
    async def get_schools(self, interaction: discord.Interaction, school_input: str):
        await interaction.response.send_autocomplete(schools_autocompletion(interaction=interaction,
                                                                            school_input=school_input))

    @delete_vulcan.on_autocomplete("class_name")
    async def get_classes(self, interaction: discord.Interaction, class_name: str):
        await interaction.response.send_autocomplete(classes_autocompletion(interaction=interaction,
                                                                            class_name=class_name))

    @delete_vulcan.on_autocomplete("group_name")
    async def get_groups(self, interaction: discord.Interaction, group_name: str):
        await interaction.response.send_autocomplete(
            groups_autocompletion(interaction=interaction, group_name=group_name))


def setup(client):
    client.add_cog(DeleteVulcan(client))
