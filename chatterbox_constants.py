from configobj import ConfigObj
import os, sys

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
SIGNAL_SHUTDOWN = 'chatterbox-shutdown'
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

COLLECTION_NAME_SHELF = 'shelf'
COLLECTION_NAME_SUBJECT = 'subject'

NOTEBOOK_TITLE_SHELF = 'Shelf'

ID_ADD_SHELF = 1001
ID_DELETE_SHELF = 1002
ID_EDIT_SHELF = 1003
ID_ADDPUBLICATION = 1004
ID_VIEW_COPYFILES = 1005
ID_VIEW_SHELF = 1006

ICON_EDIT = 'Edit.png'
ICON_ADD = 'Add.png'
ICON_CANCEL = 'Cancel.png'

config = ConfigObj("chatterbox.ini")

def read_config(key: str):
    return config[key]

def set_config(key: str, value):
    config[key] = value

def write_config():
    config.write()

def get_current_path():
    return os.path.abspath(os.path.dirname(sys.argv[0]))



