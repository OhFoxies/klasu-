import asyncio
import datetime as dt

import nextcord as discord
from nextcord.ext import commands
from scheduler.asyncio import Scheduler

from background_tasks.LuckyNumber import lucky_number
from background_tasks.SaveLuckyNumbers import save_lucky_numbers
from database.connect_to_database import connect
from utils import *


# noinspection PyTypeChecker
class Klasus(commands.Bot):
    def __init__(self, *, intents_: discord.Intents):
        super().__init__(intents=intents_, activity=discord.Game(config['activity']))
        self.bg_task = self.loop.create_task(self.lucky_number_info())
        self.bg_task = self.loop.create_task(self.lucky_number_fetch())

    async def lucky_number_fetch(self):
        await self.wait_until_ready()
        schedule_2: Scheduler = Scheduler()
        schedule_2.daily(dt.time(hour=0, minute=5), save_lucky_numbers, args=(self, ))
        while not self.is_closed():
            await asyncio.sleep(1)

    async def lucky_number_info(self):
        await self.wait_until_ready()
        schedule = Scheduler()
        schedule.daily(dt.time(hour=7, minute=0), lucky_number, args=(self,))
        while not self.is_closed():
            await asyncio.sleep(1)

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
