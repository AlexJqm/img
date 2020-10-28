import discord
import pymongo
import asyncio
import json
from discord.ext import commands
from database.connect import db_connect
from database.models.db_user import User

users = db_connect("users")

class Honor(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    @commands.command(pass_context = True, aliases=['l'])
    async def like(self, ctx, member: discord.Member = None):
        await ctx.channel.purge(limit = 1)
        if member is not None:
            if member.id != ctx.message.author.id:
                
                data = users.find({'player_id': member.id})
                user = {}
                for i in data: user = i
                if user == {}:
                    db_user = User(
                        player_id = member.id,
                        like = 0,
                        dislike = 0,
                        badge = []
                    )
                    json_data = json.loads(db_user.to_json())
                    result = users.insert_one(json_data)
                    users.update_one({'player_id': member.id}, {"$set": {'like': user['like'] + 1}})
                    await ctx.send(embed = discord.Embed(title = f"❤️ Like", description = f"{ctx.message.author.mention}, votre like a bien été pris en compte!", color = 0x26f752))
                else:
                    users.update_one({'player_id': member.id}, {"$set": {'like': user['like'] + 1}})
                    await ctx.send(embed = discord.Embed(title = f"❤️ Like", description = f"{ctx.message.author.mention}, votre like a bien été pris en compte!", color = 0x26f752))
                    
            else: await ctx.send(embed = discord.Embed(title = "💥 Une erreur s'est produite...", description = "Vous ne pouvez pas vous likez vous-même, c'est bien tenté.", color = 0xF73F26))  
        
        else: await ctx.send(embed = discord.Embed(title = "💥 Une erreur s'est produite...", description = "Vous n'avez pas mentionner de joueur: `.like @pseudo`", color = 0xF73F26))
    
    @commands.command(pass_context = True, aliases=['dl'])
    async def dislike(self, ctx, member: discord.Member = None):
        await ctx.channel.purge(limit = 1)
        if member is not None:
            if member.id != ctx.message.author.id:
                
                data = users.find({'player_id': member.id})
                user = {}
                for i in data: user = i
                if user == {}:
                    db_user = User(
                        player_id = member.id,
                        like = 0,
                        dislike = 0,
                        badge = []
                    )
                    json_data = json.loads(db_user.to_json())
                    result = users.insert_one(json_data)
                    users.update_one({'player_id': member.id}, {"$set": {'dislike': user['dislike'] + 1}})
                    await ctx.send(embed = discord.Embed(title = f"💔 Dislike", description = f"{ctx.message.author.mention}, votre dislike a bien été pris en compte!", color = 0x26f752))
                else:
                    users.update_one({'player_id': member.id}, {"$set": {'dislike': user['dislike'] + 1}})
                    await ctx.send(embed = discord.Embed(title = f"💔 Dislike", description = f"{ctx.message.author.mention}, votre dislike a bien été pris en compte!", color = 0x26f752))
                    
            else: await ctx.send(embed = discord.Embed(title = "💥 Une erreur s'est produite...", description = "Vous ne pouvez pas vous dislikez vous-même.", color = 0xF73F26))  
        
        else: await ctx.send(embed = discord.Embed(title = "💥 Une erreur s'est produite...", description = "Vous n'avez pas mentionner de joueur: `.like @pseudo`", color = 0xF73F26))
        
def setup(bot):
    bot.add_cog(Honor(bot))