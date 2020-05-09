from configobj import ConfigObj

APPLICATION_NAME = "chatterbox"
CONFIG_KEY_DATA_DIRECTORY = "datadirectory"
PATH_AUDIO_DIR = "Audio"
DATABASE_NAME = "data.db"
PATH_ICONS = "icons"
LOG_FILE_NAME = "app.log"
SIGNAL_ADD = 'chatterbox-add'
SIGNAL_DELETE = 'chatterbox-delete'
SIGNAL_SAVE = 'chatterbox-save'
SIGNAL_VIEWSTATE = 'chatterbox-viewstate'
SIGNAL_VIEW_ACTIVATED = 'chatterbox-view-loaded'
# SIGNAL_STORE = 'chatterbox-store'
SIGNAL_SHUTDOWN = 'chatterbox-shutdown'
SIGNAL_CREATE_ENTITY = 'chatterbox-create-entity'
COMMAND_ADD = 'add'
COMMAND_DELETE = 'delete'
COMMAND_SAVE = 'save'
COMMAND_DIRTY = 'dirty'
COMMAND_ADDING = 'adding'
COMMAND_EMPTY = 'empty'
COMMAND_LOADED = 'loaded'
COMMAND_VIEW_ACTIVATED = 'activated'

COPY_FILE_SOURCE_DIR = 'copy_file_source'
COPY_FILE_DEST_DIR = 'copy_file_dest'


config = ConfigObj("chatterbox.ini")

def read_config(key: str):
    return config[key]

def set_config(key: str, value):
    config[key] = value

def write_config():
    config.write()

