import os
import discord
from discord.ext import commands

bot = commands.Bot(command_prefix='.')
bot.remove_command('help')

for file in os.listdir("cogs"):
    if file.endswith(".py"):
        name = file[:-3]
        bot.load_extension(f"cogs.{name}")

print("Serveur ON")

if __name__ == "__main__":
    bot.run("NzU2NTE2MDUyNTE0MzczNzM0.X2S-eg.5thR1HK5BJ6OPrFLoTasEFLijJk")