import nextcord as discord
from nextcord.ext import commands
from database.database_requests import *
from utils import messages
from autcompletion.AutoCompletions import schools_autocompletion


class AddClass(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client

    @discord.slash_command(name="dodaj-klase",
                           description="Tworzy klasę w podanej szkole",
                           dm_permission=False,
                           force_global=True,
                           default_member_permissions=discord.Permissions(permissions=8))
    async def add_class(self, interaction: discord.Interaction,
                        school_name: str = discord.SlashOption(name="nazwa_szkoly",
                                                               description="Nazwa szkoly ktora wczesniej utworzyles",
                                                               required=True),
                        class_name: str = discord.SlashOption(name="nazwa_klasy",
                                                              required=True)):
        if not is_name_correct(name=school_name):
            await interaction.response.send_message(f"{messages['school_bad_name']}", ephemeral=True)
            return
        if not is_name_correct(name=class_name):
            await interaction.response.send_message(f"{messages['class_bad_name']}", ephemeral=True)
            return
        try:
            classes = class_list(guild_id=interaction.guild_id, school_name=school_name)
            if class_name not in classes:
                if is_classes_limit_reached(guild_id=interaction.guild_id, school_name=school_name):
                    await interaction.response.send_message(f"{messages['limit_classes']}", ephemeral=True)
                    return
                create_class(guild_id=interaction.guild_id, class_name=class_name, school_name=school_name)
                response_message = messages['class_created'].replace("{name}", class_name)
                await interaction.response.send_message(response_message.replace("{school_name}", school_name),
                                                        ephemeral=True)
                return
            response_message = messages['class_name_exists'].replace("{school_name}", school_name)
            await interaction.response.send_message(response_message.replace("{name}", class_name), ephemeral=True)
        except SchoolNotFoundError:
            await interaction.response.send_message(f"{messages['school_not_found']}".replace("{name}", school_name),
                                                    ephemeral=True)

    @add_class.on_autocomplete("school_name")
    async def get_schools(self, interaction: discord.Interaction, school_input: str):
        await interaction.response.send_autocomplete(schools_autocompletion(interaction=interaction,
                                                                            school_input=school_input))


def setup(client):
    client.add_cog(AddClass(client))
