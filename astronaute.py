import os
import discord
from discord.ext import commands
import asyncio
import pymongo
from database.connect import db_connect
intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(command_prefix = '.', intents = intents)
bot.remove_command('help')
servers = db_connect()

for file in os.listdir("cogs"):
    if file.endswith(".py"):
        name = file[:-3]
        bot.load_extension(f"cogs.{name}")

print("Bot launched")

@bot.event
async def on_ready():
    while True:
        count = 0
        voice = bot.get_channel(769619638010773524)
        for member in bot.get_all_members():
            count += 1
        await voice.edit(name = f'ℹ️ Membre: {count}')
        print(count)
        voice = bot.get_channel(769620784518922240)
        count = 0
        data = servers.find({})
        for i in data:
            count = len(i['current_players'])
        await voice.edit(name = f'ℹ️ En jeu: {count}')
        print(count)
        await asyncio.sleep(30)


if __name__ == "__main__":
    bot.run("NzU2NTE2MDUyNTE0MzczNzM0.X2S-eg.5thR1HK5BJ6OPrFLoTasEFLijJk")