import wx
import chatterbox_constants as cc


def load_default_settings():
    config: wx.ConfigBase = wx.ConfigBase.Get()
    value = config.Read(cc.CONFIG_KEY_DATA_DIRECTORY)
    if not value:
        default_path: str = wx.StandardPaths.Get().GetUserLocalDataDir()
        config.Write(cc.CONFIG_KEY_DATA_DIRECTORY, default_path)
        return default_path
    return value
