import datetime as dt

import nextcord as discord
from nextcord.ext import commands

from database.database_requests import (get_user_data,
                                        get_vulcan_data,
                                        User,
                                        VulcanData
                                        )
from embeds.embeds import message_embed, connecting, error_embed, no_messages
from utils import messages
from vulcanrequests.get_messages import GetMessages


class Messages(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client

    @discord.slash_command(name=messages['messages_command'],
                           description=messages['messages_command_desc'],
                           dm_permission=False,
                           force_global=True)
    async def lucky_number(self, interaction: discord.Interaction,
                           how_old: int = discord.SlashOption(name=messages['messages_how_old_value'],
                                                              description=messages['messages_how_old_value_desc'],
                                                              required=False)
                           ):
        user_data: User | None = get_user_data(user_id=interaction.user.id, guild_id=interaction.guild_id)
        if not user_data:
            err_embed: discord.Embed = error_embed(error=messages['need_to_register'])
            await interaction.response.send_message(embed=err_embed, ephemeral=True)
            return

        embed: discord.Embed = connecting()
        message: discord.PartialInteractionMessage = await interaction.send(embed=embed, ephemeral=True)
        vulcan_data: VulcanData = get_vulcan_data(guild_id=interaction.guild_id,
                                                  school_name=user_data.school_name,
                                                  class_name=user_data.class_name,
                                                  group_name=user_data.group_name
                                                  )
        messages_getter = GetMessages(keystore=vulcan_data.keystore, account=vulcan_data.account)
        if how_old:
            messages_list = await messages_getter.get_messages(how_old=dt.timedelta(days=how_old))
        else:
            messages_list = await messages_getter.get_messages()

        if messages_list:
            await message.delete()
            for vulcan_message in messages_list:
                embed = message_embed(vulcan_message)
                embed.title = messages["message"]
                await interaction.send(embed=embed, ephemeral=True)
        else:
            embed = no_messages()
            await message.edit(embed=embed)


def setup(client):
    client.add_cog(Messages(client))
