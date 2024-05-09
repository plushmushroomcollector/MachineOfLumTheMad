import discord
from discord import Intents
from discord.ext.commands import Bot
import discord.ext.commands as commands

class ConfigError(Exception): pass
class PluginDirectoryError(Exception): pass
class PluginError(Exception): pass

class MyBot(Bot):
    INTENTS = Intents.default()
    INTENTS.members = True
    INTENTS.message_content = True
    INTENTS.reactions = True
    INTENTS.dm_messages = True
    INTENTS.dm_reactions = True
    key = ""

    def __init__(self, key, config_file, *args, **kwargs):
        super().__init__(
            *args,
            case_insensitive=True,
            intents = MyBot.INTENTS,
            **kwargs
        )
        self.key = key
        self.config = config_file

    def run_bot(self, *args, **kwargs):
        super().run(self.key, *args, **kwargs)