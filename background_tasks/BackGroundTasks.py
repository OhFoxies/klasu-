import asyncio
import datetime as dt

import nextcord as discord
from scheduler.asyncio import Scheduler

from background_tasks.CheckLuckyNumbers import check_lucky_number
from background_tasks.LuckyNumber import lucky_number
from background_tasks.SaveLuckyNumbers import save_lucky_numbers
from utils import logs_


# noinspection PyTypeChecker
class BackGroundTasks:
    def __init__(self, client: discord.Client):
        self.client: discord.Client = client
        self.bg_task = self.client.loop.create_task(self.lucky_number_info())
        self.bg_task = self.client.loop.create_task(self.lucky_number_fetch())
        self.bg_task = self.client.loop.create_task(self.check_lucky_numbers())

    async def lucky_number_fetch(self):
        logs_.log("Background task lucky number fetcher has been loaded")
        await self.client.wait_until_ready()
        schedule: Scheduler = Scheduler()
        schedule.daily(dt.time(hour=0, minute=5), save_lucky_numbers, args=(self.client, ))
        while not self.client.is_closed():
            await asyncio.sleep(1)

    async def lucky_number_info(self):
        logs_.log("Background task lucky number sender has been loaded")
        await self.client.wait_until_ready()
        schedule = Scheduler()
        schedule.daily(dt.time(hour=7, minute=0), lucky_number, args=(self.client,))
        while not self.client.is_closed():
            await asyncio.sleep(1)

    async def check_lucky_numbers(self):
        logs_.log("Background task check lucky numbers has been loaded")
        await self.client.wait_until_ready()
        schedule = Scheduler()
        schedule.cyclic(dt.timedelta(hours=1), check_lucky_number, args=(self.client,))
        while not self.client.is_closed():
            await asyncio.sleep(1)
