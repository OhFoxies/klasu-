from typing import Any

import vulcan.data
from vulcan import Vulcan, Keystore, Account


async def get_lucky_number(keystore, account) -> int:
    keystore_: Any = Keystore.load(keystore)
    account_: Any = Account.load(account)
    user: Vulcan = Vulcan(account=account_, keystore=keystore_)
    async with user:
        await user.select_student()
        lucky_number: vulcan.data.LuckyNumber = await user.data.get_lucky_number()
    return lucky_number.number
