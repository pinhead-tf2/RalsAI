import discord
from discord.ext import commands


database_name = "history_database.sqlite"


class Responder(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, member):
        await member.send('Welcome to the server!')


def setup(bot):
    bot.add_cog(Responder(bot))
