import aiosqlite
import discord
from discord.ext import commands
from api.languagemodel.request_handler import generate_response

database_name = "history_database.sqlite"


class Responder(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, ctx):
        if ctx.author == self.bot:
            return

        async with aiosqlite.connect(database_name) as db:
            cursor = await db.execute(sql=f'SELECT is_banned FROM users WHERE id={ctx.author.id}')
            result = await cursor.fetchone()
            print(result)

            if result is None:
                print("New user detected")
                await db.execute("INSERT INTO users (id) "
                                 "VALUES (?)",
                                 (ctx.author.id))
                await db.commit()


def setup(bot):
    bot.add_cog(Responder(bot))
