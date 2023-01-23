import nextcord
from nextcord.ext import commands


class SetNotifyChannel(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client

    @nextcord.slash_command(description="Sets a notify channel for lucky number and board whipers",
                            description_localizations={
                                nextcord.Locale.pl: "Ustawia kanal powiadomien o szczesliwych numerkow oraz dyzurnych"},
                            name="set_notify_channel",
                            name_localizations={
                                nextcord.Locale.pl: "kanal_powiadomien"
                            }, default_member_permissions=nextcord.Permissions(permissions=8), force_global=True)
    async def set_notify_channel(self, interaction: nextcord.Interaction):
        pass


def setup(client):
    client.add_cog(SetNotifyChannel(client))
