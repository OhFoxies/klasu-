import nextcord as discord
from utils import messages
from vulcan.data import Exam
import datetime
import time


def exam_embed(exam: Exam) -> discord.Embed:
    match exam.type.lower():
        case "sprawdzian":
            type_formatted: str = messages['exam_form2']
        case "kartkówka":
            type_formatted: str = messages['short_test_form2']
        case _:
            type_formatted: str = "testu"
    embed: discord.Embed = discord.Embed(type="rich", title=exam.subject.name,
                                         color=discord.Color.green()
                                         if exam.type == "Kartkówka" else
                                         discord.Color.red(),
                                         timestamp=datetime.datetime.now()
                                         )

    embed.set_author(name="Nowa kartkówka! :(" if exam.type.lower() == "kartkówka"
                     else "Nowy sprawdzian! :(")
    embed.add_field(name=messages['date'].replace('{type}', type_formatted),
                    value=exam.deadline.date,
                    inline=False
                    )
    if exam.deadline.date == datetime.date.today():
        embed.add_field(name=messages['time_left'].replace('{type}', type_formatted),
                        value="Ten sprawdzian jest dzisiaj!"
                        if exam.type.lower() == "sprawdzian" else "Ta kartkówka jest dzisiaj!",
                        inline=False)
    else:
        embed.add_field(name=messages['time_left'].replace('{type}', type_formatted),
                        value=f"<t:{(exam.deadline.date_time + datetime.timedelta(hours=12)).timestamp()}:R>".replace(".0", ""), inline=False)
        # embed.add_field(name=messages['time_left'].replace('{type}', type_formatted),
        #                 value=f"{exam.deadline.date - datetime.date.today()}".replace(", 0:00:00", "")
        #                 .replace("days", "dni")
        #                 .replace("day", "dzień")
        #                 .replace("month", "miesiąc")
        #                 .replace("months", "miesięcy"),
        #                 inline=False)
    embed.add_field(name=messages['teacher'],
                    value=f"{exam.creator.name} {exam.creator.surname}",
                    inline=False)
    embed.add_field(name=messages['type'], value=exam.type, inline=False)
    embed.add_field(name=messages['description'], value=exam.topic, inline=False)
    return embed
