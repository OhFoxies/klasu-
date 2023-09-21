from typing import List

import nextcord as discord
from nextcord.ext import commands

from autocompletion.AutoCompletions import classes_autocompletion, schools_autocompletion
from database.database_requests import is_name_correct, class_list, delete_class, SchoolNotFoundError
from other_functions.Functions import user_delete_account_info
from utils import messages


class DeleteClass(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client

    @discord.slash_command(description="Usuwa wybraną klasę",
                           name="usun-klase",
                           dm_permission=False,
                           force_global=True,
                           default_member_permissions=discord.Permissions(permissions=8))
    async def delete_class(self, interaction: discord.Interaction,
                           school_name: str = discord.SlashOption(name="nazwa-szkoly",
                                                                  description="Nazwa szkoly ktora wczesniej utworzyles",
                                                                  required=True),
                           class_name: str = discord.SlashOption(name="nazwa-klasy",
                                                                 description="Nazwa klasy ktora wczesniej utworzyles",
                                                                 required=True)):

        if is_name_correct(name=school_name):
            if not is_name_correct(name=class_name):
                await interaction.response.send_message(f"{messages['class_bad_name']}", ephemeral=True)
                return
            try:
                classes: List[str] = class_list(guild_id=interaction.guild_id, school_name=school_name)
                if class_name in classes:
                    deleted_users: List[str] = delete_class(school_name=school_name, class_name=class_name,
                                                            guild_id=interaction.guild_id)
                    msg: discord.PartialInteractionMessage = await interaction.send(messages['deleting'],
                                                                                    ephemeral=True)
                    await user_delete_account_info(deleted_users=deleted_users, interaction=interaction)
                    await msg.edit(messages['deleted_class'].replace('{class}', class_name),)
                    return
                await interaction.response.send_message(
                    f"{messages['class_not_found']}".replace("{name}", class_name), ephemeral=True)
            except SchoolNotFoundError:
                await interaction.response.send_message(
                    f"{messages['school_not_found']}".replace("{name}", school_name), ephemeral=True)
                return
        await interaction.response.send_message(f"{messages['school_bad_name']}", ephemeral=True)

    @delete_class.on_autocomplete("school_name")
    async def get_schools(self, interaction: discord.Interaction, school_input: str):
        await interaction.response.send_autocomplete(schools_autocompletion(interaction=interaction,
                                                                            school_input=school_input))

    @delete_class.on_autocomplete("class_name")
    async def get_classes(self, interaction: discord.Interaction, class_name: str):
        await interaction.response.send_autocomplete(classes_autocompletion(interaction=interaction,
                                                                            class_name=class_name))


def setup(client):
    client.add_cog(DeleteClass(client))
