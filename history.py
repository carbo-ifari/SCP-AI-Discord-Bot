import discord
import os
from discord.ui import Select, Button, View, select
from utility import json_read, json_write, Sel_Action, main_menu_embed, get_ordinal, only_back_home_button

from pathlib import Path

def count_json_files(folder: str | Path, recursive: bool = True) -> int:
    p = Path(folder)
    if not p.exists() or not p.is_dir():
        return 0
    return sum(1 for _ in p.rglob("*.json"))

class HistoryView(View):
    def __init__(self, user_id: int):
        super().__init__()
        
        options = []
        empoly_dir = f'DB/{user_id}/History/'

        for i in range(0, count_json_files(empoly_dir)):
            employee_file = f'{empoly_dir}{i+1}.json'
            employee_data = json_read(employee_file)
            options.append(discord.SelectOption(
                label=f"{employee_data['name']}", 
                value=str(i+1)
            ))

        self.history_select = Select(
            placeholder="확인할 기록을 선택해주세요...",
            min_values=1,
            max_values=1,
            options=options
        )
        self.history_select.callback = self.select_callback
        self.add_item(self.history_select)

        self.cancel_button = Button(label="돌아가기", style=discord.ButtonStyle.red, emoji="🏠")
        async def _cancel_callback(interaction: discord.Interaction):
            await interaction.response.edit_message(embed=main_menu_embed(interaction.user.id), view=Sel_Action())
        self.cancel_button.callback = _cancel_callback
        self.add_item(self.cancel_button)

    async def select_callback(self, interaction: discord.Interaction):
        selected_slot = self.history_select.values[0]
        json_data = json_read(f'DB/{interaction.user.id}/History/{selected_slot}.json')
        embed = discord.Embed(
            title=f"{json_data['name']}",
            description=f'**`{json_data['introductionDialogue']}`**',
            color=discord.Color.red()
        )
        embed.add_field(name='커리어', value=f'`{json_data['career']}`', inline=True)
        embed.add_field(name='성격', value=f'`{json_data['personality']}`', inline=True)
        embed.add_field(name='전문 분야 및 심리 평가', value=f'`{json_data['profileSummary']}`', inline=False)
        embed.add_field(name='현재 감정 상태', value=f'`{json_data['emotion']}`', inline=True)
        embed.add_field(name='자존감 기본 능력치', value=f'`{json_data['selfEsteem_base']}`', inline=True)
        embed.add_field(name='정신 건강 기본 능력치', value=f'`{json_data['mentalHealth_base']}`', inline=True)
        embed.add_field(name='신체 건강 기본 능력치', value=f'`{json_data['physicalHealth_base']}`', inline=True)
        embed.set_author(name='사망한 직원의 기록입니다.')
        await interaction.response.edit_message(embed=embed, view=self)