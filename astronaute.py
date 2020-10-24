import os
import discord
from discord.ext import commands
import asyncio
intents = discord.Intents.default()
intents.members = True
bot = commands.Bot(command_prefix = '.', intents = intents)
bot.remove_command('help')

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
        await voice.edit(name = f'Membre: {count}')
        print(count)
        await asyncio.sleep(60)


if __name__ == "__main__":
    bot.run("NzU2NTE2MDUyNTE0MzczNzM0.X2S-eg.5thR1HK5BJ6OPrFLoTasEFLijJk")