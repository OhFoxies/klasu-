from datetime import datetime

import nextcord
import nextcord as discord
from nextcord.ext import commands

from database.database_requests import *


class Profile(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client

    @discord.slash_command(description="Wyświetla dane o kimś lub o tobie.",
                           name="info",
                           dm_permission=False,
                           force_global=True)
    async def me(self, interaction: discord.Interaction,
                 user: discord.Member = nextcord.SlashOption(name="użytkownik", required=False)):
        if not user:
            user: discord.Member = interaction.user
        user_data: List[Tuple[str, ...]] = get_user_data(guild_id=interaction.guild_id, user_id=user.id)
        if not user_data:
            embed: discord.Embed = discord.Embed(type="rich",
                                                 title=user.name,
                                                 colour=discord.Colour.dark_blue(),
                                                 timestamp=datetime.now(),
                                                 description="Ten użytkownik nie jest zarejestrowany do żadnej klasy! "
                                                             "Zachęć go, aby to zrobił."
                                                 if user.id != interaction.user.id else
                                                 "Nie jesteś zarejestrowany do żadnej"
                                                 "klasy. Zrób to komendą /rejestracja."
                                                 )
            embed.set_author(name=user.name, icon_url=user.avatar if user.avatar else nextcord.User.default_avatar)
            embed.set_thumbnail(url=user.avatar if user.avatar else nextcord.User.default_avatar)
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return
        embed: discord.Embed = discord.Embed(type="rich",
                                             title=user.name,
                                             colour=discord.Colour.dark_blue(),
                                             timestamp=datetime.now()
                                             )
        embed.add_field(name="Szkoła",
                        value=f"Chodzisz do szkoły: {user_data[0][1]}" if user.id == interaction.user.id
                        else f"Klasa użytkownika: {user_data[0][1]}")
        embed.add_field(name="Klasa",
                        value=f"Chodzisz do klasy: {user_data[0][0]}" if user.id == interaction.user.id
                        else f"Szkoła użytkownika: {user_data[0][0]}")
        embed.add_field(name="Grupa",
                        value=f"Twoja grupa: {user_data[0][2]}" if user.id == interaction.user.id
                        else f"Grupa użytkownika: {user_data[0][2]}")
        embed.add_field(name="Numer w dzienniku",
                        value=f"Twój numer w dzienniku: {user_data[0][3]}" if user.id == interaction.user.id
                        else f"Numer użytkownika: {user_data[0][2]}")
        embed.set_author(name=user.name, icon_url=user.avatar if user.avatar else nextcord.User.default_avatar)
        embed.set_thumbnail(url=user.avatar if user.avatar else nextcord.User.default_avatar)
        await interaction.response.send_message(embed=embed, ephemeral=True)


def setup(client):
    client.add_cog(Profile(client))
