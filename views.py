
# ------- python imports ---------------------
from typing import List, Callable

# ----- Lib imports --------------------------
import wx

# --------------------------------------------
# project imports
from lists import create_list, ColumnSpec
import fn_widget as w
import forms as frm
import chatterbox_constants as c
from fn_app import make_icon


class BaseView(wx.Panel):
    """ panel based ui with list and form """
    def __init__(self, parent):
        super().__init__(parent, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL)
        self.list = None
        self.form_panel = w.panel(self, [])
        self.form_panel.SetSizer(w.sizer())
        main_sizer = wx.BoxSizer(wx.VERTICAL)
        self.SetSizer(main_sizer)

    def bind(self, direction: c.BindDirection):
        if direction == c.BindDirection.from_window:
            self.form_panel.TransferDataFromWindow()
        else:
            self.form_panel.TransferDataToWindow()

    def set_list(self, columns: List[ColumnSpec]):
        self.list = create_list(self.Parent, columns)

    def set_form(self, form_def: frm.FormDef):
        form_def.make_form(self.form_panel)


class BaseViewNotebook(BaseView):
    """ panel ui that separates editing form from list via a notebook """
    def __init__(self, parent):
        super().__init__(parent)
        self.notebook: wx.aui.AuiNotebook = w.notebook(self)
        self.Sizer.Add(self.notebook, wx.SizerFlags(1).Expand().Border(wx.ALL, 5))

    def set_list(self, columns: List[ColumnSpec]):
        super().set_list(columns)
        self.notebook.AddPage(self.list, "List", True)

    def set_form(self, form_def: frm.FormDef):
        super().set_form(form_def)
        self.notebook.AddPage(self.form_panel, "Task", False)

    def set_current_tab(self, index):
        self.notebook.SetSelection(index)


class ModalEditView(BaseView):
    """ a panel that shows data in a list with add, delete, edit buttons for modal editing """

    def __init__(self, parent, caption):
        super().__init__(parent)

        header_panel = frm.panel(parent, "header_panel")
        caption = frm.label(header_panel, caption, "lblCaption")
        caption.Wrap(-1)
        self.btn_add_shelf = self.tool_button(header_panel, c.ID_ADD_SHELF, c.ICON_ADD)
        self.btn_delete_shelf = self.tool_button(header_panel, c.ID_DELETE_SHELF, c.ICON_CANCEL)
        # btn_delete_shelf.Enable(False)
        self.btn_edit_shelf = self.tool_button(header_panel, c.ID_EDIT_SHELF, c.ICON_EDIT)
        # btn_edit_shelf.Enable(False)
        header_sizer = frm.hsizer([caption, self.btn_add_shelf, self.btn_delete_shelf, self.btn_edit_shelf])
        header_panel.SetSizer(header_sizer)
        header_panel.Layout()
        header_sizer.Fit(header_panel)
        self.Sizer.Add(header_panel, 0, 0, 5)

    def set_list(self, columns: List[ColumnSpec]):
        super().set_list(columns)
        self.Sizer.Add(self.list, wx.SizerFlags(1).Expand().Border(wx.ALL, 5))

    def tool_button(self, parent, id, icon):
        btn = wx.Button(parent, id, wx.EmptyString, wx.DefaultPosition, wx.Size(20, 20), 0)
        btn.SetBitmap(make_icon(icon))
        return btn

