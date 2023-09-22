import asyncio
import datetime as dt
from asyncio import Task

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
        self.bg_task: Task[None] = self.client.loop.create_task(self.background_tasks())

    async def background_tasks(self):
        await self.client.wait_until_ready()
        schedule: Scheduler = Scheduler()

        schedule.daily(dt.time(hour=0, minute=5), save_lucky_numbers, args=(self.client, ))
        logs_.log("Background task lucky number fetcher has been loaded")

        schedule.daily(dt.time(hour=7, minute=0), lucky_number, args=(self.client,))
        logs_.log("Background task lucky number sender has been loaded")

        schedule.cyclic(dt.timedelta(hours=1), check_lucky_number, args=(self.client,))
        logs_.log("Background task check lucky numbers has been loaded")

        # Looping background task
        while not self.client.is_closed():
            await asyncio.sleep(1)
