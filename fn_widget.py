
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

# to do
# frame
# menus

# b = wx.BitmapButton(self, -1, bmp, (20, 120), style = wx.NO_BORDER)

# checkbox
# cb5 = wx.CheckBox(self, -1, "Align Right", style=wx.ALIGN_RIGHT)
# self.Bind(wx.EVT_CHECKBOX, self.EvtCheckBox, cb1)

def sizer() -> wx.BoxSizer:
    return wx.BoxSizer(wx.VERTICAL)

def hsizer(items):
    sizer = wx.BoxSizer(wx.HORIZONTAL)
    for item in items:
        sizer.Add(item)
    return sizer

def vsizer(items):
    sizer = wx.BoxSizer(wx.VERTICAL)
    for item in items:
        sizer.Add(item)
    return sizer

def tool_button(parent, id, text, handler):
    btn = wx.Button(parent, id, text, wx.DefaultPosition, wx.Size(40, 40), 0)
    btn.Bind(wx.EVT_BUTTON, handler)
    return btn


def notebook(parent, id = wx.ID_ANY):
    notebook = wx.aui.AuiNotebook(parent, id, wx.DefaultPosition, wx.DefaultSize, 0)
    return notebook

def panel(parent, items, id = wx.ID_ANY):
    panel = wx.Panel(parent, id, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL)
    for item in items:
        pass
        #sizer.Add(item)
    return panel

def splitter(parent, id = wx.ID_ANY):
    splitter = wx.SplitterWindow(parent, id, wx.DefaultPosition, wx.DefaultSize, wx.SP_3D)
    #splitter.Bind(wx.EVT_IDLE, m_splitter1OnIdle)
    return splitter

def static_text(parent, id = wx.ID_ANY, text = ''):
    static_text = wx.StaticText(parent, id, text, wx.DefaultPosition, wx.DefaultSize, 0)
    return static_text



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




