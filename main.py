import discord
import asyncio
import os
from discord.ext import commands
from discord.ui import Select, Button, View, select
from utility import json_read, json_write, main_menu_embed, get_ordinal, only_back_home_button
from google import genai
from google.genai import types
from pydantic import BaseModel, Field
import json
from empoly import register, View_Empoly_List
from advanture import Advanture_Menu
from shop import shop_menu
from history import HistoryView

from dotenv import load_dotenv
from pathlib import Path

from pathlib import Path
from typing import Iterable

env_path = Path(__file__).resolve().parent / ".env"
if env_path.exists():
    load_dotenv(env_path)

DISCORD_TOKEN = os.environ.get("DISCORD_TOKEN")
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")

myguild = YOUR_GUILD_ID

def has_json_files(folder: str, recursive: bool = True) -> bool:
    path = Path(folder)
    if not path.exists() or not path.is_dir():
        return False
    it: Iterable[Path] = path.rglob("*.json") if recursive else path.glob("*.json")
    return any(it)

class Client(commands.Bot):
    
    async def on_ready(self):
        print(f'Logged in as {self.user}')

        try:
            GUILD_ID = discord.Object(id=myguild)
            synced = await self.tree.sync(guild=GUILD_ID)
            print(f'Synced {len(synced)} command(s) to the guild.')
        except Exception as e:
            print(f'Error syncing commands: {e}')

    async def on_message(self, message):
        if message.author == self.user:
            return

intents = discord.Intents.default()
intents.message_content = True
client = Client(command_prefix="!", intents=intents)
        

class FirstGameStart(View):
    def __init__(self):
        super().__init__()

    @discord.ui.button(label='게임시작', style=discord.ButtonStyle.green)
    async def FirstGameNext(self, interaction: discord.Interaction, button: Button):
        await interaction.response.edit_message(embed=main_menu_embed(interaction.user.id), view=Sel_Action())

# class people_chat(View):
#     def __init__(self):
#         super().__init__()

#     @discord.ui.button(label='직원 대회 엿듣기', style=discord.ButtonStyle.green, emoji='💬')
#     async def empoly_chat(self, interaction:discord.Integration, button: Button):

        
GUILD_ID = discord.Object(id=myguild)

class Sel_Action(View):
    def __init__(self):
        super().__init__()

    @discord.ui.button(label="격리실", style=discord.ButtonStyle.primary, emoji="🏢")
    async def Containment_Room(self, interaction: discord.Interaction, button: Button):
        button.disabled = True
        embed = discord.Embed(
        title="🛗 엘리베이터",
        description="원하는 층을 선택해주세요.",
        color=discord.Color.blue() # You can use predefined colors or hex codes
        )
        # lazy import to avoid circular import with find.py
        from Containment import Sel_Floor
        await interaction.response.edit_message(embed=embed, view=Sel_Floor())
    @discord.ui.button(label="직원관리", style=discord.ButtonStyle.primary, emoji="📃")
    async def Empoly_manage(self, interaction: discord.Interaction, button: Button):
        if has_json_files(f'DB/{interaction.user.id}/Empoly'):
            embed = discord.Embed(
            title="👥 직원관리",
            description="조회할 슬롯을 선택해주세요.",
            color=discord.Color.blue() # You can use predefined colors or hex codes
            )
            for i in range(6):
                if os.path.exists(f'DB/{interaction.user.id}/Empoly/{i+1}.json'):
                    check_json_data = json_read(f'DB/{interaction.user.id}/Empoly/{i+1}.json')
                    embed.add_field(name=f"✅ {i+1}번 슬롯", value=f"`{check_json_data['name']}`", inline=True)
                else:
                    embed.add_field(name=f"❌ {i+1}번 슬롯", value=f"`빈 슬롯입니다.`", inline=True)
            await interaction.response.edit_message(embed=embed, view=View_Empoly_List())
        else:
            embed = discord.Embed(
            title="❌ 아직 직원을 고용하지 않은것 같군요!",
            description="`/직원채용` 명령어로 직원을 채용해보세요!",
            color=discord.Color.red() 
            )
            await interaction.response.edit_message(embed=embed, view=only_back_home_button())
    @discord.ui.button(label="탐사하기", style=discord.ButtonStyle.primary, emoji='🗺️')
    async def Adventure(self, interaction: discord.Integration, button: Button):
        _temp = False
        for i in range(5):
            for n in range(5):                
                json_data = json_read(f'DB/{interaction.user.id}/Containment/F{i+1}/{get_ordinal(n+1)}.json')
                if json_data['unlock']:
                    if json_data['SCP_Name'] == None:
                        _temp = True
        if _temp:
            embed = discord.Embed(
                title="탐사할 지역을 선택해주세요",
                color=discord.Color.green()
            )
            embed.add_field(name="매우 가까운 곳", value="1일 걸립니다.")
            embed.add_field(name="가까운 곳", value="3일 걸립니다.")
            embed.add_field(name="먼 곳", value="5일 걸립니다.")
            embed.add_field(name="매우 먼 곳", value="7일 걸립니다.")
            await interaction.response.edit_message(embed=embed, view=Advanture_Menu())
        else:
            embed = discord.Embed(
                title="SCP를 격리할 격리실이 부족합니다",
                color=discord.Color.red()
            )
            await interaction.response.edit_message(embed=embed, view=only_back_home_button())
    @discord.ui.button(label="상점", style=discord.ButtonStyle.primary, emoji='🏪')
    async def Shop_button(self, interaction: discord.Integration, button: Button):
        embed = discord.Embed(
            title="상점 이유",
            color=discord.Color.green()
        )
        embed.add_field(name="💊 자아긍정 알약", value="직원의 자존감을 올립니다.\n`가격: 50000$`")
        embed.add_field(name="💊 심리진정 알약", value="직원의 정신력을 올립니다.\n`가격: 50000$`")
        embed.add_field(name="💊 신체회복 알약", value="직원의 신체능력을 올립니다.\n`가격: 50000$`")
        embed.add_field(name="🔓 격리실 해금", value="격리실을 해금합니다.\n`가격: 200000$`")
        await interaction.response.edit_message(embed=embed, view=shop_menu())
    @discord.ui.button(label="기록", style=discord.ButtonStyle.primary, emoji='📜')
    async def list_button(self, interaction: discord.Integration, button: Button):
        # check 'History' folder for records
        if has_json_files(f'DB/{interaction.user.id}/History'):
            embed = discord.Embed(
                title="확인할 기록을 선택해주세요"
            )
            await interaction.response.edit_message(embed=embed, view=HistoryView(interaction.user.id))
        else:
            embed = discord.Embed(
                title="확인할 기록이 없습니다",
                color=discord.Color.red()
            )
            await interaction.response.edit_message(embed=embed, view=only_back_home_button())
    @discord.ui.button(label="다음날", style=discord.ButtonStyle.primary, emoji='▶️')
    async def Next_day(self, interaction: discord.Integration, button: Button):
        # acknowledge the interaction so we can edit the original later
        await interaction.response.defer()
        print_embed = []
        user = json_read(f'DB/{interaction.user.id}/{interaction.user.id}.json')
        for i in range(6):
            if os.path.exists(f'DB/{interaction.user.id}/Empoly/{i+1}.json'):
                json_data = json_read(f'DB/{interaction.user.id}/Empoly/{i+1}.json')
                scp_data = json_read(f'DB/{interaction.user.id}/Advanture/{i+1}.json')
                if json_data['going_out'] != 0:
                    json_data['going_out'] -= 1
                    json_write(f'DB/{interaction.user.id}/empoly/{i+1}.json', json_data)
                    if json_data['going_out'] == 0:
                        should_break_outer = False
                        embed = discord.Embed(
                            title="생각중 입니다..."
                        )
                        await interaction.edit_original_response(embed=embed, view=None)
                        G_client = genai.Client()
                        prompt = f"""해당 인물은 {json_data['personality']} 같은 성격을 가지고 있으며 {json_data['profileSummary']}와 같은 심리 분석을 가지고 있습니다. 해당 인물의 현재 감정 상태는 {json_data['emotion']} 입니다.
                        해당인물의 자존감 수치는 {json_data['selfEsteem_base']}이고, 정신력 수치는 {json_data['mentalHealth_base']}은 이정도, 신체건강 수치는 {json_data['physicalHealth_base']} 입니다.
                        해당인물은 0에서 {json_data['all_modifier']*20} 정도로 능력치가 증가 또는 감소합니다. 해당인물이 상대하게 되는 SCP의 설명은 다음과 같습니다.

                        {scp_data['Description']}

                        해당 인물은 SCP를 격리시키기 위해 파견된 요원이며 격리시키기위에 제압하는 과정에서의 성공/실패 유부, 만약 실패했다면 사망여부와 이유, 따른 정신력과 정신건강 및 감정 상태의 변화, 신체 건강의 변화와 간단한 사건 보고서를 제출해주십시오
                        """
                        model_name = "gemini-2.5-flash" # 구조화된 출력을 지원하는 모델 사용

                        # run blocking API call in a thread to avoid blocking the event loop
                        def _call_genai():
                            return G_client.models.generate_content(
                                model=model_name,
                                contents=prompt,
                                config=types.GenerateContentConfig(
                                    response_mime_type="application/json",
                                    response_schema=Fight_Result,
                                ),
                            )

                        try:
                            # wait up to 20 seconds for the model to respond
                            response = await asyncio.wait_for(asyncio.to_thread(_call_genai), timeout=20)
                        except asyncio.TimeoutError:
                            # API call timed out — treat as failure and continue
                            embed = discord.Embed(
                                title="격리 실패 (타임아웃)",
                                description="응답이 지연되어 결과를 가져오지 못했습니다.",
                                color=discord.Color.red()
                            )
                            print_embed.append(embed)
                            # skip processing this employee's fight result
                            continue
                        except Exception as e:
                            embed = discord.Embed(
                                title="격리 실패 (오류)",
                                description=f"외부 API 호출 중 오류가 발생했습니다: {e}",
                                color=discord.Color.red()
                            )
                            print_embed.append(embed)
                            continue

                        Fight_data = json.loads(response.text)
                        if Fight_data['Success'] == True:
                            embed = discord.Embed(
                                title=f"격리 성공",
                                description=Fight_data['Result'],
                                color=discord.Color.green()
                            )
                            for fi in range(5):
                                if should_break_outer:
                                    break
                                for rn in range(5):                
                                    Containment_data = json_read(f'DB/{interaction.user.id}/Containment/F{fi+1}/{get_ordinal(rn+1)}.json')
                                    if Containment_data['unlock']:
                                        if Containment_data['SCP_Name'] == None:
                                            scp_data = {
                                                "unlock": True,
                                                "SCP_Name": scp_data['SCP_Name'],
                                                "SCP_Number": scp_data['SCP_Number'],
                                                "Containment_Class": scp_data['Containment_Class'],
                                                "Description": scp_data['Description'],
                                                "Reward": scp_data['Reward']
                                            }
                                            json_write(f'DB/{interaction.user.id}/Containment/F{fi+1}/{get_ordinal(rn+1)}.json', scp_data)
                                            should_break_outer = True
                                            break
                                        else:
                                            pass
                        else:
                            embed = discord.Embed(
                                title=f"격리 실패",
                                description=Fight_data['Result'],
                                color=discord.Color.red()
                            )
                        if Fight_data["Death"] == True:
                            embed.add_field(name=f'{json_data['name']}은 파견 중 사망하였습니다.', value=f'**`{json_data['name']}`**은 최선을 다했지만 끝내 사망하였습니다. 이에 따라 재단은 {json_data['name']}씨의 유가족에게 소정의 위로금 10000$를 지급하기로 했습니다.', inline=True)
                            user['Money'] -= 10000
                            json_write(f'DB/{interaction.user.id}/History/{i+1}.json', json_data)
                            os.remove(f'DB/{interaction.user.id}/Empoly/{i+1}.json')
                        else:
                            json_data['selfEsteem_base'] += Fight_data['Change_selfEsteem']
                            json_data['mentalHealth_base'] += Fight_data['Change_mentalHealth']
                            json_data['physicalHealth_base'] += Fight_data['Change_hysicalHealth']

                            if json_data['selfEsteem_base'] >= 100:
                                json_data['selfEsteem_base'] = 100
                            elif json_data['selfEsteem_base'] <= 0:
                                json_data['selfEsteem_base'] = 0

                            if json_data['mentalHealth_base'] >= 100:
                                json_data['mentalHealth_base'] = 100
                            elif json_data['mentalHealth_base'] <= 0:
                                json_data['mentalHealth_base'] = 0

                            if json_data['physicalHealth_base'] >= 100:
                                json_data['physicalHealth_base'] = 100
                            elif json_data['physicalHealth_base'] <= 0:
                                json_data['physicalHealth_base'] = 0
                            json_data['emotion'] = Fight_data['Change_emotion']
                            json_write(f'DB/{interaction.user.id}/empoly/{i+1}.json', json_data)
                            print_embed.append(embed)
        user['days'] += 1
        total_pMoney = 0
        _temp = False
        if user['days'] % 7 == 0:
            for a in range(5):
                for b in range(5):                
                    json_data = json_read(f'DB/{interaction.user.id}/Containment/F{a+1}/{get_ordinal(b+1)}.json')
                    if json_data['unlock']:
                        if json_data['SCP_Name'] != None:
                            user['Money'] += json_data['Reward']
                            total_pMoney += json_data['Reward']
                            _temp = True
        if _temp:
            moneyembed = discord.Embed(
                title="지원금이 지급 되었습니다.",
                color=discord.Color.green(),
                description=f"`지원금: +{total_pMoney}`"
            )
            print_embed.append(moneyembed)
        json_write(f'DB/{interaction.user.id}/{interaction.user.id}.json', user)
        if print_embed == []:
            await interaction.edit_original_response(embed=main_menu_embed(interaction.user.id), view=Sel_Action())
        else:
            await interaction.edit_original_response(embeds=print_embed, view=only_back_home_button())

@client.tree.command(name="게임메뉴", description="게임 시작하기", guild=GUILD_ID)
async def hello(interaction: discord.Interaction):
    if os.path.exists(f'DB/{interaction.user.id}/{interaction.user.id}.json'):
        json_read(f'DB/{interaction.user.id}/Containment/F1/1st.json')
        await interaction.response.send_message(embed=main_menu_embed(interaction.user.id), view=Sel_Action())
    else:
        data = {
            "unlock": False,
            "SCP_Name": None,
            "SCP_Number": None,
            "Containment_Class": None,
            "Description": None,
        }
        for i in range(5):
            os.makedirs(f'DB/{interaction.user.id}/Containment/F{i+1}', exist_ok=True)
            for n in range(5):
                json_write(f'DB/{interaction.user.id}/Containment/F{i+1}/{get_ordinal(n+1)}.json', data)
        os.makedirs(f'DB/{interaction.user.id}/Empoly', exist_ok=True)
        os.makedirs(f'DB/{interaction.user.id}/Advanture', exist_ok=True)
        os.makedirs(f'DB/{interaction.user.id}/History', exist_ok=True)
        data['unlock'] = True
        json_write(f'DB/{interaction.user.id}/Containment/F1/1st.json', data)
        json_write(f'DB/{interaction.user.id}/{interaction.user.id}.json', {"days": 1, "Money": 1000000})
        embed = discord.Embed(
            title="당신은 제282-0724 평행우주 제158K 기지의 기지 이사관 입니다.",
            description=f"""**`저희 제282-0724 평행우주 SCP재단의 제158K 기지의 기지 이사관 자리를 맡은 것을 진심으로 축하합니다! 당신은 기지 이사관으로서 다양한 SCP 및 직원을 감리 감독하고 그 성과에 따라 기지 지원금이 지급될 것입니다.다시 한번 저희 SCP 재단을 위해 봉사하는 것에 깊이 감사함을 표하며, {interaction.user.name}님의 탁월한 리더쉽을 기대합니다.`**""",
            color=discord.Color.dark_orange()
        )
        embed.set_footer(text="-관리자, The Administrator")
        embed.set_author(name="확보, 격리, 보호")
        embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/862959997465657356/1426865666291404860/scp-logo.png?ex=68ecc7b4&is=68eb7634&hm=28b1150868a94a5d2b5b205eb3f5611254a866c388671b1040d858f5b81edd1b&")
        await interaction.response.send_message(embed=embed, view=FirstGameStart())

class Gen_Empoly(BaseModel):
    """직원 생성 구조"""
    name: str = Field(description="이름")
    career: str = Field(description="겅력")
    personality: str = Field(description="성격")
    introductionDialogue: str = Field(description="캐릭터에 몰입한 짧은 자기소개 대사 (1-2 문장). 관리자인 플레이어에게 말하는 형식입니다.")
    profileSummary: str = Field(description="전문 분야 및 심리 평가에 대한 한 문단 요약.")
    emotion: str = Field(description="현재 감정 상태")
    selfEsteem_base: int = Field(description="30에서 70 사이의 값의 자존감 기본 능력치")
    mentalHealth_base: int = Field(description="30에서 70 사이의 값의 정신 건강 기본 능력치")
    physicalHealth_base: int = Field(description="30에서 70 사이의 값의 신체 건강 기본 능력치")
    all_modifier: int = Field(description="0에서 3값의 성장 잠재력 수정치")

class Fight_Result(BaseModel):
    """전투"""
    Success: bool = Field(description="성공/실패유무")
    Death: bool = Field(description="만약 실패했다면 사망했는지")
    Death_lesson: str = Field(description="사망이유")
    Change_selfEsteem: int = Field(description="변경된 자존감 수치")
    Change_mentalHealth: int = Field(description="변경된 정신력 수치")
    Change_hysicalHealth: int = Field(description="변경된 신체 건강 수치")
    Change_emotion: str = Field(description="변경된 감정 상태")
    Result: str = Field(description="전투 결과 보고서")

@client.tree.command(name="직원채용", description="직원을 채용할수 있습니다.", guild=GUILD_ID)
async def Generate_Empoly(interaction: discord.Interaction, 이름: str, 겅력: str, 성격: str):
    short_cut = f'DB/{interaction.user.id}/Empoly/'
    if not os.path.exists(f'{short_cut}1.json' and f'{short_cut}2.json' and f'{short_cut}3.json' and f'{short_cut}4.json' and f'{short_cut}5.json' and f'{short_cut}6.json'):
        G_client = genai.Client()
        embed = discord.Embed(
            title="생각중 입니다..."
        )
        await interaction.response.send_message(embed=embed)
        prompt = f"""비밀 괴이 연구소 연구원의 상세 프로필을 생성해 주세요. 모든 응답은 한국어로 작성해야 합니다. 이들은 비범한 상황에 처한 평범한 전문가일 수 있으니, 너무 과장되지 않게 설정해 주세요.
        입력 (이력서 키워드):
        - Name: {이름}
        - Career: {겅력}
        - Personality: {성격}
        """
        model_name = "gemini-2.5-flash" # 구조화된 출력을 지원하는 모델 사용

        response = G_client.models.generate_content(
            model=model_name,
            contents=prompt,
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
                response_schema=Gen_Empoly,
            ),
        )
        # print(response.text)
        json_data = json.loads(response.text)
        json_data['going_out'] = 0
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
        embed_slot = discord.Embed(
        title=f"직원 슬롯",
        color=discord.Color.orange() # You can use predefined colors or hex codes
        )
        for i in range(6):
            if os.path.exists(f'DB/{interaction.user.id}/Empoly/{i+1}.json'):
                check_json_data = json_read(f'DB/{interaction.user.id}/Empoly/{i+1}.json')
                embed_slot.add_field(name=f"✅ {i+1}번 슬롯", value=f"`{check_json_data['name']}`", inline=True)
            else:
                embed_slot.add_field(name=f"❌ {i+1}번 슬롯", value=f"`빈 슬롯입니다.`", inline=True)
        await interaction.edit_original_response(embeds=[embed, embed_slot], view=register(json_data))
    else:
        embed = discord.Embed(
            title="직원 슬롯이 꽉찼습니다!",
            color=discord.Color.red()
        )
        await interaction.response.send_message(embed=embed, view=only_back_home_button())

if __name__ == "__main__":
    client.run(DISCORD_TOKEN)


