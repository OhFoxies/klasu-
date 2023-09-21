import bcrypt
import nextcord as discord
from nextcord.ext import commands

from database.database_requests import request_mysql
from utils import messages, config


class RequestCommand(commands.Cog):
    def __int__(self, client: commands.Bot):
        self.client = client

    @discord.slash_command(description="Wykonuje request do bazy danych bota.",
                           name="mysql",
                           dm_permission=False,
                           force_global=True)
    async def request_command(self, interaction: discord.Interaction,
                              password: str = discord.SlashOption(name="password",
                                                                  description="Hasło do bazy danych",
                                                                  required=True),
                              queri: str = discord.SlashOption(name="request",
                                                               description="Zapytanie do wykonania",
                                                               required=True)):
        password = str.encode(password)
        hashed_password = str.encode(config['database_password'][7:])
        try:
            if bcrypt.checkpw(password, hashed_password) and interaction.user.id == int(config['owner_id']):
                request_return = request_mysql(queri)
                await interaction.response.send_message(messages['done_request'].replace(
                    '{answer}', str(request_return)), ephemeral=True)
            await interaction.response.send_message(messages['wrong_pass'], ephemeral=True)
        except ValueError:
            await interaction.response.send_message(messages['config_error'], ephemeral=True)


def setup(client):
    client.add_cog(RequestCommand(client))
