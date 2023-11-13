import discord
from discord.ext import commands
from discord import app_commands
from dotenv import load_dotenv
import os

from src.log import setup_logger
from configs.load_configs import configs

log = setup_logger(__name__)

load_dotenv()

bot = commands.Bot(command_prefix=configs['prefix'], intents=discord.Intents.all())


@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=configs['activity_name']))
    bot.tree.on_error = on_tree_error
    for filename in os.listdir('./cogs'):
            if filename.endswith('.py'):
                await bot.load_extension(f'cogs.{filename[:-3]}')
    log.info(f'{bot.user} is online')
    slash = await bot.tree.sync()
    log.info(f'synced {len(slash)} slash commands')


@bot.command()
@commands.is_owner()
async def load(ctx, extension):
    await bot.load_extension(f'cogs.{extension}')
    await ctx.send(f'Loaded {extension} done.')


@bot.command()
@commands.is_owner()
async def unload(ctx, extension):
    await bot.unload_extension(f'cogs.{extension}')
    await ctx.send(f'Un - Loaded {extension} done.')


@bot.command()
@commands.is_owner()
async def reload(ctx, extension):
    await bot.reload_extension(f'cogs.{extension}')
    await ctx.send(f'Re - Loaded {extension} done.')


@bot.event
async def on_tree_error(itn : discord.Interaction, error : app_commands.AppCommandError):
    await itn.response.send_message(error, ephemeral=True)
    log.warning(f'an error occurred but was handled by the tree error handler, error message : {error}')


@bot.event
async def on_command_error(ctx : commands.context.Context, error : commands.errors.CommandError):
    if isinstance(error, commands.errors.CommandNotFound): return
    else: await ctx.send(error)
    log.warning(f'an error occurred but was handled by the command error handler, error message : {error}')


if __name__ == '__main__':
    bot.run(os.getenv('TOKEN'))