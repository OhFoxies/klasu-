

import nextcord as discord
from nextcord.ext import commands

from utils import messages, logs_, config
from database.database_requests import get_exam_by_id, update_exam
from vulcanrequests.get_all_exams import get_all_exams
from background_tasks.CheckForOldExams import update_exams_dates
from background_tasks.PrepareGroups import *
from threading import Thread
import asyncio


class UpdateExams(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client

    @commands.is_owner()
    @discord.slash_command(name="exams_update",
                           description=messages['ping_desc'],
                           dm_permission=False,
                           force_global=True,
                           default_member_permissions=discord.Permissions(permissions=8))
    async def update_exams(self, interaction: discord.Interaction):
        if int(config['owner_id']) == interaction.user.id:
            gr = get_all_groups()
            for i in gr:
                exams = await get_all_exams(keystore=i.keystore, account=i.account)
                for exam in exams.all_exams:
                    if get_exam_by_id(exam.id, i.id):
                        update_exam(exam, i.id)
                        logs_.log(f"Updating exam with id: {exam.id}. (Deadline: {exam.deadline.date})")
            groups = create_groups_chunks()

            if not groups:
                return

            for i in range(len(groups)):
                thread: Thread = Thread(target=self.exams_date_update_between_callbacks, args=[groups[i], i])
                thread.start()

            await interaction.response.send_message(f"Sprawdziany zwziumowane!", ephemeral=True)
            return
        await interaction.response.send_message(f"Nie owner", ephemeral=True)

    def exams_date_update_between_callbacks(self, groups_splitted: List[Group], thread_num: int):
        asyncio.run_coroutine_threadsafe(update_exams_dates(groups_splitted, self.client, thread_num), self.client.loop)
def setup(client):
    client.add_cog(UpdateExams(client))
