import datetime
from typing import List

import nextcord as discord

from database.database_requests import get_channel
from embeds.embeds import any_embed, removed_account, removed_accounts
from embeds.embeds import error_embed
from helpers.group_channel import get_group_channel
from utils import messages


async def send_message_group_channel(interaction: discord.Interaction,
                                     school_name: str,
                                     class_name: str,
                                     group_name: str,
                                     message: str,
                                     pin: bool,
                                     title: str):
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
    embed: discord.Embed = any_embed(title=title, desc=message)
    if not channel:
        return
    send: discord.Message = await channel.send(embed=embed)
    if pin:
        await send.pin()


async def user_delete_account_info(deleted_users: List[str], interaction: discord.Interaction) -> None:
    mentions: List[str] = []
    for i in deleted_users:
        try:
            user: discord.Member = await interaction.guild.fetch_member(int(i))
            mentions.append(user.mention)
            embed: discord.Embed = removed_account(interaction.guild.name)
            await user.send(embed=embed)
        except (discord.Forbidden, discord.HTTPException):
            pass

    channel: discord.TextChannel = interaction.guild.system_channel
    if not channel:
        channel = await interaction.guild.fetch_channel(interaction.channel_id)
    embed: discord.Embed = removed_accounts(mentions)
    await channel.send(embed=embed, content='\n'.join(mentions) if mentions else "")


async def date_from_string(string_date: str, msg: discord.PartialInteractionMessage) -> datetime.date | None:
    date_list: List[str] = string_date.split('.')
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
            return date
        else:
            raise TypeError
    except TypeError:
        err_embed: discord.Embed = error_embed(error=messages['date_format_not_correct'])
        await msg.edit(embed=err_embed)
        return
