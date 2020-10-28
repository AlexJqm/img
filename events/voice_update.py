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
        role = discord.utils.get(member.guild.roles, name = player['voice_name'].capitalize())
        print(role.name)

        if after.channel != None:
            if role.name != after.channel.name:
                await member.remove_roles(role)
        else: await member.remove_roles(role)
def setup(bot):
    bot.add_cog(Utils(bot))