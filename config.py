import logging

BACKEND = 'Text'  # Errbot will start in text mode (console only mode) and will answer commands from there.

BOT_DATA_DIR = r'/home/lifetimealone/code/Obuchatter/data'
BOT_EXTRA_PLUGIN_DIR = r'/home/lifetimealone/code/Obuchatter/plugins'

BOT_LOG_FILE = r'/home/lifetimealone/code/Obuchatter/errbot.log'
BOT_LOG_LEVEL = logging.DEBUG

BOT_ADMINS = ('@CHANGE_ME', )  # !! Don't leave that to "@CHANGE_ME" if you connect your errbot to a chat system !!
