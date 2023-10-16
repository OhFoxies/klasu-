import asyncio
from asyncio import Task
from threading import Thread
from typing import List

import nextcord as discord
import schedule
from .Exams import exams_sender
from .LuckyNumber import lucky_numbers_sender
from .SaveLuckyNumbers import save_and_clear_lucky_numbers
from .PrepareGroups import create_groups_chunks
from .CheckLuckyNumbers import check_lucky_number
from utils import logs_

from database.database_requests import Group


class BackgroundTasks:
    def __init__(self, client: discord.Client):
        self.client: discord.Client = client
        self.bg_task: Task[None] = self.client.loop.create_task(self.background_tasks())

    async def background_tasks(self):
        await self.client.wait_until_ready()
        logs_.log("Background task lucky numbers sender (Every day at 7:00) has been loaded")
        logs_.log("Background task exams sender (Every 5 minutes) has been loaded")
        logs_.log("Background task lucky numbers saver (Every day at 00:05) has been loaded")
        logs_.log("Background task lucky numbers checker (Every hour) has been loaded")

        # check new exams
        schedule.every(5).minutes.do(self.start_new_tasks, task=self.exams_sender_between_callbacks)

        # send lucky numbers
        schedule.every().day.at("7:00").do(self.start_new_tasks, task=self.lucky_numbers_sender_between_callbacks)

        # save lucky numbers
        schedule.every().day.at("0:05").do(self.start_new_tasks, task=self.lucky_numbers_saver_between_callbacks)

        # check lucky numbers
        schedule.every().hour.at(":00").do(self.start_new_tasks, task=self.lucky_numbers_checker_between_callbacks)

        while not self.client.is_closed():
            schedule.run_pending()
            await asyncio.sleep(1)

    @staticmethod
    def start_new_tasks(task):
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

    def exams_sender_between_callbacks(self, groups_splitted: List[Group], thread_num: int):
        asyncio.run_coroutine_threadsafe(exams_sender(groups_splitted, self.client, thread_num), self.client.loop)
