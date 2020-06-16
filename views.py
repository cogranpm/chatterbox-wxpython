
# ------- python imports ---------------------
from typing import List

# ----- Lib imports --------------------------
import wx

# --------------------------------------------
# project imports
from lists import create_list, ColumnSpec
import fn_widget as w
import forms as frm
import chatterbox_constants as c


class BaseView(wx.Panel):

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


class BaseViewNotebook(BaseView):
    """ panel ui that separates editing form from list via a notebook """
    def __init__(self, parent):
        super().__init__(parent)
        self.notebook: wx.aui.AuiNotebook = w.notebook(self)
        self.Sizer.Add(self.notebook, wx.SizerFlags(1).Expand().Border(wx.ALL, 5))

    def set_list(self, columns: List[ColumnSpec]):
        self.list = create_list(self.Parent, columns)
        self.notebook.AddPage(self.list, "List", True)

    def set_form(self, form_def: frm.FormDef):
        form_def.make_form(self.form_panel)
        self.notebook.AddPage(self.form_panel, "Task", False)

    def set_current_tab(self, index):
        self.notebook.SetSelection(index)

