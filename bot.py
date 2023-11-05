import json
import os
from dotenv import load_dotenv
import nextcord
from nextcord.ext import commands
import random
# importing the other python files

load_dotenv()
BOT_TOKEN = os.getenv('DISCORD_TOKEN')
GUILD_ID = int(os.getenv('GUILD_ID'))

intents = nextcord.Intents.default()
intents.message_content = True

bot = commands.Bot(intents=intents)
QUIZFILENAME = "quiz.json"

with open('quiz.json', 'r') as file:
    quiz_data = json.load(file)
    questions = quiz_data["questions"]
file.close()

# Called once bot is ready for further action.
@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')

class CurrentQuestion():
    def __init__(self):
        self.current_question = None
        self.options = None
        self.current_question_index = None

    def new_question(self):
        self.current_question = random.choice(questions)
        self.options = self.current_question["options"] 
        self.current_question_index = self.options.index(self.current_question["answer"])

class Buttons(nextcord.ui.View):
    def __init__(self):
         super().__init__()
         self.value = None

    def disable_all_buttons(self):
        for child in self.children:
            child.disabled = True
    
    async def handle_confirmation(self, interaction: nextcord.Interaction, value: int, button: nextcord.ui.Button):
        self.disable_all_buttons()
        if curr_question.current_question_index == value:
          button.style = nextcord.ButtonStyle.green
        else:
          button.style = nextcord.ButtonStyle.red
        self.stop()
        await interaction.response.edit_message(view=self)
    @nextcord.ui.button(label='1', style=nextcord.ButtonStyle.blurple)
    async def one(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        await self.handle_confirmation(interaction, 0, button)            
       
    @nextcord.ui.button(label='2', style=nextcord.ButtonStyle.blurple)
    async def two(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        await self.handle_confirmation(interaction, 1, button)
     
    @nextcord.ui.button(label='3', style=nextcord.ButtonStyle.blurple)
    async def three(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        await self.handle_confirmation(interaction, 2, button)
           
    @nextcord.ui.button(label='4', style=nextcord.ButtonStyle.blurple)
    async def four(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        await self.handle_confirmation(interaction, 3, button)
           
    @nextcord.ui.button(label='5', style=nextcord.ButtonStyle.blurple)
    async def five(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        await self.handle_confirmation(interaction, 4, button)
    
curr_question = CurrentQuestion()

@bot.slash_command(guild_ids=[GUILD_ID], name="question", description="gives a question")
async def question( interaction: nextcord.Interaction):
    curr_question.new_question()
    embed = nextcord.Embed(
        title= 'Quiz Question', 
        description=curr_question.current_question["question"])
        
    for i,c in enumerate(curr_question.options):
        n = i+1
        embed.add_field(name=f'{n}: {curr_question.options[i]}', value="", inline=False)

    view = Buttons()
    await interaction.response.send_message(embed=embed, view=view )


bot.run(BOT_TOKEN)

