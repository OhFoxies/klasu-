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
    channel_id: str = get_channel(guild_id=interaction.guild_id,
                                  school_name=school_name,
                                  class_name=class_name,
                                  group_name=group_name
                                  )

    try:
        channel: discord.TextChannel = await interaction.guild.fetch_channel(int(channel_id))
    except discord.NotFound:
        system_channel: discord.TextChannel = interaction.guild.system_channel
        msg: str = messages['channel_not_found'].replace('{school}', school_name)
        msg: str = msg.replace('{class}', class_name)
        msg: str = msg.replace('{group}', group_name)
        if system_channel:
            await system_channel.send(msg)
            return
        random_channel: discord.TextChannel = random.choice(interaction.guild.text_channels)
        await random_channel.send(msg)
        return
    except discord.HTTPException:
        return
    except discord.InvalidData:
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
            try:
                await user.send(messages['account_removed'].replace('{server}', interaction.guild.name))
            except (discord.Forbidden, discord.HTTPException):
                pass
        except (discord.Forbidden, discord.HTTPException):
            pass
    channel: discord.TextChannel = interaction.guild.system_channel
    if not channel:
        channel: discord.TextChannel = interaction.guild.get_channel(interaction.channel_id)
    await channel.send(messages['removed_accounts'].replace('{list}', '\n'.join(mentions)))
