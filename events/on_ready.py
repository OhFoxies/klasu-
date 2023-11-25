from nextcord.ext import commands

from logs import logs_
from database.database_requests import get_all_views
from commands.admin_send_role_message import Button


class OnReady(commands.Cog):
    """
    Executes when bot is ready to use. Saves info to logs.
    """
    def __init__(self, client: commands.Bot):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        views = get_all_views()
        for msg_id in views:
            self.client.add_view(Button(), message_id=msg_id)
        logs_.log(f"Bot is ready. Client name: {self.client.user}. Client ID: {self.client.user.id}")


def setup(client):
    client.add_cog(OnReady(client))
