from typing import Tuple

from database.database_requests import save_vulcan_data
from utils import messages
from vulcan import Keystore, Account
# noinspection PyProtectedMember
from vulcan._exceptions import (ExpiredTokenException,
                                InvalidTokenException,
                                InvalidSymbolException,
                                InvalidPINException,
                                VulcanAPIException
                                )


async def create_new_connection(guild_id: int,
                                user_id: int,
                                school_name: str,
                                class_name: str,
                                group_name: str,
                                pin: str,
                                symbol: str,
                                token: str,
                                channel_id: int) -> Tuple[bool, str]:
    device_name: str = 'klasus_' + school_name.lower() + '_' + class_name.lower() + '_' + group_name.lower()
    keystore: Keystore = await Keystore.create(device_model=device_name)
    try:
        account: Account = await Account.register(keystore=keystore,
                                                  token=token,
                                                  pin=pin,
                                                  symbol=symbol
                                                  )
        saving: bool = save_vulcan_data(guild_id=guild_id,
                                        user_id=user_id,
                                        school_name=school_name,
                                        class_name=class_name,
                                        group_name=group_name,
                                        keystore=keystore.as_dict,
                                        account=account.as_dict,
                                        channel_id=channel_id
                                        )
        if saving:
            return True, messages['vulcan_connected']
        return False, messages['vulcan_wtf']
    except ExpiredTokenException:
        return False, messages['token_expired']
    except InvalidTokenException:
        return False, messages['wrong_token']
    except InvalidSymbolException:
        return False, messages['wrong_symbol']
    except InvalidPINException:
        return False, messages['wrong_pin']
    except VulcanAPIException:
        return False, messages['api_error']
    except Exception as err:
        return False, str(err)
