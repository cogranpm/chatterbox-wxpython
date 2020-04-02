# trying to experiment with a functional style
# declarative ui something like seesaw for clojure
# where widgets are defined by functions that take sequences of properties
# client code declares function pointers rather than calling the function
# and a 'tree' of widgets is built up then rendered

# the seesaw way of doing things is that functions are called immediate
# there are keyword arguments eg :text
# container type widgets have an :items argument that take a list
# containers that take a single child have a :content argument

import wx


def sizer() -> wx.BoxSizer:
    return wx.BoxSizer(wx.VERTICAL)

def std_buttons(properties):
    parent = properties[0]
    okhandler = properties[1]
    stdButtonSizer = wx.StdDialogButtonSizer()
    stdButtonSizerOK = wx.Button(parent, wx.ID_OK)
    stdButtonSizer.AddButton(stdButtonSizerOK)
    stdButtonSizerCancel = wx.Button(parent, wx.ID_CANCEL)
    stdButtonSizer.AddButton(stdButtonSizerCancel)
    stdButtonSizer.Realize()
    stdButtonSizerOK.Bind(wx.EVT_BUTTON, okhandler)
    return stdButtonSizer


