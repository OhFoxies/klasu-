import nextcord as discord
from nextcord.ext import commands
from database.database_requests import *
from utils import messages
from autocompletion.AutoCompletions import schools_autocompletion, classes_autocompletion, groups_autocompletion
from typing import List, Tuple


class Register(commands.Cog):
    def __int__(self, client: commands.Bot):
        self.client = client

    @discord.slash_command(description="Rejestracja do bazy danych klasusia",
                           name="rejestracja",
                           dm_permission=False,
                           force_global=True)
    async def registration(self, interaction: discord.Interaction,
                           school_name: str = discord.SlashOption(name="nazwa-szkoly",
                                                                  description="Nazwa szkoly do której chodzisz",
                                                                  required=True),
                           class_name: str = discord.SlashOption(name="nazwa-klasy",
                                                                 description="Klasa do której chodzisz",
                                                                 required=True),
                           group_name: str = discord.SlashOption(name="nazwa-grupy",
                                                                 description="Twoja grupa w klasie",
                                                                 required=True),
                           number: int = discord.SlashOption(name="numer-w-dzienniku",
                                                             description="Twój numer z dziennika",
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
                        await interaction.response.send_message(messages['group_not_registered'], ephemeral=True)
                        return
                    if number <= 0 or number > 50:
                        await interaction.response.send_message(messages['wrong_number'])
                        return
                    user_data: List[Tuple[str, ...]] = get_user_data(interaction.user.id, interaction.guild_id)
                    if get_user_data(interaction.user.id, interaction.guild_id):
                        msg: str = messages['already_registered'].replace('{class}', user_data[0][0]).replace(
                            '{school}', user_data[0][1]).replace('{group}', user_data[0][2])
                        await interaction.response.send_message(msg, ephemeral=True)
                        return
                    register_user(guild_id=interaction.guild_id,
                                  user_id=interaction.user.id,
                                  group_name=group_name,
                                  school_name=school_name,
                                  class_name=class_name,
                                  number=number
                                  )
                    await interaction.response.send_message(messages['registered'], ephemeral=True)
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
