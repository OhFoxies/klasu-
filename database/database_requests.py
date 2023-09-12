from typing import List, Dict, Union, Tuple
import sqlite3


class SchoolNotFoundError(Exception):
    pass


def is_school_limit_reached(guild_id: int) -> bool:
    """
    Checks if guild with given ID has more than 25 schools saved in database
    :param guild_id: ID of guild where command is used
    :return: True if limit is reached, False if there's less than 25 schools
    """
    with sqlite3.connect("database/database.db") as connection:
        command: str = "SELECT guild_id FROM `schools` WHERE guild_id=?"
        values: Tuple[str, ...] = (str(guild_id),)
        schools: List[Tuple[str, ...]] = connection.execute(command, values).fetchall()
    return True if len(schools) + 1 > 25 else False


def is_classes_limit_reached(guild_id: int, school_name: str) -> bool:
    """
    Checks if guild with given ID has more than 25 classes saved in database
    :param school_name: name of school to get data from
    :param guild_id: ID of guild where command is used
    :return: True if limit is reached, False if there's less than 25 classes
    """
    with sqlite3.connect("database/database.db") as connection:
        command: str = "SELECT guild_id FROM `classes` WHERE guild_id=? AND school_name=?"
        values: Tuple[str, ...] = (str(guild_id), school_name)
        classes: List[Tuple[str, ...]] = connection.execute(command, values).fetchall()
        return True if len(classes) + 1 > 25 else False


def is_group_limit_reached(guild_id: int, school_name: str, class_name: str) -> bool:
    """
    Checks if guild with given ID has more than 25 groups in each class
    :param class_name: name of class to get data from
    :param school_name: name of school to get data from
    :param guild_id: ID of guild where command is used
    :return: True if limit is reached, False if there's less than 25 groups
    """
    with sqlite3.connect("database/database.db") as connection:
        command: str = "SELECT guild_id FROM `group` WHERE guild_id=? AND school_name=? AND class_name=?"
        values: Tuple[str, ...] = (str(guild_id), school_name, class_name)
        groups: List[Tuple[str, ...]] = connection.execute(command, values).fetchall()
        return True if len(groups) + 1 > 25 else False


def is_name_correct(name: str) -> bool:
    """
    checks if given name of class, group or school is correct and doesn't contain any unsupported characters
    :param name: Name to check
    :return: True if given name is correct. False if it contains unsupported characters
    """
    name: str = name.lower()
    chars: List[str] = ['a', 'ą', 'b', 'c', 'ć', 'd', 'e', 'ę', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'ł', 'm', 'n', 'ń',
                        'o', 'ó', 'p', 'q', 'r', 's', 'ś', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'ź', 'ż', '0', '1', '2',
                        '3', '4', '5', '6', '7', '8', '9', '_']
    if not len(name) > 99:
        for i in name:
            if i not in chars:
                return False
        return True
    return False


def create_guild(guild_id: int) -> bool:
    """
    This function is caused when bot joins to any guild. It checks if bot already was in this guild or not.
    Then guild_ID is saved to database
    :param guild_id: ID of guild where bot has joined
    :return: True if bot has joined to new guild. False if bot has joined to guild where was before
    """
    with sqlite3.connect("database/database.db") as connection:
        command: str = "SELECT * FROM `guilds` WHERE guild_id=?"
        values: Tuple[str, ...] = (str(guild_id),)
        guild = connection.execute(command, values).fetchall()
        if guild:
            return False
        command: str = "INSERT INTO `guilds` (`guild_id`) VALUES (?)"
        connection.execute(command, values)
        connection.commit()
        return True


def schools_list(guild_id: int) -> List[str]:
    """
    :param guild_id: ID of guild where command is used
    :return: Returns list of schools assigned to guild with given ID.
    """
    with sqlite3.connect("database/database.db") as connection:
        command: str = "SELECT school_name FROM `schools` WHERE guild_id=?"
        values: Tuple[str, ...] = (str(guild_id),)
        schools: List[Tuple[str, ...]] = connection.execute(command, values).fetchall()
        schools_new: list = []
        for i in schools:
            for j in i:
                schools_new.append(j)
        return schools_new


def create_school(guild_id: int, school_name: str) -> None:
    """
    Creates school with given name in database and assigns it to guild with given ID
    :param guild_id: ID of guild where command is used
    :param school_name: name of school given by user
    """
    with sqlite3.connect("database/database.db") as connection:
        command: str = "INSERT INTO `schools` (`guild_id`, `school_name`) VALUES (?, ?)"
        values: Tuple[str, ...] = (str(guild_id), school_name,)
        connection.execute(command, values)
        connection.commit()


def class_list(guild_id: int, school_name: str) -> List[str]:
    """
    :param guild_id: ID of guild where command is used
    :param school_name: Name of school given by user
    :return: Raises an SchoolNotFoundError error if school with given name is not found.
    If found returns a list of classes in school
    """
    with sqlite3.connect("database/database.db") as connection:
        schools: List[str] = schools_list(guild_id=guild_id)
        classes_new: list = []
        if school_name not in schools:
            raise SchoolNotFoundError
        command: str = "SELECT class_name FROM `classes` WHERE school_name=? AND guild_id=?"
        values: Tuple[str, ...] = (school_name, str(guild_id))
        classes: List[Tuple[str, ...]] = connection.execute(command, values).fetchall()
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
    with sqlite3.connect("database/database.db") as connection:
        command: str = "INSERT INTO `classes` (class_name, school_name, guild_id) VALUES (?, ?, ?)"
        values: Tuple[str, ...] = (class_name, school_name, str(guild_id))
        connection.execute(command, values)
        connection.commit()


def group_list(guild_id: int, school_name: str, class_name: str) -> List[str]:
    """

    :param guild_id:
    :param school_name:
    :param class_name:
    :return:
    """
    with sqlite3.connect("database/database.db") as connection:
        command: str = "SELECT group_name FROM `group` WHERE guild_id=? AND school_name=? AND class_name=?"
        values: Tuple[str, ...] = (str(guild_id), school_name, class_name)
        groups: List[Tuple[str, ...]] = connection.execute(command, values).fetchall()
        groups_new: list = []
        for i in groups:
            for j in i:
                groups_new.append(j)
        return groups_new


def create_group(guild_id: int, school_name: str, class_name: str, group_name: str) -> None:
    """
    Creates a group with given name in class in school.
    :param group_name: Name of group given by user
    :param guild_id: ID of guild where command is used
    :param school_name: Name of school given by user
    :param class_name: Name of class given by user
    :return: None
    """
    with sqlite3.connect("database/database.db") as connection:
        command: str = "INSERT INTO `group` (channel_id, school_name, class_name, group_name, keystore, account, " \
                       "guild_id, user_vulcan) " \
                       "VALUES (?, ?, ?, ?, ?, ?, ?, ?)"
        values: Tuple[str, ...] = ('not_set', school_name, class_name, group_name,
                                   'not_set', 'not_set', str(guild_id), 'not_set')
        connection.execute(command, values)
        connection.commit()


def save_vulcan_data(channel_id: int, guild_id: int, user_id: int, school_name: str, class_name: str, group_name: str,
                     keystore: Dict[str, str], account: Dict[str, Union[int, str]]):
    with sqlite3.connect("database/database.db") as connection:
        command: str = "UPDATE `group` SET keystore=?, account=?, user_vulcan=?, channel_id=? WHERE class_name=? " \
                       "AND guild_id=? AND school_name=? AND group_name=?"
        values: Tuple[str, ...] = (str(keystore), str(account), str(user_id),
                                   str(channel_id), class_name, str(guild_id),
                                   school_name, group_name)
        connection.execute(command, values)
        connection.commit()
        return True


def register_user(guild_id: int, user_id: int, school_name: str, class_name: str, group_name: str, number: int) -> None:
    with sqlite3.connect("database/database.db") as connection:
        command: str = "INSERT INTO `user` (user_id, class_name, school_name, group_name, guild_id, number) " \
                       "VALUES (?, ?, ?, ?, ?, ?)"
        values: Tuple[str, ...] = (str(user_id), class_name, school_name, group_name, str(guild_id), str(number))
        connection.execute(command, values)
        connection.commit()


def get_user_data(user_id: int, guild_id: int) -> List[Tuple[str]]:
    with sqlite3.connect("database/database.db") as connection:
        command: str = "SELECT class_name, school_name, group_name, number FROM `user` WHERE user_id=? AND guild_id=?"
        values: Tuple[str, str] = (str(user_id), str(guild_id))
        data: List[Tuple[str]] = connection.execute(command, values).fetchall()
        return data


def get_vulcan_data(guild_id: int, school_name: str, class_name: str, group_name: str) -> List[Tuple[str]]:
    with sqlite3.connect("database/database.db") as connection:
        command: str = "SELECT keystore, account FROM `group` WHERE school_name=? AND class_name=? " \
                       "AND group_name=? AND guild_id=?"
        values: Tuple[str, ...] = (school_name, class_name, group_name, str(guild_id))
        vulcan_data: List[Tuple[str]] = connection.execute(command, values).fetchall()
        return vulcan_data


def is_group_registered(guild_id: int, school_name: str, class_name: str, group_name: str) -> bool:
    with sqlite3.connect("database/database.db") as connection:
        command: str = "SELECT keystore, account FROM `group` WHERE school_name=? AND class_name=? " \
                       "AND group_name=? AND guild_id=?"
        values: Tuple[str, ...] = (school_name, class_name, group_name, str(guild_id))
        vulcan_data = connection.execute(command, values).fetchall()
        if vulcan_data[0][1] == 'not_set':
            return False
        return True


def change_group_channel(guild_id: int, channel_id: int, school_name: str, class_name: str, group_name: str) -> None:
    with sqlite3.connect("database/database.db") as connection:
        command: str = "UPDATE `group` SET channel_id=? WHERE class_name=? AND guild_id=? AND school_name=? " \
                       "AND group_name=?"
        values: Tuple[str, ...] = (str(channel_id), class_name, str(guild_id), school_name, group_name)
        connection.execute(command, values)
        connection.commit()


def get_channel(guild_id: int, school_name: str, class_name: str, group_name: str) -> str:
    with sqlite3.connect("database/database.db") as connection:
        command: str = "SELECT channel_id FROM `group` WHERE class_name=? AND guild_id=? AND school_name=? " \
                       "AND group_name=?"
        values: Tuple[str, ...] = (class_name, str(guild_id), school_name, group_name)
        data: List[Tuple[str]] = connection.execute(command, values).fetchall()

        return data[0][0]


def clear_user_data(user_id: int, guild_id: int) -> None:
    with sqlite3.connect("database/database.db") as connection:
        command: str = "DELETE FROM user WHERE user_id=? AND guild_id=?"
        values: Tuple[str, ...] = (str(user_id), str(guild_id))
        connection.execute(command, values)
        connection.commit()
