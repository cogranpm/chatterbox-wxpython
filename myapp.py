import wx
from mainframe import MainFrame
import chatterbox_constants as cc
from fn_app import load_default_settings
from SettingsDialogImp import SettingsDialogImp

class ChatterboxApp(wx.App):

    def __init__(self):
        super().__init__()
        self.frame = None
        self.data_directory = None

    def OnInit(self) -> bool:
        wx.ConfigBase.Set(wx.Config(cc.APPLICATION_NAME))
        self.data_directory = load_default_settings()
        self.frame = MainFrame(None, "Chatterbox")
        self.frame.Show()
        with SettingsDialogImp(self.frame, self.data_directory) as dlg:
            if dlg.ShowModal() == wx.ID_OK:
                print(dlg.dirty)
                print(dlg.data_directory)

        return True

