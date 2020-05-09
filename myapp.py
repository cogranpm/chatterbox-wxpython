import wx
#from MainFrameImp import  MainFrameImp
from frames import AppFrame
import chatterbox_constants as cc
from fn_app import load_default_settings, set_default_paths, config_logging
import logging
import datastore

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
        config_logging()
        wx.ConfigBase.Set(wx.Config(cc.APPLICATION_NAME))
        self.data_directory = load_default_settings()
        is_valid = set_default_paths(self.data_directory)
        if not is_valid:
            # give user a chance to select a new path
            pass

        # load images
        self.datastore = datastore.DataStore()
        self.frame = AppFrame()
        self.frame.Show()
        self.SetTopWindow(self.frame)
        return True

    def OnExit(self) -> int:
        # cleanup tasks here
        wx.py.dispatcher.send(signal=cc.SIGNAL_SHUTDOWN, sender=self, command=None, more=None)
        cc.write_config()
        return 0



