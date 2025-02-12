import nextcord as discord
from nextcord.ext import commands

from autocompletion.auto_completions import schools_autocompletion, classes_autocompletion
from database.database_requests import *
from utils import messages
from embeds.embeds import error_embed, any_embed


class GroupsList(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client

    @discord.slash_command(name=messages['group_list_command'],
                           description=messages['group_list_desc'],
                           dm_permission=False, force_global=True)
    async def groups(self, interaction: discord.Interaction,
                     school_name: str = discord.SlashOption(name=messages['value_school_name'],
                                                            description=messages['school_value_desc'],
                                                            required=True),
                     class_name: str = discord.SlashOption(name=messages['value_class_name'],
                                                           description=messages['class_value_desc'],
                                                           required=True)):
        if is_name_correct(name=school_name):
            if not is_name_correct(name=class_name):
                err_embed: discord.Embed = error_embed(error=messages['class_bad_name'])
                await interaction.response.send_message(embed=err_embed, ephemeral=True)
                return
            try:
                classes: List[str] = class_list(guild_id=interaction.guild_id, school_name=school_name)
                if class_name in classes:
                    groups: List[str] = group_list(guild_id=interaction.guild_id,
                                                   school_name=school_name,
                                                   class_name=class_name
                                                   )
                    embed: discord.Embed = any_embed(desc=messages['groups_list'].replace("{list}", ', '.join(groups)),
                                                     title=messages['groups_list_title'])
                    await interaction.response.send_message(embed=embed, ephemeral=True)
                    return
                else:
                    err_embed: discord.Embed = error_embed(
                        error=messages['class_not_found'].replace("{name}", class_name))
                    await interaction.response.send_message(embed=err_embed, ephemeral=True)
                    return
            except SchoolNotFoundError:
                err_embed: discord.Embed = error_embed(
                    error=messages['school_not_found'].replace("{name}", school_name))
                await interaction.response.send_message(embed=err_embed, ephemeral=True)
                return
        err_embed: discord.Embed = error_embed(error=messages['school_bad_name'])
        await interaction.response.send_message(embed=err_embed, ephemeral=True)

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
