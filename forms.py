# classes etc that help define a form and related controls
from enum import Enum, auto
from typing import List
import wx

EditFieldWidth = Enum('EditFieldWidth', 'LARGE MEDIUM SMALL DEFAULT')

font_header = None
font_help = None
spacer_width = 10
# width for single fields
width_large = 400
width_medium = 300
width_small = 150
# width for multiple fields in single line
width_large_multi = 150
width_medium_multi = 100
width_small_multi = 70

field_border_width = 5

def header_font():
    global font_header
    if font_header is None:
        font_header = wx.Font(12, wx.SWISS, wx.NORMAL, wx.BOLD)
    return font_header

def help_font():
    global font_help
    if font_help is None:
        font_help = wx.Font(10, wx.ROMAN, wx.NORMAL, wx.NORMAL)
    return font_help

def large():
    return EditFieldWidth.LARGE

def medium():
    return EditFieldWidth.MEDIUM

def small():
    return EditFieldWidth.SMALL

def default():
    return EditFieldWidth.DEFAULT


class FormSpec():
    """ for specifiying the contents of a form, a function will use this information to build up
    a 'form' and all it's contents
    a form consists of help text, title, and a bunch of labels/inputs
    once this spec is built up it can be passed into a function in order
    to render the corresponding controls
    formSpec has multipl FormLines
    FormLine has multiple EditFields
    """

    def __init__(self, parent, name: str, title: str, helpstr: str, edit_lines: List['FormLineSpec']):
        self.parent = parent
        self.title = title
        self.helpstr = helpstr
        self.edit_lines = edit_lines
        self.name = name

    def build(self):
        #panel = wx.Panel(self.parent, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL)
        panel = FormPanel(self.parent, self.name)
        box = wx.BoxSizer(wx.VERTICAL)
        lbl_header = wx.StaticText(panel, 0, self.title)
        lbl_help = wx.StaticText(panel, 0, self.helpstr.lstrip())
        lbl_header.SetFont(header_font())
        lbl_help.SetFont(help_font())
        box.Add(lbl_header, 0, wx.ALL, 5)
        # add a static line
        box.Add(wx.StaticLine(panel), 0, wx.EXPAND | wx.TOP | wx.BOTTOM, 5)
        box.Add(lbl_help, 0, wx.ALL, 5)
        box.Add(wx.StaticLine(panel), 0, wx.EXPAND | wx.TOP | wx.BOTTOM, 5)

        gridsizer = wx.FlexGridSizer(cols=2, hgap=5, vgap=5)
        gridsizer.AddGrowableCol(1)

        for line in self.edit_lines:
            line.build(panel, gridsizer)

        # can add a sizer to a sizer, not just add widget to sizer, creates a nested sizer
        box.Add(gridsizer, 0, wx.EXPAND | wx.ALL, 10)

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
        box.Fit(self.parent)  # this call triggers the layout alorithm to fire
        box.SetSizeHints(self.parent)
        # panel.SetBackgroundColour("orange")
        panel.Refresh()
        return panel

class FormLineSpec():
    """ can be made up of multiple edit fields or a single, such as zip, state, city on a single line """

    def __init__(self, labelstr: str, edit_fields: List['EditFieldSpec']):
        self.labelstr = labelstr
        self.edit_fields = edit_fields

    def build(self, panel, sizer):
        if self.labelstr is not None:
            lbl = wx.StaticText(panel, -1, f"{self.labelstr}:")
            sizer.Add(lbl, proportion=0, flag=wx.ALIGN_RIGHT | wx.ALIGN_CENTER_VERTICAL)
        else:
            sizer.AddSpacer(spacer_width)

        if len(self.edit_fields) == 1:
            edit_field = self.edit_fields[0]
            width = edit_field.width
            sizer_flags = wx.SizerFlags()
            size = None
            if width == EditFieldWidth.LARGE:
                sizer_flags.Expand()
            control = edit_field.build(panel, False)
            sizer.Add(control, sizer_flags)
        else:
            cstsizer = wx.BoxSizer(wx.HORIZONTAL)
            for i, edit in enumerate(self.edit_fields):
                control = edit.build(panel, True)
                sizer_flags = wx.SizerFlags()
                if i == 0:
                    sizer_flags.Expand().Proportion(1)
                elif i != len(self.edit_fields):
                    sizer_flags.Border(wx.LEFT | wx.RIGHT, field_border_width)
                cstsizer.Add(control, sizer_flags)

            sizer.Add(cstsizer, 0, wx.EXPAND)

class EditFieldSpec():
    """ this is an edit field in a form, for example a combo box, or text box etc """

    def __init__(self, name: str, width: EditFieldWidth = EditFieldWidth.DEFAULT):
        self.name = name
        self.width = width

    def get_size(self, multi_column: bool = False):
        size = None
        if not multi_column:
            if self.width == EditFieldWidth.MEDIUM:
                size = wx.Size(width_medium, -1)
            else:
                size = wx.Size(width_small, -1)
        else:
            txt_width = width_large_multi
            if self.width == EditFieldWidth.SMALL:
                txt_width = width_small_multi
            elif self.width == EditFieldWidth.MEDIUM:
                txt_width = width_medium_multi
            size = wx.Size(txt_width, -1)
        return size


class FormPanel(wx.Panel):

    def __init__(self, parent, name):
        super().__init__(parent=parent, name=name)


class TextField(EditFieldSpec):

    def __init__(self, name, width: EditFieldWidth):
        super().__init__(name, width)

    def build(self, panel: wx.Panel, multi_column: bool = False):
        size = self.get_size(multi_column)
        if size is None:
            control = wx.TextCtrl(panel, -1, "", name=self.name)
        else:
            control = wx.TextCtrl(panel, -1, "", size=size, name=self.name)
        return control


class ComboField(EditFieldSpec):

    def __init__(self, name, width: EditFieldWidth):
        super().__init__(name, width)

    def build(self, panel: wx.Panel, multi_column: bool = False):
        size = self.get_size(multi_column)
        if size is None:
            control = wx.Choice(panel, -1, "", name=self.name)
        else:
            control = wx.Choice(panel, -1, "", size=size, name=self.name)
        return control


class CheckboxField(EditFieldSpec):
    def __init__(self, name):
        super().__init__(name, None)

    def build(self, panel: wx.Panel, multi_column: bool = False):
        return wx.CheckBox(panel, -1, "", name=self.name)



def edit_line(labelstr, edit_fields):
    return FormLineSpec(labelstr, edit_fields)

def form(parent, name, title, helpstr, edit_lines):
    return FormSpec(parent, name, title, helpstr, edit_lines)

def tool_button(parent, id, text, handler):
    btn = wx.Button(parent, id, text, wx.DefaultPosition, wx.Size(40, 40), 0)
    btn.Bind(wx.EVT_BUTTON, handler)
    return btn


def hsizer(items):
    sizer = wx.BoxSizer(wx.HORIZONTAL)
    for item in items:
        sizer.Add(item)
    return sizer


def vsizer():
    sizer = wx.BoxSizer(wx.VERTICAL)
    return sizer

