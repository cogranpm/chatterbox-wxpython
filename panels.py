import wx
from dataclasses import dataclass

@dataclass(frozen=True)
class PanelSpec:
    parent: wx.Window
    name: str
    title: str
    collection_name: str

def build_panel(spec: PanelSpec):
    pass