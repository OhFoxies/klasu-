from nextcord.ext import commands

from logs import logs_


class OnReady(commands.Cog):
    """
    Executes when bot is ready to use. Saves info to logs.
    """
    def __init__(self, client: commands.Bot):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        logs_.log(f"Bot is ready. Client name: {self.client.user}. Client ID: {self.client.user.id}")


def setup(client):
    client.add_cog(OnReady(client))
