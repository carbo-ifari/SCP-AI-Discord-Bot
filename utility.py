import json
import os
import discord
from discord.ui import Select, Button, View, select

def get_ordinal(n):
    if n == 1:
        return "1st"
    elif n == 2:
        return "2nd"
    elif n == 3:
        return "3rd"
    else:
        return f"{n}th"

def json_write(data_path, data):
    with open(data_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

def json_read(data_path):
    with open(data_path, 'r', encoding='utf-8') as f:
        return json.load(f)
    
def Sel_Action():
    from main import Sel_Action
    return Sel_Action()

def main_menu_embed(user_id):
    embed = discord.Embed(
    title=f"💻 {json_read(f'DB/{user_id}/{user_id}.json')['days']}일차 사무실",
    description=f"현재 자금: `{json_read(f'DB/{user_id}/{user_id}.json')['Money']}$`",
    color=discord.Color.blue() # You can use predefined colors or hex codes
    )
    embed.add_field(name='🏢 격리실', value='격리중인 SCP를 확인 할 수 있습니다.', inline=True)
    embed.add_field(name='📃 직원관리', value='직원 목록을 조회 해볼 수 있습니다. 직원을 채용할려면 **`/채용`**을 입력해주세요', inline=True)
    embed.add_field(name='🗺️ 탐사하기', value='SCP를 탐사하고 찾을 수 있습니다.', inline=True)
    embed.add_field(name='🏪 상점', value='직원을 위한 아이템 또는 격리실을 건설할수 있습니다.', inline=True)
    embed.add_field(name='🗄️ 기록', value='개발ing', inline=True)
    embed.add_field(name='📅 다음날', value='다음날로 날짜를 넘깁니다.', inline=True)
    embed.set_thumbnail(url='https://scp-wiki.wdfiles.com/local--files/about-the-scp-foundation/scp-logo-signature.png')
    return embed

class only_back_home_button(View):
    def __init__(self):
        super().__init__()
    @discord.ui.button(label="돌아가기", style=discord.ButtonStyle.red, emoji="🏠")
    async def Cancel_register(self, interaction: discord.Interaction, button: Button):
        await interaction.response.edit_message(embed=main_menu_embed(interaction.user.id), view=Sel_Action())