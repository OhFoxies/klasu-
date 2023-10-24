import nextcord as discord
from utils import messages
from vulcan.data import Exam
import datetime
from database.database_requests import Group
from typing import List


def exam_embed(exam: Exam) -> discord.Embed:
    match exam.type.lower():
        case "sprawdzian":
            type_formatted: str = messages['exam_form2']
        case "kartkówka":
            type_formatted: str = messages['short_test_form2']
        case _:
            type_formatted: str = "testu"
    embed: discord.Embed = discord.Embed(type="rich", title=exam.subject.name,
                                         color=discord.Color.yellow()
                                         if exam.type == "Kartkówka" else
                                         discord.Color.red(),
                                         timestamp=datetime.datetime.now()
                                         )

    embed.set_author(name=messages['new_short_test'] if exam.type.lower() == "kartkówka"
                     else messages['new_exam_normal'])
    embed.add_field(name=messages['date'].replace('{type}', type_formatted),
                    value=exam.deadline.date,
                    inline=False
                    )
    if exam.deadline.date == datetime.date.today():
        embed.add_field(name=messages['time_left'].replace('{type}', type_formatted),
                        value=messages['exam_today']
                        if exam.type.lower() == "sprawdzian" else messages['short_test_today'],
                        inline=False)
    else:
        embed.add_field(name=messages['time_left'].replace('{type}', type_formatted),
                        value=f"<t:{(exam.deadline.date_time + datetime.timedelta(hours=16)).timestamp()}:R>".replace(
                            ".0", ""), inline=False)
    embed.add_field(name=messages['teacher'],
                    value=f"{exam.creator.name} {exam.creator.surname}",
                    inline=False)
    embed.add_field(name=messages['type'], value=exam.type, inline=False)
    embed.add_field(name=messages['description'], value=exam.topic, inline=False)
    return embed


def lucky_number_embed_daily(lucky_num: int, users: List[discord.Member], group: Group) -> discord.Embed:
    mentions: List[str] = [user.mention for user in users]
    embed: discord.Embed = discord.Embed(type="rich", title=messages['lucky_number_title'],
                                         color=discord.Color.green(),
                                         timestamp=datetime.datetime.now(),
                                         description=
                                         messages['lucky_number']
                                         .replace('{school}', group.school_name)
                                         .replace('{number}', str(lucky_num))
                                         .replace('{user}', ', '.join(mentions)) if mentions else
                                         messages['lucky_number']
                                         .replace('{school}', group.school_name)
                                         .replace('{number}', str(lucky_num))
                                         .replace('{user}', messages['lucky_number_no_users'])
                                         )
    if users:
        embed.set_author(name=users[0].name, icon_url=users[0].avatar if users[0].avatar else users[0].default_avatar)

    return embed


def lucky_number_embed(lucky_num: int, user: discord.Member, school_name: str) -> discord.Embed:
    if lucky_num == 0:
        embed: discord.Embed = discord.Embed(type="rich", title=messages['lucky_number_title'],
                                             color=discord.Color.green(),
                                             timestamp=datetime.datetime.now(),
                                             description=messages['no_education'])
        embed.set_author(name=user.name, icon_url=user.avatar if user.avatar else user.default_avatar)
        return embed
    embed: discord.Embed = discord.Embed(type="rich", title=messages['lucky_number_title'],
                                         color=discord.Color.green(),
                                         timestamp=datetime.datetime.now(),
                                         description=
                                         messages['lucky_number']
                                         .replace('{school}', school_name)
                                         .replace('{number}', str(lucky_num))
                                         .replace('Użytkownik: {user}', '')
                                         )
    embed.set_author(name=user.name, icon_url=user.avatar if user.avatar else user.default_avatar)
    return embed


def connecting(user: discord.Member) -> discord.Embed:
    embed: discord.Embed = discord.Embed(type="rich", title=messages['connecting_title'],
                                         color=discord.Color.yellow(),
                                         timestamp=datetime.datetime.now(),
                                         description=messages['connecting_to_vulcan'])
    embed.set_author(name=user.name, icon_url=user.avatar if user.avatar else user.default_avatar)
    return embed
