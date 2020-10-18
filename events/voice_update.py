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
name_list = ['Alfa','Bravo','Charlie','Delta','Echo','Foxtrot','Golf','Hotel','India','Juliett','Kilo','Lima','Mike','November','Oscar','Papa','Quebec','Romeo','Sierra','Tango','Uniform','Victor','Whiskey','X-ray','Yankee','Zulu']
waiting_dict = {}

class VoiceUpdate(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        logs = discord.utils.get(member.guild.channels, name = "⛔astronaute-logs")
        
        #position des vocaux par rapport au nombre de joueurs décroissants
        try:
            name_dict =  {}
            for key in name_list:
                try:
                    voice = discord.utils.get(member.guild.channels, name = key)
                    if voice.name is not None and len(voice.members) < 2:
                        name_dict[voice.name] = len(voice.members)
                        open_server = discord.utils.get(member.guild.categories, name = os.getenv("NAME_CAT_SERV_OPEN"))
                        await voice.edit(category = open_server)
                    if voice.name is not None and len(voice.members) == 2:
                        full_server = discord.utils.get(member.guild.categories, name = os.getenv("NAME_CAT_SERV_FULL"))
                        await voice.edit(category = full_server)
                except: pass
                pass
            name_dict = sorted(name_dict.items(), key = lambda x: x[1], reverse = True)
            for key in name_dict:
                voice = discord.utils.get(member.guild.channels, name = key[0])
                await voice.edit(position = name_dict.index(key))
        except: pass
        
        for i in member.guild.voice_channels:
            if i.name in name_list:
                voice = discord.utils.get(member.guild.channels, name = i.name)
                if len(voice.members) == 0:
                    text = discord.utils.get(member.guild.channels, name = voice.name.lower())
                    role = discord.utils.get(member.guild.roles, name = voice.name)            
                    role_host = discord.utils.get(member.guild.roles, name = "Hote")
                    servers.delete_one({'voice_id': voice.id})
                    await voice.delete()
                    await text.delete()
                    await role.delete()
                    await member.remove_roles(role_host)
                    await logs.send(f"🔴 Le serveur {voice.name} a été supprimé.")
        #quitté un serveur
       
        
        #rejoindre un serveur
        try:
            if after.channel.name in name_list:
                if servers.count_documents({'voice_name': after.channel.name, "banned":{"$in":[member.id]}}) == 1:
                    await member.edit(voice_channel = None)
                await member.add_roles(discord.utils.get(member.guild.roles, name = after.channel.name))
                await logs.send(f"🟢 Le joueur {member.mention} a rejoint le serveur {after.channel.name}.")
            if after.channel.name == os.getenv("NAME_VOC_JOIN_AUTO"):
                name_dict = {}
                for key in name_list:
                    try:
                        voice = discord.utils.get(member.guild.channels, name = key)
                        if voice.name is not None and len(voice.members) < 10:
                            name_dict[voice.name] = len(voice.members)
                    except: pass
                    pass
                name_dict = sorted(name_dict.items(), key = lambda x: x[1], reverse = True)
                while True:
                    if servers.count_documents({'voice_name': name_dict[0][0], "banned":{"$in":[member.id]}}) == 1:
                        name_dict = sorted(name_dict.items(), key = lambda x: x[1], reverse = True)
                    if servers.count_documents({'voice_name': name_dict[0][0], "private": True}) == 1:
                        name_dict = sorted(name_dict.items(), key = lambda x: x[1], reverse = True)
                    else: break
                await member.add_roles(discord.utils.get(member.guild.roles, name = name_dict[0][0]))
                await member.edit(voice_channel = discord.utils.get(member.guild.channels, name = name_dict[0][0]))
                await logs.send(f"🟢 Le joueur {member.mention} a rejoint le serveur {after.channel.name}.")
        except: pass

        #créé un serveur
        global waiting_dict
        try:
            if after.channel.name == os.getenv("NAME_VOC_CREATE_AUTO"):
                if member.name in waiting_dict.keys():
                    while waiting_dict[member.name] >= int(time.time()):
                        await asyncio.sleep(1)
                        print(waiting_dict[member.name], int(time.time()))
                    waiting_dict.pop(member.name)

                waiting_dict[member.name] = int(time.time()) + 30
                data = servers.find({})
                server_list = []
                for i in data: server_list.append(i)
                count = 0
                for i in server_list:
                    while i['voice_name'] == list(name_list)[count]: count += 1
                channel_name = list(name_list)[count]

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
                    voice_id = voice.id,
                    voice_name = voice.name,
                    text_id = text.id,
                    private = False,
                    code = None,
                    region = None,
                    banned = []
                )
                json_data = json.loads(db_server.to_json())
                result = servers.insert_one(json_data)
        except: pass
                
def setup(bot):
    bot.add_cog(VoiceUpdate(bot))
