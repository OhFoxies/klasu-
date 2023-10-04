import nextcord as discord
from nextcord.ext import commands

from autocompletion.AutoCompletions import schools_autocompletion
from database.database_requests import *
from utils import messages


class AddClass(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client

    @discord.slash_command(name=messages['add_class_command'],
                           description=messages['add_class_desc'],
                           dm_permission=False,
                           force_global=True,
                           default_member_permissions=discord.Permissions(permissions=8))
    async def add_class(self,
                        interaction: discord.Interaction,
                        school_name: str = discord.SlashOption(name=messages['value_school_name'],
                                                               description=messages['school_value_desc'],
                                                               required=True),
                        class_name: str = discord.SlashOption(name=messages['value_class_name'],
                                                              description=messages['class_new_value_desc'],
                                                              required=True)):
        if not is_name_correct(name=school_name):
            await interaction.response.send_message(f"{messages['school_bad_name']}", ephemeral=True)
            return
        if not is_name_correct(name=class_name):
            await interaction.response.send_message(f"{messages['class_bad_name']}", ephemeral=True)
            return
        try:
            classes: List[str] = class_list(guild_id=interaction.guild_id, school_name=school_name)
            if class_name not in classes:
                if is_classes_limit_reached(guild_id=interaction.guild_id, school_name=school_name):
                    await interaction.response.send_message(f"{messages['limit_classes']}", ephemeral=True)
                    return
                create_class(guild_id=interaction.guild_id, class_name=class_name, school_name=school_name)
                response_message: str = messages['class_created'].replace("{name}", class_name).replace(
                    "{school_name}", school_name)
                await interaction.response.send_message(response_message,
                                                        ephemeral=True)
                return
            response_message: str = messages['class_name_exists'].replace("{school_name}", school_name).replace(
                "{name}", class_name)
            await interaction.response.send_message(response_message, ephemeral=True)
        except SchoolNotFoundError:
            await interaction.response.send_message(f"{messages['school_not_found']}".replace("{name}", school_name),
                                                    ephemeral=True)

    @add_class.on_autocomplete("school_name")
    async def get_schools(self, interaction: discord.Interaction, school_input: str):
        await interaction.response.send_autocomplete(schools_autocompletion(interaction=interaction,
                                                                            school_input=school_input))


def setup(client):
    client.add_cog(AddClass(client))
