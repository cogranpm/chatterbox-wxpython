
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

font_header = None
font_help = None

def header_font():
    global font_header
    if font_header is None:
        font_header = wx.Font(18, wx.SWISS, wx.NORMAL, wx.BOLD)
    return font_header

def help_font():
    global font_help
    if font_help is None:
        font_help = wx.Font(14, wx.ROMAN, wx.NORMAL, wx.NORMAL)
    return font_help

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

def form(parent, content, headerstr, helpstr):
    """ represents a bunch of text fields and labels layed out in a grid """
    panel = wx.Panel(parent, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL)
    box = wx.BoxSizer(wx.VERTICAL)
    lbl_header = wx.StaticText(panel, 0, headerstr)
    lbl_help = wx.StaticText(panel, 0, helpstr.lstrip())
    lbl_header.SetFont(header_font())
    lbl_help.SetFont(help_font())
    box.Add(lbl_header, 0, wx.ALL, 5)
    # add a static line
    box.Add(wx.StaticLine(panel), 0, wx.EXPAND | wx.TOP | wx.BOTTOM, 5)
    box.Add(lbl_help, 0, wx.ALL, 5)
    box.Add(wx.StaticLine(panel), 0, wx.EXPAND | wx.TOP | wx.BOTTOM, 5)

    btn_save = wx.Button(panel, -1, "Save")
    btn_cancel = wx.Button(panel, -1, "Cancel")
    btnSizer = wx.BoxSizer(wx.HORIZONTAL)
    # this spacer pushes the buttons to the right
    # btnSizer.Add((20, 20), 1)
    btnSizer.AddStretchSpacer(20)
    btnSizer.Add(btn_save)
    btnSizer.AddSpacer(20)
    btnSizer.Add(btn_cancel)
    btnSizer.AddSpacer(20)
    box.Add(btnSizer, 0, wx.EXPAND | wx.BOTTOM | wx.ALIGN_RIGHT, 10)

    panel.SetSizer(box)
    box.Fit(parent)  # this call triggers the layout alorithm to fire
    box.SetSizeHints(parent)
    #panel.SetBackgroundColour("orange")
    panel.Refresh()

    return panel

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




