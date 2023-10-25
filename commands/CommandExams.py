import nextcord as discord
from nextcord.ext import commands

from database.database_requests import *
from embeds.embeds import exam_embed, connecting, error_embed, no_exams
from utils import messages
from vulcan.data import Exam
from vulcanrequests.get_exams import get_exams_klasus


class ExamsCommand(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client

    @discord.slash_command(name=messages['exams_command'],
                           description=messages['exams_command_desc'],
                           dm_permission=False,
                           force_global=True)
    async def exams(self, interaction: discord.Interaction,
                    date_to: str = discord.SlashOption(name=messages['date_value'],
                                                       description=messages['date_value_desc'],
                                                       required=False)):

        user_data: User | None = get_user_data(user_id=interaction.user.id, guild_id=interaction.guild_id)
        if not user_data:
            err_embed: discord.Embed = error_embed(error=messages['need_to_register'])
            await interaction.response.send_message(embed=err_embed, ephemeral=True)
            return

        vulcan_data: VulcanData = get_vulcan_data(guild_id=interaction.guild_id,
                                                  school_name=user_data.school_name,
                                                  class_name=user_data.class_name,
                                                  group_name=user_data.group_name
                                                  )
        embed: discord.Embed = connecting()
        msg: discord.PartialInteractionMessage = await interaction.send(embed=embed, ephemeral=True)
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
                        err_embed: discord.Embed = error_embed(error=messages['date_from_today'])
                        await msg.edit(embed=err_embed)
                        return
                else:
                    raise TypeError
            except TypeError:
                err_embed: discord.Embed = error_embed(error=messages['date_format_not_correct'])
                await msg.edit(embed=err_embed)
                return

        exams: List[Exam | None] = await get_exams_klasus(keystore=vulcan_data.keystore,
                                                          account=vulcan_data.account,
                                                          date_to=date if date_to else None)
        embeds: List[discord.Embed] = []
        if not exams:
            no_exams_embed: discord.Embed = no_exams()
            await msg.edit(embed=no_exams_embed)
        for exam in exams:
            embed: discord.Embed = exam_embed(exam)
            embed.set_author(name=interaction.user.name, icon_url=interaction.user.avatar if interaction.user.avatar
                             else discord.User.default_avatar)
            embeds.append(embed)
        await msg.edit(embeds=embeds, content="")


def setup(client):
    client.add_cog(ExamsCommand(client))
