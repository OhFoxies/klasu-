import datetime as dt
from typing import Any, AsyncIterator, Optional, List

import vulcan.data
from vulcan import Vulcan, Keystore, Account


async def get_exams_klasus(keystore, account, date_to: Optional[dt.date] = None) -> List[Optional[vulcan.data.Exam]]:
    _keystore: Any = Keystore.load(keystore)
    _account: Any = Account.load(account)
    user: Vulcan = Vulcan(account=_account, keystore=_keystore)
    await user.select_student()

    async with user:
        exams: AsyncIterator[vulcan.data.Exam] = await user.data.get_exams()
        exams_in_date: List[Optional[vulcan.data.Exam]] = []
        async for i in exams:
            if i.deadline.date >= dt.date.today():
                if date_to:
                    if i.deadline.date <= date_to:
                        exams_in_date.append(i)
                else:
                    exams_in_date.append(i)
    exams_in_date.sort(key=lambda x: x.deadline.date)
    return exams_in_date
