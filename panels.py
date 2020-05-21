import wx
import wx.py as py
from dataclasses import dataclass
import forms as frm
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
    delete_handler: Any
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
        self.collection_name = spec.collection_name
        self.db = wx.GetApp().datastore
        if not spec.collection_name is None:
            self.db.create_entity(spec.collection_name)

        main_sizer = frm.vsizer()
        self.SetSizer(main_sizer)
        header_panel = frm.panel_header(self, spec.name + "Header", spec.title,
                                              spec.add_handler, spec.delete_handler,
                                              spec.edit_handler)
        main_sizer.Add(header_panel, 0, 0, 5)
        self.list = spec.listspec.build(self)
        main_sizer.Add(self.list, wx.SizerFlags(1).Expand().Border(wx.ALL, 5))




