import wx


class MainFrame(wx.Frame):

    def __init__(self, parent, title):
        wx.Frame.__init__(self, parent, -1, title, size=(970, 720),
                          style=wx.DEFAULT_FRAME_STYLE | wx.NO_FULL_REPAINT_ON_RESIZE)
        self.SetMinSize((640, 480))
        self.Centre(wx.BOTH)

