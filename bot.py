#packages
import os
import discord
from discord.ext import commands
from dotenv import load_dotenv
import time
import openAIClient
import fileManager

#version
__version__ = "0.0.1.3"

#constants
#VALID_CMD_STR = "Valid commands are !recap, !recruit, !press, !rumor, !reloadWorld, !exit and !fan"
VALID_CMD_STR = "Valid commands are !recap and !preview"

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

async def sendFile(ctx, filePath):
    guild = bot.get_guild(DISCORD_SERVER)
    if guild:
        target_channel = guild.get_channel(DISCORD_CHANNEL)
        if target_channel and filePath :
            # Create a discord.File object
            file_to_send = discord.File(filePath)
            await target_channel.send(file=file_to_send, content=f"@everyone Hot off the press from {ctx.author.mention}")
        else:
            if target_channel:
                print (f"Invlaid File Path {filePath}")
                await ctx.channel.send(f"Invlaid File Path {filePath}")
                return
            else:
                print("Target channel not found.")
                await ctx.channel.send("Target channel not found.")
                return
    else:
        print("Server not found.")
        await ctx.channel.send("Server not found.")
        return
    await ctx.channel.send("Thanks! Your message has been sent to recaps channel!")

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
async def uptime(ctx):
    uptime_seconds = time.time() - start_time
    time_string = fileManager.format_time_fixed(uptime_seconds)
    await ctx.send(time_string)

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
    #build recap name
    recapName = fileManager.createFileName(ctx)
    
    #generate content
    filePath = await openAIClient.gameRecap(fileManager.world_guide, fileManager.STYLE_GUIDES["game_recap.txt"], fileManager.PERSONALITIES["Carter_Langofrd.txt"], ctx.message.content, recapName)
    
    #send the file
    await sendFile(ctx, filePath)

@bot.command()
async def preview(ctx):
    #build preview name
    previewName = fileManager.createFileName(ctx)
    
    #generate content
    filePath = await openAIClient.gamePreview(fileManager.world_guide, fileManager.STYLE_GUIDES["game_preview.txt"], fileManager.PERSONALITIES["RG3.txt"], ctx.message.content, previewName)
    
    #send the file
    await sendFile(ctx, filePath)
    
@bot.command()
async def recruit(ctx):
    #build preview name
    previewName = fileManager.createFileName(ctx)
    
    #generate content
    filePath = await openAIClient.recruit_spotlight(
        world_guide=fileManager.world_guide, 
        article_style_guid=fileManager.STYLE_GUIDES["recruit_spotlight.txt"], 
        picture_style_guide=fileManager.STYLE_GUIDES["recruit_spotlight.txt"], 
        personality_guide=fileManager.PERSONALITIES["Pat_McAfee.txt"], 
        user_input=ctx.message.content, 
        report_name=previewName
        )
    
    #send the file
    await sendFile(ctx, filePath)
    
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
        else:
            print(f"Invalid Command by {message.author}")
            #respond to dm with invalid cmd name and list valid cmd names
            await message.channel.send("Commands must start with !. {VALID_CMD_STR}")
start_time= time.time()
fileManager.loadWorld()
bot.run(TOKEN)
