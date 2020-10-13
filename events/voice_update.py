import discord
import pymongo
import asyncio
import time
import json
import os
from random import randrange
from discord.ext import commands
from os.path import join, dirname
from dotenv import load_dotenv
from database.connect import db_connect
from database.models.db_user import Server

dotenv_path = join(dirname(__file__), '../.env')
load_dotenv(dotenv_path)

servers = db_connect()
server_dict = {'Alfa':'🇦','Bravo':'🇧','Charlie':'🇨','Delta':'🇩','Echo':'🇪','Foxtrot':'🇫','Golf':'🇬','Hotel':'🇭','India':'🇮','Juliett':'🇯','Kilo':'🇰','Lima':'🇱','Mike':'🇲','November':'🇳','Oscar':'🇴','Papa':'🇵','Quebec':'🇶','Romeo':'🇷','Sierra':'🇸','Tango':'🇹','Uniform':'🇺','Victor':'🇻','Whiskey':'🇼','X-ray':'🇽','Yankee':'🇾','Zulu':'🇿'}
waiting_create = []
waiting_auto = []
waiting_join = []

class VoiceUpdate(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        logs = discord.utils.get(member.guild.channels, name = "⛔astronaute-logs")

        #position des vocaux par rapport au nombre de joueurs décroissants
        try:
            serveur_dict = {}
            for key in server_dict.keys():
                try:
                    voice = discord.utils.get(member.guild.channels, name = key)
                    if voice.name is not None and len(voice.members) < 10:
                        serveur_dict[voice.name] = len(voice.members)
                        open_server = discord.utils.get(member.guild.categories, name = os.getenv("NAME_CAT_SERV_OPEN"))
                        await voice.edit(category = open_server)
                    if voice.name is not None and len(voice.members) == 10:
                        full_server = discord.utils.get(member.guild.categories, name = os.getenv("NAME_CAT_SERV_FULL"))
                        await voice.edit(category = full_server)
                except: pass
                pass
            serveur_dict= sorted(serveur_dict.items(), key = lambda x: x[1], reverse = True)
            for key in serveur_dict:
                voice = discord.utils.get(member.guild.channels, name = key[0])
                await voice.edit(position = serveur_dict.index(key))
        except: pass

        #quitté un serveur
        try:
            role_serv = None
            host = False
            if before.channel.name in server_dict.keys(): role_serv = discord.utils.get(member.guild.roles, name = before.channel.name.capitalize())
            if servers.count_documents({'voice_name': before.channel.name.capitalize(), 'finished': None, 'host_name': member.name}) > 0:  host = True

            voice = discord.utils.get(member.guild.channels, name = role_serv.name.capitalize())
            text = discord.utils.get(member.guild.channels, name = role_serv.name.lower())

            if (after.channel is None) or (after.channel.name != role_serv.name):
                role_host = discord.utils.get(member.guild.roles, name = "Hote")

                if host and len(voice.members) > 0:
                    new_host = voice.members[randrange(len(voice.members))]
                    await new_host.add_roles(role_host)
                    servers.update_one({'voice_name': voice.name, 'finished': None}, {"$set": {'host_name': new_host.name, 'host_id': new_host.id}})
                    await logs.send(f"🟢 Le joueur {new_host.mention} a été designer par défaut comme nouvel hôte du serveur {role_serv.name}.")
                    await text.send(embed = discord.Embed(title = f"ℹ️ Serveur {text.name.capitalize()}", description = f"Le joueur {new_host.mention} à été designer par défaut comme nouvel hôte du serveur {text.name.capitalize()}.", color = 0x26f752))
                await member.remove_roles(role_serv)
                await member.remove_roles(role_host)
                await logs.send(f"🔴 Le joueur {member.mention} a quitté le serveur {role_serv.name}.")
                servers.update_one({'voice_name': role_serv.name, 'finished': None}, {'$pull': {'current_players': member.name}})

            if (after.channel is None) or (after.channel.name != role_serv.name):
                if len(voice.members) == 0:
                    text = discord.utils.get(member.guild.channels, name = role_serv.name.lower())
                    role = discord.utils.get(member.guild.roles, name = role_serv.name)            
                    role_host = discord.utils.get(member.guild.roles, name = "Hote")
                    servers.update_one({'voice_name': role_serv.name, 'finished': None}, {"$set": {"finished": int(time.time())}})
                    await voice.delete()
                    await text.delete()
                    await role.delete()
                    await member.remove_roles(role_host)
                    await logs.send(f"🔴 Le serveur {voice.name} a été supprimé.")
        except: pass
        
        #rejoindre un serveur automatiquement
        try:
            if after.channel.name == os.getenv("NAME_VOC_JOIN_AUTO"):
                waiting_auto.append(member.name)
                if waiting_auto[0] != member.name:
                    await asyncio.sleep(waiting_auto.index(member.name)*3)

                serveur_dict = {}
                for key in server_dict.keys():
                    try:
                        voice = discord.utils.get(member.guild.channels, name = key)
                        if voice.name is not None and len(voice.members) < 10:
                            serveur_dict[voice.name] = len(voice.members)
                    except: pass
                    pass
                serveur_dict = sorted(serveur_dict.items(), key = lambda x: x[1], reverse = True)
                while True:
                    if servers.count_documents({'voice_name': serveur_dict[0][0], 'finished': None, "ban_players":{"$in":[member.id]}}) == 1:
                        serveur_dict = sorted(serveur_dict.items(), key = lambda x: x[1], reverse = True)
                    if servers.count_documents({'voice_name': serveur_dict[0][0], 'finished': None, "private": True}) == 1:
                        serveur_dict = sorted(serveur_dict.items(), key = lambda x: x[1], reverse = True)
                    else: break
                await member.add_roles(discord.utils.get(member.guild.roles, name = serveur_dict[0][0]))
                servers.update_one({'voice_name': serveur_dict[0][0], 'finished': None}, {'$push': {'current_players': member.name}})
                await member.edit(voice_channel = discord.utils.get(member.guild.channels, name = serveur_dict[0][0]))
                await logs.send(f"🟢 Le joueur {member.mention} a rejoint le serveur {after.channel.name}.")
                waiting_auto.remove(member.name)
        except: pass
        
        #rejoindre un serveur manuellement
        try:
          if after.channel.name in server_dict.keys() and servers.count_documents({"finished": None, "current_players":{"$in":[member.name]}}) == 0:
              waiting_join.append(member.name)
              if waiting_join[0] != member.name:
                  await asyncio.sleep(waiting_join.index(member.name)*2)

              if servers.count_documents({'voice_name': serveur_dict[0][0], 'finished': None, "ban_players":{"$in":[member.id]}}) == 1:
                  await member.edit(voice_channel = None)
              await member.add_roles(discord.utils.get(member.guild.roles, name = after.channel.name))
              await logs.send(f"🟢 Le joueur {member.mention} a rejoint le serveur {after.channel.name}.")
              if servers.count_documents({"current_players":{"$in":[member.name]}}) == 0:
                  servers.update_one({'voice_name': after.channel.name, 'finished': None}, {'$push': {'current_players': member.name}})
              else: pass

              waiting_join.remove(member.name)
        except: pass
        #créé un serveur
        try:
            global waiting_list
            if after.channel.name == os.getenv("NAME_VOC_CREATE_AUTO"):

                if member.name not in waiting_create:
                    waiting_create.append(member.name)
                    if waiting_create[0] != member.name:
                        await asyncio.sleep(waiting_create.index(member.name)*5)

                    data = servers.find({'finished': None})

                    server_list = []
                    for i in data: server_list.append(i)

                    count = 0
                    for i in server_list:
                        while i['voice_name'] == list(server_dict.keys())[count]: count += 1
                    channel_name = list(server_dict.keys())[count]

                    open_server = discord.utils.get(member.guild.categories, name = os.getenv("NAME_CAT_SERV_OPEN"))
                    cat_chat = discord.utils.get(member.guild.categories, name = os.getenv("NAME_CAT_TEXT_CHAT"))
                    voice = await member.guild.create_voice_channel(channel_name, category = open_server, user_limit = 10)
                    text = await member.guild.create_text_channel(channel_name, category = cat_chat)
                    link = await voice.create_invite(max_age = 0)

                    role_host = discord.utils.get(member.guild.roles, name = "Hote")
                    role_chan = await member.guild.create_role(name = channel_name, colour = discord.Colour(0xf1f1f1))
                    await text.set_permissions(role_chan, read_messages = True, send_messages = True, add_reactions = False)

                    role_membre = discord.utils.get(member.guild.roles, name = "Crewmate")
                    await voice.set_permissions(role_membre, connect = True, view_channel = True)
                    await text.set_permissions(role_membre, read_messages = False, send_messages = False)

                    role_modo = discord.utils.get(member.guild.roles, name = "Security")
                    await voice.set_permissions(role_modo, connect = True, view_channel = True)
                    await text.set_permissions(role_modo, read_messages = True, send_messages = True)

                    await member.add_roles(role_chan, role_host)
                    await member.edit(voice_channel = discord.utils.get(member.guild.channels, name = channel_name))

                    await logs.send(f"🟢 Le joueur {member.mention} a créé le serveur {voice.name}.")

                    id = servers.count_documents({}) + 1
                    db_server = Server(
                        _id = id,
                        host_id = member.id,
                        host_name = member.name,
                        voice_id = voice.id,
                        voice_name = voice.name,
                        text_id = text.id,
                        text_name = text.name,
                        private = False,
                        code = None,
                        region = None,
                        created = int(time.time()),
                        finished = None,
                        current_players = [member.name],
                        ban_players = [],
                        link = str(link)
                    )
                    json_data = json.loads(db_server.to_json())
                    result = servers.insert_one(json_data)
                    waiting_create.remove(member.name)
        except: pass

def setup(bot):
    bot.add_cog(VoiceUpdate(bot))
