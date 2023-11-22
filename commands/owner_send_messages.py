import asyncio
from threading import Thread

import nextcord as discord
from nextcord.ext import commands

from background_tasks.messages import MessagesSender
from database.database_requests import *
from helpers.create_groups_chunks import create_groups_chunks
from utils import messages, config


class SendMessagesManual(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client

    @discord.slash_command(name=messages['send_messages_manual'],
                           description=messages['send_messages_manual_desc'],
                           dm_permission=False,
                           force_global=True)
    async def exams(self, interaction: discord.Interaction,
                    old_msg: str = discord.SlashOption(name="old_message",
                                                       description="should be old messages be sent",
                                                       required=True),
                    ):
        if int(config['owner_id']) == interaction.user.id:
            msg = await interaction.send("Wysyłanie wiadomości... czekaj", ephemeral=True)
            groups = create_groups_chunks()

            if not groups:
                return

            for i in range(len(groups)):
                thread: Thread = Thread(target=self.messages_sender_between_callbacks, args=[groups[i], i, old_msg])
                thread.start()
            await msg.edit("Kiedyś się skończy na pewno.")
        else:
            await interaction.response.send_message(f"Nie owner", ephemeral=True)

    def messages_sender_between_callbacks(self, groups_splitted: List[Group], thread_num: int, old_msg: str):
        send_old = True if old_msg == "true" else False

        sender = MessagesSender(groups_splitted=groups_splitted, thread_num=thread_num, client=self.client, old=send_old)
        asyncio.run_coroutine_threadsafe(sender.check_for_new_messages(), self.client.loop)


def setup(client):
    client.add_cog(SendMessagesManual(client))
