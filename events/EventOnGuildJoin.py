import nextcord as discord
from nextcord.ext import commands
from database.database_requests import *
from logs import logs_


class GuildJoin(commands.Cog):
    """
    Event to save in database and in log file bot adventure in guilds.
    """
    def __init__(self, client: commands.Bot):
        self.client = client

    @commands.Cog.listener()
    async def on_guild_join(self, guild: discord.Guild):
        creation: bool = create_guild(guild_id=guild.id)
        if creation:
            logs_.log(f"I have joined to NEW guild: {guild.name} with ID: {guild.id}")
        else:
            logs_.log(f"I have joined to the guild I have already been in: {guild.name} with ID: {guild.id}")


def setup(client):
    client.add_cog(GuildJoin(client))
