import discord
import pymongo
import os
from discord.ext import commands
from os.path import join, dirname
from dotenv import load_dotenv
from database.connect import db_connect
from PIL import Image, ImageDraw, ImageFilter, ImageFont
import requests

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
        role = [role.name for role in ctx.message.author.roles if role.name == "Admin" or role.name == "Security"]
        if 'Admin' in role or 'Security' in role:
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
        role = [role.name for role in ctx.message.author.roles if role.name == "Admin" or role.name == "Security"]
        if 'Admin' in role or 'Security' in role:
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
        role = [role.name for role in ctx.message.author.roles if role.name == "Admin" or role.name == "Security"]
        if 'Admin' in role or 'Security' in role:
            await ctx.channel.purge()

    @commands.command(pass_context = True)
    async def rules(self, ctx, msgID: int):
        await ctx.channel.purge(limit = 1)
        msg = await ctx.fetch_message(msgID)
        role = [role.name for role in ctx.message.author.roles if role.name == "Admin" or role.name == "Security"]
        if 'Admin' in role or 'Security' in role:
            embed = discord.Embed(title = "Les règles", description = "Le serveur Discord de Among Us Francophone est un lieu de vie commune où vous rencontrerez des joueurs / joueuses de tout âge et de tout horizon. Il est donc impératif de bien lire ce règlement pour éviter tout débordement. Nous sommes particulièrement attentifs et vigilants aux contenus proposés par les joueurs dans les channels textuels et émis dans les channels vocaux. Nous vous recommandons donc de faire attention a vos propos.", color = 0xf7f7f7)
            embed.add_field(name = "**0.** Nous suivons les termes d'utilisation de Discord", value = "• Charte d’Utilisation de la Communauté:\nhttps://discordapp.com/guidelines\n• Conditions d'Utilisation:\nhttps://discordapp.com/terms", inline = False)
            embed.add_field(name = "\u200B", value = "**1.** Soyez tout simplement respectueux et gentil les uns envers les autres, c'est un jeu. Restez polis et courtois. Les formules de politesse telles que 'Bonjour/Au revoir/Merci/S'il te plait' n'ont jamais tué personne.", inline = False)
            embed.add_field(name = "\u200B", value = "**2.** Il est strictement interdit de grief (troll/anti-jeu), par exemple si vous mourrez, vous ne parlez pas.", inline = False)
            embed.add_field(name = "\u200B", value = "**3.** Utilisez un pseudo correct , non insultant ou provocant. Vous pouvez signaler tout pseudo qui vous paraît ne pas être conforme au règlement. La modération se réserve le droit de supprimer votre pseudo. Même règlement pour les avatars.", inline = False)
            embed.add_field(name = "\u200B", value = "**4.** Le spam sur le discord est bien évidemment interdit ainsi que toute sorte de harcèlement ou de jugement raciste et/ou faisant la promotion d'une quelconque sorte de haine.", inline = False)
            embed.add_field(name = "\u200B", value = "**5.** Aucun contenu NSFW n'est autorisé (Not Safe For Work) autrement dit pornographique ou choquant.", inline = False)
            embed.add_field(name = "\u200B", value = "**6.** Quand vous êtes en vocal vous **DEVEZ**:\n**6.1** - Être mute jusqu'à tant qu'un 'meeting' commence.\n**6.2** - Mute dès que le vote est terminé. Pas après.\n**6.3** - Ne plus parler dès que vous êtes mort.\n**6.4** - Ne restez pas AFK.\n**6.5** - Avoir un micro acceptable.\n**6.6** - Ces règles sont générales, vous pouvez créer vos propres règles si tout le monde est d'accord avec avant le début de la partie. Nous vous connectons, mais ne créons pas de règles.", inline = False)
            embed.add_field(name = "\u200B", value = "**7.** Veillez à utiliser les channels approprié a vos demandes.", inline = False)
            embed.add_field(name = "\u200B", value = "**8.** Toute insulte ou divulgation d'informations personnelles est strictement interdite.", inline = False)
            embed.add_field(name = "\u200B", value = "**9.** Merci de ne pas explicitivement montrer publiquement vos opinions politiques, religieuses ou tout autre pouvant créer un débat stérile.", inline = False)
            embed.add_field(name = "\u200B", value = "**10.** En cas de problèmes, spams MP/DM, insultes, menaces, caractères raciste et 'j'en-passe', contactez l'un des modérateurs disponible avec le channel #report sans oubliez de mentionner le joueur et le channel qui nécessite une intervention et écrivez un signalement avec si possible des preuves.", inline = False)
            embed.add_field(name = "\u200B", value = "Si vous êtes pas content d’une sanction ou warn , nous sommes aptes à discutez avec vous. Dans le respect et faire une étude de cas.", inline = False)
            embed.add_field(name = "\u200B", value = "Sachez que le staff communique via un channel privé et invisible. Chaque problème sera donc automatiquement connu par tout les membres. Inutile de spam un staff.", inline = False)
            embed.add_field(name = "\u200B", value = "**11.** Toute sorte de pub ou promotion est interdite sans l'accord de la modération.", inline = False)
            embed.add_field(name = "\u200B", value = "👇 Appuie ici si tu les as lu. Merci!", inline = False)
            embed.set_thumbnail(url = self.bot.user.avatar_url)
            embed.set_author(name = "Among Us France", icon_url= self.bot.user.avatar_url)
            await msg.edit(embed = embed)
            
    @commands.command(pass_context = True)
    async def move(self, ctx, member: discord.Member = None, channel_id = None):
        await ctx.channel.purge(limit = 1)
        role = [role.name for role in ctx.message.author.roles if role.name == "Admin" or role.name == "Security"]
        if 'Admin' in role or 'Security' in role:
            channel = ctx.message.author.voice.channel
            voice = discord.utils.get(self.bot.voice_clients, guild = ctx.guild)
            if voice and voice.is_connected(): await voice.move_to(channel)
            else: voice = await channel.connect()
              
    @commands.command(pass_context = True)
    async def setup(self, ctx):
        await ctx.channel.purge(limit = 1)
        cat_server = await ctx.guild.create_category_channel('Serveurs')
        await ctx.guild.create_category_channel('Chat serveur')
        await ctx.guild.create_category_channel('Serveurs disponibles')
        await ctx.guild.create_category_channel('Serveurs complets')
        await ctx.guild.create_voice_channel('Creer un serveur', category = cat_server)
        await ctx.guild.create_voice_channel('Rejoindre un serveur', category = cat_server)
        
    @commands.command(pass_context = True)
    async def movebot(self, ctx):
        await ctx.channel.purge(limit = 1)
        channel = ctx.message.author.voice.channel
        voice = discord.utils.get(self.bot.voice_clients, guild = ctx.guild)
        if voice and voice.is_connected(): await voice.move_to(channel)
        else: voice = await channel.connect()
            
            
    @commands.command(pass_context=True)
    async def test(self, ctx, member: discord.Member = None):
        # Saves the Profile Picture as a file for PIL to edit it.
        with requests.get(member.avatar_url) as r:
            img_data = r.content
        with open('profile.jpg', 'wb') as handler:
            handler.write(img_data)
        im1 = Image.open("background.png")
        im2 = Image.open("profile.jpg")

        # Font Stuff
        draw = ImageDraw.Draw(im1)
        font = ImageFont.truetype("BebasNeue-Regular.ttf", 32)
        # Add the Text to the result image
        guild = bot.get_guild(guild_id)
        draw.text((160, 40),f"Welcome {member.name}",(255,255,255),font=font)
        draw.text((160, 80),f"You are the {guild.member_count}th member",(255,255,255),font=font)

        size = 129

        im2 = im2.resize((size, size), resample=0)
        # Creates the mask for the profile picture
        mask_im = Image.new("L", im2.size, 0)
        draw = ImageDraw.Draw(mask_im)
        draw.ellipse((0, 0, size, size), fill=255)

        mask_im.save('mask_circle.png', quality=95)

        # Masks the profile picture and adds it to the background.
        back_im = im1.copy()
        back_im.paste(im2, (11, 11), mask_im)


        back_im.save('welcomeimage.png', quality=95)
        # Stuff to send the embed with a local image.
        f = discord.File(path, filename="welcomeimage.png")

        embed = discord.Embed()
        embed.set_image(url="attachment://welcomeimage.png")
        
        await ctx.send(embed = embed)
def setup(bot):
    bot.add_cog(Utils(bot))