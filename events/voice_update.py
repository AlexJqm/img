import discord
from discord.ext import commands, tasks
from database.connect import db_connect
from random import randrange

servers = db_connect('servers')

class Utils(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        pass
def setup(bot):
    bot.add_cog(Utils(bot))