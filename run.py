import discord
from discord import Intents
from config import CONFIG
from plugins.manifest import MANIFEST
from plugins.manifest import IMPORT_LIST
import sys, importlib

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
    from discord_bot.DiscordBot import MyBot

    my_bot = MyBot(CONFIG['DISCORDAPPKEY'], CONFIG, command_prefix=CONFIG['COMMAND_PREFIX'])
    
    @my_bot.command(name='plugin-load', aliases=[])
    @is_admin
    async def plugin_load(ctx, *plugin_name : str):
        plugin_name = ' '.join(plugin_name)
        
        if not plugin_name in MANIFEST:
            await ctx.send(f'plugin: {plugin_name} was not found in the manifest')
            return
        else:
            plugin_module = None
            try:
                plugin_module = importlib.import_module(f'{CONFIG['PLUGINS_DIR']}.{MANIFEST[plugin_name]}')
            except:
                plugin_module= None
            
            if plugin_module is None:
                await ctx.send(f'plugin: {plugin_name} was not found in the plugins folder or the wrong plugins folder is listed in the configuration file')
                return
            else:
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
        if plugin_name in my_bot.cogs:
            await my_bot.remove_cog(plugin_name)
            await ctx.send(f'plugin: {plugin_name} was unloaded')
            plugin_module = importlib.import_module(f'{CONFIG['PLUGINS_DIR']}.{MANIFEST[plugin_name]}')
            plugin_class = getattr(plugin_module, MANIFEST[plugin_name])
            await my_bot.add_cog(plugin_class(my_bot))
            await ctx.send(f'plugin: {plugin_name} was reloaded')
        else:
            await ctx.send(f'{plugin_name} is not loaded')

    @my_bot.command(name='plugin-help', aliases=[])
    async def plugin_help(ctx, *plugin_name : str):
        plugin_name = ' '.join(plugin_name)
        if plugin_name in my_bot.cogs:
            await ctx.send(my_bot.cogs.get(plugin_name).help)
        else:
            await ctx.send(f'{plugin_name} is not loaded')

    @my_bot.command(name='git-source', aliases=[])
    async def git_source(ctx):
        await ctx.author.send('https://github.com/plushmushroomcollector/MachineOfLumTheMad')

    @my_bot.command(name='refresh-manifest', aliases=[])
    async def refresh_manifest(ctx):
        #TODO: fix this functionality
        importlib.reload(sys.modules['plugins.manifest'])
        from plugins.manifest import MANIFEST
        ctx.send('manifest has been refreshed')

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