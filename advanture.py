import discord
import os
from discord.ui import Select, Button, View, select
from utility import json_read, json_write, Sel_Action, main_menu_embed, get_ordinal, only_back_home_button
import json

from google import genai
from google.genai import types
from pydantic import BaseModel, Field

from dotenv import load_dotenv
from pathlib import Path

env_path = Path(__file__).resolve().parent / ".env"
if env_path.exists():
    load_dotenv(env_path)

GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")

class Gen_SCP(BaseModel):
    """SCP 생성 구조"""
    SCP_Name: str = Field(description="SCP's name")
    SCP_Number: int = Field(description="SCP's number")
    Containment_Class: str = Field(description="SCP's containment Class.")
    Description: str = Field(description="SCP's Description.")
    Reward: int = Field(description="When the SCP is isolated, an appropriate amount (between $10,000 and $50,000) shall be paid monthly as performance-based compensation.")

class Advanture_Menu(View):
    def __init__(self):
        super().__init__()

    @select(
        options=[
            discord.SelectOption(label="매우 가까운 곳", value="1"),
            discord.SelectOption(label="가까운 곳", value="3"),
            discord.SelectOption(label="먼 곳", value="5"),
            discord.SelectOption(label="매우 먼 곳", value="7")
        ],
        placeholder="원하는 지역을 선택해주세요",
        min_values=1,
        max_values=1
    )

    async def Advanture_callback(self, interaction: discord.Interaction, select: Select):
        embed = discord.Embed(
            title="탐사를 보낼 직원을 선택해주세요",
            color=discord.Color.green()
        )
        for i in range(6):
            if os.path.exists(f'DB/{interaction.user.id}/Empoly/{i+1}.json'):
                if json_read(f'DB/{interaction.user.id}/Empoly/{i+1}.json')['going_out'] > 0:
                    embed.add_field(name=f"{i+1}번 슬롯", value=f"`{json_read(f'DB/{interaction.user.id}/Empoly/{i+1}.json')['name']}`님은 외출중입니다.")
                else:    
                    embed.add_field(name=f"{i+1}번 슬롯", value=f"`{json_read(f'DB/{interaction.user.id}/Empoly/{i+1}.json')['name']}`")
            else:
                embed.add_field(name=f"{i+1}번 슬롯", value=f"비어있습니다.")
        await interaction.response.edit_message(embed=embed, view=Advanture_Menu_Sel(select.values[0]))

    @discord.ui.button(label="돌아가기", style=discord.ButtonStyle.red, emoji="🏠")
    async def Cancel_register(self, interaction: discord.Interaction, button: Button):
        await interaction.response.edit_message(embed=main_menu_embed(interaction.user.id), view=Sel_Action())

class Advanture_Menu_Sel(View):
    def __init__(self, days):
        super().__init__()
        self.days = days

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
        G_client = genai.Client()
        if os.path.exists(f'DB/{interaction.user.id}/Empoly/{selected_slot}.json'):
            if json_read(f'DB/{interaction.user.id}/Empoly/{selected_slot}.json')['going_out'] == 0:
                if json_read(f'DB/{interaction.user.id}/Empoly/{selected_slot}.json')['selfEsteem_base'] == 0:
                    embed = discord.Embed(
                    title="해당 직원의 자존감이 너무 낮습니다. 다시 골라주세요.",
                    color=discord.Color.red()
                    )
                    for i in range(6):
                        if os.path.exists(f'DB/{interaction.user.id}/Empoly/{i+1}.json'):
                            embed.add_field(name=f"{i+1}번 슬롯", value=f"`{json_read(f'DB/{interaction.user.id}/Empoly/{i+1}.json')['name']}`")
                        else:
                            embed.add_field(name=f"{i+1}번 슬롯", value=f"비어있습니다.")
                    await interaction.response.edit_message(embed=embed, view=self)
                elif json_read(f'DB/{interaction.user.id}/Empoly/{selected_slot}.json')['mentalHealth_base'] == 0:
                    embed = discord.Embed(
                    title="해당 직원의 정신 건강이 너무 낮습니다. 다시 골라주세요.",
                    color=discord.Color.red()
                    )
                    for i in range(6):
                        if os.path.exists(f'DB/{interaction.user.id}/Empoly/{i+1}.json'):
                            embed.add_field(name=f"{i+1}번 슬롯", value=f"`{json_read(f'DB/{interaction.user.id}/Empoly/{i+1}.json')['name']}`")
                        else:
                            embed.add_field(name=f"{i+1}번 슬롯", value=f"비어있습니다.")
                    await interaction.response.edit_message(embed=embed, view=self)
                elif json_read(f'DB/{interaction.user.id}/Empoly/{selected_slot}.json')['physicalHealth_base'] == 0:
                    embed = discord.Embed(
                    title="해당 직원의 신체 건강이 너무 낮습니다. 다시 골라주세요.",
                    color=discord.Color.red()
                    )
                    for i in range(6):
                        if os.path.exists(f'DB/{interaction.user.id}/Empoly/{i+1}.json'):
                            embed.add_field(name=f"{i+1}번 슬롯", value=f"`{json_read(f'DB/{interaction.user.id}/Empoly/{i+1}.json')['name']}`")
                        else:
                            embed.add_field(name=f"{i+1}번 슬롯", value=f"비어있습니다.")
                    await interaction.response.edit_message(embed=embed, view=self)
                else:
                    embed = discord.Embed(
                        title="생각중 입니다..."
                    )
                    await interaction.response.edit_message(embed=embed, view=None)
                    json_data = json_read(f'DB/{interaction.user.id}/Empoly/{selected_slot}.json')
                    json_data['going_out'] = int(self.days)
                    json_write(f'DB/{interaction.user.id}/Empoly/{selected_slot}.json', json_data)
                    embed = discord.Embed(
                        title=f"{json_data['name']}은 탐사를 떠났습니다.",
                        description=f'{self.days}일 뒤에 돌아옵니다.',
                        color=discord.Color.green()
                    )
                    prompt = f"""Generate a new anomalous entity for a secret research facility. The entity's appearance is a tall, shadowy figure with two glowing eyes. Based on this visual, provide:

                            1. A compelling Name or designation for the anomaly.
                            2. A Containment Class from this list: 'Safe', 'Euclid', 'Keter'.
                            3. Please answer in Korean.
                            4. This SCP must be configured considering that it took {self.days} days to locate."""
                    model_name = "gemini-2.5-flash" # 구조화된 출력을 지원하는 모델 사용

                    # `response_mime_type`과 `response_schema`를 설정하여 JSON 출력을 강제합니다.
                    response = G_client.models.generate_content(
                        model=model_name,
                        contents=prompt,
                        config=types.GenerateContentConfig(
                            response_mime_type="application/json",
                            response_schema=Gen_SCP, # 정의한 Pydantic 클래스를 스키마로 사용
                        ),
                    )
                    # print(response.text)
                    scp_json_data = json.loads(response.text)
                    json_write(f'DB/{interaction.user.id}/Advanture/{selected_slot}.json', scp_json_data)
                    # embed = discord.Embed(
                    # title=f"{json_data['SCP_Name']} (SCP-{json_data['SCP_Number']})",
                    # description=json_data['Description'],
                    # color=discord.Color.blue()
                    # )
                    # embed.add_field(name='격리등급', value=f'`{json_data['Containment_Class']}`', inline=True)
                    # await interaction.followup.send(embed=embed)
                    await interaction.edit_original_response(embed=embed, view=only_back_home_button())
            else:
                embed = discord.Embed(
                    title="해당 직원은 이미 외출 중입니다. 다시 골라주세요.",
                    color=discord.Color.red()
                )
                for i in range(6):
                    if os.path.exists(f'DB/{interaction.user.id}/Empoly/{i+1}.json'):
                        embed.add_field(name=f"{i+1}번 슬롯", value=f"`{json_read(f'DB/{interaction.user.id}/Empoly/{i+1}.json')['name']}`")
                    else:
                        embed.add_field(name=f"{i+1}번 슬롯", value=f"비어있습니다.")
                await interaction.response.edit_message(embed=embed, view=self)
        else:
            embed = discord.Embed(
                title="비어 있는 슬롯입니다. 다시 골라주세요.",
                color=discord.Color.red()
            )
            for i in range(6):
                if os.path.exists(f'DB/{interaction.user.id}/Empoly/{i+1}.json'):
                    embed.add_field(name=f"{i+1}번 슬롯", value=f"`{json_read(f'DB/{interaction.user.id}/Empoly/{i+1}.json')['name']}`")
                else:
                    embed.add_field(name=f"{i+1}번 슬롯", value=f"비어있습니다.")
            await interaction.response.edit_message(embed=embed, view=self)

    @discord.ui.button(label="돌아가기", style=discord.ButtonStyle.red, emoji="🏠")
    async def Cancel_register(self, interaction: discord.Interaction, button: Button):
        await interaction.response.edit_message(embed=main_menu_embed(interaction.user.id), view=Sel_Action())