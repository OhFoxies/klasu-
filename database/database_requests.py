import datetime
import json
import sqlite3
from dataclasses import dataclass
from typing import List, Dict, Union, Tuple, Optional, Any

import vulcan.data


@dataclass
class User:
    school_name: str
    class_name: str
    group_name: str
    number: int


@dataclass
class VulcanData:
    keystore: dict
    account: dict


class SchoolNotFoundError(Exception):
    pass


def is_school_limit_reached(guild_id: int) -> bool:
    """
    Checks if guild with given ID has more than 25 schools saved in database.
    :param guild_id: ID of guild where command is used.
    :return: True if limit is reached, False if there's less than 25 schools.
    """
    with sqlite3.connect("database/database.db") as connection:
        command: str = "SELECT guild_id FROM `schools` WHERE guild_id=?"
        values: Tuple[str, ...] = (str(guild_id),)
        schools: List[Tuple[str, ...]] = connection.execute(command, values).fetchall()
    return True if len(schools) + 1 > 25 else False


def is_classes_limit_reached(guild_id: int, school_name: str) -> bool:
    """
    Checks if guild with given ID has more than 25 classes saved in database.
    :param school_name: name of school to get data from.
    :param guild_id: ID of guild where command is used.
    :return: True if limit is reached, False if there's less than 25 classes.
    """
    with sqlite3.connect("database/database.db") as connection:
        command: str = "SELECT guild_id FROM `classes` WHERE guild_id=? AND school_name=?"
        values: Tuple[str, ...] = (str(guild_id), school_name)
        classes: List[Tuple[str, ...]] = connection.execute(command, values).fetchall()
        return True if len(classes) + 1 > 25 else False


def is_group_limit_reached(guild_id: int, school_name: str, class_name: str) -> bool:
    """
    Checks if guild with given ID has more than 25 groups in each class.
    :param class_name: name of class to get data from.
    :param school_name: name of school to get data from.
    :param guild_id: ID of guild where command is used.
    :return: True if limit is reached, False if there's less than 25 groups.
    """
    with sqlite3.connect("database/database.db") as connection:
        command: str = "SELECT guild_id FROM `group` WHERE guild_id=? AND school_name=? AND class_name=?"
        values: Tuple[str, ...] = (str(guild_id), school_name, class_name)
        groups: List[Tuple[str, ...]] = connection.execute(command, values).fetchall()
        return True if len(groups) + 1 > 25 else False


def is_name_correct(name: str) -> bool:
    """
    Checks if given string is correct and doesn't contain any unsupported characters.
    :param name: Name to check.
    :return: True if given name is correct. False if it contains unsupported characters.
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
    Then guild_ID is saved to database.
    :param guild_id: ID of guild where bot has joined.
    :return: True if bot has joined to new guild. False if bot has joined to guild where was before.
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
    :param guild_id: ID of guild where command is used.
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
    Creates school with given name in database and assigns it to guild with given ID.
    :param guild_id: ID of guild where command is used.
    :param school_name: name of school given by user.
    """
    with sqlite3.connect("database/database.db") as connection:
        command: str = "INSERT INTO `schools` (`guild_id`, `school_name`, `lucky_number`) VALUES (?, ?, ?)"
        values: Tuple[str, ...] = (str(guild_id), school_name, "not_set")
        connection.execute(command, values)
        connection.commit()


def class_list(guild_id: int, school_name: str) -> List[str]:
    """
    :param guild_id: ID of guild where command is used.
    :param school_name: Name of school given by user.
    :return: List of classes in school.
    :raises SchoolNotFoundError: If school with given name is not found.
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
    :param guild_id: ID of guild where command is used.
    :param school_name: Name of school given by user.
    :param class_name: Name of class given by user
    """
    with sqlite3.connect("database/database.db") as connection:
        command: str = "INSERT INTO `classes` (class_name, school_name, guild_id) VALUES (?, ?, ?)"
        values: Tuple[str, ...] = (class_name, school_name, str(guild_id))
        connection.execute(command, values)
        connection.commit()


def group_list(guild_id: int, school_name: str, class_name: str) -> List[str]:
    """
    :param guild_id: ID of guild where command is used.
    :param school_name: Name of school given by user.
    :param class_name: Name of class given by user.
    :return: list of groups in class in given school.
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
    :param group_name: Name of group given by user.
    :param guild_id: ID of guild where command is used.
    :param school_name: Name of school given by user.
    :param class_name: Name of class given by user.
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
                     keystore: Dict[str, str], account: Dict[str, Union[int, str]]) -> bool:
    """
    Saves vulcan data to group .
    :param channel_id: channel id to set as group notify channel.
    :param guild_id: ID of guild where command is used.
    :param user_id: ID of user who used the command.
    :param school_name: name of school where to save data.
    :param class_name: name of class where to save data.
    :param group_name: name of group where to save data.
    :param keystore: keystore generated by vulcan-api as dict.
    :param account: account info generated by vulcan-api as dict.
    :returns: True
    """
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
    """
    Saves user info, and saves user in given group.
    :param guild_id: ID of guild where command is used.
    :param user_id: ID of user who used the command.
    :param school_name: name of school where to save data.
    :param class_name: name of class where to save data.
    :param group_name: name of group where to save data.
    :param number: user's e-grade number.
    """
    with sqlite3.connect("database/database.db") as connection:
        command: str = "INSERT INTO `user` (user_id, class_name, school_name, group_name, guild_id, number) " \
                       "VALUES (?, ?, ?, ?, ?, ?)"
        values: Tuple[str, ...] = (str(user_id), class_name, school_name, group_name, str(guild_id), str(number))
        connection.execute(command, values)
        connection.commit()


def get_user_data(user_id: int, guild_id: int) -> User | None:
    """
    Gets user data by user's ID and guild ID.
    :returns: User class. None if user is not registered

    """
    with sqlite3.connect("database/database.db") as connection:
        command: str = "SELECT class_name, school_name, group_name, number FROM `user` WHERE user_id=? AND guild_id=?"
        values: Tuple[str, str] = (str(user_id), str(guild_id))
        user_data: List[Tuple[str]] = connection.execute(command, values).fetchall()
        if not user_data:
            return None
        return User(school_name=user_data[0][1],
                    class_name=user_data[0][0],
                    group_name=user_data[0][2],
                    number=int(user_data[0][3])
                    )


def get_vulcan_data(guild_id: int, school_name: str, class_name: str, group_name: str) -> VulcanData:
    """
    Gets keystore and account data to send requests to vulcan.
    :returns: keystore and account. Every item as tuple inside list.
    """
    with sqlite3.connect("database/database.db") as connection:
        command: str = "SELECT keystore, account FROM `group` WHERE school_name=? AND class_name=? " \
                       "AND group_name=? AND guild_id=?"
        values: Tuple[str, ...] = (school_name, class_name, group_name, str(guild_id))
        vulcan_data: List[Tuple[str]] = connection.execute(command, values).fetchall()
        keystore: dict = json.loads(vulcan_data[0][0].replace("'", '"'))
        account: dict = json.loads(vulcan_data[0][1].replace("'", '"'))
        return VulcanData(keystore=keystore, account=account)


def is_group_registered(guild_id: int, school_name: str, class_name: str, group_name: str) -> bool:
    """
    Checks if group  with given name is connected to vulcan.
    :returns: True if group is connected, False if not.
    """
    with sqlite3.connect("database/database.db") as connection:
        command: str = "SELECT keystore, account FROM `group` WHERE school_name=? AND class_name=? " \
                       "AND group_name=? AND guild_id=?"
        values: Tuple[str, ...] = (school_name, class_name, group_name, str(guild_id))
        vulcan_data = connection.execute(command, values).fetchall()
        if vulcan_data[0][1] == 'not_set':
            return False
        return True


def change_group_channel(guild_id: int, channel_id: int, school_name: str, class_name: str, group_name: str) -> None:
    """
    Changes ID of group's notify channel.
    """
    with sqlite3.connect("database/database.db") as connection:
        command: str = "UPDATE `group` SET channel_id=? WHERE class_name=? AND guild_id=? AND school_name=? " \
                       "AND group_name=?"
        values: Tuple[str, ...] = (str(channel_id), class_name, str(guild_id), school_name, group_name)
        connection.execute(command, values)
        connection.commit()


def get_channel(guild_id: int, school_name: str, class_name: str, group_name: str) -> str:
    """
    :returns: ID of group's notify channel.
    """
    with sqlite3.connect("database/database.db") as connection:
        command: str = "SELECT channel_id FROM `group` WHERE class_name=? AND guild_id=? AND school_name=? " \
                       "AND group_name=?"
        values: Tuple[str, ...] = (class_name, str(guild_id), school_name, group_name)
        data: List[Tuple[str]] = connection.execute(command, values).fetchall()

        return data[0][0]


def clear_user_data(user_id: int, guild_id: int) -> None:
    """
    Clears all data of user with given ID from database.
    """
    with sqlite3.connect("database/database.db") as connection:
        command: str = "DELETE FROM user WHERE user_id=? AND guild_id=?"
        values: Tuple[str, ...] = (str(user_id), str(guild_id))
        connection.execute(command, values)
        connection.commit()


def delete_school(school_name: str, guild_id: int) -> List[str]:
    """
    Deletes school with given name in guild with given ID. Also removes all classes and groups and users registered
    in removed groups in this school.
    :returns: deleted user's ids.
    """
    with sqlite3.connect("database/database.db") as connection:
        command: str = "SELECT user_id FROM `user` WHERE school_name=? AND guild_id=?"
        values: Tuple[str, ...] = (school_name, str(guild_id))
        _deleted_users: List[Tuple[str, ...]] = connection.execute(command, values).fetchall()
        requests: List[str] = ["DELETE FROM `schools` WHERE school_name=? AND guild_id=?",
                               "DELETE FROM `classes` WHERE school_name=? AND guild_id=?",
                               "DELETE FROM `group` WHERE school_name=? AND guild_id=?",
                               "DELETE FROM `user` WHERE school_name=? AND guild_id=?"]
        for request in requests:
            connection.execute(request, values)
        connection.commit()
        deleted_users: List[str] = []
        for i in _deleted_users:
            for j in i:
                deleted_users.append(j)
        return deleted_users


def delete_class(school_name: str, guild_id: int, class_name: str) -> List[str]:
    """
    Deletes given class and groups in this class also removes all users registered in this removed groups.
    :returns: deleted user's ids.
    """
    with sqlite3.connect("database/database.db") as connection:
        command: str = "SELECT user_id FROM `user` WHERE school_name=? AND guild_id=? AND class_name=?"
        values: Tuple[str, ...] = (school_name, str(guild_id), class_name)
        _deleted_users: List[Tuple[str, ...]] = connection.execute(command, values).fetchall()
        requests: List[str] = ["DELETE FROM `classes` WHERE school_name=? AND guild_id=? AND class_name=?",
                               "DELETE FROM `group` WHERE school_name=? AND guild_id=? AND class_name=?",
                               "DELETE FROM `user` WHERE school_name=? AND guild_id=? AND class_name=?"]
        for request in requests:
            connection.execute(request, values)
        connection.commit()
        deleted_users: List[str] = []
        for i in _deleted_users:
            for j in i:
                deleted_users.append(j)
        return deleted_users


def delete_group(school_name: str, guild_id: int, class_name: str, group_name: str) -> List[str]:
    """
    Deletes given group and removes all users registered in this group.
    :returns: deleted user's ids.
    """
    with sqlite3.connect("database/database.db") as connection:
        command: str = "SELECT user_id FROM `user` WHERE school_name=? AND guild_id=? AND class_name=? AND group_name=?"
        values: Tuple[str, ...] = (school_name, str(guild_id), class_name, group_name)
        _deleted_users: List[Tuple[str, ...]] = connection.execute(command, values).fetchall()
        requests: List[str] = ["DELETE FROM `group` WHERE school_name=? AND guild_id=? AND class_name=? "
                               "AND group_name=?",
                               "DELETE FROM `user` WHERE school_name=? AND guild_id=? AND class_name=? "
                               "AND group_name=?"]
        for request in requests:
            connection.execute(request, values)
        connection.commit()
        deleted_users: List[str] = []
        for i in _deleted_users:
            for j in i:
                deleted_users.append(j)
        return deleted_users


def delete_vulcan_connection(school_name: str, guild_id: int, class_name: str, group_name: str) -> List[str]:
    """
    Disconnects Vulcan from given group by removing keystore and account and channel_id from database
    and removes all users registered in this group.
    :returns: deleted user's ids.
    """
    with sqlite3.connect("database/database.db") as connection:
        command: str = "SELECT user_id FROM `user` WHERE school_name=? AND guild_id=? AND class_name=? AND group_name=?"
        values: Tuple[str, ...] = (school_name, str(guild_id), class_name, group_name)
        _deleted_users: List[Tuple[str, ...]] = connection.execute(command, values).fetchall()
        values: Tuple[str, ...] = (school_name, str(guild_id), class_name, group_name)
        requests: List[str] = ["UPDATE `group` SET keystore='not_set', account='not_set', user_vulcan='not_set', "
                               "channel_id='not_set' WHERE school_name=? AND guild_id=? AND class_name=? "
                               "AND group_name=?",
                               "DELETE FROM `user` WHERE school_name=? AND guild_id=? AND class_name=? "
                               "AND group_name=?"]
        for request in requests:
            connection.execute(request, values)
        connection.commit()
        deleted_users: List[str] = []
        for i in _deleted_users:
            for j in i:
                deleted_users.append(j)
        return deleted_users


def get_lucky_numbers(school_name: str, guild_id: int, number: int, group_name: str, class_name: str) -> List[str]:
    """
    :returns: IDs of users with lucky number in given group.
    """
    with sqlite3.connect("database/database.db") as connection:
        command: str = "SELECT user_id FROM `user` WHERE school_name=? AND guild_id=? " \
                       "AND number=? AND group_name=? AND class_name=?"
        values: Tuple[str, ...] = (school_name, str(guild_id), str(number), group_name, class_name)
        _lucky_users: List[Tuple[str, ...]] = connection.execute(command, values).fetchall()
        lucky_users: List[str] = []
        for i in _lucky_users:
            for j in i:
                lucky_users.append(j)
        return lucky_users


def get_groups_in_school(school_name: str, guild_id: int) -> List[Tuple[str]]:
    """
    :returns: list of all groups in given school.
    """
    with sqlite3.connect("database/database.db") as connection:
        command: str = "SELECT group_name, class_name FROM `group` WHERE school_name=? AND guild_id=?"
        values: Tuple[str, ...] = (school_name, str(guild_id))
        classes: List[Tuple[str, ...]] = connection.execute(command, values).fetchall()
        return classes


def get_group_channels(school_name: str, guild_id: int) -> List[str]:
    """
    :returns: list of all group's channels ids in given school.
    """
    with sqlite3.connect("database/database.db") as connection:
        command: str = "SELECT channel_id FROM `group` WHERE school_name=? AND guild_id=?"
        values: Tuple[str, ...] = (school_name, str(guild_id))
        _channels: List[Tuple[str, ...]] = connection.execute(command, values).fetchall()
        channels: List[str] = []
        for i in _channels:
            for j in i:
                channels.append(j)
        return channels


def save_lucky_number(guild_id: int, school_name: str, number: int) -> None:
    """
    Saves daily lucky number in school in each server for optimization. By doing so bot doesn't need to connect
    everytime to Vulcan to check a lucky number.
    """
    with sqlite3.connect("database/database.db") as connection:
        command: str = "UPDATE `schools` SET `lucky_number`=? WHERE `school_name`=? AND `guild_id`=?"
        values: Tuple[str, ...] = (str(number), school_name, str(guild_id))
        connection.execute(command, values)
        connection.commit()


def get_lucky_number_in_school(guild_id: int, school_name: str) -> int | None:
    """
    :returns: lucky number in given school. Returns None if no there is no lucky number saved.
    """
    with sqlite3.connect("database/database.db") as connection:
        command: str = "SELECT `lucky_number` FROM `schools` WHERE `school_name`=? AND `guild_id`=?"
        values: Tuple[str, ...] = (school_name, str(guild_id))
        lucky_number: List[Tuple[str]] = connection.execute(command, values).fetchall()
        if lucky_number[0][0].isnumeric():
            return int(lucky_number[0][0])
        return None


# noinspection SqlWithoutWhere
def reset_lucky_number():
    """
    Clears all lucky numbers in all schools.
    """
    with sqlite3.connect("database/database.db") as connection:
        command: str = "UPDATE `schools` SET `lucky_number`='not_set'"
        connection.execute(command)
        connection.commit()


def request_mysql(req: str) -> Optional[List[Optional[Tuple[str]]]]:
    """
    Executes any Sqlite3 query to database.
    :returns: None if query is not a select, if it is, it returns fetched data
    """
    with sqlite3.connect("database/database.db") as connection:
        x: List[Any] = connection.execute(req).fetchall()
        connection.commit()
        return x


@dataclass
class Group:
    school_name: str
    class_name: str
    group_name: str
    keystore: dict
    account: dict
    guild_id: int
    channel_id: int
    id: int


def get_all_groups() -> List[Optional[Group]]:
    with sqlite3.connect("database/database.db") as connection:
        command: str = ("SELECT school_name, class_name, group_name, keystore, account, guild_id, channel_id, ID "
                        "FROM `group` WHERE keystore != 'not_set' AND account != 'not_set'")
        response: List[Any] = connection.execute(command).fetchall()
        groups: List[Group] = []
        for i in response:
            keystore: dict = json.loads(i[3].replace("'", '"'))
            account: dict = json.loads(i[4].replace("'", '"'))
            group: Group = Group(school_name=i[0],
                                 class_name=i[1],
                                 group_name=i[2],
                                 keystore=keystore,
                                 account=account,
                                 guild_id=int(i[5]),
                                 channel_id=int(i[6]),
                                 id=i[7]
                                 )
            groups.append(group)
        return groups


@dataclass
class ExamSaved:
    exam_id: int
    message_id: int
    date_modified: datetime.datetime
    deadline: datetime.date


# dt.datetime.strptime("2023-10-10 10:10:18", "%Y-%m-%d %H:%M:%S")

def get_exams_in_group(group_id: int) -> List[Optional[ExamSaved]]:
    """

    """
    with sqlite3.connect("database/database.db") as connection:
        command: str = "SELECT exam_id, message_id, date_modified, deadline FROM `exams` WHERE group_id=?"
        values: Tuple[int] = (group_id,)
        response: List[Any] = connection.execute(command, values).fetchall()
        exams: List[Optional[ExamSaved]] = []
        for i in response:
            exam: ExamSaved = ExamSaved(exam_id=i[0], message_id=i[1],
                                        date_modified=datetime.datetime.strptime(i[2], "%Y-%m-%d %H:%M:%S"),
                                        deadline=datetime.datetime.strptime(i[3], "%Y-%m-%d"))
            exams.append(exam)

        return exams


def save_exams_to_group(new_exams: List[ExamSaved],
                        group_id: int) -> None:
    """

    """
    with sqlite3.connect("database/database.db") as connection:
        command: str = "INSERT INTO exams (exam_id, group_id, message_id, date_modified, deadline, removed) VALUES (?, ?, ?, ?, ?, ?)"
        for exam in new_exams:
            values: Tuple[int, int, int, str, str, int] = (
                exam.exam_id, group_id, exam.message_id, str(exam.date_modified), str(exam.deadline), 0)
            connection.execute(command, values)
        connection.commit()


def save_changes_to_exam(exam: ExamSaved, group_id: int) -> None:
    with sqlite3.connect("database/database.db") as connection:
        command: str = "UPDATE `exams` SET date_modified=?, message_id=?, deadline=? WHERE group_id=? AND exam_id=?"
        values: Tuple[str, int, str, int, int] = (str(exam.date_modified), exam.message_id, str(exam.deadline), group_id, exam.exam_id)
        connection.execute(command, values)
        connection.commit()


def update_exam(e: vulcan.data.Exam, group_id: int) -> None:
    with sqlite3.connect("database/database.db") as connection:
        command: str = "UPDATE `exams` SET deadline=?, removed=?, date_modified=? WHERE group_id=? AND exam_id=?"
        values = (str(e.deadline.date), 0, str(e.date_modified), group_id, e.id)
        connection.execute(command, values)
        connection.commit()


def get_exam_by_id(e: int, group_id: int) -> bool:
    with sqlite3.connect("database/database.db") as connection:
        command: str = "SELECT * FROM `exams` WHERE exam_id=? AND group_id=?"
        values = (e, group_id)
        x = connection.execute(command, values).fetchall()
        if not x:
            return False
        else:
            return True


def get_old_exams(group_id: int) -> List[Optional[ExamSaved]]:
    with sqlite3.connect("database/database.db") as connection:
        command: str = "SELECT exam_id, message_id, date_modified, deadline FROM `exams` WHERE group_id=? AND removed=0"
        values = (group_id,)
        x = connection.execute(command, values).fetchall()
        old_exams: Optional[List[ExamSaved]] = []
        for exam in x:
            if datetime.datetime.strptime(exam[3], "%Y-%m-%d").date() < datetime.date.today():
                old_exams.append(ExamSaved(exam_id=exam[0],
                                           message_id=exam[1],
                                           date_modified=datetime.datetime.strptime(exam[2], "%Y-%m-%d %H:%M:%S"),
                                           deadline=datetime.datetime.strptime(exam[3], "%Y-%m-%d"))
                                 )
        return old_exams


def get_today_exams(group_id: int) -> List[Optional[ExamSaved]]:
    with sqlite3.connect("database/database.db") as connection:
        command: str = "SELECT exam_id, message_id, date_modified, deadline FROM `exams` WHERE group_id=? AND removed=0"
        values = (group_id,)
        x = connection.execute(command, values).fetchall()
        today_exams: Optional[List[ExamSaved]] = []
        for exam in x:
            if datetime.datetime.strptime(exam[3], "%Y-%m-%d").date() == datetime.date.today():
                today_exams.append(ExamSaved(exam_id=exam[0],
                                             message_id=exam[1],
                                             date_modified=datetime.datetime.strptime(exam[2], "%Y-%m-%d %H:%M:%S"),
                                             deadline=datetime.datetime.strptime(exam[3], "%Y-%m-%d"))
                                   )
        return today_exams


def remove_exam(group_id: int, exam_id: int) -> None:
    with sqlite3.connect("database/database.db") as connection:
        command: str = "UPDATE `exams` SET removed=1 WHERE group_id=? AND exam_id=?"
        values = (group_id, exam_id)
        connection.execute(command, values)
        connection.commit()
