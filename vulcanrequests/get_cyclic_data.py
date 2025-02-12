import datetime as dt
from typing import AsyncIterator, Optional, List
import vulcan.data
from vulcan import Vulcan, Keystore, Account
from vulcanrequests.serializables import Exams, Homeworks


class CyclicDataGetter:
    def __init__(self, keystore, account):
        self.account = Account.load(account)
        self.keystore = Keystore.load(keystore)
        self.exams: Exams = ...
        self.messages: List[Optional[vulcan.data.Message]] = []
        self.homeworks: Homeworks = ...
        self.user: Vulcan = Vulcan(keystore=self.keystore, account=self.account)

    async def create_data(self):
        async with self.user:
            await self.user.select_student()
            await self.get_exams_data()
            await self.messages_data()
            await self.homework_data()

    async def get_exams_data(self):
        exams: AsyncIterator[vulcan.data.Exam] = await self.user.data.get_exams()
        exams_2_days_old: List[Optional[vulcan.data.Exam]] = []
        upcoming_exams: List[Optional[vulcan.data.Exam]] = []
        all_exams: List[Optional[vulcan.data.Exam]] = []
        async for i in exams:
            if i.date_created.date >= dt.date.today() - dt.timedelta(days=1):
                exams_2_days_old.append(i)
            if i.deadline.date >= dt.date.today():
                upcoming_exams.append(i)
            all_exams.append(i)
        exams_2_days_old.sort(key=lambda x: x.deadline.date)
        upcoming_exams.sort(key=lambda x: x.deadline.date)

        self.exams = Exams(new_exams=exams_2_days_old, upcoming_exams=upcoming_exams, all_exams=all_exams)

    async def messages_data(self):
        boxes = await self.user.data.get_message_boxes()
        async for i in boxes:
            messages = await self.user.data.get_messages(i.global_key)
            async for message in messages:
                if message.sent_date.date_time >= dt.datetime.today() - dt.timedelta(days=1):
                    self.messages.append(message)

    async def homework_data(self):
        homework: AsyncIterator[vulcan.data.Homework] = await self.user.data.get_homework()

        homework_2_day_old: List[Optional[vulcan.data.Homework]] = []
        all_homework: List[Optional[vulcan.data.Homework]] = []

        async for i in homework:
            if i.date_created.date >= dt.date.today() - dt.timedelta(days=1):
                homework_2_day_old.append(i)
            all_homework.append(i)

        homework_2_day_old.sort(key=lambda x: x.deadline.date)
        all_homework.sort(key=lambda x: x.deadline.date)
        self.homeworks = Homeworks(all_homeworks=all_homework, new_homeworks=homework_2_day_old)
