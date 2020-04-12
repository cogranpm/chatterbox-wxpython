# classes etc that help define a form and related controls
from enum import Enum, auto
from typing import List, Tuple
from lists import ListItem
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
        self.sizer = vsizer()

    def build(self):

        lbl_header = wx.StaticText(self.parent, 0, self.title)
        lbl_help = wx.StaticText(self.parent, 0, self.helpstr.lstrip())
        lbl_header.SetFont(header_font())
        lbl_help.SetFont(help_font())
        self.sizer.Add(lbl_header, 0, wx.ALL, 5)
        # add a static line
        self.sizer.Add(wx.StaticLine(self.parent), 0, wx.EXPAND | wx.TOP | wx.BOTTOM, 5)
        self.sizer.Add(lbl_help, 0, wx.ALL, 5)
        self.sizer.Add(wx.StaticLine(self.parent), 0, wx.EXPAND | wx.TOP | wx.BOTTOM, 5)

        gridsizer = wx.FlexGridSizer(cols=2, hgap=5, vgap=5)
        gridsizer.AddGrowableCol(1)

        for line in self.edit_lines:
            line.build(self.parent, gridsizer)

        # can add a sizer to a sizer, not just add widget to sizer, creates a nested sizer
        self.sizer.Add(gridsizer, 1, wx.EXPAND | wx.ALL, 10)

        # btn_save = wx.Button(panel, -1, "Save")
        # btn_cancel = wx.Button(panel, -1, "Cancel")
        # btnSizer = wx.BoxSizer(wx.HORIZONTAL)
        # # this spacer pushes the buttons to the right
        # # btnSizer.Add((20, 20), 1)
        # btnSizer.AddStretchSpacer(20)
        # btnSizer.Add(btn_save)
        # btnSizer.AddSpacer(20)
        # btnSizer.Add(btn_cancel)
        # btnSizer.AddSpacer(20)
        # box.Add(btnSizer, 0, wx.EXPAND | wx.BOTTOM | wx.ALIGN_RIGHT, 10)

        stdButtonSizer = wx.StdDialogButtonSizer()
        stdButtonSizerOK = wx.Button(self.parent, wx.ID_OK, name="btnOK")
        stdButtonSizerOK.SetDefault()
        stdButtonSizer.AddButton(stdButtonSizerOK)
        stdButtonSizerCancel = wx.Button(self.parent, wx.ID_CANCEL, name="btnCancel")
        stdButtonSizer.AddButton(stdButtonSizerCancel)
        stdButtonSizer.Realize()
        self.sizer.Add(stdButtonSizer, 0, wx.EXPAND, 5)
        self.parent.Sizer.Add(self.sizer, wx.SizerFlags(1).Expand())

class FormLineSpec():
    """ can be made up of multiple edit fields or a single, such as zip, state, city on a single line """

    def __init__(self, labelstr: str, edit_fields: List['EditFieldSpec']):
        self.labelstr = labelstr
        self.edit_fields = edit_fields

    def build(self, parent, sizer):
        if self.labelstr is not None:
            lbl = wx.StaticText(parent, -1, f"{self.labelstr}:")
            sizer.Add(lbl, proportion=0, flag=wx.ALIGN_RIGHT | wx.ALIGN_CENTER_VERTICAL)
        else:
            sizer.AddSpacer(spacer_width)

        if len(self.edit_fields) == 1:
            edit_field = self.edit_fields[0]
            width = edit_field.width
            sizer_flags = wx.SizerFlags()
            if width == EditFieldWidth.LARGE:
                sizer_flags.Expand()
            control = edit_field.build(parent, False)
            sizer.Add(control, sizer_flags)
        else:
            cstsizer = wx.BoxSizer(wx.HORIZONTAL)
            for i, edit in enumerate(self.edit_fields):
                control = edit.build(parent, True)
                sizer_flags = wx.SizerFlags()
                if i == 0:
                    sizer_flags.Expand().Proportion(1).Border(0)
                elif i != len(self.edit_fields):
                    sizer_flags.Border(wx.LEFT | wx.RIGHT, field_border_width)
                else:
                    sizer_flags.Expand().Border(0)
                cstsizer.Add(control, sizer_flags)
                del sizer_flags

            sizer.Add(cstsizer, -1, wx.EXPAND)

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


class TextField(EditFieldSpec):

    def __init__(self, name, width: EditFieldWidth, validator: wx.PyValidator = None):
        super().__init__(name, width)
        self.validator = validator

    def build(self, parent, multi_column: bool = False):
        size = self.get_size(multi_column)
        if size is None:
            control = wx.TextCtrl(parent, -1, "", name=self.name, validator=self.validator)
        else:
            control = wx.TextCtrl(parent, -1, "", size=size, name=self.name, validator=self.validator)
        # if self.validator is not None:
        #     control.Validator = self.validator
        return control


class ComboField(EditFieldSpec):

    def __init__(self, name, width: EditFieldWidth, contents: List[ListItem] = None):
        super().__init__(name, width)
        self.contents = contents
        self.control = wx.ComboBox()

    def build(self, parent,  multi_column: bool = False):
        size = self.get_size(multi_column)
        style = wx.CB_READONLY
        choices = []
        if size is None:
            self.control.Create(parent, -1, name=self.name, choices=choices, style=style)
        else:
            self.control.Create(parent, -1, size=size, name=self.name, choices=choices, style=style)
        if self.contents is not None:
            for item in self.contents:
                self.control.Append(item.label, item.code )
        self.control.Bind(wx.EVT_COMBOBOX, self.on_select)
        return self.control

    def on_select(self, event):
        # an example of how to get the selected item data
        listitem = self.control.GetClientData(self.control.GetSelection())
        print(listitem)


class CheckboxField(EditFieldSpec):
    def __init__(self, name):
        super().__init__(name, None)

    def build(self, parent, multi_column: bool = False):
        return wx.CheckBox(parent, -1, "", name=self.name)



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

