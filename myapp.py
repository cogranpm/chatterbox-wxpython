import wx
from MainFrameImp import  MainFrameImp
import chatterbox_constants as cc
from fn_app import load_default_settings


class ChatterboxApp(wx.App):

    def __init__(self):
        super().__init__()
        # I don't know why but when these are given initial values
        # the settings in the OnInit are ignored when using the wx.App.Get() to retrieve instance
        # in other parts of the application
        #self.frame = None
        #self.data_directory = ''

    def OnInit(self) -> bool:
        """ System, Toolkit and WxWidgets fully initialized"""
        super().OnInit()
        wx.ConfigBase.Set(wx.Config(cc.APPLICATION_NAME))
        self.data_directory = load_default_settings()
        self.frame = MainFrameImp(None)
        self.frame.Show()
        self.SetTopWindow(self.frame)
        return True

