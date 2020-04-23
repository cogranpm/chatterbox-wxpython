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


class FieldValidator(wx.Validator):
    """ can always use the same validator for all controls and do a switch on control name """

    def __init__(self, data, key, validators):
        """ at this moment in time takes a key and index to support both map data and list
        validators is a list of functions to apply
        """
        super().__init__()
        self.data = data
        self.key = key
        self.validators = validators

    def Clone(self):
        return FieldValidator(self.data, self.key, self.validators)

    def set_data(self, data):
        self.data = data

    def Validate(self, win):
        control = self.GetWindow()
        for validator in self.validators:
            result = validator(control)
            if not result:
                return result
        return True

    def TransferToWindow(self):
        control = self.GetWindow()
        print(control.Name)
        record = self.data[self.key]
        control.SetValue(str(record) if record is not None else "")
        return True

    def TransferFromWindow(self):
        control = self.GetWindow()
        self.data[self.key] = control.GetValue()
        return True


class CheckboxValidator(wx.Validator):

    def __init__(self, data, key, validators):
        super().__init__()
        self.data = data
        self.key = key
        self.validators = validators

    def Clone(self):
        return CheckboxValidator(self.data, self.key, self.validators)

    def set_data(self, data):
        self.data = data

    def Validate(self, win):
        control = self.GetWindow()
        for validator in self.validators:
            result = validator(control)
            if not result:
                return result
        return True

    def TransferToWindow(self):
        control = self.GetWindow()
        bool_data = self.data[self.key]
        control.SetValue(bool_data if bool_data is not None else False)
        return True

    def TransferFromWindow(self):
        control = self.GetWindow()
        self.data[self.key] = control.GetValue()
        return True


