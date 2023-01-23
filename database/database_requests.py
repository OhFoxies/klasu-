from database.connect_to_database import cursor
from typing import List


def is_school_limit_reached(guild_id: int) -> bool:
    """
    Checks if guild with given ID has more than 10 schools saved in database
    :param guild_id: ID of guild where command is used
    :return: True if limit is reached, False if there's less than 10 schools
    """
    command = "SELECT guild_id FROM `schools` WHERE guild_id=?"
    values = (str(guild_id), )
    schools = cursor.execute(command, values).fetchall()
    return True if len(schools) + 1 > 10 else False


def is_classes_limit_reached(guild_id: int, school_name: str) -> bool:
    """
    Checks if guild with given ID has more than 50 classes saved in database
    :param school_name: name of school to get data from
    :param guild_id: ID of guild where command is used
    :return: True if limit is reached, False if there's less than 50 classes
    """
    command = "SELECT guild_id FROM `classes` WHERE guild_id=? AND school_name=?"
    values = (str(guild_id), school_name)
    classes = cursor.execute(command, values).fetchall()
    return True if len(classes) + 1 > 50 else False


def is_name_correct(name: str, guild_id: int) -> bool:
    """
    checks if given name of class, group or school is correct and doesn't contain any unsupported characters
    :param name: Name to check
    :param guild_id: ID of guild where command is used
    :return: True if given name is correct. False if it contains unsupported characters
    """
    name = name.lower()
    chars = ['a', 'ą', 'b', 'c', 'ć', 'd', 'e', 'ę', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'ł', 'm', 'n', 'ń', 'o', 'ó',
             'p', 'q', 'r', 's', 'ś', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'ź', 'ż', '0', '1', '2', '3', '4', '5', '6',
             '7', '8', '9', '_']
    if len(name) > 99 or name.endswith(f"_{guild_id}"):
        return False
    for i in name:
        if i not in chars:
            return False
    return True


class SchoolNotFoundError(Exception):
    pass


def create_guild(guild_id: int) -> bool:
    """
    This function is caused when bot joins to any guild. It checks if bot already was in this guild or not.
    Then guild_ID is saved to database
    :param guild_id: ID of guild where bot has joined
    :return: True if bot has joined to new guild. False if bot has joined to guild where was before
    """

    command = "SELECT * FROM `guilds` WHERE guild_id=?"
    values = (str(guild_id), )
    guild = cursor.execute(command, values).fetchall()
    if guild:
        return False
    command = "INSERT INTO `guilds` (`guild_id`) VALUES (?)"
    cursor.execute(command, values)
    cursor.commit()
    return True


def create_school(guild_id: int, school_name: str) -> bool:
    """
    Creates school with given name in database and assigns it to guild with given id
    :param guild_id: ID of guild where command is used
    :param school_name: name of school given by user
    :return: True if school with this name already exists. False if it doesn't
    """
    command = "SELECT * FROM `schools` WHERE guild_id=? AND school_name=?"
    values = (str(guild_id), school_name)
    schools = cursor.execute(command, values).fetchall()
    if schools:
        return True
    command = "INSERT INTO `schools` (`guild_id`, `school_name`) VALUES (?, ?)"
    values = (str(guild_id), school_name,)
    cursor.execute(command, values)
    cursor.commit()
    return False


def schools_list(guild_id: int) -> List[str]:
    """
    :param guild_id: ID of guild where command is used
    :return: Returns list of schools assigned to guild with given ID.
    """
    command = "SELECT school_name FROM `schools` WHERE guild_id=?"
    values = (str(guild_id), )
    schools = cursor.execute(command, values).fetchall()
    schools_new = []
    for i in schools:
        for j in i:
            schools_new.append(j)
    return schools_new


def class_list(guild_id: int, school_name: str) -> List[str]:
    """
    :param guild_id: ID of guild where command is used
    :param school_name: Name of school given by user
    :return: Raises an SchoolNotFoundError error if school with given name is not found.
    If found returns a list of classes in school
    """
    schools = schools_list(guild_id=guild_id)
    classes_new = []
    if school_name not in schools:
        raise SchoolNotFoundError
    command = "SELECT class_name FROM `classes` WHERE school_name=? AND guild_id=?"
    values = (school_name, str(guild_id))
    classes = cursor.execute(command, values).fetchall()
    for i in classes:
        for j in i:
            classes_new.append(j)
    return classes_new


def create_class(guild_id: int, school_name: str, class_name: str) -> None:
    """
    Creates a class with given name in school.
    :param guild_id: ID of guild where command is used
    :param school_name: Name of school given by user
    :param class_name: Name of class given by user
    :return: None
    """
    command = "INSERT INTO `classes` (class_name, school_name, guild_id) VALUES (?, ?, ?)"
    values = (class_name, school_name, str(guild_id))
    cursor.execute(command, values)
    cursor.commit()
