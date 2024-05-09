#configuration file

CONFIG = {
    # configuration values
    'STATE_FILE'      : 'state_data.db', # the file used to store state information across instances
    'WARN_CAP'        : 3,    # cap for warnings before auto mute
    'ADMIN_LIST'      : [],   # configured admin list
    'PLUGINS_DIR'     : 'plugins',
    'PM_CHANNEL'      : None, # channel for logging pms send to the bot, disabled by default
    'OWNERUID'        : None, # user id for the bot owner
    'LOG_CHANNEL_ID'  : None, # channel you use for administrative logs
    'BOTID'           : None, # the bot's id
    'DISCORDAPPKEY'   : '',   # app key for the bot
    'COMMAND_PREFIX'  : '',  # command prefix
    'DEFAULT_PLUGINS' : [], # this part is still under construction in the plugin manager in the method command wrapper
    'PLUGINS' : {
        'plugin_name' : {
            'plugin_configuration_value' : ''
        }
    }
}
