import nextcord as discord
from nextcord.ext import commands

from background_tasks.BackGroundTasks import BackGroundTasks
from database.connect_to_database import connect
from utils import *


# noinspection PyTypeChecker
class Klasus(commands.Bot):
    def __init__(self, *, intents_: discord.Intents):
        super().__init__(intents=intents_, activity=discord.Game(config['activity']))
        self.bg_tasks: BackGroundTasks = BackGroundTasks(self)

    def start_bot(self):
        logs_.log("Staring bot.")
        connect()
        load_cogs(self)
        self.run(config["token"])


if __name__ == "__main__":
    intents: discord.Intents = discord.Intents.default()
    intents.all()
    client: Klasus = Klasus(intents_=intents)
    try:
        client.start_bot()
    except discord.LoginFailure:
        logs_.log("Your bot's token's incorrect. Check config file!", is_error=True)
        logs_.log("Press enter to exit!", is_error=True)
        input()
        sys.exit()
