import json
import os.path
import sys
from os import listdir
from typing import Dict, List

import bcrypt

from logs import logs_


def load_config() -> Dict[str, str]:
    """
    Loads config file from config/config.json directory
    :return: bot config files. Token and user settings.
    """
    config_syntax: Dict[str, str] = {
        "token": "Your bot token here ",
        "activity": "Any activity",
        "//comment": "Your password will be hashed after running the bot",
        "database_password": "any_password",
        "owner_id": "id_of_your_account"
    }
    logs_.log("Trying to read config files")
    if not os.path.isfile("./config/config.json"):
        with open("./config/config.json", 'w', encoding="utf-8") as file:
            json.dump(config_syntax, file, indent=4)
            logs_.log(f"Config files have been updated. Please enter values in new options.")
            print("Press ENTER to close the program")
            input()
            sys.exit()
    with open("./config/config.json", 'r+', encoding="utf-8") as file:
        try:
            config_file: Dict[str, str] = json.load(file)
        except json.JSONDecodeError:
            print("Something is wrong with your config. ")
            input()
            sys.exit()
        if list(config_syntax.keys()) != list(config_file.keys()):
            logs_.log("Updating config files...")
            missing: List[str] = [i for i in list(config_syntax.keys()) if i not in list(config_file.keys())]

            if missing:
                for i in missing:
                    config_file[i] = config_syntax[i]
                    logs_.log(f"Please check out new value in config.json file: {i}")
                with open("./config/config.json", 'w', encoding="utf-8") as file_:
                    json.dump(config_file, file_, indent=4)
                logs_.log(f"Config files have been updated. Please enter values in new options.")
                print("Press ENTER to close the program")
                input()
                sys.exit()

    password = config_file['database_password']
    if password == 'any_password' or password == "":
        logs_.log("Set up your password!", is_error=True)
        print("Press ENTER to close the program")
        input()
        sys.exit()
    if not password.startswith('hashed='):
        salt: bytes = bcrypt.gensalt()
        hashed: bytes = bcrypt.hashpw(str.encode(password), salt)
        config_file['database_password'] = 'hashed=' + str(hashed)[2:-1]
    with open("./config/config.json", 'w', encoding="utf-8") as file:
        json.dump(config_file, file, indent=4)

    logs_.log("Config files loaded")
    return config_file


def load_messages() -> Dict[str, str]:
    """
    Loads messages file from config/lang.json directory
    :return: dictionary with all messages
    """
    try:
        with open("config/lang.json", encoding="utf-8") as file:
            messages_file: Dict[str, str] = json.load(file)
            logs_.log("Messages files found. Messages loaded.")
    except FileNotFoundError as error:
        logs_.log(f"{error}", True)
        logs_.log(f"Klasuś can't find its messages file. Download it from gitHub and put it config/ directory", True)
        input()
        sys.exit()
    return messages_file


def load_cogs(client) -> None:
    """
    Loads extensions from commands and events folders. You can add as many as you want
    :param client: client of bot account from nextcord lib
    """
    logs_.log("Starting loading cogs.")
    for event in listdir('./events'):
        if event.endswith('.py'):
            client.load_extension(f'events.{event[:-3]}')
            logs_.log(f"Loaded event extension {event[:-3]}")

    for command in listdir(f'./commands'):
        if command.endswith('.py'):
            client.load_extension(f'commands.{command[:-3]}')
            logs_.log(f"Loaded command extension {command[:-3]}")


# Creating messages and config dictionaries for usage in other files.
messages: Dict[str, str] = load_messages()
config: Dict[str, str] = load_config()
