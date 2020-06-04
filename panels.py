import wx
import wx.py as py
import wx.dataview as dv
from dataclasses import dataclass
import forms as frm
from fn_app import get_data_store
from typing import Any
from lists import ListSpec
import chatterbox_constants as c

@dataclass(frozen=True)
class PanelSpec:
    parent: wx.Window
    name: str
    title: str
    collection_name: str
    listspec: ListSpec
    add_handler: Any
    edit_handler: Any

class BasePanel(wx.Panel):
    """ shows a list of panels and all the children """
    def __init__(self, spec: PanelSpec):
        super().__init__(parent=spec.parent,
                         id=wx.ID_ANY,
                         pos=wx.DefaultPosition,
                         size=wx.DefaultSize,
                         style=wx.TAB_TRAVERSAL,
                         name=spec.name)
        self.spec = spec
        self.collection_name = spec.collection_name
        self.db = get_data_store()
        main_sizer = frm.vsizer()
        self.SetSizer(main_sizer)
        header_panel = frm.panel_header(self, spec.name + "Header", spec.title,
                                        spec.add_handler,
                                        self.delete,
                                        spec.edit_handler)
        main_sizer.Add(header_panel, 0, 0, 5)
        self.list = spec.listspec.make_list(self)
        main_sizer.Add(self.list, wx.SizerFlags(1).Expand().Border(wx.ALL, 5))

    def delete(self, event):
        selected_item = self.list.GetSelection()
        if selected_item is not None:
            if frm.confirm_delete(self):
                    self.spec.listspec.model.ItemDeleted(dv.NullDataViewItem, selected_item)
                    record = self.spec.listspec.model.ItemToObject(selected_item)
                    self.db.remove(self.spec.collection_name, record)
                    self.spec.listspec.model.data.remove(record)
                    self.spec.listspec.model.Cleared()



