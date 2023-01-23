import nextcord
from nextcord.ext import commands


class Register(commands.Cog):
    def __int__(self, client: commands.Bot):
        self.client = client

    @nextcord.slash_command(description="Adds you to the database. So you can be mentioned.",
                            description_localizations={
                                nextcord.Locale.pl: "Dodaje cię do bazy danych dzięki czemu będziesz pingowany."},
                            name="registration",
                            name_localizations={nextcord.Locale.pl: "rejestracja"}, dm_permission=False,
                            force_global=True)
    async def registration(self, interaction: nextcord.Interaction,
                           name: str = nextcord.SlashOption(name="name",
                                                            name_localizations={nextcord.Locale.pl: "imie"},
                                                            description="Your name",
                                                            description_localizations={
                                                                nextcord.Locale.pl: "twoje imie"},
                                                            required=True),
                           second_name: str = nextcord.SlashOption(name="second_name",
                                                                   name_localizations={nextcord.Locale.pl: "nazwisko"},
                                                                   description="Your second name",
                                                                   description_localizations={
                                                                       nextcord.Locale.pl: "twoje nazwisko"},
                                                                   required=True),
                           number: int = nextcord.SlashOption(name="egradebook_number",
                                                              name_localizations={
                                                                  nextcord.Locale.pl: "numer_w_dzienniku"},
                                                              description="Your egrade book number",
                                                              description_localizations={
                                                                  nextcord.Locale.pl: "twoj numer w dziennku"},
                                                              required=True)):
        print(f"{interaction.user} used command: register")
        await interaction.response.send_message(f"{name} {second_name}, {number}", ephemeral=True)


def setup(client):
    client.add_cog(Register(client))
