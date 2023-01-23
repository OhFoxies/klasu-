import vulcan
import os
import asyncio

# Returns keystore and account objects used to create Vulcan object.
# Done by using vulcandata: https://github.com/kapi2289/vulcan-api
# Function first checks if user has already createad API key if not then function starts creating process with logs
# given by a user. It's very important do don't make a mistake while giving logs if mistake is done then bot won't work
# if function returns vulcandata error then that means you gave wrong logs.


async def create_keystore_and_account() -> (vulcan.Account, vulcan.Account):
    while True:
        try:
            with open("vulcandata/keystore/keystore.json", 'r') as file:
                keystore = vulcan.Keystore.load(file)
                break
        except FileNotFoundError:
            name = input("Jaką chcesz wyświetlać nazwę urządzenia w dziennku?: ")
            keystore = await vulcan.Keystore.create(device_model=name)
            with open("vulcandata/keystore/keystore.json", 'w') as file:
                file.write(keystore.as_json)
            continue

    while True:
        try:
            with open("vulcandata/account/account.json", 'r') as file:
                account = vulcan.Account.load(file)
                break
        except FileNotFoundError:
            print("Nie odnaleziono pliku z danymi o koncie! Musimy go utworzyć.\n"
                  "Zaloguj się na swoję konto na dzienniku, przejdź do zakładki uczeń.\n"
                  "Następnie do zakładki 'dostęp mobilny'. Klinij niebieski przycisk 'dodaj urządzenie'.\n"
                  "Wyświetlą Ci się różne dane. Przepisuj je po kolei do programu i klikaj enter.")
            token = input("Wpisz token: ")
            symbol = input("Wpisz symbol konta: ")
            pin = input("Wpisz pin: ")
            print("Sprawdzam dane")
            # noinspection PyProtectedMember
            try:
                account = await vulcan.Account.register(keystore, token, symbol, pin)
                with open("vulcandata/account/account.json", 'w') as file:
                    file.write(account.as_json)
                break
            except (vulcan._exceptions.InvalidTokenException, vulcan._exceptions.InvalidPINException,
                    vulcan._exceptions.InvalidSymbolException, vulcan._exceptions.ExpiredTokenException):
                print("Podane informacje są nie prawidłowe! Zacznij od nowa. (Odświerz strone).")
                input("Nacisnij enter aby zacząc od nowa.")
                os.system("cls")
                continue
    return {"keystore": keystore, "account": account}


loop = asyncio.get_event_loop()
account_data = loop.run_until_complete(create_keystore_and_account())
