import sys
from os import listdir
from logs import logs_
import json
from typing import Dict


def load_config() -> Dict[str, str]:
    """
    Loads config file from config/config.json directory
    :return: bot config files. Token and user settings.
    """
    config_syntax: Dict[str, str] = {
        "token": "Your bot token here ",
        "activity": "Any activity",
    }
    logs_.log("Trying to read config files")
    with open("./config/config.json", 'r+', encoding="UTF-8") as file:
        try:
            config_file: Dict[str, str] = json.load(file)
        except json.JSONDecodeError:
            print("Something is wrong with your config. ")
            input()
            sys.exit()
        if list(config_syntax.keys()) != list(config_file.keys()):
            logs_.log("Updating config files...")
            missing = [i for i in list(config_syntax.keys()) if i not in list(config_file.keys())]

            for i in missing:
                config_file[i] = config_syntax[i]
                logs_.log(f"Please check out new value in config.json file: {i}")
            logs_.log(f"Config files have been updated. Please enter values in new options.")
            print("Press ENTER to close the program")
            input()
            sys.exit()

    with open("./config/config.json", 'w', encoding="UTF-8") as file:
        json.dump(config_file, file, indent=4)
    logs_.log("Config files loaded")
    return config_file


def load_messages() -> Dict[str, str]:
    """
    Loads messages file from config/lang.json directory
    :return: dictionary with all messages
    """
    try:
        with open("config/lang.json", encoding="UTF-8") as file:
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
messages = load_messages()
config = load_config()
