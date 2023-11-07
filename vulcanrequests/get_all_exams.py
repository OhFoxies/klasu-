import datetime as dt
from typing import Any, AsyncIterator, Optional, List
from dataclasses import dataclass
import vulcan.data
from vulcan import Vulcan, Keystore, Account


@dataclass
class Exams:
    new_exams: List[Optional[vulcan.data.Exam]]
    upcoming_exams: List[Optional[vulcan.data.Exam]]
    all_exams: List[Optional[vulcan.data.Exam]]


async def get_all_exams(keystore, account) -> Exams:
    _keystore: Any = Keystore.load(keystore)
    _account: Any = Account.load(account)
    user: Vulcan = Vulcan(account=_account, keystore=_keystore)

    async with user:
        await user.select_student()
        exams: AsyncIterator[vulcan.data.Exam] = await user.data.get_exams()
        exams_2_days_old: List[Optional[vulcan.data.Exam]] = []
        upcoming_exams: List[Optional[vulcan.data.Exam]] = []
        all_exams = []
        async for i in exams:
            if i.date_created.date >= dt.date.today() - dt.timedelta(days=1):
                exams_2_days_old.append(i)
            if i.deadline.date >= dt.date.today():
                upcoming_exams.append(i)
            all_exams.append(i)
        exams_2_days_old.sort(key=lambda x: x.deadline.date)
        upcoming_exams.sort(key=lambda x: x.deadline.date)

        final_exams: Exams = Exams(new_exams=exams_2_days_old, upcoming_exams=upcoming_exams, all_exams=all_exams)
    return final_exams
