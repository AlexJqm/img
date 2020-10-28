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
        print(player)
        host = False
        if player['host_name'] == member.name: host == True
        role = discord.utils.get(member.guild.roles, name = player['voice_name'].capitalize())
        role_host = discord.utils.get(member.guild.roles, name = 'Hote')
        try: voice = discord.utils.get(member.guild.channels, name = player['voice_name'].capitalize())
        except: voice = None
        print(voice, host, len(voice.members))
        if host and voice is not None and len(voice.members) > 0:
            print("true")
            new_host = voice.members[randrange(len(voice.members))]
            await new_host.add_roles(role_host)
            await member.remove_roles(role_host)
            servers.update_one({'voice_name': voice.name, 'finished': None}, {"$set": {'host_name': new_host.name, 'host_id': new_host.id}})
            await text.send(embed = discord.Embed(title = f":information_source: Serveur {text.name.capitalize()}", description = f"Le joueur {new_host.mention} à été designer par défaut comme nouvel hôte du serveur {text.name.capitalize()}.", color = 0x26f752))
        if after.channel != None:
            if role.name != after.channel.name:
                await member.remove_roles(role)
        else: await member.remove_roles(role)

def setup(bot):
    bot.add_cog(Utils(bot))