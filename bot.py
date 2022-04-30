from discord.ext import commands
import discord



intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(command_prefix='pog!', intents=intents)

bot.load_extension('valorant')
bot.load_extension('smokegrass')

# scp .\bot.py pi@raspberrypi:~/Desktop/discordbot
# scp .\mongod.service izzaz@DESKTOP-DOGCEP1:~/Desktop/

bot.run('OTY4ODkyNjE4NzA2NjUzMjQ1.YmldkQ.jBpymg3cI_m-0orVfr_TFQ8piYA')