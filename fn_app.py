import wx
import chatterbox_constants as cc


def load_default_settings(data_directory):
    config: wx.ConfigBase = wx.ConfigBase.Get()
    value = config.Read(data_directory)
    print(value)
