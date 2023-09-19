import nextcord as discord
from nextcord.ext import commands
from database.database_requests import request


class RequestCommand(commands.Cog):
    def __int__(self, client: commands.Bot):
        self.client = client

    @discord.slash_command(description="Wykonuje request do bazy danych tylko wlasciciel",
                           name="mysql",
                           dm_permission=False,
                           force_global=True)
    async def request_command(self, interaction: discord.Interaction,
                           request_promt: str = discord.SlashOption(name="request",
                                                                  description="Zapytanie do wykonania",
                                                                  required=True)):
        if interaction.user.id == 863422015226249238:
            wzium = request(request_promt)
            interaction.response.send_message(wzium)
        else:
            interaction.response.send_message("Nie mo")


def setup(client):
    client.add_cog(RequestCommand(client))
