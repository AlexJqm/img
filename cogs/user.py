import discord
import pymongo
import os
from discord.ext import commands
from os.path import join, dirname
from dotenv import load_dotenv
from database.connect import db_connect

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

servers = db_connect("servers")

def find_server():
    data = servers.find({})
    name_list = []
    for i in data:
        name_list.append(i['voice_name'])
    return name_list

class User(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def ping(self, ctx):
        await ctx.send(f"Pong! I am {str(self.bot.latency*1000)[:4]}ms latent to discord servers")

    @commands.command(pass_context = True, aliases=['wi'])
    async def whereis(self, ctx, member: discord.Member = None):
        await ctx.channel.purge(limit = 1)
        if member is not None:
            try:
                data = servers.find({"current_players":{"$in":[member.name]}})
                player = {}
                for i in data: player = i
                
                voice = discord.utils.get(member.guild.channels, name = player['voice_name'].capitalize())
                
                if len(voice.members) < 10:
                    link = await voice.create_invite()
                    await ctx.send(embed = discord.Embed(title = f"👀 Where is...", description = f"Le joueur {member.name} se trouve dans le serveur {player['voice_name']}.\n[Rejoindre {member.name}]({link})", color = 0x26f752))
                
                else: await ctx.send(embed = discord.Embed(title = f"👀 Where is...", description = f"Le joueur {member.name} se trouve dans le serveur {player['voice_name']}.\nVous ne pouvez pas le rejoindre.", color = 0xF73F26))
            
            except: await ctx.send(embed = discord.Embed(title = "💥 Une erreur s'est produite...", description = f"Le joueur {member.name} n'est dans aucun serveur.", color = 0xF73F26))
        
        else: await ctx.send(embed = discord.Embed(title = "💥 Une erreur s'est produite...", description = "Vous devez choisir un joueur: `.whereis @pseudo`", color = 0xF73F26))


    @commands.command(pass_context = True, aliases=['i'])
    async def info(self, ctx, serv = None):
        await ctx.channel.purge(limit = 1)
        name_list = find_server()
        try:
            if serv is None and ctx.message.author.voice.channel.name in name_list:
                find_role = [role.name for role in ctx.message.author.roles if role.name in name_list]
                role = discord.utils.get(ctx.message.author.guild.roles, name = find_role[0])  
                voice = discord.utils.get(ctx.message.author.guild.channels, name = role.name)
                data = servers.find({"voice_name": voice.name, "finished": None})
                server = {}
                for i in data: server = i
                find_role = [role.name for role in ctx.message.author.roles if role.name in name_list]
                if server['voice_name'] == find_role[0] and serv is None:
                    voice = discord.utils.get(ctx.message.author.guild.channels, name = server['voice_name'])
                    players = [member.name for member in voice.members]
                    players = '\n- '.join(players)
                    link = await voice.create_invite()
                await ctx.send(embed = discord.Embed(title = f"ℹ️ Serveur {server['voice_name']}", description = f"Il reste {10 - len(voice.members)} places disponibles sur ce serveur.\n- {players}\n\nCode du serveur: {server['code']}\nRegion du serveur: {server['region']}", color = 0x26f752))
            elif serv is not None:
                if serv.capitalize() in name_list:
                    try:
                        data = servers.find({"voice_name": serv.capitalize(), "finished": None})
                        server = {}
                        for i in data: server = i
                        voice = discord.utils.get(ctx.message.author.guild.channels, name = server['voice_name'])
                        players = [member.name for member in voice.members]
                        players = '\n- '.join(players)
                        if server['private'] == False:
                            if len(voice.members) < 10:
                                link = await voice.create_invite()
                                await ctx.send(embed = discord.Embed(title = f"ℹ️ Serveur {server['voice_name']}", description = f"Il reste {10 - len(voice.members)} places disponibles sur ce serveur.\n- {players}\n[Rejoindre le serveur {server['voice_name']}]({link})", color = 0x26f752))

                            else: await ctx.send(embed = discord.Embed(title = f"ℹ️ Serveur {server['voice_name']}", description = f"Aucune place disponible sur ce serveur.\n- {players}\n", color = 0xF73F26))
                        else:  await ctx.send(embed = discord.Embed(title = f"ℹ️ Serveur {server['voice_name']}", description = f"Il reste {10 - len(voice.members)} places disponibles sur ce serveur.\n- {players}\nCe serveur est privé.", color = 0x26f752))

                    except: await ctx.send(embed = discord.Embed(title = "💥 Une erreur s'est produite...", description = "Ce serveur n'existe pas actuellement.", color = 0xF73F26)) 

                else: await ctx.send(embed = discord.Embed(title = "💥 Une erreur s'est produite...", description = "Serveur introuvable.", color = 0xF73F26))
            else: await ctx.send(embed = discord.Embed(title = "💥 Une erreur s'est produite...", description = "Vous devez choisir un serveur: `.info serveur`", color = 0xF73F26))
        except: pass
        try:
            if ctx.message.author.voice is None:
                if serv is not None:
                    if serv.capitalize() in name_list:
                        try:
                            data = servers.find({"voice_name": serv.capitalize(), "finished": None})
                            server = {}
                            for i in data: server = i
                            voice = discord.utils.get(ctx.message.author.guild.channels, name = server['voice_name'])
                            players = [member.name for member in voice.members]
                            players = '\n- '.join(players)
                            if server['private'] == False:
                                if len(voice.members) < 10:
                                    link = await voice.create_invite()
                                    await ctx.send(embed = discord.Embed(title = f"ℹ️ Serveur {server['voice_name']}", description = f"Il reste {10 - len(voice.members)} places disponibles sur ce serveur.\n- {players}\n[Rejoindre le serveur {server['voice_name']}]({link})", color = 0x26f752))
                                
                                else: await ctx.send(embed = discord.Embed(title = f"ℹ️ Serveur {server['voice_name']}", description = f"Aucune place disponible sur ce serveur.\n- {players}\n", color = 0xF73F26))
                            else:  await ctx.send(embed = discord.Embed(title = f"ℹ️ Serveur {server['voice_name']}", description = f"Il reste {10 - len(voice.members)} places disponibles sur ce serveur.\n- {players}\nCe serveur est privé.", color = 0x26f752))

                        except: await ctx.send(embed = discord.Embed(title = "💥 Une erreur s'est produite...", description = "Ce serveur n'existe pas actuellement.", color = 0xF73F26)) 
                    
                    else: await ctx.send(embed = discord.Embed(title = "💥 Une erreur s'est produite...", description = "Serveur introuvable.", color = 0xF73F26))
                else: await ctx.send(embed = discord.Embed(title = "💥 Une erreur s'est produite...", description = "Vous devez choisir un serveur: `.info serveur`", color = 0xF73F26))
        except: pass

    @commands.command(pass_context = True)
    async def host(self, ctx):
        await ctx.channel.purge(limit = 1)
        name_list = find_server()
        find_role = [role.name for role in ctx.message.author.roles if role.name in name_list]
        if find_role[0] is not None:
            role = discord.utils.get(ctx.message.author.guild.roles, name = find_role[0])  
            voice = discord.utils.get(ctx.message.author.guild.channels, name = role.name)
            data = servers.find({'voice_name': voice.name, 'finished': None})
            server = {}
            for i in data: server = i
            if server['host_name'] is not None:
                await ctx.send(embed = discord.Embed(title = f"ℹ️ Serveur {voice.name}", description = f"L'hôte du serveur est {server['host_name']}", color = 0x26f752))
        else: await ctx.send(embed = discord.Embed(title = "💥 Une erreur s'est produite...", description = "Vous n'êtes dans aucun serveur.", color = 0xF73F26))


    @commands.command(pass_context = True, aliases=['inv'])
    async def invite(self, ctx, member: discord.Member = None):
        await ctx.channel.purge(limit = 1)
        name_list = find_server()
        find_role = [role.name for role in ctx.message.author.roles if role.name in name_list]
        role = discord.utils.get(member.guild.roles, name = find_role[0])  
        voice = discord.utils.get(member.guild.channels, name = role.name)
        data = servers.find({"voice_name": voice.name, "finished": None})
        server = {}
        for i in data: server = i
        if server['private'] == False:
            if member is not None:
                try:
                    role = [role.name for role in ctx.message.author.roles if role.name in name_list]
                    voice = discord.utils.get(member.guild.channels, name = role[0].capitalize())
                    link = await voice.create_invite()
                    await member.send(embed = discord.Embed(title = "✉️ Invitation", description = f"Le joueur {ctx.message.author.mention} vous invite à rejoindre une partie sur Among Us Francophone.\n[Clique ici pour rejoindre le serveur {voice.name}]({link})", color = 0xF73F26))
                    await ctx.send(embed = discord.Embed(title = f"ℹ️ Serveur {voice.name}", description = f"Le joueur {ctx.message.author.mention} a invité {member.mention} à rejoindre le serveur.", color = 0x26f752))
                except:
                    await ctx.send(embed = discord.Embed(title = "💥 Une erreur s'est produite...", description = f"Vous devez être dans un serveur pour inviter une personne.", color = 0xF73F26))
            else: await ctx.send(embed = discord.Embed(title = "💥 Une erreur s'est produite...", description = "Vous devez choisir un joueur: `.invite @pseudo`", color = 0xF73F26))
        else: await ctx.send(embed = discord.Embed(title = "💥 Une erreur s'est produite...", description = "Vous ne pouvez pas inviter un joueur dans un serveur privé.", color = 0xF73F26))
    
    @commands.command(pass_context = True, aliases=['vh'])
    async def votehost(self, ctx, member: discord.Member = None):
        await ctx.channel.purge(limit = 1)
        name_list = find_server()
        if member is not None:
            find_role = [role.name for role in ctx.message.author.roles if role.name in name_list]
            role = discord.utils.get(member.guild.roles, name = find_role[0])  
            voice = discord.utils.get(member.guild.channels, name = role.name)
            
            new_host = member
            old_host = None
            
            data = servers.find({'voice_name': voice.name, 'finished': None})
            server = {}
            for i in data: server = i
            for member in voice.members:
                if member.id == server['host_id']: old_host = member
                else: pass
            find_role = [role.name for role in new_host.roles if role.name == "Hote"]
            
            if "Hote" not in find_role:
                
                def check_react(reaction, user):
                    if reaction.message.id != msg.id: return False
                    if user.id == int(os.getenv("BOT_ID")): return False
                    if str(reaction.emoji) not in reactmoji: return False
                    return True
                
                user_list = [new_host.name]
                
                accept, contest = 0, 0
                req_accept = int(len(voice.members)/2)
                req_contest = int(len(voice.members)/3)
                if req_accept == 0: req_accept += 1
                if req_contest == 0: req_contest += 1
                
                embed = discord.Embed(title = "💬 Vote nouvel hôte", description = f"{role.mention}\nLe joueur {ctx.message.author.mention} a lancé un vote pour que {new_host.mention} devienne le nouvel hôte.\n0/{req_accept} votes nécessaires pour valider et 0/{req_contest} pour annuler.", color = 0xf7f7f7)
                msg = await ctx.send(embed = embed)
                
                while True:
                    reactmoji = ['🟢', '❌']
                    for react in reactmoji: await msg.add_reaction(react)
                    res, user = await self.bot.wait_for('reaction_add', check = check_react)
                    
                    if '🟢' in res.emoji:
                        if user.name not in user_list:
                            accept += 1
                            user_list.append(user.name)
                        voted = '\n'.join(user_list)
                        embed = discord.Embed(title = "💬 Vote nouvel hôte", description = f"{role.mention}\nLe joueur {ctx.message.author.mention} a lancé un vote pour que {new_host.mention} devienne le nouvel hôte.\n{accept}/{req_accept} votes nécessaires pour valider et {contest}/{req_contest} pour annuler.", color = 0xf7f7f7)
                        embed.add_field(name = "\u200B", value = f"Listes des votants:\n{voted}", inline = False)
                        await msg.edit(embed = embed)
                    
                    elif '❌' in res.emoji:
                        if user.name not in user_list:
                            contest += 1
                            user_list.append(user.name)
                        voted = '\n'.join(user_list)
                        embed = discord.Embed(title = "💬 Vote nouvel hôte", description = f"{role.mention}\nLe joueur {ctx.message.author.mention} a lancé un vote pour que {new_host.mention} devienne le nouvel hôte.\n{accept}/{req_accept} votes nécessaires pour valider et {contest}/{req_contest} pour annuler.", color = 0xf7f7f7)
                        embed.add_field(name = "\u200B", value = f"Listes des votants:\n{voted}", inline = False)
                        await msg.edit(embed = embed)
                    
                    if accept == req_accept:
                        role_host = discord.utils.get(member.guild.roles, name = "Hote")
                        servers.update_one({'voice_name': voice.name, 'finished': None}, {"$set": {'host_name': new_host.name, 'host_id': new_host.id}})
                        await old_host.remove_roles(role_host)
                        await new_host.add_roles(role_host)
                        await msg.clear_reactions()
                        embed = discord.Embed(title = "💬 Vote nouvel hôte terminé", description = f"{role.mention}\nLe joueur {new_host.mention} devient le nouvel hôte.", color = 0x26f752)
                        await msg.edit(embed = embed)
                        break
                    
                    if contest == req_contest:
                        await msg.clear_reactions()
                        embed = discord.Embed(title = "💬 Vote nouvel hôte terminé", description = f"{role.mention}\nLe joueur {new_host.mention} ne deviendras pas le nouvel hôte.", color = 0xF73F26)
                        await msg.edit(embed = embed)
                        break
            
            else: await ctx.send(embed = discord.Embed(title = "💥 Une erreur s'est produite...", description = f"{old_host.name} est déjà l'hôte du serveur.", color = 0xF73F26))
        else: await ctx.send(embed = discord.Embed(title = "💥 Une erreur s'est produite...", description = "Vous devez choisir un joueur: `.votehost @pseudo`", color = 0xF73F26))

    @commands.command(pass_context = True, aliases=['h'])
    async def help(self, ctx, arg = None):
        await ctx.channel.purge(limit = 1)
        if arg == 'user':
            embed = discord.Embed(title = "Les commandes utilisateurs", description = "**.info** *(alias: .i)*\nAffiche les informations à propos d'un serveur.\nExemple: `.info alfa`\nSi vous vous trouvez déjà dans un serveur, utiliser simplement `.info` pour afficher les informations de votre serveur.", color = 0x26f752)
            embed.add_field(name = "\u200B", value = "**.whereis** *(alias: .wi)*\nRenvois la position du joueur s'il est dans un serveur.\nExemple: `.whereis @pseudo`", inline = False)
            embed.add_field(name = "\u200B", value = "**.invite** *(alias: .inv)*\nEnvois une invitation en message privé à un joueur.\nExemple: `.invite @pseudo`", inline = False)
            embed.add_field(name = "\u200B", value = "**.host**\nAffiche le nom de l'hôte du serveur dans lequel vous vous trouvez.\nExemple: `.host`", inline = False)
            embed.add_field(name = "\u200B", value = "**.votehost** *(alias: .vh)*\nLance un vote pour élire un nouvel hôte.\nExemple: `.votehost @pseudo`", inline = False)
            await ctx.send(embed = embed)
        elif arg == 'host':
            embed = discord.Embed(title = "Les commandes hôtes", description = "**.kick** *(alias: .k)*\nExclut un joueur du serveur.\nExemple: `.kick @pseudo`", color = 0x26f752)
            embed.add_field(name = "\u200B", value = "**.ban** *(alias: .b)*\nBannie un joueur du serveur.\nExemple: `.ban @pseudo`", inline = False)
            embed.add_field(name = "\u200B", value = "**.private** *(alias: .pv)*\nRend le serveur invisible et inaccessible à tout le monde.\nExemple: `.private`", inline = False)
            embed.add_field(name = "\u200B", value = "**.public** *(alias: .pu)*\nRend le serveur visible et accessible.\nExemple: `.public`", inline = False)
            embed.add_field(name = "\u200B", value = "**.setcode** *(alias: .sc)*\nInsert le code du serveur dans les informations.\nExemple: `.setcode BBHF`", inline = False)
            embed.add_field(name = "\u200B", value = "**.setregion** *(alias: .sr)*\nInsert la region du serveur dans les informations.\nExemple: `.setregion EU`", inline = False)
            embed.add_field(name = "\u200B", value = "**.sound** *(alias: .s)*\nOuvre le contrôleur de son.\nExemple: `.sound`", inline = False)
            await ctx.send(embed = embed)
        else: await ctx.send(embed = discord.Embed(title = "💥 Une erreur s'est produite...", description = "Vous devez choisir **user** ou **host**: `.help user`", color = 0xF73F26))


def setup(bot):
    bot.add_cog(User(bot))