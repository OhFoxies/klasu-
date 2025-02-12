import asyncio
import datetime as dt
from asyncio import Task
from threading import Thread
from typing import List, Any

import nextcord as discord
from scheduler import Scheduler

from database.database_requests import Group
from helpers.create_groups_chunks import create_groups_chunks
from utils import logs_
from .check_lucky_numbers import check_lucky_number
from .cyclic_data_handler import CyclicDataSender
from .date_updates import UpdateDates
from .lucky_number import lucky_numbers_sender
from .save_lucky_numbers import save_and_clear_lucky_numbers


class BackgroundTasks:
    def __init__(self, client: discord.Client):
        self.client: discord.Client = client
        self.bg_task: Task[None] = self.client.loop.create_task(self.background_tasks())

    async def background_tasks(self):
        await self.client.wait_until_ready()
        schedule = Scheduler()

        schedule.daily(dt.time(hour=0, minute=10), self.start_new_tasks,
                       args=(self.update_dates_between_callbacks,))
        logs_.log("Date updater loaded (Every day at 00:10) has been loaded")

        schedule.cyclic(dt.timedelta(minutes=5), self.start_new_tasks, args=(
            self.cyclic_data_between_callbacks,))
        logs_.log("Background cyclic data handler (Every 5 minutes) has been loaded")

        schedule.daily(dt.time(hour=7, minute=0), self.start_new_tasks, args=(
            self.lucky_numbers_sender_between_callbacks,))
        logs_.log("Background task lucky numbers sender (Every day at 7:00) has been loaded")

        schedule.hourly(dt.time(minute=0, second=0), self.start_new_tasks, args=(
            self.lucky_numbers_checker_between_callbacks,))
        logs_.log("Background task lucky numbers checker (Every hour) has been loaded")

        schedule.daily(dt.time(hour=0, minute=5), self.start_new_tasks, args=(
            self.lucky_numbers_saver_between_callbacks,))
        logs_.log("Background task lucky numbers saver (Every day at 00:05) has been loaded")

        while not self.client.is_closed():
            schedule.exec_jobs()
            await asyncio.sleep(1)

    @staticmethod
    def start_new_tasks(task: Any):
        groups = create_groups_chunks()

        if not groups:
            return

        for i in range(len(groups)):
            thread: Thread = Thread(target=task, args=[groups[i], i])
            thread.start()

    def lucky_numbers_sender_between_callbacks(self, groups_splitted: List[Group], thread_num: int):
        asyncio.run_coroutine_threadsafe(lucky_numbers_sender(groups_splitted,
                                                              self.client,
                                                              thread_num),
                                         self.client.loop)

    def lucky_numbers_saver_between_callbacks(self, groups_splitted, thread_num: int):
        asyncio.run_coroutine_threadsafe(save_and_clear_lucky_numbers(groups_splitted, thread_num), self.client.loop)

    def lucky_numbers_checker_between_callbacks(self, groups_splitted, thread_num: int):
        asyncio.run_coroutine_threadsafe(check_lucky_number(groups_splitted, thread_num), self.client.loop)

    def cyclic_data_between_callbacks(self, groups_splitted: List[Group], thread_num: int):
        cyclic_data_handler: CyclicDataSender = CyclicDataSender(thread_num=thread_num, client=self.client,
                                                                 groups=groups_splitted)
        asyncio.run_coroutine_threadsafe(cyclic_data_handler.handle_data(), self.client.loop)

    def update_dates_between_callbacks(self, groups_splitted: List[Group], thread_num: int):
        dates_updater = UpdateDates(thread_num=thread_num, groups=groups_splitted, client=self.client)
        asyncio.run_coroutine_threadsafe(dates_updater.update_dates(), self.client.loop)
