import vulcan.data
from vulcan import Vulcan, Keystore, Account
from typing import Any


async def get_lucky_number(keystore, account) -> int:
    keystore_: Any = Keystore.load(keystore)
    account_: Any = Account.load(account)
    user: Vulcan = Vulcan(account=account_, keystore=keystore_)
    await user.select_student()
    lucky_number: vulcan.data.LuckyNumber = await user.data.get_lucky_number()
    await user.close()
    return lucky_number.number
