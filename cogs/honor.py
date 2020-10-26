import discord
import pymongo
import asyncio
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
        data = users.find({'player_id': member.id})
        user = {}
        for i in data: user = i
        if use == {}:
            db_user = User(
                  player_id = member.id,
                  like = member.name,
                  voice_id = voice.id,
                  voice_name = voice.name,
                  text_id = text.id,
                  private = False,
                  code = None,
                  region = None,
                  created = int(time.time()),
                  link = str(link),
                  current_players = [member.name],
                  banned = []
              )
              json_data = json.loads(db_server.to_json())
              result = servers.insert_one(json_data)
        
    @commands.command(pass_context = True, aliases=['dl'])
    async def dislike(self, ctx, member: discord.Member = None):
        await ctx.channel.purge(limit = 1)
        
def setup(bot):
    bot.add_cog(Honor(bot))