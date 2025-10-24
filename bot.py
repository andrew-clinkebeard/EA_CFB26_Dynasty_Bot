import os
import discord
from discord.ext import commands
from dotenv import load_dotenv

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
        guild = bot.get_guild(1431022749047984302)  # Replace with your server ID
        if guild:
            target_channel = guild.get_channel(TARGET_CHANNEL_ID)
            if target_channel:
                # Post the DM content to your channel
                await target_channel.send(
                    f"📩 DM from **{message.author}**: {message.content}"
                )
            else:
                print("⚠️ Target channel not found.")
        else:
            print("⚠️ Guild not found.")

        # Optionally reply to the user
        await message.channel.send("Thanks! Your message has been sent to the admins. ✅")

    # Process other bot commands (so !commands still work)
    await bot.process_commands(message)


bot.run(TOKEN)
