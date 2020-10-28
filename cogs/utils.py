import discord
from discord.ext import commands
import subprocess

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
    async def clear(self, ctx):
        await ctx.channel.purge(limit = 1)
        role = [role.name for role in ctx.message.author.roles if role.name == "Admin"]
        if 'Admin' in role:
            await ctx.channel.purge()

    @commands.command(pass_context = True)
    async def rules(self, ctx, msgID: int):
        await ctx.channel.purge(limit = 1)
        msg = await ctx.fetch_message(msgID)
        role = [role.name for role in ctx.message.author.roles if role.name == "Admin"]
        if 'Admin' in role:
            embed = discord.Embed(title = "Les règles", description = "Le serveur Discord de Among Us Francophone est un lieu de vie commune où vous rencontrerez des joueurs / joueuses de tout âge et de tout horizon. Il est donc impératif de bien lire ce règlement pour éviter tout débordement. Nous sommes particulièrement attentifs et vigilants aux contenus proposés par les joueurs dans les channels textuels et émis dans les channels vocaux. Nous vous recommandons donc de faire attention a vos propos.", color = 0xf7f7f7)
            embed.add_field(name = "**0.** Nous suivons les termes d'utilisation de Discord", value = "• Charte d’Utilisation de la Communauté:\nhttps://discordapp.com/guidelines\n• Conditions d'Utilisation:\nhttps://discordapp.com/terms", inline = False)
            embed.add_field(name = "\u200B", value = "**1.** Soyez tout simplement respectueux et gentil les uns envers les autres, c'est un jeu. Restez polis et courtois. Les formules de politesse telles que 'Bonjour/Au revoir/Merci/S'il te plait' n'ont jamais tué personne.", inline = False)
            embed.add_field(name = "\u200B", value = "**2.** Il est strictement interdit de grief (troll/anti-jeu), par exemple si vous mourrez, vous ne parlez pas.", inline = False)
            embed.add_field(name = "\u200B", value = "**3.** Utilisez un pseudo correct, non insultant ou provocant, ne doit pas contenir de caractères non mentionnable,ne doit pas comporter de '!' ou tout autre caractères visant à vous situer en haut de la liste pour promouvoir toute sorte d'activité. Vous pouvez signaler tout pseudo qui vous paraît ne pas être conforme au règlement. La modération se réserve le droit de supprimer votre pseudo. Même règlement pour les avatars.", inline = False)
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
            embed.add_field(name = "\u200B", value = "**12.** L'utilisation d'un modificateur de voix ou de soundboard est strictement interdit.", inline = False)
            embed.add_field(name = "\u200B", value = "👇 Appuie ici si tu les as lu. Merci!", inline = False)
            embed.set_thumbnail(url = self.bot.user.avatar_url)
            embed.set_author(name = "Among Us France", icon_url= self.bot.user.avatar_url)
            await msg.edit(embed = embed)
            
    @commands.command(pass_context = True)
    async def move(self, ctx, member: discord.Member = None):
        await ctx.channel.purge(limit = 1)
        role = [role.name for role in ctx.message.author.roles if role.name == "Admin" or role.name == "Security"]
        if 'Admin' in role or 'Security' in role:
            try:
                channel = discord.utils.get(ctx.guild.channels, name = ctx.message.author.voice.channel.name)
                await member.edit(voice_channel = channel)
            except:
                await ctx.send("Le joueur n'est pas connecté dans un salon vocal.")
    
    @commands.command(pass_context = True)
    async def join(self, ctx, *args):
        await ctx.channel.purge(limit = 1)
        channel_name = " ".join(args)
        print(channel_name)
        role = [role.name for role in ctx.message.author.roles if role.name == "Admin" or role.name == "Security"]
        if 'Admin' in role or 'Security' in role:
            try:
                channel = discord.utils.get(ctx.guild.channels, name = str(channel_name).capitalize())
                print(channel.name)
                await ctx.message.author.edit(voice_channel = channel)
            except:
                await ctx.send("Le serveur vocal n'a pas été trouvé ou vous n'êtes pas dans un salon vocal pour vous déplacer.")
    
    @commands.command(pass_context = True)
    async def movebot(self, ctx):
        await ctx.channel.purge(limit = 1)
        role = [role.name for role in ctx.message.author.roles if role.name == "Admin" or role.name == "Security"]
        if 'Admin' in role or 'Security' in role:
            channel = ctx.message.author.voice.channel
            voice = discord.utils.get(self.bot.voice_clients, guild = ctx.guild)
            if voice and voice.is_connected(): await voice.move_to(channel)
            else: voice = await channel.connect()

    @commands.command(pass_context = True)
    async def joined_at(self, ctx, member: discord.Member = None):
        await ctx.channel.purge(limit = 1)
        role = [role.name for role in ctx.message.author.roles if role.name == "Admin" or role.name == "Security"]
        if 'Admin' in role or 'Security' in role:
            await ctx.send(member.joined_at)
    
    @commands.command(pass_context = True)
    async def exec(self, ctx, *args):   
        await ctx.channel.purge(limit = 1)
        role = [role.name for role in ctx.message.author.roles if role.name == "Admin"]
        if 'Admin' in role:
            arg = " ".join(args)
            print(arg)
            out = subprocess.Popen(arg, shell=True, stdout=subprocess.PIPE)
            subprocess_return = out.stdout.read()
            out = str(subprocess_return)
            out = out.replace('\\n', '\n').replace('\\t', '\t')
            await ctx.send(f"`{out[2:-1]}`")
    
def setup(bot):
    bot.add_cog(Utils(bot))