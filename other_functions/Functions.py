import nextcord
import nextcord as discord
from database.database_requests import get_channel
from utils import messages
import random
from typing import List


async def send_message_group_channel(interaction: discord.Interaction,
                                     school_name: str,
                                     class_name: str,
                                     group_name: str,
                                     message: str,
                                     pin: bool):
    channel_id = get_channel(guild_id=interaction.guild_id,
                             school_name=school_name,
                             class_name=class_name,
                             group_name=group_name
                             )

    channel = interaction.guild.get_channel(int(channel_id))
    if not channel:
        system_channel: nextcord.TextChannel = interaction.guild.system_channel
        msg = messages['channel_not_found'].replace('{school}', school_name)
        msg = msg.replace('{class}', class_name)
        msg = msg.replace('{group}', group_name)
        if system_channel:
            await system_channel.send(msg)
            return
        random_channel = random.choice(interaction.guild.text_channels)
        await random_channel.send(msg)
        return

    send: nextcord.Message = await channel.send(message)
    if pin:
        await send.pin()


async def user_delete_account_info(deleted_users: List[str], interaction: discord.Interaction) -> None:
    mentions: List[str] = []
    for i in deleted_users:
        ping = await interaction.guild.fetch_member(int(i))
        if ping:
            mentions.append(ping.mention)
            try:
                await ping.send(messages['account_removed'].replace('{server}', interaction.guild.name))
            except (discord.Forbidden, discord.HTTPException):
                pass
    channel: discord.TextChannel = interaction.guild.system_channel
    if not channel:
        channel: discord.TextChannel = interaction.guild.get_channel(interaction.channel_id)
    await channel.send(messages['removed_accounts'].replace('{list}', '\n'.join(mentions)))
