import nextcord as discord
from nextcord.ext import commands

from database.database_requests import get_user_data, User, get_role, save_view
from embeds.embeds import role_embed, error_embed, any_embed
from utils import messages


class RoleMessage(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client

    @discord.slash_command(name=messages['role_message'],
                           description=messages['role_message_desc'],
                           dm_permission=False,
                           force_global=True)
    async def klasus_command(self, interaction: discord.Interaction,
                             channel: discord.TextChannel = discord.SlashOption(
                                 name=messages['value_channel'],
                                 description=messages['channel_value_desc'],
                                 required=True)):
        embed = role_embed()
        view = Button()
        msg = await channel.send(embed=embed, view=view)
        save_view(msg.id)
        await view.wait()
        await interaction.response.send_message(embed=embed, ephemeral=True)


class Button(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.value = None

    @discord.ui.button(label=messages['role_button'], style=discord.ButtonStyle.green, custom_id="button:wzium")
    async def button(self, button: discord.ui.Button, interaction: discord.Interaction):
        user_data: User | None = get_user_data(user_id=interaction.user.id, guild_id=interaction.guild_id)
        if not user_data:
            err_embed: discord.Embed = error_embed(error=messages['role_not_in'])
            await interaction.response.send_message(embed=err_embed, ephemeral=True)
            return
        role_id: int = get_role(guild_id=interaction.guild_id, school_name=user_data.school_name,
                                group_name=user_data.group_name, class_name=user_data.class_name)
        if role_id == 0:
            err_embed: discord.Embed = error_embed(error=messages['role_not_in'])
            await interaction.response.send_message(embed=err_embed, ephemeral=True)
            return

        role = interaction.guild.get_role(role_id)
        if not interaction.user.get_role(role_id):
            await interaction.user.add_roles(role)
            embed = any_embed(desc=messages['role_added'], title=messages['role_added_title'])
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return
        await interaction.user.remove_roles(role)
        embed = any_embed(desc=messages['role_deleted'], title=messages['role_deleted_title'], color=discord.Color.red())
        await interaction.response.send_message(embed=embed, ephemeral=True)
        return


def setup(client):
    client.add_cog(RoleMessage(client))
