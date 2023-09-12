from utils import *
from logs import logs_
from database.connect_to_database import connect
import nextcord as discord
from nextcord.ext import commands


class Klasus(commands.Bot):
    def __init__(self, *, intents_: discord.Intents):
        super().__init__(intents=intents_, activity=discord.Game(config['activity']))

    def start_bot(self):
        logs_.log("Staring bot.")
        connect()
        load_cogs(self)
        self.run(config["token"])


if __name__ == "__main__":
    intents: discord.Intents = discord.Intents.default()
    intents.all()
    client: Klasus = Klasus(intents_=intents)
    client.start_bot()
