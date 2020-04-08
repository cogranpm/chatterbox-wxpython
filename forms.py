# classes etc that help define a form and related controls
from enum import Enum, auto
from typing import List
import wx

EditFieldType = Enum('EditFieldType', 'TEXT COMBO CHECK')
EditFieldWidth = Enum('EditFieldWidth', 'LARGE MEDIUM SMALL')


class FormSpec():
    """ for specifiying the contents of a form, a function will use this information to build up
    a 'form' and all it's contents
    a form consists of help text, title, and a bunch of labels/inputs
    once this spec is built up it can be passed into a function in order
    to render the corresponding controls
    formSpec has multipl FormLines
    FormLine has multiple EditFields
    """

    def __init__(self, parent, title: str, helpstr: str, edit_lines: List['FormLineSpec']):
        self.parent = parent
        self.title = title
        self.helpstr = helpstr
        self.edit_lines = edit_lines


class FormLineSpec():
    """ can be made up of multiple edit fields or a single, such as zip, state, city on a single line """

    def __init__(self, labelstr: str, edit_fields: List['EditFieldSpec']):
        self.labelstr = labelstr
        self.edit_fields = edit_fields


class EditFieldSpec():
    """ this is an edit field in a form, for example a combo box, or text box etc """

    def __init__(self, name: str, type: EditFieldType, width: EditFieldWidth):
        self.type = type
        self.name = name
        self.width = width


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

def text():
    return EditFieldType.TEXT

def edit(name, type=EditFieldType.TEXT, width=EditFieldWidth.LARGE):
    return EditFieldSpec(name, type, width)

def edit_line(labelstr, edit_fields):
    return FormLineSpec(labelstr, edit_fields)

def form(parent, title, helpstr, edit_lines):
    return FormSpec(parent, title, helpstr, edit_lines)

def build(form: FormSpec):
    panel = wx.Panel(form.parent, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL)
    box = wx.BoxSizer(wx.VERTICAL)
    lbl_header = wx.StaticText(panel, 0, form.title)
    lbl_help = wx.StaticText(panel, 0, form.helpstr.lstrip())
    lbl_header.SetFont(header_font())
    lbl_help.SetFont(help_font())
    box.Add(lbl_header, 0, wx.ALL, 5)
    # add a static line
    box.Add(wx.StaticLine(panel), 0, wx.EXPAND | wx.TOP | wx.BOTTOM, 5)
    box.Add(lbl_help, 0, wx.ALL, 5)
    box.Add(wx.StaticLine(panel), 0, wx.EXPAND | wx.TOP | wx.BOTTOM, 5)

    gridsizer = wx.FlexGridSizer(cols=2, hgap=5, vgap=5)
    gridsizer.AddGrowableCol(1)

    for line in form.edit_lines:
        build_line(panel, line, gridsizer)

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
    box.Fit(form.parent)  # this call triggers the layout alorithm to fire
    box.SetSizeHints(form.parent)
    #panel.SetBackgroundColour("orange")
    panel.Refresh()
    return panel


def build_line(panel, line, gridsizer):
    if line.labelstr is not None:
        lbl = wx.StaticText(panel, -1, f"{line.labelstr}:")
        gridsizer.Add(lbl, proportion=0, flag=wx.ALIGN_RIGHT | wx.ALIGN_CENTER_VERTICAL)
    else:
        gridsizer.AddSpacer(spacer_width)

    if len(line.edit_fields) == 1:
        width = line.edit_fields[0].width
        if width == EditFieldWidth.LARGE:
            flag = wx.EXPAND
            txt = wx.TextCtrl(panel, -1, "")
            gridsizer.Add(txt, proportion=0, flag=flag)
        elif width == EditFieldWidth.MEDIUM:
            txt = wx.TextCtrl(panel, -1, "", size=(width_medium, -1))
            gridsizer.Add(txt)
        else:
            txt = wx.TextCtrl(panel, -1, "", size=(width_small, -1))
            gridsizer.Add(txt)
    else:
        cstsizer = wx.BoxSizer(wx.HORIZONTAL)

        for i, edit in enumerate(line.edit_fields):
            txt_width = width_large_multi
            if edit.width == EditFieldWidth.SMALL:
                txt_width = width_small_multi
            elif edit.width == EditFieldWidth.MEDIUM:
                txt_width = width_medium_multi
            txt = wx.TextCtrl(panel, -1, "", size=(txt_width, -1))
            if i == 0:
                cstsizer.Add(txt, 1) # first item expands, may need to change
            elif i != len(line.edit_fields):
                cstsizer.Add(txt, 0, wx.LEFT | wx.RIGHT, field_border_width)  # border on each side of field
            else:
                cstsizer.Add(txt)

        gridsizer.Add(cstsizer, 0, wx.EXPAND)
