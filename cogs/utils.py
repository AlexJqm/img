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

class Utils(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context = True, aliases=['reg'])
    async def register(self, ctx):
        await ctx.channel.purge(limit = 1)
        role = [role.name for role in ctx.message.author.roles if role.name == "Admin" or role.name == "Modérateur" or role.name == "Modérateur+"]
        if 'Admin' in role or 'Modérateur' in role:
            embed = discord.Embed(title = "Bienvenue", description = "Merci de vouloir rejoindre notre communauté. Afin de que tout le monde puisse jouer dans des bonnes conditions, je vous invite à lire les règles du serveur avant de vous enregistrer ici: <#757321244000649387>", color = 0xf7f7f7)
            embed.add_field(name = "\u200B", value = "Une fois enregistrer, lisez attentivement les explications dans chaque channel, afin de comprendre le fonctionnement du serveur. Si vous rencontrez des problèmes, vous pouvez contacter l'équipe de <@&757263307987222569> <@&759375942887538720> dans le salon <#758303712660815893>.", inline = False)
            embed.set_author(name = "Among Us France", icon_url= self.bot.user.avatar_url)
            embed.set_thumbnail(url = self.bot.user.avatar_url)
            embed.add_field(name = "\u200B", value = "👇 Enregistre toi ici!", inline = False)
            msg = await ctx.channel.send(embed = embed)
            
            while True:
                reactmoji = ['🆕']
                for react in reactmoji: await msg.add_reaction(react)
                
                def check_react(reaction, user):
                    if reaction.message.id != msg.id: return False
                    if user.id == int(os.getenv("BOT_ID")): return False
                    if str(reaction.emoji) not in reactmoji: return False
                    return True
                
                res, user = await self.bot.wait_for('reaction_add', check = check_react)
                
                if '🆕' in str(res.emoji):
                    await msg.remove_reaction(res.emoji, user)
                    await user.add_roles(discord.utils.get(ctx.message.author.guild.roles, name = "Membre"))
                
                if str(res.emoji) not in reactmoji: await msg.remove_reaction(res.emoji, user)

    @commands.command(pass_context = True)
    async def stats(self, ctx):
        await ctx.channel.purge(limit = 1)
        role = [role.name for role in ctx.message.author.roles if role.name == "Admin" or role.name == "Modérateur" or role.name == "Modérateur+"]
        if 'Admin' in role or 'Modérateur' in role:
            def reload(total_server, total_player, online_player):
                for i in server_dict.keys():
                    try:
                        channel = discord.utils.get(ctx.guild.channels, name = i)
                        if channel.name is not None:
                            total_server += 1
                            total_player += len(channel.members)
                    except: pass
                    pass
                online_player = sum(member.status != discord.Status.offline and not member.bot for member in ctx.message.guild.members)
                return(total_server, total_player, online_player)
            
            total_server, total_player, online_player = 0,0,0
            total_server, total_player, online_player = reload(total_server, total_player, online_player)
            
            embed = discord.Embed(title = "Statistiques", description = "Pour afficher les statistiques en temps réel,\nveuillez rafraichir avec l'émoji = 🔄", color = 0xf7f7f7)
            embed.add_field(name = "\u200B", value = "Joueurs en jeu:\nNombre de serveurs:\nJoueurs en ligne:", inline = True)
            embed.add_field(name = "\u200B", value = "\u200B", inline = True)
            embed.add_field(name = "\u200B", value = f"{total_player}\n{total_server}\n{online_player}", inline = True)
            embed.add_field(name = "\u200B", value = "👇 Rafraichis ici!", inline = False)
            embed.set_author(name = "Among Us France", icon_url= self.bot.user.avatar_url)
            embed.set_thumbnail(url = self.bot.user.avatar_url)
            msg = await ctx.send(embed = embed)
            
            while True:
                reactmoji = ['🔄']
                for react in reactmoji:
                    await msg.add_reaction(react)
                def check_react(reaction, user):
                    if reaction.message.id != msg.id: return False
                    if user.id == int(os.getenv("BOT_ID")): return False
                    if str(reaction.emoji) not in reactmoji: return False
                    return True
                res, user = await self.bot.wait_for('reaction_add', check = check_react)
                if '🔄' in str(res.emoji):
                    embed.clear_fields()
                    total_server, total_player, online_player = 0,0,0
                    total_server, total_player, online_player = reload(total_server, total_player, online_player)
                    embed.add_field(name = "\u200B", value = "Joueurs en jeu:\nNombre de serveurs:\nJoueurs en ligne:", inline = True)
                    embed.add_field(name = "\u200B", value = "\u200B", inline = True)
                    embed.add_field(name = "\u200B", value = f"{total_player}\n{total_server}\n{online_player}", inline = True)
                    embed.add_field(name = "\u200B", value = "👇 Rafraichis ici!", inline = False)
                    await msg.remove_reaction(res.emoji, user)
                    await msg.edit(embed = embed)
                if str(res.emoji) not in reactmoji: await msg.remove_reaction(res.emoji, user)

    @commands.command(pass_context = True)
    async def clear(self, ctx):
        role = [role.name for role in ctx.message.author.roles if role.name == "Admin" or role.name == "Modérateur" or role.name == "Modérateur+"]
        if 'Admin' in role or 'Modérateur' in role:
            await ctx.channel.purge()

def setup(bot):
    bot.add_cog(Utils(bot))