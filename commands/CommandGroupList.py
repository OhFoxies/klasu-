import nextcord as discord
from nextcord.ext import commands

from autocompletion.AutoCompletions import schools_autocompletion, classes_autocompletion
from database.database_requests import *
from utils import messages


class GroupsList(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client

    @discord.slash_command(name="lista-grupy",
                           description="Wyswietla liste grup w podanej klasie",
                           dm_permission=False, force_global=True)
    async def groups(self, interaction: discord.Interaction,
                     school_name: str = discord.SlashOption(name="nazwa-szkoły",
                                                            required=True),
                     class_name: str = discord.SlashOption(name="nazwa-klasy",
                                                           required=True)):
        if is_name_correct(name=school_name):
            if not is_name_correct(name=class_name):
                await interaction.response.send_message(f"{messages['class_bad_name']}", ephemeral=True)
                return
            try:
                classes: List[str] = class_list(guild_id=interaction.guild_id, school_name=school_name)
                if class_name in classes:
                    groups: List[str] = group_list(guild_id=interaction.guild_id,
                                                   school_name=school_name,
                                                   class_name=class_name
                                                   )
                    await interaction.response.send_message(
                        f"{messages['groups_list']}".replace("{list}", ', '.join(groups)), ephemeral=True)
                    return
                else:
                    await interaction.response.send_message(
                        f"{messages['class_not_found']}".replace("{name}", class_name), ephemeral=True)
                    return
            except SchoolNotFoundError:
                await interaction.response.send_message(
                    f"{messages['school_not_found']}".replace("{name}", school_name),
                    ephemeral=True)
                return
        await interaction.response.send_message(f"{messages['school_bad_name']}", ephemeral=True)
        return

    @groups.on_autocomplete("school_name")
    async def get_schools(self, interaction: discord.Interaction, school_input: str):
        await interaction.response.send_autocomplete(schools_autocompletion(interaction=interaction,
                                                                            school_input=school_input))

    @groups.on_autocomplete("class_name")
    async def get_classes(self, interaction: discord.Interaction, class_name: str):
        await interaction.response.send_autocomplete(classes_autocompletion(interaction=interaction,

                                                                            class_name=class_name))


def setup(client):
    client.add_cog(GroupsList(client))
