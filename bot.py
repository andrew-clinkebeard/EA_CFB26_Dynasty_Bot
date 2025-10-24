#main file to handlie initial discord message and to send out pdf

#version
__version__ = "0.0.1.3" 

#commands string
class msgCommands:
    cmd = ""
    GAME_RECAP_STR = "recap"
    RECRUIT_SPOTLIGHT_STR = "recruit"
    PRESS_RELEASE_STR = "press"
    FAN_BLOG_STR = "fan"
    RUMOR_MILL_STR = "rumor"

VALID_CMD_STR = "Valid commands are !recap, !recruit, !press, and !fan"

#packages
import os
import discord
from discord.ext import commands
from dotenv import load_dotenv
import openAIClient

#load tokens
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

# Set up bot with intents
intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.dm_messages = True

bot = commands.Bot(command_prefix="!", intents=intents)

# Replace this with your target channel ID
TARGET_CHANNEL_ID = 1431123905304596510  # example: 128502034523456789   

@bot.event
async def on_ready():
    print(f"{bot.user} is online and ready to receive DMs!")

@bot.event
async def on_message(message: discord.Message):
    # Ignore messages from the bot itself
    if message.author == bot.user:
        return

    # Check if message is a DM (private message)
    if isinstance(message.channel, discord.DMChannel):
        #determine which message it is
        cmdIndex = message.content.find('!')
        if cmdIndex != -1:
            #split command from rest of string
            msgParts = message.content.split(" " , 1)
            msgCommands.cmd = msgParts[0].strip('!')
            msgContents = msgParts[1]

            match msgCommands.cmd:
                case msgCommands.GAME_RECAP_STR:
                    filePath = openAIClient.gameRecap()
                case msgCommands.RECRUIT_SPOTLIGHT_STR:
                    openAIClient.pressRelease()
                case msgCommands.PRESS_RELEASE_STR:
                    openAIClient.pressRelease()
                case msgCommands.FAN_BLOG_STR:
                    openAIClient.fanBlogs()
                case _ :
                    await message.channel.send(f"Invalid Command: {VALID_CMD_STR}")

            guild = bot.get_guild(1431022749047984302)  # Replace with your server ID
            if guild:
                target_channel = guild.get_channel(TARGET_CHANNEL_ID)
                if target_channel:
                    # Post the DM content to your channel
                    await target_channel.send(
                        f"📩 DM from **{message.author}**: Command: {msgCommands.cmd} Contents: {msgContents}"
                    )
                     # Create a discord.File objectz
                    file_to_send = discord.File(filePath)
                    await target_channel.send(file=file_to_send, content="@everyone Hot off the press")
                    #await target_channel.send(file=discord.File(r'C:\\Users\\Andrew Clinkenbeard\\Desktop\\8.jpg'))
                else:
                    print("Target channel not found.")
            else:
                print("Guild not found.")

            # Optionally reply to the user
            await message.channel.send("Thanks! Your message has been sent to the admins. ✅")
        else:
            print("Command not found.")
            #respond to dm with invalid cmd name and list valid cmd names
            await message.channel.send("Commands must start with !. {VALID_CMD_STR}")

    #not sure if we need or not, throws error rn
    # Process other bot commands (so !commands still work)
    #await bot.process_commands(message) 


bot.run(TOKEN)
