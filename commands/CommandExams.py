import datetime
import json

import nextcord as discord
from nextcord.ext import commands

from database.database_requests import *
from utils import messages
from vulcan.data import Exam
from vulcanrequests.get_exams import get_exams_klasus


class ExamsCommand(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client

    @discord.slash_command(name=messages['exams_command'],
                           description=messages['exams_command_desc'],
                           dm_permission=False,
                           force_global=True,
                           default_member_permissions=discord.Permissions(permissions=8))
    async def exams(self, interaction: discord.Interaction,
                   date_to: str = discord.SlashOption(name=messages['date_value'],
                                                      description=messages['date_value_desc'],
                                                      required=False)):

        user_data: List[Tuple[str, ...]] = get_user_data(user_id=interaction.user.id, guild_id=interaction.guild_id)
        if not user_data:
            await interaction.response.send_message(messages['need_to_register'], ephemeral=True)
            return

        vulcan: List[Tuple[str, ...]] = get_vulcan_data(guild_id=interaction.guild_id,
                                                        school_name=user_data[0][1],
                                                        class_name=user_data[0][0],
                                                        group_name=user_data[0][2]
                                                        )
        keystore: dict = json.loads(vulcan[0][0].replace("'", '"'))
        account: dict = json.loads(vulcan[0][1].replace("'", '"'))

        msg: discord.PartialInteractionMessage = await interaction.send(messages["getting_exams"], ephemeral=True)
        date = None
        if date_to:
            date_list: List[str] = date_to.split('.')
            try:
                if len(date_list) == 3 and len(date_list[0]) == 2 and len(date_list[1]) == 2 and len(date_list[2]) == 4:
                    for i in date_list:
                        for j in i:
                            try:
                                int(j)
                            except ValueError:
                                raise TypeError
                    date = datetime.date(day=int(date_list[0]), month=int(date_list[1]), year=int(date_list[2]))
                    if not date >= datetime.date.today():
                        await msg.edit(messages['date_from_today'])
                        return
                else:
                    raise TypeError
            except TypeError:
                await msg.edit(messages['date_format_not_correct'])
                return

        exams: List[Exam | None] = await get_exams_klasus(keystore=keystore, account=account,
                                                          date_to=date if date_to else None)
        embeds: List[discord.Embed] = []
        if not exams:
            await msg.edit(messages['no_exams'])
        for i in exams:
            match i.type.lower():
                case "sprawdzian":
                    type_formatted: str = messages['exam_form2']
                case "kartkówka":
                    type_formatted: str = messages['short_test_form2']
                case _:
                    type_formatted: str = "testu"
            embed: discord.Embed = discord.Embed(type="rich", title=i.subject.name,
                                                 color=discord.Color.green() if i.type == "Kartkówka" else
                                                 discord.Color.red(),
                                                 timestamp=datetime.datetime.now()
                                                 )

            embed.set_author(name=interaction.user.name, icon_url=interaction.user.avatar if interaction.user.avatar
                             else discord.User.default_avatar)
            embed.add_field(name=messages['date'].replace('{type}', type_formatted),
                            value=i.deadline.date,
                            inline=False
                            )
            if i.deadline.date == datetime.date.today():
                embed.add_field(name=messages['time_left'].replace('{type}', type_formatted),
                                value="Ten sprawdzian jest dzisiaj!"
                                if i.type.lower() == "sprawdzian" else "Ta kartkówka jest dzisiaj!",
                                inline=False)
            else:
                embed.add_field(name=messages['time_left'].replace('{type}', type_formatted),
                                value=f"{i.deadline.date - datetime.date.today()}".replace(", 0:00:00", "")
                                .replace("days", "dni")
                                .replace("day", "dzień")
                                .replace("month", "miesiąc")
                                .replace("months", "miesięcy"),
                                inline=False)
            embed.add_field(name=messages['teacher'], value=f"{i.creator.name} {i.creator.surname}", inline=False)
            embed.add_field(name=messages['type'], value=i.type, inline=False)
            embed.add_field(name=messages['description'], value=i.topic, inline=False)
            embeds.append(embed)
        await msg.edit(embeds=embeds, content="")


def setup(client):
    client.add_cog(ExamsCommand(client))
