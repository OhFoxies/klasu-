import nextcord as discord
from nextcord.ext import commands
from database.database_requests import (class_list,
                                        group_list,
                                        is_group_registered,
                                        SchoolNotFoundError,
                                        )
from autocompletion.AutoCompletions import schools_autocompletion, classes_autocompletion, groups_autocompletion
from utils import messages
from group_functions.GroupFunctions import send_message_group_channel
from typing import List


class SendGroupInfo(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client

    @discord.slash_command(description="Wysyła wiadomość na kanał grupy",
                           name="group-info",
                           dm_permission=False,
                           force_global=True,
                           default_member_permissions=discord.Permissions(permissions=8))
    async def change_channel(self, interaction: discord.Interaction,
                             school_name: str = discord.SlashOption(name="nazwa-szkoly",
                                                                    description="Nazwa szkoly ktora wczesniej "
                                                                                "utworzyles",
                                                                    required=True),
                             class_name: str = discord.SlashOption(name="nazwa-klasy",
                                                                   description="Nazwa klasy ktora wczesniej utworzyles",
                                                                   required=True),
                             group_name: str = discord.SlashOption(name="nazwa-grupy",
                                                                   description="Nazwa grupy ktora wczesniej utworzyles",
                                                                   required=True),
                             message: str = discord.SlashOption(name="wiadomość",
                                                                required=True)):

        try:
            classes: List[str] = class_list(guild_id=interaction.guild_id, school_name=school_name)
            if class_name in classes:
                groups_list: List[str] = group_list(guild_id=interaction.guild_id, school_name=school_name,
                                                    class_name=class_name)
                if group_name in groups_list:
                    if is_group_registered(guild_id=interaction.guild_id,
                                           school_name=school_name,
                                           class_name=class_name,
                                           group_name=group_name):
                        await send_message_group_channel(school_name=school_name,
                                                         class_name=class_name,
                                                         group_name=group_name,
                                                         interaction=interaction,
                                                         message=message,
                                                         pin=False
                                                         )
                        await interaction.response.send_message(messages['send'], ephemeral=True)
                        return
                    await interaction.response.send_message(messages['group_not_connected'], ephemeral=True)
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

    @change_channel.on_autocomplete("school_name")
    async def get_schools(self, interaction: discord.Interaction, school_input: str):
        await interaction.response.send_autocomplete(schools_autocompletion(interaction=interaction,
                                                                            school_input=school_input))

    @change_channel.on_autocomplete("class_name")
    async def get_classes(self, interaction: discord.Interaction, class_name: str):
        await interaction.response.send_autocomplete(classes_autocompletion(interaction=interaction,
                                                                            class_name=class_name))

    @change_channel.on_autocomplete("group_name")
    async def get_groups(self, interaction: discord.Interaction, group_name: str):
        await interaction.response.send_autocomplete(
            groups_autocompletion(interaction=interaction, group_name=group_name))


def setup(client):
    client.add_cog(SendGroupInfo(client))
