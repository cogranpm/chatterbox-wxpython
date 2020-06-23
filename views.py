
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
        super().__init__(parent, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL, name="fred")
        self.list = None
        main_sizer = frm.vsizer()
        self.SetSizer(main_sizer)

    def bind(self, direction: c.BindDirection):
        pass

    def set_list(self, columns: List[ColumnSpec]):
        self.list = create_list(self, columns)



class BaseViewNotebook(BaseView):
    """ panel ui that separates editing form from list via a notebook """
    def __init__(self, parent):
        super().__init__(parent)
        self.notebook: wx.aui.AuiNotebook = w.notebook(self)
        self.Sizer.Add(self.notebook, wx.SizerFlags(1).Expand().Border(wx.ALL, 5))
        self.form_panel = w.panel(self, [])
        self.form_panel.SetSizer(w.sizer())

    def bind(self, direction: c.BindDirection):
        if direction == c.BindDirection.from_window:
            self.form_panel.TransferDataFromWindow()
        else:
            self.form_panel.TransferDataToWindow()

    def set_list(self, columns: List[ColumnSpec]):
        super().set_list(columns)
        self.notebook.AddPage(self.list, "List", True)

    def set_form(self, form_def: frm.FormDef):
        form_def.make_form(self.form_panel)
        self.notebook.AddPage(self.form_panel, "Task", False)

    def set_current_tab(self, index):
        self.notebook.SetSelection(index)



class ModalEditView(BaseView):
    """ a panel that shows data in a list with add, delete, edit buttons for modal editing """

    def __init__(self, parent, caption):
        self.caption = caption
        super().__init__(parent)
        self.SetSizer(frm.vsizer())
        self.arrange_widgets(self)
        self.Sizer.Add(self, wx.SizerFlags(1).Expand())


    def arrange_widgets(self, parent):
        header_panel = frm.panel(parent, "header_panel")
        lbl_caption = frm.label(header_panel, self.caption, "lblCaption")
        lbl_caption.Wrap(-1)
        self.btn_add = tool_button(header_panel, c.ID_ADD, c.ICON_ADD)
        self.btn_delete = tool_button(header_panel, c.ID_DELETE, c.ICON_CANCEL)
        # btn_delete.Enable(False)
        self.btn_edit = tool_button(header_panel, c.ID_EDIT, c.ICON_EDIT)
        # btn_edit_shelf.Enable(False)
        header_sizer = frm.hsizer([lbl_caption, self.btn_add, self.btn_delete, self.btn_edit])
        header_panel.SetSizer(header_sizer)
        header_panel.Layout()
        header_sizer.Fit(header_panel)
        self.Sizer.Add(header_panel, 0, 0, 5)

    def set_list(self, columns: List[ColumnSpec]):
        # super().set_list(columns)
        self.list = create_list(self, columns)
        self.Sizer.Add(self.list, wx.SizerFlags(1).Expand().Border(wx.ALL, 5))


class ModalEditViewParent:
    """ no visual parent
      is passed a splitter and a child component
     """

    def __init__(self, splitter, child_panel, caption):
        self.caption = caption
        self.child_panel = child_panel
        self.splitter = splitter
        self.main_panel = self.make_main_container(splitter)
        self.main_panel.SetSizer(frm.vsizer())
        self.arrange_widgets(self.main_panel)
        self.splitter.SplitVertically(self.main_panel, self.child_panel, 248)
        #self.Sizer.Add(self.main_panel, wx.SizerFlags(1).Expand())

    def get_main_panel(self):
        return self.main_panel

    def make_main_container(self, parent):
        return w.panel(parent, [])

    # to do, factor this out into a single re-usable function
    # it is shared by modaleditview
    def arrange_widgets(self, parent):
        header_panel = frm.panel(parent, "header_panel")
        lbl_caption = frm.label(header_panel, self.caption, "lblCaption")
        lbl_caption.Wrap(-1)
        self.btn_add = tool_button(header_panel, c.ID_ADD, c.ICON_ADD)
        self.btn_delete = tool_button(header_panel, c.ID_DELETE, c.ICON_CANCEL)
        # btn_delete.Enable(False)
        self.btn_edit = tool_button(header_panel, c.ID_EDIT, c.ICON_EDIT)
        # btn_edit_shelf.Enable(False)
        header_sizer = frm.hsizer([lbl_caption, self.btn_add, self.btn_delete, self.btn_edit])
        header_panel.SetSizer(header_sizer)
        header_panel.Layout()
        header_sizer.Fit(header_panel)
        self.main_panel.Sizer.Add(header_panel, 0, 0, 5)

    def set_list(self, columns: List[ColumnSpec]):
        # super().set_list(columns)
        self.list = create_list(self.main_panel, columns)
        self.main_panel.Sizer.Add(self.list, wx.SizerFlags(1).Expand().Border(wx.ALL, 5))

def tool_button(parent, id, icon):
    btn = wx.Button(parent, id, wx.EmptyString, wx.DefaultPosition, wx.Size(20, 20), 0)
    btn.SetBitmap(make_icon(icon))
    return btn




