import nextcord as discord
from nextcord.ext import commands

from autocompletion.AutoCompletions import schools_autocompletion, classes_autocompletion, groups_autocompletion
from database.database_requests import *
from other_functions.Functions import send_message_group_channel
from utils import messages
from vulcanrequests.connect import create_new_connection


class ConnectToVulcan(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client

    @discord.slash_command(name="vulcan-podlacz",
                           description="podłącza daną grupę do Vulcana",
                           dm_permission=False,
                           force_global=True,
                           default_member_permissions=discord.Permissions(permissions=8))
    async def connect_to_vulcan(self, interaction: discord.Interaction,
                                school_name: str = discord.SlashOption(name="nazwa-szkoly",
                                                                       description="Nazwa szkoly ktora wczesniej "
                                                                                   "utworzyles",
                                                                       required=True),
                                class_name: str = discord.SlashOption(name="nazwa-klasy",
                                                                      description="Nazwa klasy ktora wczesniej "
                                                                                  "utworzyles",
                                                                      required=True),
                                group_name: str = discord.SlashOption(name="nazwa-grupy",
                                                                      description="Nazwa grupy ktora wczesniej "
                                                                                  "utworzyles",
                                                                      required=True),
                                token: str = discord.SlashOption(name="token",
                                                                 description="Token z Twojego dziennika Vulcan. "
                                                                             "Więcej info komenda vulcanrequests-pomoc",
                                                                 required=True),
                                pin: str = discord.SlashOption(name="pin",
                                                               description="Pin z Twojego dziennika Vulcan. Więcej "
                                                                           "info komenda vulcanrequests-pomoc",
                                                               required=True),
                                symbol: str = discord.SlashOption(name="symbol",
                                                                  description="Symbol z Twojego dziennika Vulcan. "
                                                                              "Więcej info komenda "
                                                                              "vulcanrequests-pomoc",
                                                                  required=True),
                                channel: discord.TextChannel = discord.SlashOption(name="kanał")):
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
                        await interaction.response.send_message(messages['group_registered'], ephemeral=True)
                        return
                    message: discord.PartialInteractionMessage = \
                        await interaction.send(messages['connecting'], ephemeral=True)
                    connecting: Tuple[bool, str] = await create_new_connection(guild_id=interaction.guild_id,
                                                                               user_id=interaction.user.id,
                                                                               school_name=school_name,
                                                                               class_name=class_name,
                                                                               group_name=group_name,
                                                                               token=token,
                                                                               pin=pin,
                                                                               symbol=symbol,
                                                                               channel_id=channel.id
                                                                               )
                    if not connecting[0]:
                        await message.edit(connecting[1])
                        return
                    msg: str = messages['channel_registered'].replace('{school}', school_name).replace(
                        '{class}', class_name).replace('{group}', group_name)
                    await send_message_group_channel(school_name=school_name,
                                                     class_name=class_name,
                                                     group_name=group_name,
                                                     interaction=interaction,
                                                     message=msg,
                                                     pin=True
                                                     )

                    await message.edit(connecting[1])
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

    @connect_to_vulcan.on_autocomplete("school_name")
    async def get_schools(self, interaction: discord.Interaction, school_input: str):
        await interaction.response.send_autocomplete(schools_autocompletion(interaction=interaction,
                                                                            school_input=school_input))

    @connect_to_vulcan.on_autocomplete("class_name")
    async def get_classes(self, interaction: discord.Interaction, class_name: str):
        await interaction.response.send_autocomplete(classes_autocompletion(interaction=interaction,
                                                                            class_name=class_name))

    @connect_to_vulcan.on_autocomplete("group_name")
    async def get_groups(self, interaction: discord.Interaction, group_name: str):
        await interaction.response.send_autocomplete(
            groups_autocompletion(interaction=interaction, group_name=group_name))


def setup(client):
    client.add_cog(ConnectToVulcan(client))
