 import discord
import asyncio
from discord.ext import commands, tasks
import time
import datetime
import pytz

class Utils(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    @commands.command(pass_context = True)
    async def report(self, ctx):
        
        data = servers.find({})
      
def setup(bot):
    bot.add_cog(Utils(bot))