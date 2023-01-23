import nextcord
from nextcord.ext import commands


class LuckyNumber(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client

    @nextcord.slash_command(description="Returns a lucky number and ping person with it.",
                            description_localizations={
                                nextcord.Locale.pl: "Wyświetla dzisiejszy szczęśliwy numerek i "
                                                    "oznacza osobę z tym numerem"},
                            name="lucky-number",
                            name_localizations={
                                nextcord.Locale.pl: "szczesliwy_numerek"},
                            dm_permission=False,
                            force_global=True)
    async def lucky_number(self, interaction: nextcord.Interaction):
        print(f"{interaction.user} used command: lucky-number")
        number = await get_lucky_number()
        await interaction.response.send_message(f"Szczęśliwy numerek dnia dzisiejszego to: {number}", ephemeral=True)


def setup(client):
    client.add_cog(LuckyNumber(client))
