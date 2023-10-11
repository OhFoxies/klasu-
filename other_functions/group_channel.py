import nextcord as discord
from utils import messages
from random import choice


async def get_group_channel(channel_id: int,
                            guild: discord.Guild,
                            class_name: str,
                            school: str,
                            group: str) -> discord.TextChannel | None:
    try:
        channel: discord.TextChannel = await guild.fetch_channel(channel_id)
        return channel
    except discord.NotFound:
        system_channel: discord.TextChannel = guild.system_channel
        msg: str = messages['channel_not_found'].replace('{school}', school)
        msg: str = msg.replace('{class}', class_name)
        msg: str = msg.replace('{group}', group)
        if system_channel:
            await system_channel.send(msg)
        random_channel: discord.TextChannel = choice(guild.text_channels)
        await random_channel.send(msg)
        return None
    except (discord.HTTPException, discord.InvalidData):
        return None
