from other_functions.GroupChannel import get_group_channel
from typing import List

import nextcord as discord

from database.database_requests import get_channel
from utils import messages


async def send_message_group_channel(interaction: discord.Interaction,
                                     school_name: str,
                                     class_name: str,
                                     group_name: str,
                                     message: str,
                                     pin: bool):
    channel_id: str = get_channel(guild_id=interaction.guild_id,
                                  school_name=school_name,
                                  class_name=class_name,
                                  group_name=group_name
                                  )
    channel: discord.TextChannel = await get_group_channel(guild=interaction.guild,
                                                           school=school_name,
                                                           class_name=class_name,
                                                           group=group_name,
                                                           channel_id=int(channel_id))
    if not channel:
        return
    send: discord.Message = await channel.send(message)
    if pin:
        await send.pin()


async def user_delete_account_info(deleted_users: List[str], interaction: discord.Interaction) -> None:
    mentions: List[str] = []
    for i in deleted_users:
        try:
            user: discord.Member = await interaction.guild.fetch_member(int(i))
            mentions.append(user.mention)
            await user.send(messages['account_removed'].replace('{server}', interaction.guild.name))
        except (discord.Forbidden, discord.HTTPException):
            pass

    channel: discord.TextChannel = interaction.guild.system_channel
    if not channel:
        channel = await interaction.guild.fetch_channel(interaction.channel_id)
    await channel.send(messages['removed_accounts'].replace('{list}', '\n'.join(mentions)))
