import discord
from discord import Intents
from config import CONFIG
from plugins.administrative_tools import administrative_tools
from plugins.manifest import MANIFEST
from plugins.manifest import IMPORT_LIST
import datetime
import importlib

import functools as ft

def is_admin(func):
        @ft.wraps(func)
        async def decorated(ctx, *args, **kwargs):
            if ctx.author.id in CONFIG['ADMIN_LIST']:
                return await func(ctx, *args, **kwargs)
            else:
                await ctx.send(f'{ctx.author.mention} you are not an admin')

        return decorated

def run_bot():
    from discord_bot import My_Bot

    my_bot = My_Bot(CONFIG['DISCORDAPPKEY'], CONFIG, command_prefix=CONFIG['COMMAND_PREFIX'])
    
    @my_bot.command(name='plugin-load', aliases=[])
    @is_admin
    async def plugin_load(ctx, *plugin_name : str):
        plugin_name = ' '.join(plugin_name)
        plugin_module = importlib.import_module(f'{CONFIG['PLUGINS_DIR']}.{MANIFEST[plugin_name]}')
        plugin_class = getattr(plugin_module, MANIFEST[plugin_name])
        await my_bot.add_cog(plugin_class(my_bot))
        await ctx.send(f'plugin: {plugin_name} was loaded')

    @my_bot.command(name='plugin-remove', aliases=['plugin-unload'])
    @is_admin
    async def plugin_remove(ctx, *plugin_name : str):
        plugin_name = ' '.join(plugin_name)
        await my_bot.remove_cog(plugin_name)
        await ctx.send(f'plugin: {plugin_name} was unloaded')

    @my_bot.command(name='plugin-reload', aliases=[])
    @is_admin
    async def plugin_reload(ctx, *plugin_name : str):
        plugin_name = ' '.join(plugin_name)
        await my_bot.remove_cog(plugin_name)
        await ctx.send(f'plugin: {plugin_name} was unloaded')
        plugin_module = importlib.import_module(f'{CONFIG['PLUGINS_DIR']}.{MANIFEST[plugin_name]}')
        plugin_class = getattr(plugin_module, MANIFEST[plugin_name])
        await my_bot.add_cog(plugin_class(my_bot))
        await ctx.send(f'plugin: {plugin_name} was reloaded')

    @my_bot.command(name='plugin-help', aliases=[])
    async def plugin_help(ctx, *plugin_name : str):
        plugin_name = ' '.join(plugin_name)
        await ctx.send(my_bot.cogs.get(plugin_name).help)

    @my_bot.event
    async def on_ready():
        print(f'We have logged in as {my_bot.user}')

        for plugin_name in IMPORT_LIST:
            plugin_module = importlib.import_module(f'{CONFIG['PLUGINS_DIR']}.{MANIFEST[plugin_name]}')
            plugin_class = getattr(plugin_module, MANIFEST[plugin_name])
            await my_bot.add_cog(plugin_class(my_bot))
            print (f'module: {plugin_name} loaded')

    my_bot.run_bot()

run_bot()