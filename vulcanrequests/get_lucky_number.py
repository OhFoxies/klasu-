from vulcan import Vulcan, Keystore, Account


async def get_lucky_number(keystore, account) -> int:
    keystore_ = Keystore.load(keystore)
    account_ = Account.load(account)
    user = Vulcan(account=account_, keystore=keystore_)
    await user.select_student()
    lucky_number = await user.data.get_lucky_number()
    await user.close()
    return lucky_number.number
