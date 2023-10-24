import datetime as dt
from typing import Any, AsyncIterator, Optional, List

import vulcan.data
from vulcan import Vulcan, Keystore, Account


async def get_new_exams(keystore, account) -> List[Optional[vulcan.data.Exam]]:
    _keystore: Any = Keystore.load(keystore)
    _account: Any = Account.load(account)
    user: Vulcan = Vulcan(account=_account, keystore=_keystore)

    async with user:
        await user.select_student()
        exams: AsyncIterator[vulcan.data.Exam] = await user.data.get_exams()
        exams_created_today: List[Optional[vulcan.data.Exam]] = []
        async for i in exams:
            if i.date_created.date >= dt.date.today() - dt.timedelta(days=1):
                exams_created_today.append(i)

        exams_created_today.sort(key=lambda x: x.deadline.date)
    return exams_created_today
