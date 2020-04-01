import wx


class TestFrame(wx.Frame):

    def __init__(self, parent):
        wx.Frame.__init__(self, parent, id=wx.ID_ANY, title=u"Chatterbox", pos=wx.DefaultPosition,
                          size=wx.Size(1133, 716), style=wx.DEFAULT_FRAME_STYLE | wx.MAXIMIZE | wx.TAB_TRAVERSAL,
                          name=u"MainFrame")

        self.SetSizeHints(wx.DefaultSize, wx.DefaultSize)