import discord
import pymongo
import os
from discord.ext import commands
from os.path import join, dirname
from dotenv import load_dotenv
from database.connect import db_connect

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

servers = db_connect()
server_dict = {'Alfa':'🇦','Bravo':'🇧','Charlie':'🇨','Delta':'🇩','Echo':'🇪','Foxtrot':'🇫','Golf':'🇬','Hotel':'🇭','India':'🇮','Juliett':'🇯','Kilo':'🇰','Lima':'🇱','Mike':'🇲','November':'🇳','Oscar':'🇴','Papa':'🇵','Quebec':'🇶','Romeo':'🇷','Sierra':'🇸','Tango':'🇹','Uniform':'🇺','Victor':'🇻','Whiskey':'🇼','X-ray':'🇽','Yankee':'🇾','Zulu':'🇿'}

class Host(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context = True, aliases=['k'])
    async def kick(self, ctx, member: discord.Member = None):
        await ctx.channel.purge(limit = 1)
        logs = discord.utils.get(ctx.message.author.guild.channels, name = "⛔astronaute-logs")
        role = [role.name for role in ctx.message.author.roles if role.name == "Hote"]
        
        if 'Hote' in role:
            if member is not None:
                if [role.name for role in member.roles if role.name == "Admin" or role.name == "Security"] == []:
                    find_role = [role.name for role in ctx.message.author.roles if role.name in server_dict.keys()]
                    role = discord.utils.get(member.guild.roles, name = find_role[0])  
                    voice = discord.utils.get(member.guild.channels, name = role.name)

                    if member in voice.members:
                        await member.edit(voice_channel = None)
                        await ctx.send(embed = discord.Embed(title = f"ℹ️ Serveur {voice.name}", description = f"L'hôte {ctx.message.author.mention} a kické {member.mention} du serveur.", color = 0x26f752))
                        await logs.send(f"ℹ️ L'hôte {ctx.message.author.mention} a kické {member.mention} du serveur {voice.name}.")
                    else: await ctx.send(embed = discord.Embed(title = "💥 Une erreur s'est produite...", description = "Le joueur n'est pas dans le serveur.", color = 0xF73F26))
                else: await ctx.send(embed = discord.Embed(title = "💥 Une erreur s'est produite...", description = "Vous ne pouvez pas kick un modérateur.", color = 0xF73F26))
            else: await ctx.send(embed = discord.Embed(title = "💥 Une erreur s'est produite...", description = "Vous devez choisir un joueur: `!kick @pseudo`", color = 0xF73F26))
        else: await ctx.send(embed = discord.Embed(title = "💥 Une erreur s'est produite...", description = "Vous n'êtes pas l'hôte du serveur.", color = 0xF73F26))

    @commands.command(pass_context = True, aliases=['b'])
    async def ban(self, ctx, member: discord.Member = None):
        await ctx.channel.purge(limit = 1)
        logs = discord.utils.get(ctx.message.author.guild.channels, name = "⛔astronaute-logs")
        role = [role.name for role in ctx.message.author.roles if role.name == "Hote"]
    
        if 'Hote' in role:
            if member is not None:
                check = [role.name for role in member.roles if role.name == "Admin" or role.name == "Security"]
                if check == []:
                    find_role = [role.name for role in ctx.message.author.roles if role.name in server_dict.keys()]
                    role = discord.utils.get(member.guild.roles, name = find_role[0])  
                    voice = discord.utils.get(member.guild.channels, name = role.name)

                    if member in voice.members:
                        await member.edit(voice_channel = None)
                        servers.update_one({'voice_name': voice.name}, {'$push': {'banned': member.id}})
                        await ctx.send(embed = discord.Embed(title = f"ℹ️ Serveur {voice.name}", description = f"L'hôte {ctx.message.author.mention} a banni {member.mention} du serveur.", color = 0x26f752))
                        await logs.send(f"ℹ️ L'hôte {ctx.message.author.mention} a banni {member.mention} du serveur {voice.name}.")
                    else: await ctx.send(embed = discord.Embed(title = "💥 Une erreur s'est produite...", description = "Le joueur n'est pas dans le serveur.", color = 0xF73F26))
                else: await ctx.send(embed = discord.Embed(title = "💥 Une erreur s'est produite...", description = "Vous ne pouvez pas bannir un modérateur.", color = 0xF73F26))
            else: await ctx.send(embed = discord.Embed(title = "💥 Une erreur s'est produite...", description = "Vous devez choisir un joueur: `!ban @pseudo`", color = 0xF73F26))
        else: await ctx.send(embed = discord.Embed(title = "💥 Une erreur s'est produite...", description = "Vous n'êtes pas l'hôte du serveur.", color = 0xF73F26))

    @commands.command(pass_context = True, aliases=['pv'])
    async def private(self, ctx):
        await ctx.channel.purge(limit = 1)
        logs = discord.utils.get(ctx.message.author.guild.channels, name = "⛔astronaute-logs")
        role = [role.name for role in ctx.message.author.roles if role.name == "Hote"]
    
        if 'Hote' in role:
            find_role = [role.name for role in ctx.message.author.roles if role.name in server_dict.keys()]
            role = discord.utils.get(ctx.message.author.guild.roles, name = find_role[0])  
            voice = discord.utils.get(ctx.message.author.guild.channels, name = role.name)
            data = servers.find({'voice_name': voice.name})
            server = {}
            for i in data: server = i
            if server['private'] == False:
                servers.update_one({'voice_name': voice.name}, {"$set": {'private': True}})
                role_membre = discord.utils.get(ctx.message.author.guild.roles, name = "Crewmate")
                await voice.set_permissions(role_membre, connect = True, view_channel = False)
                await ctx.send(embed = discord.Embed(title = f"ℹ️ Serveur {voice.name}", description = f"L'hôte {ctx.message.author.mention} a passé le serveur en privé.", color = 0x26f752))
                await logs.send(f"🟢 L'hôte {ctx.message.author.mention} a rendu le serveur {voice.name} privé.")
            else: await ctx.send(embed = discord.Embed(title = "💥 Une erreur s'est produite...", description = "Votre serveur est déjà privé.", color = 0xF73F26))
        else: await ctx.send(embed = discord.Embed(title = "💥 Une erreur s'est produite...", description = "Vous n'êtes pas l'hôte du serveur.", color = 0xF73F26))

    @commands.command(pass_context = True, aliases=['pu'])
    async def public(self, ctx, member: discord.Member = None):
        await ctx.channel.purge(limit = 1)
        logs = discord.utils.get(ctx.message.author.guild.channels, name = "⛔astronaute-logs")
        role = [role.name for role in ctx.message.author.roles if role.name == "Hote"]
    
        if 'Hote' in role:
            find_role = [role.name for role in ctx.message.author.roles if role.name in server_dict.keys()]
            role = discord.utils.get(ctx.message.author.guild.roles, name = find_role[0])  
            voice = discord.utils.get(ctx.message.author.guild.channels, name = role.name)
            data = servers.find({'voice_name': voice.name})
            server = {}
            for i in data: server = i
            if server['private'] == True:
                servers.update_one({'voice_name': voice.name}, {"$set": {'private': False}})
                role_membre = discord.utils.get(ctx.message.author.guild.roles, name = "Crewmate")
                await voice.set_permissions(role_membre, connect = True, view_channel = True)
                await ctx.send(embed = discord.Embed(title = f"ℹ️ Serveur {voice.name}", description = f"L'hôte {ctx.message.author.mention} a passé le serveur en publique.", color = 0x26f752))
                await logs.send(f"🟢 L'hôte {ctx.message.author.mention} a rendu le serveur {voice.name} publique.")
            else: await ctx.send(embed = discord.Embed(title = "💥 Une erreur s'est produite...", description = "Votre serveur est déjà publique.", color = 0xF73F26))
        else: await ctx.send(embed = discord.Embed(title = "💥 Une erreur s'est produite...", description = "Vous n'êtes pas l'hôte du serveur.", color = 0xF73F26))

    @commands.command(pass_context = True, aliases=['sc'])
    async def setcode(self, ctx, arg = None):
        await ctx.channel.purge(limit = 1)
        role = [role.name for role in ctx.message.author.roles if role.name == "Hote"]
        if 'Hote' in role:
            if arg is not None:
                find_role = [role.name for role in ctx.message.author.roles if role.name in server_dict.keys()]
                role = discord.utils.get(ctx.message.author.guild.roles, name = find_role[0])  
                voice = discord.utils.get(ctx.message.author.guild.channels, name = role.name)
                servers.update_one({'voice_name': voice.name}, {"$set": {'code': arg.upper()}})
            else: await ctx.send(embed = discord.Embed(title = "💥 Une erreur s'est produite...", description = "Vous devez saisir le code: `!setcode BBHF`", color = 0xF73F26))
        else: await ctx.send(embed = discord.Embed(title = "💥 Une erreur s'est produite...", description = "Vous n'êtes pas l'hôte du serveur.", color = 0xF73F26))
    
    @commands.command(pass_context = True, aliases=['sr'])
    async def setregion(self, ctx, arg = None):
        await ctx.channel.purge(limit = 1)
        role = [role.name for role in ctx.message.author.roles if role.name == "Hote"]
        if 'Hote' in role:
            if arg is not None:
                find_role = [role.name for role in ctx.message.author.roles if role.name in server_dict.keys()]
                role = discord.utils.get(ctx.message.author.guild.roles, name = find_role[0])  
                voice = discord.utils.get(ctx.message.author.guild.channels, name = role.name)
                servers.update_one({'voice_name': voice.name}, {"$set": {'region': arg.upper()}})
            else: await ctx.send(embed = discord.Embed(title = "💥 Une erreur s'est produite...", description = "Vous devez saisir la region: `!setregion EU`", color = 0xF73F26))
        else: await ctx.send(embed = discord.Embed(title = "💥 Une erreur s'est produite...", description = "Vous n'êtes pas l'hôte du serveur.", color = 0xF73F26))
    
    @commands.command(pass_context = True, aliases=['s'])
    async def sound(self, ctx):
        await ctx.channel.purge(limit = 1)
        role = [role.name for role in ctx.message.author.roles if role.name == "Hote"]
        
        if 'Hote' in role:
            msg = await ctx.channel.send(embed = discord.Embed(title = "Controleur de son", description = "🔊 Unmute \n🔇 Mute\n🗑️ Fermer le controleur de son", color = 0xf7f7f7))
            while True:
                find_role = [role.name for role in ctx.message.author.roles if role.name in server_dict.keys()]
                role = discord.utils.get(ctx.message.author.guild.roles, name = find_role[0])  
                voice = discord.utils.get(ctx.message.author.guild.channels, name = role.name)
                reactmoji = ['🔊', '🔇', '🗑️']
                for react in reactmoji:
                    await msg.add_reaction(react)
                def check_react(reaction, user):
                    if reaction.message.id != msg.id: return False
                    if user.id == int(os.getenv("BOT_ID")): return False
                    if str(reaction.emoji) not in reactmoji: return False
                    return True
                res, user = await self.bot.wait_for('reaction_add', check = check_react)
                if user != ctx.message.author:
                    await msg.remove_reaction(res.emoji, user)
                    pass
                elif '🔊' in str(res.emoji):
                    await msg.remove_reaction(res.emoji, user)
                    for member in voice.members:
                        await member.edit(mute = False)
                elif '🔇' in str(res.emoji):
                    await msg.remove_reaction(res.emoji, user)
                    for member in voice.members:
                        await member.edit(mute = True)
                elif '🗑️' in str(res.emoji):
                    await msg.delete()
                    break
                else: await msg.clear_reactions()
        else: await ctx.send(embed = discord.Embed(title = "💥 Une erreur s'est produite...", description = "Vous n'êtes pas l'hôte du serveur.", color = 0xF73F26))


def setup(bot):
    bot.add_cog(Host(bot))