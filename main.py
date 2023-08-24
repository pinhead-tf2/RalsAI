from datetime import datetime
from os import getenv, listdir
from os.path import isfile
from time import time
from traceback import format_exception

import discord
from discord import option
from discord.commands import SlashCommandGroup
from discord.ext import commands
from dotenv import load_dotenv
from aiohttp import ClientSession
from database_initializer import create_database

database_name = "history_database.sqlite"

load_dotenv()

intents = discord.Intents.default()
intents.message_content = True

bot = discord.Bot(
    debug_guilds=[991589246949404673],
    status=discord.Status.dnd,
    activity=discord.Game(name="Initializing..."),
    owner_ids=[246291288775852033],
    intents=intents
)

bot.startup_complete = False
bot.startTime = time()
bot.languagemodel_thinking = False
bot.error_webhook = bot.webhook_session = bot.languagemodel_session = None


@bot.event
async def on_ready():
    if bot.startup_complete:
        try:
            await bot.webhook_session.close()
            await bot.languagemodel_session.close()
            await bot.close()
        except RuntimeError:
            await bot.close()
        finally:
            # create self-restart script here
            exit()

    if not isfile(database_name):
        await create_database()  # this just cleans this file up a lot

    bot.webhook_session = ClientSession()
    bot.languagemodel_session = ClientSession()
    # bot.error_webhook = discord.Webhook.from_url(
    #     getenv("DISCORD_ERROR_WEBHOOK"),
    #     session=bot.webhook_session
    # )

    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name='the Dark Worlds'),
                              status=discord.Status.online)
    print(f"{bot.user} started | Start timestamp: {datetime.now().strftime('%I:%M %p, %m/%d/%Y')} | "
          f"Time to start: {round(time() - bot.startTime, 4)} seconds")

    bot.startup_complete = True


admin = SlashCommandGroup("admin", "Admin/owner only commands", checks=[commands.is_owner()], )


@admin.command()
@commands.is_owner()
async def shutdown(ctx):
    await ctx.respond("ok, shutting down", ephemeral=True)
    try:
        await bot.webhook_session.close()
        await bot.languagemodel_session.close()
        await bot.close()
    except AttributeError:
        await bot.close()


edit = admin.create_subgroup("edit", "Profile related commands")


@edit.command()
@commands.is_owner()
@option("name", description="New name for the bot to use")
async def username(ctx,
                   name: str):
    old_name = bot.user.name
    try:
        await bot.user.edit(username=name)
    except discord.HTTPException as error:
        await ctx.respond(f"**Error:** Username could not be changed. `({error.code})`\n"
                          f"**HTTP Status:** {error.status}\n"
                          f"**Error Details:** `{error.text}`",
                          ephemeral=True)
    await ctx.respond(f"Successfully changed my username from `{old_name}` to **{bot.user.name}**.")


@edit.command()
@commands.is_owner()
@option("picture", description="New avatar for the bot to use")
async def avatar(ctx,
                 picture: discord.Attachment):
    try:
        await bot.user.edit(avatar=await picture.read())
    except discord.HTTPException as error:
        await ctx.respond(f"**Error:** Avatar could not be changed. `({error.code})`\n"
                          f"**HTTP Status:** {error.status}\n"
                          f"**Error Details:** `{error.text}`",
                          ephemeral=True)
    except discord.InvalidArgument:
        await ctx.respond(f"**Error**: The picture supplied isn't in the right format.",
                          ephemeral=True)
    await ctx.respond(f"Successfully changed my avatar!")


cogs = admin.create_subgroup("cogs", "Cog-related commands")


async def get_loaded_cogs():
    loaded_cogs = []
    for loaded_cog in list(bot.cogs):
        loaded_cogs.append(f"cogs.{loaded_cog}.{loaded_cog}".lower())
    return loaded_cogs


async def cog_names(ctx: discord.AutocompleteContext):
    load_choice = ctx.options['load_choice']
    loaded_cogs = await get_loaded_cogs()
    if load_choice == 'reload' or load_choice == 'unload':
        return loaded_cogs
    else:
        unloaded_cogs = []

        for folder_name in listdir('./cogs'):
            for cog_name in listdir(f'./cogs/{folder_name}'):
                if filename.endswith('.py'):
                    unloaded_cogs.append(f'cogs.{folder_name}.{cog_name[:-3]}'.lower())

        for loaded_cog in loaded_cogs:
            filter(loaded_cog.__ne__, unloaded_cogs)

        return unloaded_cogs


@cogs.command(name="cog", description="Manages the load state of a cog")
@option("load_choice", description="Choose what you'll do with the cog", choices=['reload', 'load', 'unload'])
@option("cog_name", description="Select the cog you wish to manage",
        autocomplete=discord.utils.basic_autocomplete(cog_names))
@commands.is_owner()
async def cog(ctx,
              load_choice: str,
              cog_name: str
              ):
    interaction = await ctx.respond(f"*Attempting to {load_choice} cog {cog_name}...*", ephemeral=True)
    match load_choice:
        case 'reload':
            bot.reload_extension(cog_name)
        case 'load':
            bot.load_extension(cog_name)
        case 'unload':
            bot.unload_extension(cog_name)
        case _:
            await interaction.edit_original_response(content="Invalid cog choice.", ephemeral=True)
    await interaction.edit_original_response(content=f"**Successfully {load_choice}ed {cog_name}!**")


@cogs.command()
@commands.is_owner()
async def list_cogs(ctx):
    await ctx.respond("Loaded cogs: ".join(map(str, bot.cogs)))


@bot.event
async def on_application_command_error(ctx: discord.ApplicationContext, error: Exception):
    if isinstance(error, discord.ApplicationCommandInvokeError):
        if isinstance((error := error.original), discord.HTTPException):
            message = (
                "An HTTP exception has occurred: "
                f"{error.status} {error.__class__.__name__}"
            )
            if error.text:
                message += f": {error.text}"
            return await ctx.respond(message, ephemeral=True)
        elif not isinstance(error, discord.DiscordException):
            await ctx.respond("Unexpected error encountered, details have been noted and sent to developers",
                              ephemeral=True)
            header = f"Command: `/{ctx.command.qualified_name}`"
            if ctx.guild is not None:
                header += f" | Guild: `{ctx.guild.name} ({ctx.guild_id})`"
            # await bot.error_webhook.send(
            #     f"{header}\n```\n{''.join(format_exception(type(error), error, error.__traceback__))}\n```"
            # )
            raise error
    await ctx.respond(
        embed=discord.Embed(
            title=error.__class__.__name__,
            description=str(error),
            color=discord.Color.red(),
        ), ephemeral=True
    )


for foldername in listdir('./cogs'):
    for filename in listdir(f'./cogs/{foldername}'):
        if filename.endswith('.py'):
            bot.load_extension(f'cogs.{filename[:-3]}')

bot.add_application_command(admin)

bot.run(getenv("DISCORD_TOKEN"))