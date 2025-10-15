import discord
import os
from discord.ui import Select, Button, View, select
from utility import json_read, json_write, Sel_Action, main_menu_embed, get_ordinal, only_back_home_button

class shop_menu(View):
    def __init__(self):
        super().__init__()

    @discord.ui.button(label="자아긍정 알약", style=discord.ButtonStyle.primary, emoji="💊")
    async def use_potion_selfEsteem(self, interaction: discord.Interaction, button: Button):
        if json_read(f'DB/{interaction.user.id}/{interaction.user.id}.json')['Money'] >= 50000:
            embed = discord.Embed(
                title="누구에게 사용하시겠습니까?",
                description="자아긍정 알약을 사용할 직원을 선택해주세요.",
                color=discord.Color.blue()
            )
            await interaction.response.edit_message(embed=embed, view=shop_menu_empoly_list(interaction.user.id, 'selfEsteem_base'))
        else:
            embed = discord.Embed(
                title="돈이 부족합니다!",
                color=discord.Color.red()
            )
            await interaction.response.edit_message(embed=embed, view=only_back_home_button())
    @discord.ui.button(label="심리진정 알약", style=discord.ButtonStyle.primary, emoji="💊")
    async def use_potion_mentalHealth(self, interaction: discord.Interaction, button: Button):
        if json_read(f'DB/{interaction.user.id}/{interaction.user.id}.json')['Money'] >= 50000:
            embed = discord.Embed(
                title="누구에게 사용하시겠습니까?",
                description="심리진정 알약을 사용할 직원을 선택해주세요.",
                color=discord.Color.blue()
            )
            await interaction.response.edit_message(embed=embed, view=shop_menu_empoly_list(interaction.user.id, 'mentalHealth_base'))
        else:
            embed = discord.Embed(
                title="돈이 부족합니다!",
                color=discord.Color.red()
            )
            await interaction.response.edit_message(embed=embed, view=only_back_home_button())
    @discord.ui.button(label="신체회복 알약", style=discord.ButtonStyle.primary, emoji="💊")
    async def use_potion_physicalHealth(self, interaction: discord.Interaction, button: Button):
        if json_read(f'DB/{interaction.user.id}/{interaction.user.id}.json')['Money'] >= 50000:
            embed = discord.Embed(
                title="누구에게 사용하시겠습니까?",
                description="신체회복 알약을 사용할 직원을 선택해주세요.",
                color=discord.Color.blue()
            )
            await interaction.response.edit_message(embed=embed, view=shop_menu_empoly_list(interaction.user.id, 'physicalHealth_base'))
        else:
            embed = discord.Embed(
                title="돈이 부족합니다!",
                color=discord.Color.red()
            )
            await interaction.response.edit_message(embed=embed, view=only_back_home_button())
    @discord.ui.button(label="격리실 해금", style=discord.ButtonStyle.primary, emoji="🔓")
    async def unlock_con(self, interaction: discord.Interaction, button: Button):
        if json_read(f'DB/{interaction.user.id}/{interaction.user.id}.json')['Money'] >= 200000:
            embed = discord.Embed(
                title="격리실을 해금 하시겠습니까?",
                color=discord.Color.blue()
            )
            await interaction.response.edit_message(embed=embed, view=unlock_con())
        else:
            embed = discord.Embed(
                title="돈이 부족합니다!",
                color=discord.Color.red()
            )
            await interaction.response.edit_message(embed=embed, view=only_back_home_button())
    @discord.ui.button(label="돌아가기", style=discord.ButtonStyle.red, emoji="🏠")
    async def Cancel_register(self, interaction: discord.Interaction, button: Button):
        await interaction.response.edit_message(embed=main_menu_embed(interaction.user.id), view=Sel_Action())

class unlock_con(View):
    def __init__(self):
        super().__init__()

    @discord.ui.button(label="실행", style=discord.ButtonStyle.green, emoji="✅")
    async def use_potion_run(self, interaction: discord.Interaction, button: Button):
        embed = discord.Embed(
            title=f"격리실 해제 되었습니다.",
            color=discord.Color.green()
        )
        should_break_outer = False
        for fi in range(5):
            if should_break_outer:
                break
            for rn in range(5):                
                Containment_data = json_read(f'DB/{interaction.user.id}/Containment/F{fi+1}/{get_ordinal(rn+1)}.json')
                if Containment_data['unlock'] == False:
                    should_break_outer = True
                    Containment_data['unlock'] = True
                    json_write(f'DB/{interaction.user.id}/Containment/F{fi+1}/{get_ordinal(rn+1)}.json', Containment_data)
                    break
        user_data=json_read(f'DB/{interaction.user.id}/{interaction.user.id}.json')
        user_data['Money'] -= 200000
        json_write(f'DB/{interaction.user.id}/{interaction.user.id}.json', user_data)
        await interaction.response.edit_message(embed=embed, view=only_back_home_button())
    @discord.ui.button(label="취소", style=discord.ButtonStyle.red, emoji="❌")
    async def use_potion_cancel(self, interaction: discord.Interaction, button: Button):
        await interaction.response.edit_message(embed=main_menu_embed(interaction.user.id), view=Sel_Action())

class shop_menu_empoly_list(View):
    def __init__(self, user_id: int, potion):
        super().__init__()

        self.potion = potion
        options = []
        empoly_dir = f'DB/{user_id}/Empoly/'

        if os.path.isdir(empoly_dir):
            for i in range(1, 7):
                employee_file = f'{empoly_dir}{i}.json'
                if os.path.exists(employee_file):
                    try:
                        employee_data = json_read(employee_file)
                        employee_name = employee_data.get('name', f'직원 {i}')
                        options.append(discord.SelectOption(
                            label=f"{employee_name}", 
                            value=str(i)
                        ))
                    except Exception as e:
                        print(f"직원 파일 읽기 오류 {employee_file}: {e}")

        if not options:
            options.append(discord.SelectOption(label="채용한 직원이 없습니다.", value="no_employee", disabled=True))

        self.employee_select = Select(
            placeholder="치료할 직원을 선택하세요...",
            min_values=1,
            max_values=1,
            options=options
        )
        self.employee_select.callback = self.select_callback
        self.add_item(self.employee_select)

    async def select_callback(self, interaction: discord.Interaction):
        selected_slot = self.employee_select.values[0]
        
        empoly_dir = f'DB/{interaction.user.id}/Empoly/'
        empoly_data = json_read(f'{empoly_dir}{selected_slot}.json')
        if empoly_data[self.potion] == 100:
            embed = discord.Embed(
            title="해당직원의 해당 능력치는 이미 100입니다.",
            color=discord.Color.red()
            )
            await interaction.response.edit_message(embed=embed, view=only_back_home_button())
        else:
            embed = discord.Embed(
                title=f"{empoly_data['name']} 직원을 치료하시겠습니까?",
                color=discord.Color.green()
            )
            await interaction.response.edit_message(embed=embed, view=re_check_potion(self.potion, f'{empoly_dir}{selected_slot}.json'))

class re_check_potion(View):
    def __init__(self, potion, data_path):
        super().__init__()
        self.potion = potion
        self.data_path = data_path

    @discord.ui.button(label="실행", style=discord.ButtonStyle.green, emoji="✅")
    async def use_potion_run(self, interaction: discord.Interaction, button: Button):
        empoly_data = json_read(self.data_path)
        _temp = empoly_data[self.potion] + 30
        if _temp >= 100:
            _temp = 100
        embed = discord.Embed(
            title=f"{empoly_data['name']}의 능력치가 회복 되었습니다.",
            description=f"{empoly_data[self.potion]} -> {_temp}",
            color=discord.Color.green
        )
        empoly_data[self.potion] = _temp
        json_write(self.data_path, empoly_data)
        user_data=json_read(f'DB/{interaction.user.id}/{interaction.user.id}.json')
        user_data['Money'] -= 50000
        json_write(f'DB/{interaction.user.id}/{interaction.user.id}.json', user_data)
        await interaction.response.edit_message(embed=embed, view=only_back_home_button())
    @discord.ui.button(label="취소", style=discord.ButtonStyle.red, emoji="❌")
    async def use_potion_cancel(self, interaction: discord.Interaction, button: Button):
        await interaction.response.edit_message(embed=main_menu_embed(interaction.user.id), view=Sel_Action())