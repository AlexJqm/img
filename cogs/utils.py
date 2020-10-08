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
        role = [role.name for role in ctx.message.author.roles if role.name == "Admin" or role.name == "Modérateur"]
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
        online_player = sum(member.status != discord.Status.offline and not member.bot for member in ctx.message.guild.members)
        print(online_player)
        await ctx.channel.purge(limit=1)
        role = [role.name for role in ctx.message.author.roles if role.name == "Admin" or role.name == "Modérateur"]
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
        role = [role.name for role in ctx.message.author.roles if role.name == "Admin" or role.name == "Modérateur"]
        if 'Admin' in role or 'Modérateur' in role:
            await ctx.channel.purge()

    @commands.command(pass_context = True)
    async def tt1(self, ctx):
        role = [role.name for role in ctx.message.author.roles if role.name == "Admin" or role.name == "Modérateur"]
        if 'Admin' in role or 'Modérateur' in role:
            embed = discord.Embed(title = "__Comment ça fonctionne:__", description = "Le classement ELO attribue au joueur, suivant ses performances passées, un nombre de points tel que deux joueurs supposés de même force aient le même nombre de points. Plus le joueur est performant et plus son nombre de points ELO est élevé. Si un joueur réalise une performance supérieure à son niveau estimé, il gagne des points ELO. Réciproquement, il en perd s'il réalise une contre-performance.", color = 0xf7f7f7)
            embed.add_field(name = "__**Leaderboards:**__", value = "Overall - Impostor - Crewmate", inline = False)
            embed.add_field(name = "**Lancer un match classé:**", value = "__Etape 1:__ 10 joueurs rejoignent le salon vocal #ranked.\n__Etape 2:__ Assurez-vous que les paramètres de la partie correspondent à nos règles.\n__Etape 3:__ Ecrivez `!start polus`, `!start skeld`, ou `!start mira` dans le salon textuel dédier à votre serveur vocal.\n> Les joueurs se verront attribuer un numéro, qui sera utilisé pour identifier qui sont les imposteurs lors de la soumission des résultats.", inline = False)
            embed.add_field(name = "**Pour soumettre le résultat d'un match:**", value = "Ecrivez `!impostor # # win` ou `!impostor # # lose`.\n> # est remplacé par les numéros des joueurs qui sont les imposteurs.\n*Par exemple: si le joueur 3 et le joueur 7 sont des imposteurs et qu'ils ont gagné, la commande serait:*\n`!impostor 3 7 w`\nSi les résultats sont inexacts, 1 joueur peut cliquer sur :no_entry: pour laisser le match non validé.\nLes résultats sont soumis dès que 5 joueurs cliquent sur ✅ pour confirmer les résultats.\nUne fois confirmés, les résultats ne peuvent pas être modifiés.", inline = False)
            embed.add_field(name = "**Autres commandes:**", value = "`!stats` -- Affiche l'ensemble de vos stats et de vos ELO.\n`!map` -- Voir les stats par carte.\n`!current` -- Liste des matchs non validé.\n`!cancel` -- Supprime un match non validé.\n`!leaderboard` -- Affiche le classement de la saison en cours.", inline = False)
            embed.add_field(name = "__**Règles:**__", value = "1. Les participants sont responsables de s'assurer que les matchs sont correctement lancés et soumis.\n2. Toute forme de triche sera sévèrement sanctionné et pourra entraîner un bannissement.\n3. Si un membre remarque une tricherie, signalez-le dans le salon #report.\n4. Les spectateurs peuvent être considérés comme des complices et donc comme de la tricherie.", inline = False)
            embed.set_author(name = "Among Us Francophone", icon_url= self.bot.user.avatar_url)
            embed.set_footer(text = "Among Us Francophone - Dernière mise à jour: 08/10/2020")
            msg = await ctx.send(embed = embed)

    @commands.command(pass_context = True)
    async def tt2(self, ctx):
        role = [role.name for role in ctx.message.author.roles if role.name == "Admin" or role.name == "Modérateur"]
        if 'Admin' in role or 'Modérateur' in role:
            embed = discord.Embed(title = "**Among Us Francophone Challenge #1**", description = "> Êtes-vous le <@&763675029723545621>?\n> Êtes-vous le prochain <@&763675011550150716>?\n> Ou êtes-vous le prochain <@&763675102105174026>?\n> Pouvez-vous être parmi les meilleurs de nos classements?\n> Venez vous classer parmi nous!", color = 0xf7f7f7)
            embed.add_field(name = "**Lancement le DATE jusqu'au DATE**", value = "1. Among Us Francophone Challenge #1 est un tournoi sur 4 semaines, du DATE au DATE. \n2. Tous les <@&757888566553477161> peuvent participer.\n3. Les gagnants du tournoi sont jugés par leur ELO et leur rang.\n4. L'ELO est calculé à partir des résultats des matchs soumis à <@763443258889338900>, décrits dans #comment-ça-fonctionne\n5. Les classements sont réinitialisés au début du tournoi.\n6. Les matchs du tournoi doivent se dérouler avec les paramètres de la carte indiqués dans #paramètre-de-match\n7. Une inactivité de plus de 7 jours entraînera la perte d'une partie du MMR.\n8. Tous les prix sont exclusifs les uns des autres, ainsi un participant ne peut pas obtenir plus d'un prix.", inline = False)
            embed.add_field(name = "__**Prix:**__", value = "1er Overall <@&763675029723545621>\n1er Crewmate <@&763675011550150716>\n1er Impostor <@&763675102105174026>", inline = True)
            embed.add_field(name = "\u200B", value = "2ème Overall\n3ème Overall", inline = True)
            embed.set_author(name = "Among Us Francophone", icon_url= self.bot.user.avatar_url)
            embed.set_footer(text = "Among Us Francophone - Dernière mise à jour: 08/10/2020")
            msg = await ctx.send(embed = embed)
            
def setup(bot):
    bot.add_cog(Utils(bot))