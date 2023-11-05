import json
import os
from dotenv import load_dotenv
import discord
from discord import app_commands
from discord.ext import commands
import random

load_dotenv()
BOT_TOKEN = os.getenv('DISCORD_TOKEN')
GUILD_ID = int(os.getenv('GUILD_ID'))

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(intents=intents, command_prefix='!')
QUIZFILENAME = "quiz.json"

with open('quiz.json', 'r') as file:
    quiz_data = json.load(file)
    questions = quiz_data["questions"]
file.close()

# Called once bot is ready for further action.
@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')
    await bot.tree.sync()

@bot.command()
@commands.is_owner()
async def sync(ctx):
    await ctx.bot.tree.sync()
    await ctx.send("Synced")

class CurrentQuestion():
    def __init__(self):
        self.current_question = None
        self.options = None
        self.current_question_index = None

    def new_question(self):
        self.current_question = random.choice(questions)
        self.options = self.current_question["options"] 
        self.current_question_index = self.options.index(self.current_question["answer"])

class Buttons(discord.ui.View):
    def __init__(self):
         super().__init__()
         self.value = None

    def disable_all_buttons(self):
        for child in self.children:
            child.disabled = True
    
    async def handle_confirmation(self, interaction: discord.Interaction, value: int, button: discord.ui.Button):
        self.disable_all_buttons()
        if curr_question.current_question_index == value:
          button.style = discord.ButtonStyle.green
        else:
          button.style = discord.ButtonStyle.red
        self.stop()
        await interaction.response.edit_message(view=self)
    @discord.ui.button(label='1', style=discord.ButtonStyle.blurple)
    async def one(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.handle_confirmation(interaction, 0, button)            
       
    @discord.ui.button(label='2', style=discord.ButtonStyle.blurple)
    async def two(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.handle_confirmation(interaction, 1, button)
     
    @discord.ui.button(label='3', style=discord.ButtonStyle.blurple)
    async def three(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.handle_confirmation(interaction, 2, button)
           
    @discord.ui.button(label='4', style=discord.ButtonStyle.blurple)
    async def four(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.handle_confirmation(interaction, 3, button)
           
    @discord.ui.button(label='5', style=discord.ButtonStyle.blurple)
    async def five(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.handle_confirmation(interaction, 4, button)
    
curr_question = CurrentQuestion()

@bot.tree.command(name="question")
async def question(interaction: discord.Interaction):
    """Gives a question"""
    curr_question.new_question()
    embed = discord.Embed(
        title= 'Quiz Question', 
        description=curr_question.current_question["question"])
        
    for i,c in enumerate(curr_question.options):
        embed.add_field(name=f'{i+1}: {curr_question.options[i]}', value="", inline=False)

    view = Buttons()
    await interaction.response.send_message(embed=embed, view=view )


bot.run(BOT_TOKEN)
