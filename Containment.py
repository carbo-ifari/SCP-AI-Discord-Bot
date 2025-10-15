import discord
from discord.ext import commands
from discord import app_commands
from discord.ui import Select, Button, View, select
from utility import json_read, json_write, Sel_Action, main_menu_embed, get_ordinal

class Sel_Floor(View):
    def __init__(self):
        super().__init__()

    @select(
        options=[
            discord.SelectOption(label="1️⃣ 1층", value="F1"),
            discord.SelectOption(label="2️⃣ 2층", value="F2"),
            discord.SelectOption(label="3️⃣ 3층", value="F3"),
            discord.SelectOption(label="4️⃣ 4층", value="F4"),
            discord.SelectOption(label="5️⃣ 5층", value="F5"),
        ],
        placeholder="원하는 창을 선택하세요...",
        min_values=1,
        max_values=1,
    )

    async def select_callback(self, interaction: discord.Interaction, select: Select):
        select_floor = select.values[0]
        embed = discord.Embed(
        title="🛗 격리실을 선택해주세요",
        color=discord.Color.blue() # You can use predefined colors or hex codes
        )
        for i in range(5):
            json_data = json_read(f'DB/{interaction.user.id}/Containment/{select_floor}/{get_ordinal(i+1)}.json')
            if json_data['unlock'] == False:
                embed.add_field(name=f"🔒 {i+1}번방", value=f"`아직 개방되지 않았습니다`")
            else:
                if json_data["SCP_Number"] == None:
                    embed.add_field(name=f"{i+1}번방", value=f"`빈 방입니다.`")
                else:
                    embed.add_field(name=f"{i+1}번방", value=f"`SCP-{json_data['SCP_Number']}: {json_data['SCP_Name']}`",)
        await interaction.response.edit_message(embed=embed,view=Sel_Room_List(select_floor))
    @discord.ui.button(label="돌아가기", style=discord.ButtonStyle.red, emoji="🏠")
    async def BackHome(self, interaction: discord.Interaction, button: Button):
        await interaction.response.edit_message(embed=main_menu_embed(interaction.user.id), view=Sel_Action())


class Sel_Room_List(View):
    def __init__(self, select_floor):
        super().__init__()
        self.select_floor = select_floor

    @select(
        options=[
            discord.SelectOption(label="1번방", value="1st", emoji="1️⃣"),
            discord.SelectOption(label="2번방", value="2nd", emoji="2️⃣"),
            discord.SelectOption(label="3번방", value="3rd", emoji="3️⃣"),
            discord.SelectOption(label="4번방", value="4th", emoji="4️⃣"),
            discord.SelectOption(label="5번방", value="5th", emoji="5️⃣"),
        ],
        placeholder="원하는 방을 선택하세요...",
        min_values=1,
        max_values=1,
    )

    async def select_callback(self, interaction: discord.Interaction, select: Select):
        select_room = select.values[0]
        if json_read(f'DB/{interaction.user.id}/Containment/{self.select_floor}/{select_room}.json')['unlock'] == False:
            embed = discord.Embed(
            title=f"{int(self.select_floor[1:])}층 {int(select_room[:-2])}번방",
            description="**🔒 아직 개방되지 않은 방입니다.**",
            color=discord.Color.red() # You can use predefined colors or hex codes
            )
            await interaction.response.edit_message(embed=embed,view=self)
            return
        else:
            if json_read(f'DB/{interaction.user.id}/Containment/{self.select_floor}/{select_room}.json')["SCP_Number"] == None:
                embed = discord.Embed(
                title=f"{int(self.select_floor[1:])}층 {int(select_room[:-2])}번방",
                description="**🦗 빈 방입니다.**",
                color=discord.Color.red() # You can use predefined colors or hex codes
                )
                await interaction.response.edit_message(embed=embed,view=self)
                return
        json_data = json_read(f'DB/{interaction.user.id}/Containment/{self.select_floor}/{select_room}.json')
        embed = discord.Embed(
        title=f"🔍 {self.select_floor} {select_room} 정보",
        color=discord.Color.blue() # You can use predefined colors or hex codes
        )
        embed.add_field(name=f"SCP-{json_data['SCP_Number']}:{json_data['SCP_Name']}", value=f"`SCP-{json_data['Description']}`", inline=False)
        embed.add_field(name="격리단계", value=f"`{json_data['Containment_Class']}`", inline=False)
        await interaction.response.edit_message(embed=embed,view=self)

    @discord.ui.button(label="돌아가기", style=discord.ButtonStyle.red, emoji="🏠")
    async def BackHome(self, interaction: discord.Interaction, button: Button):
        await interaction.response.edit_message(embed=main_menu_embed(interaction.user.id), view=Sel_Action())