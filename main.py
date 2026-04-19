import get_ics_file
import read_file
import config
import os
from datetime import date, timedelta
import time
import asyncio
import discord
import bot_token
from discord.ext import tasks, commands
from discord import app_commands
import data

year = str(date.today())[:5]
today = date.today()

def get_file():
    zeus = get_ics_file.Zeus()
    file = zeus.download()

    return read_file.ICS(file)

global ics
ics = None

class Client(commands.Bot):
    async def on_ready(self):
        print(f'We have logged in as {client.user}')
        if not update_ics.is_running():
            update_ics.start()
        try:
            guild = discord.Object(id=config.GUILD)
            synced = await self.tree.sync(guild=guild)
            print(f"Synced {len(synced)} commands to guild!")
        except Exception as e:
            print(f"Error: {e}")

    async def on_message(self,message):
        if message.author == client.user:
            return

        if message.content.startswith('$hello'):
            await message.channel.send('Hello!')

intents = discord.Intents.default()
intents.message_content = True

client = Client(command_prefix='!', intents=intents)

GUILD_ID = discord.Object(id=config.GUILD)

@client.tree.command(name="today",description="See today's planning", guild=GUILD_ID)
async def Today(interaction: discord.Interaction):
    ics = read_file.ICS(config.FILE_PATH)
    ics.open()
    result = ics.parse_day(str(today))

    await interaction.response.send_message(data.print_day(result))
    ics.close()

@client.tree.command(name="week",description="See the week's planning", guild=GUILD_ID)
async def Week(interaction: discord.Interaction):
    ics = read_file.ICS(config.FILE_PATH)
    ics.open()
    list = []
    monday = data.detect_week(today)
    for i in range (0,7):
        list.append(ics.parse_day(str(monday + timedelta(days=i))))

    await interaction.response.send_message(data.print_week(list,monday))
    ics.close()

@client.tree.command(name="planning",description="See the day's planning", guild=GUILD_ID)
async def Planning(interaction: discord.Interaction, month: str, day: str):
    ics = read_file.ICS(config.FILE_PATH)
    ics.open()
    result = ics.parse_day(str(f"{year}{month}-{day}"))

    await interaction.response.send_message(data.print_day(result))
    ics.close()

# @client.tree.command(name="debug",description="test func", guild=GUILD_ID)
# async def Degub(interaction: discord.Interaction, month: str, day: str):
#    ics = read_file.ICS(config.FILE_PATH)
#    ics.open()
#    ics.read_all(str(f"{year}{month}-{day}"))
#
#    await interaction.response.send_message("printed vals in terminal")
#    ics.close()

@tasks.loop(seconds=config.CLOCK)
async def update_ics():
    try: os.remove(config.FILE_PATH)
    except FileNotFoundError: pass

    await asyncio.to_thread(get_file)
    print("ICS file updated")

@update_ics.before_loop
async def before_update():
    await client.wait_until_ready()

client.run(bot_token.TOKEN)