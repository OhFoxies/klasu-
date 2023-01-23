from vulcandata.connect import account_data
from vulcan import Vulcan

# Return today lucky number (int), if today is a day with no education it returns 0.
# It uses a client object created by connect.py file.


async def get_lucky_number() -> int:
    user = Vulcan(account=account_data['account'], keystore=account_data['keystore'])
    await user.select_student()
    lucky_number = await user.data.get_lucky_number()
    await user.close()
    return lucky_number.number
