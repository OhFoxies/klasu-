import nextcord as discord
from nextcord.ext import commands

from autocompletion.AutoCompletions import schools_autocompletion
from database.database_requests import *
from utils import messages
from embeds.embeds import error_embed, any_embed


class ClassesList(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client

    @discord.slash_command(name=messages['class_list_command'],
                           description=messages['class_list_desc'],
                           dm_permission=False,
                           force_global=True)
    async def classes(self, interaction: discord.Interaction,
                      school_name: str = discord.SlashOption(name=messages['value_school_name'],
                                                             description=messages['school_value_desc'],
                                                             required=True)):
        if not is_name_correct(name=school_name):
            err_embed: discord.Embed = error_embed(error=messages['school_bad_name'])
            await interaction.response.send_message(embed=err_embed, ephemeral=True)
            return

        try:
            classes: List[str] = class_list(guild_id=interaction.guild_id, school_name=school_name)
            if classes:
                embed: discord.Embed = any_embed(
                    desc=messages['your_classes']
                    .replace("{school_name}", school_name)
                    .replace("{classes_list}", ', '.join(classes)),
                    title=messages['classes_list_title'])
                await interaction.response.send_message(embed=embed, ephemeral=True)
                return

            err_embed: discord.Embed = error_embed(error=messages['no_classes_found'].replace("{name}", school_name))
            await interaction.response.send_message(embed=err_embed, ephemeral=True)
        except SchoolNotFoundError:
            err_embed: discord.Embed = error_embed(error=messages['school_not_found'].replace("{name}", school_name))
            await interaction.response.send_message(embed=err_embed, ephemeral=True)

    @classes.on_autocomplete("school_name")
    async def get_schools(self, interaction: discord.Interaction, school_input: str):
        await interaction.response.send_autocomplete(schools_autocompletion(interaction=interaction,
                                                                            school_input=school_input))


def setup(client):
    client.add_cog(ClassesList(client))
