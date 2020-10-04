import discord
import os
import random
import math

from discord.ext.commands import CommandNotFound
from discord.ext import commands
from discord.utils import get
import time
import datetime
import asyncio
import apscheduler
import numpy as np
from apscheduler.schedulers.asyncio import AsyncIOScheduler

scheduler = AsyncIOScheduler()
bot = commands.Bot(command_prefix = "/")
print("started Speed Dating Bot")

@bot.event
async def on_ready():
    global vc
    global guild
    guild = bot.guilds[0]
    print(f'We have logged in as {bot.user} at {datetime.datetime.now()}')

@bot.command()
@commands.has_guild_permissions(administrator=True)
async def startSpeedDating(ctx):
    if not scheduler.running:
        scheduler.start()
        channel = bot.get_channel(int(os.environ.get('ANNOUNCEMENT_CHANNEL')))
        await channel.send('SpeedDating wurde gestartet')
        await rematchUsers()


@bot.command()
@commands.has_guild_permissions(administrator=True)
async def stopSpeedDating(ctx):
    if scheduler.running:
        channel = bot.get_channel(int(os.environ.get('ANNOUNCEMENT_CHANNEL')))
        await channel.send('SpeedDating wurde beendet')
        scheduler.shutdown()

# ignore command not found errors
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, CommandNotFound):
        return
    raise error
    
async def announceRematch():
    channel = bot.get_channel(int(os.environ.get('ANNOUNCEMENT_CHANNEL')))
    await channel.send('Neue Datezuweisung in 10 Sekunden!')

async def listVoiceChannels():
    voice_channel_list = []
    for channel in guild.voice_channels:
        voice_channel_list.append(channel)
    return voice_channel_list

#
async def rematchUsers():
    waitingRoom = bot.get_channel(int(os.environ.get('WAITING_CHANNEL')))
    speedDatingChannels = [i for i in await listVoiceChannels() if str(i).startswith('SpeedDating#')]
    for channel in speedDatingChannels:
        for user in channel.members:
            await user.move_to(waitingRoom)
        await channel.delete()
    datingUsers = waitingRoom.members
    if len(datingUsers) == 0:
        print(f"No Erstis to Speeddate :(")
        return
    print(f"Speeddating uses {len(datingUsers)} Erstis")
    random.shuffle(datingUsers)
    pairs = np.array_split(np.array(datingUsers), math.ceil(len(datingUsers)/2))
    i=1
    for pair in pairs:
        category = bot.get_channel(int(os.environ.get('SPEEDDATING_CATEGORY')))
        channel = await category.create_voice_channel('SpeedDating#'+str(i), user_limit=2)
        for user in pair:
            await user.move_to(channel)


#Schedulers
scheduler.add_job(rematchUsers, 'interval', minutes=2, start_date=datetime.datetime.now() + datetime.timedelta(0,10))
scheduler.add_job(announceRematch, 'interval', minutes=2, start_date=datetime.datetime.now())

token = os.environ.get('BOT_TOKEN')

bot.run(token)