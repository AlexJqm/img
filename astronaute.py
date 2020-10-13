import os
import discord
from discord.ext import commands

bot = commands.Bot(command_prefix='!')
bot.remove_command('help')

for file in os.listdir("events"):
    if file.endswith(".py"):
        name = file[:-3]
        bot.load_extension(f"events.{name}")

for file in os.listdir("cogs"):
    if file.endswith(".py"):
        name = file[:-3]
        bot.load_extension(f"cogs.{name}")

print("Serveur ON")

if __name__ == "__main__":
    bot.run("NzYzNDQzMjU4ODg5MzM4OTAw.X33x8Q.v6ab7HeG6-4Wp6nQ3BCWCCI3_FQ")
    NzU2NTE2MDUyNTE0MzczNzM0.X2S-eg.5thR1HK5BJ6OPrFLoTasEFLijJk