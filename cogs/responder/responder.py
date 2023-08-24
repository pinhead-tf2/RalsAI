import aiosqlite
import discord
from discord.ext import commands
from api.languagemodel.request_handler import generate_response

chat_history = {
    "internal": [
        [
            "<|BEGIN-VISIBLE-CHAT|>",
            "Greetings! I am Ralsei! You, it's wonderful to meet you!"
        ]
    ],
    "visible": [
        [
            "",
            "Greetings! I am Ralsei! You, it's wonderful to meet you!"
        ]
    ]
}


def save_chat_history(new_history):
    chat_history = new_history


def load_chat_history():
    return chat_history


class Responder(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        if (message.author.id != self.bot.user.id and message.channel.id == 1144025916729724928 and
                self.bot.user.mentioned_in(message) and self.bot.languagemodel_thinking is False):
            new_history = generated_response = None

            async with message.channel.typing():
                self.bot.languagemodel_thinking = True
                formatted_username = f'[{message.author.name}]: '
                cleaned_message_content = message.clean_content.replace("@", "")
                formatted_message = formatted_username + cleaned_message_content

                print(formatted_message)

                new_history, generated_response = await generate_response(self.bot.languagemodel_session,
                                                                          formatted_message,
                                                                          load_chat_history())

            save_chat_history(new_history)
            await message.reply(generated_response)
            self.bot.languagemodel_thinking = False


def setup(bot):
    bot.add_cog(Responder(bot))
