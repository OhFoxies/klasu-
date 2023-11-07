import nextcord as discord
from nextcord.ext import commands

from logs import logs_
from utils import messages


class SlashCommandError(commands.Cog):
    """
    Listens for any errors caused by application command usage. Saves it to logs as ERROR, and gives Python error
    Feedback
    """
    def __init__(self, client: commands.Bot):
        self.client = client

    @commands.Cog.listener()
    async def on_application_command_error(self, interaction: discord.Interaction,
                                           error: discord.errors.ApplicationError):
        if isinstance(error, discord.errors.ApplicationError):
            await interaction.send(f"{messages['response_error']}\n"
                                                    f"```{error}```", ephemeral=True)
            logs_.log(f"Command {interaction.application_command.name} used by {interaction.user} caused error", True)
            logs_.log(f"{error}", True)


def setup(client):
    client.add_cog(SlashCommandError(client))
