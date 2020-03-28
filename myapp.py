import wx
from mainframe import MainFrame
import chatterbox_constants as cc
from fn_app import load_default_settings


class ChatterboxApp(wx.App):

    def __init__(self):
        super().__init__()
        self.frame = None

    def OnInit(self) -> bool:
        wx.ConfigBase.Set(wx.Config(cc.APPLICATION_NAME))
        load_default_settings(cc.CONFIG_KEY_DATA_DIRECTORY)
        self.frame = MainFrame(None, "Chatterbox")
        self.frame.Show()
        return True

