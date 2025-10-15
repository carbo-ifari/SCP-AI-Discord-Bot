import discord
import os
from discord.ui import Select, Button, View, select
from utility import json_read, json_write, Sel_Action, main_menu_embed, get_ordinal, only_back_home_button

class register(View):
    def __init__(self, json_data):
        super().__init__()
        self.json_data = json_data
    
    @select(
        options=[
            discord.SelectOption(label="1️⃣ 1번 슬롯", value="1"),
            discord.SelectOption(label="2️⃣ 2번 슬롯", value="2"),
            discord.SelectOption(label="3️⃣ 3번 슬롯", value="3"),
            discord.SelectOption(label="4️⃣ 4번 슬롯", value="4"),
            discord.SelectOption(label="5️⃣ 5번 슬롯", value="5"),
            discord.SelectOption(label="6️⃣ 6번 슬롯", value="6"),
        ],
        placeholder="원하는 슬롯을 선택하세요...",
        min_values=1,
        max_values=1,
    )
    async def select_callback(self, interaction: discord.Interaction, select: Select):
        selected_slot = select.values[0]
        if not os.path.exists(f'DB/{interaction.user.id}/Empoly/{selected_slot}.json'):
            json_write(f'DB/{interaction.user.id}/Empoly/{selected_slot}.json', self.json_data)
            embed = discord.Embed(
            title="✅ 등록 완료",
            description=f"선택한 슬롯에 새로운 직원이 등록되었습니다.",
            color=discord.Color.blue() # You can use predefined colors or hex codes
            )
            await interaction.response.edit_message(embed=embed, view=only_back_home_button())
        else:
            embed = discord.Embed(
            title="❌ 이미 사용중인 슬롯",
            description=f"{selected_slot}번 슬롯은 이미 사용 중입니다. 덮어씌우시겠습니까?",
            color=discord.Color.red() # You can use predefined colors or hex codes
            )
            await interaction.response.edit_message(embed=embed,view=re_check(f'DB/{interaction.user.id}/Empoly/{selected_slot}.json', self.json_data))

    @discord.ui.button(label="취소하기", style=discord.ButtonStyle.red, emoji="❌")
    async def Cancel_register(self, interaction: discord.Interaction, button: Button):
        await interaction.response.edit_message(embed=main_menu_embed(interaction.user.id), view=Sel_Action())

class re_check(View):
    def __init__(self, path, json_data):
        super().__init__()
        self.path = path
        self.json_data = json_data
    @discord.ui.button(label="덮어씌우기", style=discord.ButtonStyle.green, emoji="⚠️")
    async def Overwrite(self, interaction: discord.Interaction, button: Button):
        json_write(self.path, self.json_data)
        embed = discord.Embed(
        title="✅ 덮어씌우기 완료",
        description=f"선택한 슬롯에 새로운 직원이 덮어씌워졌습니다.",
        color=discord.Color.blue() # You can use predefined colors or hex codes
        )
        await interaction.response.edit_message(embed=embed, view=only_back_home_button())
    @discord.ui.button(label="뒤로가기", style=discord.ButtonStyle.red, emoji="❌")
    async def Cancel_overwrite(self, interaction: discord.Interaction, button: Button):
        json_data = self.json_data
        embed = discord.Embed(
        title=f"{json_data['name']}",
        description=f'**`{json_data['introductionDialogue']}`**',
        color=discord.Color.blue() # You can use predefined colors or hex codes
        )
        embed.add_field(name='커리어', value=f'`{json_data['career']}`', inline=True)
        embed.add_field(name='성격', value=f'`{json_data['personality']}`', inline=True)
        embed.add_field(name='전문 분야 및 심리 평가', value=f'`{json_data['profileSummary']}`', inline=False)
        embed.add_field(name='현재 감정 상태', value=f'`{json_data['emotion']}`', inline=True)
        embed.add_field(name='자존감 기본 능력치', value=f'`{json_data['selfEsteem_base']}`', inline=True)
        embed.add_field(name='정신 건강 기본 능력치', value=f'`{json_data['mentalHealth_base']}`', inline=True)
        embed.add_field(name='신체 건강 기본 능력치', value=f'`{json_data['physicalHealth_base']}`', inline=True)
        await interaction.response.edit_message(embed=embed, view=register())

class View_Empoly_List(View):
    def __init__(self):
        super().__init__()

    @select(
        options=[
            discord.SelectOption(label="1️⃣ 1번 슬롯", value="1"),
            discord.SelectOption(label="2️⃣ 2번 슬롯", value="2"),
            discord.SelectOption(label="3️⃣ 3번 슬롯", value="3"),
            discord.SelectOption(label="4️⃣ 4번 슬롯", value="4"),
            discord.SelectOption(label="5️⃣ 5번 슬롯", value="5"),
            discord.SelectOption(label="6️⃣ 6번 슬롯", value="6"),
        ],
        placeholder="원하는 슬롯을 선택하세요...",
        min_values=1,
        max_values=1,
    )
    async def select_callback(self, interaction: discord.Interaction, select: Select):
        selected_slot = select.values[0]
        try:
            json_data = json_read(f'DB/{interaction.user.id}/Empoly/{selected_slot}.json')
        except FileNotFoundError:
            embed = discord.Embed(
            title=f"{selected_slot}번 슬롯",
            description="**❌ 빈 슬롯입니다.**",
            color=discord.Color.red() # You can use predefined colors or hex codes
            )
            await interaction.response.edit_message(embed=embed,view=self)
        embed = discord.Embed(
        title=f"{json_data['name']}",
        description=f'**`{json_data['introductionDialogue']}`**',
        color=discord.Color.blue() # You can use predefined colors or hex codes
        )
        embed.add_field(name='커리어', value=f'`{json_data['career']}`', inline=True)
        embed.add_field(name='성격', value=f'`{json_data['personality']}`', inline=True)
        embed.add_field(name='전문 분야 및 심리 평가', value=f'`{json_data['profileSummary']}`', inline=False)
        embed.add_field(name='현재 감정 상태', value=f'`{json_data['emotion']}`', inline=True)
        embed.add_field(name='자존감 기본 능력치', value=f'`{json_data['selfEsteem_base']}`', inline=True)
        embed.add_field(name='정신 건강 기본 능력치', value=f'`{json_data['mentalHealth_base']}`', inline=True)
        embed.add_field(name='신체 건강 기본 능력치', value=f'`{json_data['physicalHealth_base']}`', inline=True)
        if json_data['going_out'] > 0:
            embed.add_field(name='외출 여부', value=f'`외출중: {json_data['going_out']}일 남음`', inline=True)
        else:
            embed.add_field(name='외출 여부', value=f'`재실중`', inline=True)
        await interaction.response.edit_message(embed=embed,view=self)
    @discord.ui.button(label="돌아가기", style=discord.ButtonStyle.red, emoji="🏠")
    async def Cancel_register(self, interaction: discord.Interaction, button: Button):
        await interaction.response.edit_message(embed=main_menu_embed(interaction.user.id), view=Sel_Action())