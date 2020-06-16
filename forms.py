# classes etc that help define a form and related controls
from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum, auto
from typing import List, Tuple
from lists import ListItem
from models import ViewState
import chatterbox_constants as c
import wx
import wx.py as py
import wx.stc
from fn_app import make_icon
import fn_widget as w

EditFieldWidth = Enum('EditFieldWidth', 'LARGE MEDIUM SMALL DEFAULT')
DisplayType = Enum('DisplayType', 'DIALOG PANEL')

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


class EditFieldDef(ABC):

    def __init__(self, name: str, width: EditFieldWidth, validator: wx.PyValidator):
        self.name = name
        self.width = width
        self.validator = validator
        self.control = None
        self.pause_dirty_events = False

    @abstractmethod
    def make_field(self, parent, multi_column: bool = False):
        pass

    def get_size(self, multi_column: bool = False):
        size = wx.Size()
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

    def get_sizer_flags(self):
        sizer_flags = wx.SizerFlags()
        if self.width == EditFieldWidth.LARGE:
            sizer_flags.Expand()
        return sizer_flags

    def set_sizer_properties(self, sizer: wx.Sizer, row: int):
        pass

    def focus(self):
        if self.control is not None:
            self.control.SetFocus()

    def enable(self, flag):
        if self.control is not None:
            if flag:
                self.control.Enable()
            else:
                self.control.Disable()


class TextFieldDef(EditFieldDef):

    def __init__(self, name: str, width: EditFieldWidth, validator: wx.PyValidator, multi_line: bool = False):
        super().__init__(name, width, validator)
        self.multi_line = multi_line

    def make_field(self, parent, multi_column: bool = False):
        style = 0
        if self.multi_line:
            style = wx.TE_MULTILINE
        size = self.get_size(multi_column)
        self.control = wx.TextCtrl(parent, -1, "", size=size, name=self.name, validator=self.validator, style=style)
        self.control.Bind(wx.EVT_TEXT, self.on_change_text)
        return self.control

    def reset(self):
        self.control.SetValue('')

    def set_sizer_properties(self, sizer: wx.Sizer, row: int):
        if self.control.HasFlag(wx.TE_MULTILINE):
            sizer.AddGrowableRow(row, 1)

    def on_change_text(self, event):
        """ this is the place to raise a dirty message """
        # need to not fire this if the form I belong too is in the loading state
        if not self.pause_dirty_events:
            py.dispatcher.send(signal=c.SIGNAL_VIEWSTATE, sender=self, command=c.COMMAND_DIRTY, more=self)


class CodeEditorDef(EditFieldDef):

    def __init__(self, name: str, width: EditFieldWidth, validator: wx.PyValidator):
        super().__init__(name, width, validator)

    def make_field(self, parent, multi_column: bool = False):
        size = self.get_size(multi_column)
        self.control = wx.py.editwindow.EditWindow(parent=parent)
        if self.validator is not None:
            self.control.Validator = self.validator

        self.control.Bind(wx.stc.EVT_STC_CHANGE, self.on_change_text)
        return self.control

    def reset(self):
        self.control.SetValue('')

    def get_sizer_flags(self):
        flags = super().get_sizer_flags()
        flags.Proportion(1)
        return flags

    def set_sizer_properties(self, sizer: wx.Sizer, row: int):
        sizer.AddGrowableRow(row, 1)

    def on_change_text(self, event):
        if not self.pause_dirty_events:
            py.dispatcher.send(signal=c.SIGNAL_VIEWSTATE, sender=self, command=c.COMMAND_DIRTY, more=self)


class CheckboxFieldDef(EditFieldDef):

    def __init__(self, name: str, width: EditFieldWidth, validator: wx.PyValidator):
        super().__init__(name, width, validator)

    def make_field(self, parent, multi_column: bool = False):
        self.control = wx.CheckBox(parent, -1, "", name=self.name, validator=self.validator)
        self.control.Bind(wx.EVT_CHECKBOX, self.on_select)
        return self.control

    def reset(self):
        self.control.SetValue(False)

    def on_select(self, event):
        """ this is the place to raise the dirty message """
        # need to not fire this if the form I belong too is in the loading state
        if not self.pause_dirty_events:
            py.dispatcher.send(signal=c.SIGNAL_VIEWSTATE, sender=self, command=c.COMMAND_DIRTY, more=self)


class ComboFieldDef(EditFieldDef):

    def __init__(self, name: str, width: EditFieldWidth, contents: List[ListItem], validator: wx.PyValidator):
        super().__init__(name, width, validator)
        self.contents = contents

    def make_field(self, parent,  multi_column: bool = False):
        size = self.get_size(multi_column)
        style = wx.CB_READONLY
        choices = []
        self.control.Create(parent, -1, name=self.name, choices=choices, style=style, validator=self.validator)
        if self.contents is not None:
            for item in self.contents:
                self.control.Append(item.label, item.code )

        self.control.Bind(wx.EVT_COMBOBOX, self.on_select)
        return self.control

    def reset(self):
        self.control.SetSelection(0)

    def on_select(self, event):
        """ this is the place to raise the dirty message """
        # need to not fire this if the form I belong too is in the loading state
        if not self.pause_dirty_events:
            py.dispatcher.send(signal=c.SIGNAL_VIEWSTATE, sender=self, command=c.COMMAND_DIRTY, more=self)


@dataclass(frozen=True)
class FormLineDef:
    label: str
    edit_fields: List['EditFieldDef']

    def make_line(self, parent: wx.Window, sizer: wx.Sizer, row: int):
        if self.label is not None:
            lbl = wx.StaticText(parent, -1, f"{self.label}:")
            sizer.Add(lbl, proportion=0, flag=wx.ALIGN_RIGHT | wx.ALIGN_CENTER_VERTICAL)
        else:
            sizer.AddSpacer(spacer_width)

        if len(self.edit_fields) == 1:
            edit_field = self.edit_fields[0]
            control = edit_field.make_field(parent, False)
            sizer.Add(control, edit_field.get_sizer_flags())
            edit_field.set_sizer_properties(sizer, row)
        else:
            cstsizer = wx.BoxSizer(wx.HORIZONTAL)
            for i, edit in enumerate(self.edit_fields):
                control = edit.make_field(parent, True)
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


@dataclass(frozen=True)
class FormDef:
    title: str
    help: str
    edit_lines: List['FormLineDef']
    name: str

    def make_form(self, parent: wx.Window, display_type=DisplayType.PANEL, ok_handler=None, cancel_handler=None):
        sizer = vsizer()
        lbl_header = wx.StaticText(parent, 0, self.title)

        lbl_header.SetFont(header_font())

        sizer.Add(lbl_header, 0, wx.ALL, 5)
        # add a static line
        sizer.Add(wx.StaticLine(parent), 0, wx.EXPAND | wx.TOP | wx.BOTTOM, 5)

        if self.help is not None:
            lbl_help = wx.StaticText(parent, 0, self.help.lstrip())
            lbl_help.SetFont(help_font())
            sizer.Add(lbl_help, 0, wx.ALL, 5)

        sizer.Add(wx.StaticLine(parent), 0, wx.EXPAND | wx.TOP | wx.BOTTOM, 5)

        grid_sizer = wx.FlexGridSizer(cols=2, hgap=5, vgap=5)
        grid_sizer.AddGrowableCol(1)
        grid_sizer.SetFlexibleDirection(wx.BOTH)

        for counter, line in enumerate(self.edit_lines):
            line.make_line(parent, grid_sizer, counter)

        # can add a sizer to a sizer, not just add widget to sizer, creates a nested sizer
        flags = wx.SizerFlags(1).Expand().Border(wx.ALL, 10)
        sizer.Add(grid_sizer, flags)

        if display_type == DisplayType.DIALOG:
            std_btn_sizer = wx.StdDialogButtonSizer()
            std_btn_ok = wx.Button(parent, wx.ID_OK, name="btnOK")
            std_btn_ok.SetDefault()
            if ok_handler is not None:
                bind_button(std_btn_ok, ok_handler)
            std_btn_sizer.AddButton(std_btn_ok)
            std_btn_cancel = wx.Button(parent, wx.ID_CANCEL, name="btnCancel")
            std_btn_sizer.AddButton(std_btn_cancel)
            if cancel_handler is not None:
                bind_button(std_btn_cancel, cancel_handler)
            std_btn_sizer.Realize()
            self.sizer.Add(std_btn_sizer, 0, wx.EXPAND, 5)

        parent.Sizer.Add(sizer, wx.SizerFlags(1).Expand())


# _____________________
# older stuff appears below


def is_child_of(widgets, child_widget):
    """ recursive function to find out if the child_widget is an
    ancestor of any widget in widgets,
    if so return that widget """
    if child_widget.Parent is None:
        return None
    else:
        for item in widgets:
            if child_widget.Parent is item:
                return item
        return is_child_of(widgets, child_widget.Parent)


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

def bind_button(btn, handler):
    btn.Bind(wx.EVT_BUTTON, handler)



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
        self.view_state = ViewState.empty

    def build(self, display_type=DisplayType.PANEL, ok_handler=None, cancel_handler=None):

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
        gridsizer.SetFlexibleDirection(wx.BOTH)

        for counter, line in enumerate(self.edit_lines):
            line.build(self.parent, gridsizer, counter)

        # can add a sizer to a sizer, not just add widget to sizer, creates a nested sizer
        flags = wx.SizerFlags(1).Expand().Border(wx.ALL, 10)
        self.sizer.Add(gridsizer, flags)

        if display_type == DisplayType.DIALOG:
            stdButtonSizer = wx.StdDialogButtonSizer()
            stdButtonSizerOK = wx.Button(self.parent, wx.ID_OK, name="btnOK")
            stdButtonSizerOK.SetDefault()
            if ok_handler is not None:
                bind_button(stdButtonSizerOK, ok_handler)

            stdButtonSizer.AddButton(stdButtonSizerOK)
            stdButtonSizerCancel = wx.Button(self.parent, wx.ID_CANCEL, name="btnCancel")
            stdButtonSizer.AddButton(stdButtonSizerCancel)
            if cancel_handler is not None:
                bind_button(stdButtonSizerCancel, cancel_handler)
            stdButtonSizer.Realize()
            self.sizer.Add(stdButtonSizer, 0, wx.EXPAND, 5)

        self.parent.Sizer.Add(self.sizer, wx.SizerFlags(1).Expand())

    def set_viewstate(self, state: ViewState):
        if state == ViewState.adding:
            self.reset_fields()
            self.enable_fields(True)
            self.setfocusfirst()
            py.dispatcher.send(signal=c.SIGNAL_VIEWSTATE, sender=self, command=c.COMMAND_ADDING, more=self)
        elif state == ViewState.empty:
            self.reset_fields()
            self.enable_fields(False)
            py.dispatcher.send(signal=c.SIGNAL_VIEWSTATE, sender=self, command=c.COMMAND_EMPTY, more=self)
        elif state == ViewState.loaded:
            self.enable_fields(True)
            self.setfocusfirst()
            py.dispatcher.send(signal=c.SIGNAL_VIEWSTATE, sender=self, command=c.COMMAND_LOADED, more=self)
            self.pause_dirty_events(False)
        elif state == ViewState.loading:
            self.pause_dirty_events(True)

        self.view_state = state

    def setfocusfirst(self):
        first_line = self.edit_lines[0]
        if first_line is not None:
            first_control = first_line.edit_fields[0]
            if first_control is not None:
                first_control.focus()

    def reset_fields(self):
        for line in self.edit_lines:
            for edit_field in line.edit_fields:
                edit_field.reset()

    def enable_fields(self, flag):
        for line in self.edit_lines:
            for edit_field in line.edit_fields:
                edit_field.enable(flag)

    def pause_dirty_events(self, flag):
        for line in self.edit_lines:
            for edit_field in line.edit_fields:
                edit_field.pause_dirty_events = flag

    def bind(self, record):
        for line in self.edit_lines:
            for edit_field in line.edit_fields:
                if edit_field.control is not None and edit_field.control.Validator is not None:
                    edit_field.control.Validator.set_data(record)


class FormLineSpec:
    """ can be made up of multiple edit fields or a single, such as zip, state, city on a single line """

    def __init__(self, labelstr: str, edit_fields: List['EditFieldSpec']):
        self.labelstr = labelstr
        self.edit_fields = edit_fields

    def build(self, parent, sizer, row: int):
        if self.labelstr is not None:
            lbl = wx.StaticText(parent, -1, f"{self.labelstr}:")
            sizer.Add(lbl, proportion=0, flag=wx.ALIGN_RIGHT | wx.ALIGN_CENTER_VERTICAL)
        else:
            sizer.AddSpacer(spacer_width)

        if len(self.edit_fields) == 1:
            edit_field = self.edit_fields[0]
            control = edit_field.build(parent, False)
            sizer.Add(control, edit_field.get_sizer_flags())
            edit_field.set_sizer_properties(sizer, row)
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
        self.control = None
        self.pause_dirty_events = False

    def get_size(self, multi_column: bool = False):
        size = wx.Size()
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

    def get_sizer_flags(self):
        sizer_flags = wx.SizerFlags()
        if self.width == EditFieldWidth.LARGE:
            sizer_flags.Expand()
        return sizer_flags

    def set_sizer_properties(self, sizer: wx.Sizer, row: int):
        pass

    def focus(self):
        if self.control is not None:
            self.control.SetFocus()

    def enable(self, flag):
        if self.control is not None:
            if flag:
                self.control.Enable()
            else:
                self.control.Disable()

class TextField(EditFieldSpec):

    def __init__(self, name, width: EditFieldWidth, validator: wx.PyValidator = None, style: int = None):
        super().__init__(name, width)
        self.validator = validator
        self.style = style

    def build(self, parent, multi_column: bool = False):
        style = 0 if self.style is None else self.style
        size = self.get_size(multi_column)
        self.control = wx.TextCtrl(parent, -1, "", size=size, name=self.name, validator=self.validator, style=style)
        self.control.Bind(wx.EVT_TEXT, self.on_change_text)
        return self.control

    def reset(self):
        self.control.SetValue('')

    def set_sizer_properties(self, sizer: wx.Sizer, row: int):
        if self.control.HasFlag(wx.TE_MULTILINE):
            sizer.AddGrowableRow(row, 1)

    def on_change_text(self, event):
        """ this is the place to raise a dirty message """
        # need to not fire this if the form I belong too is in the loading state
        if not self.pause_dirty_events:
            py.dispatcher.send(signal=c.SIGNAL_VIEWSTATE, sender=self, command=c.COMMAND_DIRTY, more=self)


class CodeEditor(EditFieldSpec):

    def __init__(self, name, width: EditFieldWidth, validator: wx.PyValidator = None):
        super().__init__(name, width)
        self.validator = validator

    def build(self, parent, multi_column: bool = False):
        size = self.get_size(multi_column)
        self.control = wx.py.editwindow.EditWindow(parent=parent)
        if self.validator is not None:
            self.control.Validator = self.validator

        self.control.Bind(wx.stc.EVT_STC_CHANGE, self.on_change_text)
        return self.control

    def reset(self):
        self.control.SetValue('')

    def get_sizer_flags(self):
        flags = super().get_sizer_flags()
        flags.Proportion(1)
        return flags

    def set_sizer_properties(self, sizer: wx.Sizer, row: int):
        sizer.AddGrowableRow(row, 1)

    def on_change_text(self, event):
        if not self.pause_dirty_events:
            py.dispatcher.send(signal=c.SIGNAL_VIEWSTATE, sender=self, command=c.COMMAND_DIRTY, more=self)


class ComboField(EditFieldSpec):

    def __init__(self, name, width: EditFieldWidth, contents: List[ListItem] = None, validator: wx.Validator = None):
        super().__init__(name, width)
        self.contents = contents
        self.control = wx.ComboBox()
        self.validator = validator

    def build(self, parent,  multi_column: bool = False):
        size = self.get_size(multi_column)
        style = wx.CB_READONLY
        choices = []
        self.control.Create(parent, -1, name=self.name, choices=choices, style=style, validator=self.validator)
        if self.contents is not None:
            for item in self.contents:
                self.control.Append(item.label, item.code )

        self.control.Bind(wx.EVT_COMBOBOX, self.on_select)
        return self.control

    def reset(self):
        self.control.SetSelection(0)

    def on_select(self, event):
        """ this is the place to raise the dirty message """
        # need to not fire this if the form I belong too is in the loading state
        if not self.pause_dirty_events:
            py.dispatcher.send(signal=c.SIGNAL_VIEWSTATE, sender=self, command=c.COMMAND_DIRTY, more=self)


class CheckboxField(EditFieldSpec):
    def __init__(self, name, validator: wx.PyValidator = None):
        super().__init__(name, None)
        self.validator = validator
        self.control = None

    def build(self, parent, multi_column: bool = False):
        self.control = wx.CheckBox(parent, -1, "", name=self.name, validator=self.validator)
        self.control.Bind(wx.EVT_CHECKBOX, self.on_select)
        return self.control

    def reset(self):
        self.control.SetValue(False)

    def on_select(self, event):
        """ this is the place to raise the dirty message """
        # need to not fire this if the form I belong too is in the loading state
        if not self.pause_dirty_events:
            py.dispatcher.send(signal=c.SIGNAL_VIEWSTATE, sender=self, command=c.COMMAND_DIRTY, more=self)


class FormDialog(wx.Dialog):

    def __init__(self, parent, title, record, collection_name):
        super().__init__(parent, id=wx.ID_ANY, title=title, pos=wx.DefaultPosition,
                           size=wx.Size(600, 800), style=wx.DEFAULT_DIALOG_STYLE | wx.WS_EX_VALIDATE_RECURSIVELY)
        self.record = record
        self.collection_name = collection_name
        self.Bind(wx.EVT_INIT_DIALOG, self.OnInitDialog)


    def build(self, form: FormSpec):
        self.SetSizeHints(wx.DefaultSize, wx.DefaultSize)

        main_sizer = wx.BoxSizer(wx.VERTICAL)
        self.SetSizer(main_sizer)

        form.build(display_type=DisplayType.DIALOG, ok_handler=self.on_ok, cancel_handler=self.on_cancel)

        self.Layout()
        self.Centre(wx.BOTH)
        main_sizer.Fit(self)
        self.TransferDataToWindow()

    def OnInitDialog(self, event):
        pass

    def on_ok(self, event):
        event.Skip()

    def on_cancel(self, event):
        event.Skip()


def edit_line(labelstr, edit_fields):
    return FormLineSpec(labelstr, edit_fields)


def make_dialog(parent, record, title: str, collection_name: str) -> FormDialog:
    return FormDialog(parent=parent, title=title, record=record, collection_name=collection_name)


def form(parent, name, title, helpstr, edit_lines):
    return FormSpec(parent, name, title, helpstr, edit_lines)


def panel(parent, name):
    return wx.Panel(parent, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL, name)


def label(parent, caption, name):
    lbl = wx.StaticText(parent, id=wx.ID_ANY, label=caption, name=name)
    return lbl

def generic_button(parent, id, text, handler, size, icon=None):
    btn = wx.Button(parent, id, text, wx.DefaultPosition,size, 0)
    bind_button(btn, handler)
    if not icon is None:
        btn.SetBitmap(make_icon(icon))
    return btn

def panel_tool_button(parent, id, text, handler, icon):
    return generic_button(parent, id, text, handler, wx.Size(20, 20), icon)

def tool_button(parent, id, text, handler):
    return generic_button(parent, id, text, handler, wx.Size(40, 40))

def command_button(parent, id, text, handler):
    return generic_button(parent, id, text, handler, wx.Size(220, 30))

def splitter(parent):
    return wx.SplitterWindow(parent, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.SP_3D)

def panel_header(parent, name, caption, add_handler, delete_handler, edit_handler):
    header_panel = panel(parent, name)
    shelf_caption = label(header_panel, caption, "lbl" + name)
    shelf_caption.Wrap(-1)
    btn_add_shelf = panel_tool_button(header_panel, c.ID_ADD_SHELF, wx.EmptyString,
                                      add_handler, c.ICON_ADD)

    btn_delete_shelf = panel_tool_button(header_panel, c.ID_DELETE_SHELF, wx.EmptyString,
                                         delete_handler, c.ICON_CANCEL)
    # btn_delete_shelf.Enable(False)
    btn_edit_shelf = panel_tool_button(header_panel, c.ID_EDIT_SHELF, wx.EmptyString,
                                       edit_handler, c.ICON_EDIT)
    # btn_edit_shelf.Enable(False)

    header_sizer = hsizer([shelf_caption, btn_add_shelf, btn_delete_shelf, btn_edit_shelf])
    header_panel.SetSizer(header_sizer)
    header_panel.Layout()
    header_sizer.Fit(header_panel)
    return header_panel

def single_edit(parent):
    return wx.TextCtrl(parent, -1, "", size=(-1, -1))

def multi_edit(parent):
    return wx.TextCtrl(parent, -1, "",
                       style=wx.TE_MULTILINE|wx.TE_PROCESS_ENTER)


def hsizer(items):
    sizer = wx.BoxSizer(wx.HORIZONTAL)
    flag = wx.SizerFlags().Expand()
    for item in items:
        if type(item) == wx.TextCtrl:
            flag.Proportion(1)
        sizer.Add(item, flag)
    return sizer


def vsizer():
    sizer = wx.BoxSizer(wx.VERTICAL)
    return sizer

def confirm_delete(parent):
    dlg = wx.MessageDialog(parent, 'Delete, are you sure?',
                           'Delete', wx.OK | wx.CANCEL | wx.CANCEL_DEFAULT | wx.ICON_EXCLAMATION)
    result = dlg.ShowModal()
    dlg.Destroy()
    if result == wx.ID_OK:
        return True
    else:
        return False

