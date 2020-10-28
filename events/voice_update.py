import discord
from discord.ext import commands, tasks
from database.connect import db_connect

servers = db_connect('servers')

class Utils(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        print(member.name)
        try: print("before :", before.channel.name)
        except: pass
        try: print("after :", after.channel.name)
        except: pass
        data = servers.find({"current_players": {"$in": [member.name]}})
        player = {}
        for i in data: player = i
        voice = discord.utils.get(member.guild.channels, name = player['voice_name'].capitalize())
        print(voice.name)

        if voice.name != before.channel.name:
            print('hello')

def setup(bot):
    bot.add_cog(Utils(bot))