import datetime
from typing import List

import nextcord as discord

import vulcan.data
from database.database_requests import Group
from utils import messages
from vulcan.data import Exam


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
    embed.add_field(name=messages['description'], value=exam.topic if exam.topic else messages['no_desc'], inline=False)
    return embed


def lucky_number_embed_daily(lucky_num: int, users: List[discord.Member], group: Group) -> discord.Embed:
    mentions: List[str] = [user.mention for user in users]
    embed: discord.Embed = discord.Embed(type="rich", title=messages['lucky_number_title'],
                                         color=discord.Color.green(),
                                         timestamp=datetime.datetime.now(),
                                         description=messages['lucky_number']
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
                                         description=messages['lucky_number']
                                         .replace('{school}', school_name)
                                         .replace('{number}', str(lucky_num))
                                         .replace('Użytkownik: {user}', '')
                                         )
    embed.set_author(name=user.name, icon_url=user.avatar if user.avatar else user.default_avatar)
    return embed


def connecting() -> discord.Embed:
    embed: discord.Embed = discord.Embed(type="rich", title=messages['connecting_title'],
                                         color=discord.Color.yellow(),
                                         timestamp=datetime.datetime.now(),
                                         description=messages['connecting_to_vulcan'])
    return embed


def error_embed(error: str) -> discord.Embed:
    embed: discord.Embed = discord.Embed(type="rich", title=messages['error_title'],
                                         color=discord.Color.red(),
                                         timestamp=datetime.datetime.now(),
                                         description=error)
    return embed


def registered() -> discord.Embed:
    embed: discord.Embed = discord.Embed(type="rich", title=messages['register_success'],
                                         color=discord.Color.green(),
                                         timestamp=datetime.datetime.now(),
                                         description=messages['registered'])
    return embed


def unregistered() -> discord.Embed:
    embed: discord.Embed = discord.Embed(type="rich", title=messages['unregister_title'],
                                         color=discord.Color.green(),
                                         timestamp=datetime.datetime.now(),
                                         description=messages['unregistered'])
    return embed


def no_exams() -> discord.Embed:
    embed: discord.Embed = discord.Embed(type="rich", title=messages['no_exams_title'],
                                         color=discord.Color.green(),
                                         timestamp=datetime.datetime.now(),
                                         description=messages['no_exams'])
    return embed


def any_embed(title: str, desc: str, color=discord.Color.green()) -> discord.Embed:
    embed: discord.Embed = discord.Embed(type="rich", title=title,
                                         color=color,
                                         timestamp=datetime.datetime.now(),
                                         description=desc)
    return embed


def removed_account(guild_name: str) -> discord.Embed:
    embed: discord.Embed = discord.Embed(type="rich", title=messages['account_deletion_title'],
                                         color=discord.Color.red(),
                                         timestamp=datetime.datetime.now(),
                                         description=messages['account_removed'].replace('{server}', guild_name))
    return embed


def removed_accounts(accounts: List[str]) -> discord.Embed:
    embed: discord.Embed = discord.Embed(type="rich", title=messages['accounts_deletion_title'],
                                         color=discord.Color.red(),
                                         timestamp=datetime.datetime.now(),
                                         description=messages['removed_accounts'].replace('{test}',
                                                                                          ', '.join(accounts)
                                                                                          if accounts else ""))
    return embed


def exam_deletion_embed(date: str, desc: str, exam_type: str, subject: str) -> discord.Embed:
    match exam_type.lower():
        case "sprawdzian":
            title: str = messages['deleted_exam_title']
        case "kartkówka":
            title: str = messages['deleted_short_exam_title']
        case _:
            title: str = messages['deleted_exam_title']
    embed: discord.Embed = discord.Embed(type="rich", title=title,
                                         color=discord.Color.purple(),
                                         timestamp=datetime.datetime.now(),
                                         description=messages['deleted_exam_desc']
                                         .replace('{lesson}', subject)
                                         .replace('{date}', date)
                                         .replace('{desc}', desc)
                                         if title == messages['deleted_exam_title']

                                         else
                                         messages['deleted_short_exam_desc']
                                         .replace('{lesson}', subject)
                                         .replace('{date}', date)
                                         .replace('{desc}', desc)
                                         )

    return embed


def message_embed(message: vulcan.data.Message) -> discord.Embed:
    embed = discord.Embed(type="rich", title=messages["new_message_title"],
                          color=discord.Color.blue(),
                          timestamp=datetime.datetime.now(),
                          )
    embed.add_field(name=messages['new_message_author'], value=message.sender.name, inline=False)
    embed.add_field(name=messages['new_message_theme'], value=message.subject, inline=False)
    content = (
        message.content.replace("<p><br></p>", "\n")
        .replace("<p>", "")
        .replace("</p>", "\n")
        .replace("<li>", "- ")
        .replace("</li>", "\n")
        .replace("<ol>", "")
        .replace("</ol>", "")
        .replace("<br>", "\n")
        .replace("</blockquote>", "\n")
        .replace("<blockquote>", "> ")
        .replace("<ul>", "")
        .replace("</ul>", "")
        .replace("<strong>", "**")
        .replace("</strong>", "**")
        .replace("<em>", "*")
        .replace("</em>", "*")
        .replace("<u>", "__")
        .replace("</u>", "__")
    )

    embed.add_field(name=messages['new_message_content'], value=content, inline=False)
    if message.attachments:
        attachment_format = ""
        for attachment in message.attachments:
            attachment_format += "[" + attachment.name + "]" + "(" + attachment.link + ")\n"
        embed.add_field(name=messages['attachments'], value=attachment_format, inline=False)

    embed.add_field(name=messages['new_message_date'], value=message.sent_date, inline=False)
    return embed


def no_messages() -> discord.Embed:
    embed = discord.Embed(type="rich", title=messages["no_messages"],
                          color=discord.Color.blue(),
                          timestamp=datetime.datetime.now(),
                          description=messages["no_messages_desc"]
                          )
    return embed


def role_embed() -> discord.Embed:
    embed = discord.Embed(type="rich", title=messages["role_embed"],
                          color=discord.Color.blue(),
                          timestamp=datetime.datetime.now(),
                          description=messages["role_embed_desc"]
                          )
    return embed


def homework_embed(homework: vulcan.data.Homework) -> discord.Embed:
    embed = discord.Embed(type="rich", title=homework.subject.name,
                          color=discord.Color.orange(),
                          timestamp=datetime.datetime.now())
    embed.add_field(name=messages['homework_date'], value=homework.deadline.date, inline=False)

    if homework.deadline.date == datetime.date.today():
        embed.add_field(name=messages['homework_time_left'],
                        value=messages['homework_today'],
                        inline=False)
    else:
        embed.add_field(name=messages['homework_time_left'],
                        value=f"<t:{homework.deadline.date_time.timestamp()}:R>".replace(
                            ".0", ""), inline=False)
    embed.add_field(name=messages['teacher'],
                    value=f"{homework.creator.name} {homework.creator.surname}",
                    inline=False)

    embed.add_field(name=messages['description'], value=homework.content if homework.content else messages['no_desc'],
                    inline=False)
    if homework.attachments:
        attachment_format = ""
        for attachment in homework.attachments:
            attachment_format += "[" + attachment.name + "]" + "(" + attachment.link + ")\n"
        embed.add_field(name=messages['attachments'], value=attachment_format, inline=False)

    embed.add_field(name=messages['homework_answer'],
                    value=messages['answer_required'] if homework.is_answer_required else messages[
                        'answer_no_required'], inline=False)
    return embed


def homework_deletion_embed(subject, date, desc) -> discord.Embed:
    embed: discord.Embed = discord.Embed(type="rich", title=messages['deleted_homework_title'],
                                         color=discord.Color.purple(),
                                         timestamp=datetime.datetime.now(),
                                         description=messages['deleted_homework']
                                         .replace('{subject}', subject)
                                         .replace('{date}', date)
                                         .replace('{content}', desc))

    return embed
