import os
import discord
from discord.ext import commands
from colorama import Fore, init
intents = discord.Intents.default()
intents.members = True
bot = commands.Bot(command_prefix = '.', intents = intents)
bot.remove_command('help')

for file in os.listdir("cogs"):
    if file.endswith(".py"):
        name = file[:-3]
        bot.load_extension(f"cogs.{name}")

print(Fore.RED + "Bot launched" + Fore.RESET)

@bot.command(pass_context = True)
async def stat(ctx):
    print(bot.get_all_members().count())
    for member in bot.get_all_members():
        if member.status != discord.Status.offline:
            print(member.name, member.status)

if __name__ == "__main__":
    bot.run("NzU2NTE2MDUyNTE0MzczNzM0.X2S-eg.5thR1HK5BJ6OPrFLoTasEFLijJk")