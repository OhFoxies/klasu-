import datetime as dt
from typing import Any, AsyncIterator, Optional, List

import vulcan.data
from vulcan import Vulcan, Keystore, Account


async def get_new_exams(keystore, account) -> List[Optional[vulcan.data.Exam]]:
    _keystore: Any = Keystore.load(keystore)
    _account: Any = Account.load(account)
    user: Vulcan = Vulcan(account=_account, keystore=_keystore)
    await user.select_student()

    exams: AsyncIterator[vulcan.data.Exam] = await user.data.get_exams()
    exams_created_today: List[Optional[vulcan.data.Exam]] = []
    async for i in exams:
        if i.date_created.date >= dt.date.today()-dt.timedelta(days=1):
            exams_created_today.append(i)

    swapped: bool = False
    for n in range(len(exams_created_today.copy()) - 1, 0, -1):
        for i in range(n):
            if exams_created_today[i].deadline.date > exams_created_today[i + 1].deadline.date:
                swapped = True
                exams_created_today[i], exams_created_today[i + 1] = exams_created_today[i + 1], exams_created_today[i]
        if not swapped:
            return exams_created_today
    await user.close()
    return exams_created_today
