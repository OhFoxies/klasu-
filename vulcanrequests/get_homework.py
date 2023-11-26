import datetime as dt
from typing import Any, AsyncIterator, Optional, List

import vulcan.data
from vulcan import Vulcan, Keystore, Account


async def get_homework(keystore, account, date_to: Optional[dt.date] = None) -> List[Optional[vulcan.data.Homework]]:
    _keystore: Any = Keystore.load(keystore)
    _account: Any = Account.load(account)
    user: Vulcan = Vulcan(account=_account, keystore=_keystore)

    async with user:
        await user.select_student()
        homework: AsyncIterator[vulcan.data.Homework] = await user.data.get_homework()
        homework_in_date: List[Optional[vulcan.data.Homework]] = []
        async for i in homework:
            if i.deadline.date >= dt.date.today():
                if date_to:
                    if i.deadline.date <= date_to:
                        homework_in_date.append(i)
                else:
                    homework_in_date.append(i)
    homework_in_date.sort(key=lambda x: x.deadline.date)
    return homework_in_date
