import nextcord as discord
from nextcord.ext import commands

from autocompletion.AutoCompletions import schools_autocompletion
from database.database_requests import *
from utils import messages


class ClassesList(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client

    @discord.slash_command(name="lista-klasy",
                           description="Wyswietla liste klas w podanej szkole",
                           dm_permission=False,
                           force_global=True)
    async def classes(self, interaction: discord.Interaction,
                      school_name: str = discord.SlashOption(name="nazwa-szkoły",
                                                             required=True)):
        if not is_name_correct(name=school_name):
            await interaction.response.send_message(f"{messages['school_bad_name']}", ephemeral=True)
            return
        try:
            classes: List[str] = class_list(guild_id=interaction.guild_id, school_name=school_name)
            if classes:
                classes_message: str = messages['your_classes'].replace("{school_name}", school_name).replace(
                    "{classes_list}", ', '.join(classes))
                await interaction.response.send_message(classes_message, ephemeral=True)
                return
            await interaction.response.send_message(f"{messages['no_classes_found']}".replace("{name}", school_name),
                                                    ephemeral=True)
        except SchoolNotFoundError:
            await interaction.response.send_message(f"{messages['school_not_found']}".replace("{name}", school_name),
                                                    ephemeral=True)

    @classes.on_autocomplete("school_name")
    async def get_schools(self, interaction: discord.Interaction, school_input: str):
        await interaction.response.send_autocomplete(schools_autocompletion(interaction=interaction,
                                                                            school_input=school_input))


def setup(client):
    client.add_cog(ClassesList(client))
