import wx


def not_empty(control):
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

class NameValidator(wx.Validator):
    """ can always use the same validator for all controls and do a switch on control name """

    def __init__(self, data):
        super().__init__()
        self.data = data

    def Clone(self):
        return NameValidator(self.data)

    def set_data(self, data):
        self.data = data

    def Validate(self, win):
        control = self.GetWindow()
        if control.GetName() == "name":
            return not_empty(control)
        return True


    def TransferToWindow(self):
        print("TransferToWindow called")
        print(self.data)
        control = self.GetWindow()
        if control.GetName() == "name":
            control.SetValue(self.data[0])
        elif control.GetName() == "age":
            control.SetValue(self.data[1])
        return True

    def TransferFromWindow(self):
        print("transfer from window called")
        control = self.GetWindow()
        self.data[0] = control.GetValue()
        return True
