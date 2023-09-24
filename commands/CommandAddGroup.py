import nextcord as discord
from nextcord.ext import commands

from autocompletion.AutoCompletions import schools_autocompletion, classes_autocompletion
from database.database_requests import *
from utils import messages


class AddGroup(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client

    @discord.slash_command(name=messages['add_group_command'],
                           description=messages['add_group_desc'],
                           dm_permission=False,
                           force_global=True,
                           default_member_permissions=discord.Permissions(permissions=8))
    async def add_group(self, interaction: discord.Interaction,
                        school_name: str = discord.SlashOption(name=messages['value_school_name'],
                                                               required=True),
                        class_name: str = discord.SlashOption(name=messages['value_class_name'],
                                                              required=True),
                        group_name: str = discord.SlashOption(name=messages['value_group_name'],
                                                              required=True)):
        if is_group_limit_reached(guild_id=interaction.guild_id, class_name=class_name, school_name=school_name):
            await interaction.response.send_message(f"{messages['groups_limit']}", ephemeral=True)
        if is_name_correct(name=school_name):
            if not is_name_correct(name=class_name):
                await interaction.response.send_message(f"{messages['class_bad_name']}", ephemeral=True)
                return
            if not is_name_correct(name=group_name):
                await interaction.response.send_message(f"{messages['group_bad_name']}", ephemeral=True)
                return
            try:
                classes: List[str] = class_list(guild_id=interaction.guild_id, school_name=school_name)
                if class_name in classes:
                    if group_name in group_list(guild_id=interaction.guild_id, class_name=class_name,
                                                school_name=school_name):
                        await interaction.response.send_message(f"{messages['group_exists']}", ephemeral=True)
                        return
                    create_group(guild_id=interaction.guild_id, school_name=school_name, class_name=class_name,
                                 group_name=group_name)
                    response_message: str = messages['group_created'].replace("{name}", group_name).replace(
                        "{school}", school_name).replace("{class}", class_name)
                    await interaction.response.send_message(response_message,
                                                            ephemeral=True)
                    return
                await interaction.response.send_message(
                    f"{messages['class_not_found']}".replace("{name}", class_name), ephemeral=True)
            except SchoolNotFoundError:
                await interaction.response.send_message(
                    f"{messages['school_not_found']}".replace("{name}", school_name), ephemeral=True)
                return
        await interaction.response.send_message(f"{messages['school_bad_name']}", ephemeral=True)

    @add_group.on_autocomplete("school_name")
    async def get_schools(self, interaction: discord.Interaction, school_input: str):
        await interaction.response.send_autocomplete(schools_autocompletion(interaction=interaction,
                                                                            school_input=school_input))

    @add_group.on_autocomplete("class_name")
    async def get_classes(self, interaction: discord.Interaction, class_name: str):
        await interaction.response.send_autocomplete(classes_autocompletion(interaction=interaction,
                                                                            class_name=class_name))


def setup(client):
    client.add_cog(AddGroup(client))
