from os import listdir
from logs import logs_
import json


def load_config() -> dict:
    """
    Loads config file from config/config.json directory
    :return: bot config files. Token and user settings.
    """
    try:
        with open("./config/config.json", 'r', encoding="UTF-8") as file:
            config_file = json.load(file)
            logs_.log("Config files found.")
    except FileNotFoundError as error:
        logs_.log(f"{error}", True)
        logs_.log(f"Klasuś can't find its config file. Download it from gitHub and put it config/ directory", True)
        input()
        quit()
    return config_file


def load_messages() -> dict:
    """
    Loads messages file from config/lang.json directory
    :return: dictionary with all messages
    """
    try:
        with open("config/lang.json", encoding="UTF-8") as messages_file:
            messages_file = json.load(messages_file)
            logs_.log("Messages files found. Messages loaded.")
    except FileNotFoundError as error:
        logs_.log(f"{error}", True)
        logs_.log(f"Klasuś can't find its messages file. Download it from gitHub and put it config/ directory", True)
        input()
        quit()
    return messages_file


def load_cogs(client) -> None:
    """
    Loads extensions from commands and events folders. You can add as many as you want
    :param client: client of bot account from nextcord lib
    """
    logs_.log("Starting landing cogs.")
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
