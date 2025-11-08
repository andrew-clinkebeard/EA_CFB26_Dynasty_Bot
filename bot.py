#packages
import os
import sys
import discord
from datetime import datetime
from discord.ext import commands
from dotenv import load_dotenv
import openAIClient
import fileManager

#version
__version__ = "0.0.1.3"

#constants
#VALID_CMD_STR = "Valid commands are !recap, !recruit, !press, !rumor, !reloadWorld, !exit and !fan"
VALID_CMD_STR = "Valid commands are !recap"

#globals
filePath = ""

#load tokens
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
DISCORD_SERVER = int(os.getenv("DISCORD_SERVER"))
DISCORD_CHANNEL = int(os.getenv("DISCORD_CHANNEL"))

# Set up bot with intents
intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.dm_messages = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"{bot.user} is online and ready to receive DMs!")

@bot.command()
async def exit(ctx):
    await ctx.send("Shutting down…")
    await bot.close()

@bot.command()
async def helpme(ctx):
    await ctx.send(f"{VALID_CMD_STR}")

@bot.command()
async def restart(ctx):
    await bot.close() # Close the bot connection
    fileManager.loadWorld()
    bot.run(TOKEN)

@bot.command()
async def reloadWorld(ctx):
    fileManager.loadWorld()
    await ctx.send("World reloaded")

@bot.command()
async def hello(ctx):
    await ctx.send(f'Hello {ctx.author.display_name}! 👋')

@bot.command()
async def recap(ctx):
    global filePath
    # Get the current date and time
    now = datetime.now()
    # Format the datetime object into the desired string format
    timestamp_str = now.strftime("%Y%m%d%H%M%S")
    
    #build recap name
    recapName = "\\" + ctx.message.author.display_name + "_" + timestamp_str+  ".pdf"
    filePath = await openAIClient.gameRecap(fileManager.world_guide, fileManager.STYLE_GUIDES["game_recap.txt"], fileManager.PERSONALITIES["Carter_Langofrd.txt"], ctx.message.content, fileManager.reportDir, recapName)
    
@bot.command()
async def recruit(ctx):
    await ctx.send(f'recruit {ctx.author.display_name}! 👋')
    
@bot.command()
async def press(ctx):
    await ctx.send(f'press {ctx.author.display_name}! 👋')
    
@bot.command()
async def fan(ctx):
    await ctx.send(f'fan {ctx.author.display_name}! 👋')
    
@bot.command()
async def rumor(ctx):
    await ctx.send(f'rumor {ctx.author.display_name}! 👋')


@bot.event
async def on_message(message: discord.Message):
    # Ignore messages from the bot itself
    if message.author == bot.user:
        return

    # Check if message is a DM (private message)
    if isinstance(message.channel, discord.DMChannel):
        #determine which message it is
        cmdIndex = message.content.find('!')
        if cmdIndex == 0:
            #split command from rest of string
            msgParts = message.content.split(" " , 1)

            if len(msgParts) != 2:
                await bot.process_commands(message)
            else:
                await bot.process_commands(message)

                guild = bot.get_guild(DISCORD_SERVER)  # Replace with your server ID
                if guild:
                    target_channel = guild.get_channel(DISCORD_CHANNEL)
                    if target_channel and filePath :
                        # Create a discord.File object
                        file_to_send = discord.File(filePath)
                        await target_channel.send(file=file_to_send, content=f"@everyone Hot off the press from {message.author.mention}")
                    else:
                        print("Target channel not found.")
                else:
                    print("Guild not found.")

                # Optionally reply to the user
                await message.channel.send("Thanks! Your message has been sent to recaps channel!")
        else:
            print(f"Invalid Command by {message.author}")
            #respond to dm with invalid cmd name and list valid cmd names
            await message.channel.send("Commands must start with !. {VALID_CMD_STR}")

fileManager.loadWorld()
bot.run(TOKEN)
