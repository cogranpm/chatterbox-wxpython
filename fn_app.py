import wx
import chatterbox_constants as cc
import os
import logging

def load_default_settings():
    config: wx.ConfigBase = wx.ConfigBase.Get()
    value = config.Read(cc.CONFIG_KEY_DATA_DIRECTORY)
    if not value:
        default_path: str = wx.StandardPaths.Get().GetUserLocalDataDir()
        config.Write(cc.CONFIG_KEY_DATA_DIRECTORY, default_path)
        return default_path
    return value


def change_data_directory(path):
    config: wx.ConfigBase = wx.ConfigBase.Get()
    config.Write(cc.CONFIG_KEY_DATA_DIRECTORY, path)
    # set default paths
    # change database
    # close and reopen the database and reset everything


def set_default_paths(path) -> bool:
    # make sure the path exists
    # set the database name
    # initialize database
    # make audio subdirectory if not exists
    # if the path doesn't exist return false, which triggers user to locate again
    return True


def make_icon(name):
    path = os.path.join(cc.PATH_ICONS, name)
    return wx.Bitmap(path, wx.BITMAP_TYPE_PNG)


def config_logging():
    logging.basicConfig(filename=cc.LOG_FILE_NAME, level=logging.INFO, format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')


def get_data_store():
    return wx.GetApp().datastore

