import wx

class NotEmpty(wx.PyValidator):

    def __init__(self):
        super().__init__()

    def Clone(self):
        return NotEmpty()

    def Validate(self, parent):
        control = self.GetWindow()
        val = control.GetValue()
        if len(val) == 0:
            wx.MessageBox("Cannot be empty", "Error")
            control.SetBackgroundColour("pink")
            control.SetFocus()
            control.Refresh()
            return False
        else:
            control.SetBackgroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_WINDOW))
            control.Refresh()
            return True

    def TransferToWindow(self):
        return True

    def TransferFromWindow(self):
        return True