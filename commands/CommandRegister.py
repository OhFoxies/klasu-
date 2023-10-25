import nextcord as discord
from nextcord.ext import commands

from autocompletion.AutoCompletions import schools_autocompletion, classes_autocompletion, groups_autocompletion
from database.database_requests import *
from utils import messages
from embeds.embeds import error_embed, registered


class Register(commands.Cog):
    def __int__(self, client: commands.Bot):
        self.client = client

    @discord.slash_command(name=messages['register_command'],
                           description=messages['register_desc'],
                           dm_permission=False,
                           force_global=True)
    async def registration(self, interaction: discord.Interaction,
                           school_name: str = discord.SlashOption(name=messages['value_school_name'],
                                                                  description=messages['school_new_value_desc'],
                                                                  required=True),
                           class_name: str = discord.SlashOption(name=messages['value_class_name'],
                                                                 description=messages['class_new_value_desc'],
                                                                 required=True),
                           group_name: str = discord.SlashOption(name=messages['value_group_name'],
                                                                 description=messages['group_new_value_desc'],
                                                                 required=True),
                           number: int = discord.SlashOption(name=messages['number_value'],
                                                             description=messages['number_value_desc'],
                                                             required=True)):

        try:
            classes: List[str] = class_list(guild_id=interaction.guild_id, school_name=school_name)
            if class_name in classes:
                groups_list: List[str] = group_list(guild_id=interaction.guild_id, school_name=school_name,
                                                    class_name=class_name)
                if group_name in groups_list:
                    if not is_group_registered(guild_id=interaction.guild_id,
                                               school_name=school_name,
                                               class_name=class_name,
                                               group_name=group_name):
                        err_embed: discord.Embed = error_embed(messages['group_not_registered'])
                        await interaction.response.send_message(embed=err_embed, ephemeral=True)
                        return

                    if number <= 0 or number > 50:
                        err_embed: discord.Embed = error_embed(messages['wrong_number'])
                        await interaction.response.send_message(embed=err_embed, ephemeral=True)
                        return

                    user_data: User | None = get_user_data(interaction.user.id, interaction.guild_id)
                    if user_data:
                        msg: str = messages['already_registered'].replace('{class}', user_data.class_name).replace(
                            '{school}', user_data.school_name).replace('{group}', user_data.group_name)
                        err_embed: discord.Embed = error_embed(msg)
                        await interaction.response.send_message(embed=err_embed, ephemeral=True)
                        return
                    register_user(guild_id=interaction.guild_id,
                                  user_id=interaction.user.id,
                                  group_name=group_name,
                                  school_name=school_name,
                                  class_name=class_name,
                                  number=number
                                  )
                    embed: discord.Embed = registered()
                    await interaction.response.send_message(embed=embed, ephemeral=True)
                    return

                err_embed: discord.Embed = error_embed(messages['group_not_found'].replace("{name}", group_name))

                await interaction.response.send_message(embed=err_embed, ephemeral=True)
                return

            err_embed: discord.Embed = error_embed(messages['class_not_found'].replace("{name}", class_name))

            await interaction.response.send_message(embed=err_embed, ephemeral=True)
            return

        except SchoolNotFoundError:
            err_embed: discord.Embed = error_embed(messages['school_not_found'].replace("{name}", school_name))

            await interaction.response.send_message(embed=err_embed, ephemeral=True)
            return

    @registration.on_autocomplete("school_name")
    async def get_schools(self, interaction: discord.Interaction, school_input: str):
        await interaction.response.send_autocomplete(schools_autocompletion(interaction=interaction,
                                                                            school_input=school_input))

    @registration.on_autocomplete("class_name")
    async def get_classes(self, interaction: discord.Interaction, class_name: str):
        await interaction.response.send_autocomplete(classes_autocompletion(interaction=interaction,
                                                                            class_name=class_name))

    @registration.on_autocomplete("group_name")
    async def get_groups(self, interaction: discord.Interaction, group_name: str):
        await interaction.response.send_autocomplete(
            groups_autocompletion(interaction=interaction, group_name=group_name))


def setup(client):
    client.add_cog(Register(client))
